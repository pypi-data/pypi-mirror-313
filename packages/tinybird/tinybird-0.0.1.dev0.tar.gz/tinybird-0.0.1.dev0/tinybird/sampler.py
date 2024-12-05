import datetime
import decimal
import logging
import re
import time
from threading import Event, Lock, Thread
from typing import Any, List, Optional, Tuple, Union

import numpy as np
import orjson
from typing_extensions import TypeAlias

from tinybird.ch import HTTPClient
from tinybird.csv_tools import csv_from_python_object

TIME_BETWEEN_PUSHES = 30
MAX_SAMPLE_BURST_SIZE = 1000
MAX_GUESS_STR_SIZE = 1024


Guess: TypeAlias = Tuple[str, str, Optional[str], str, str, Union[int, float], str]


class Sampler(Thread):
    def __init__(
        self,
        user_id: str,
        datasource_id: str,
        host: str,
        database: str,
        logger=logging,
        debug: bool = False,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self._sample: List[Tuple[Any, Optional[str]]] = []
        self.exit_event: Event = Event()
        self.time_between_pushes: int = 1
        self.sample_allowance: int = MAX_SAMPLE_BURST_SIZE
        self.user_id: str = user_id
        self.datasource_id: str = datasource_id
        self.database: str = database
        self.clickhouse_client: HTTPClient = HTTPClient(host, database)
        self.logger = logger
        self.mutex: Lock = Lock()
        self.debug: bool = debug
        super().__init__(*args, **kwargs, name=f"sampler-{datasource_id}")  # type: ignore
        self.start()

    def sample(self, value, timestamp: Optional[str] = None) -> None:
        if self.sample_allowance == 0:
            return
        with self.mutex:
            self._sample.append((value, timestamp))
        self.sample_allowance -= 1

    def run(self) -> None:
        time.sleep(1)
        while not self.exit_event.wait(self.time_between_pushes):
            try:
                self.sample_allowance = min(self.sample_allowance + 5, MAX_SAMPLE_BURST_SIZE)
                self._process_sample()
                if self.debug:
                    self.time_between_pushes = 1
            except Exception as e:
                self.logger.warning(f"Sampling error: {e}")

    def _process_sample(self) -> None:
        self.time_between_pushes = TIME_BETWEEN_PUSHES

        with self.mutex:
            if not self._sample:
                return
            sample = self._sample
            self._sample = []

        guess_list: List[Guess] = []
        for x in sample:
            try:
                obj = orjson.loads(x[0].decode("utf-8", "replace")) if isinstance(x[0], bytes) else x[0]
                guess(self.user_id, self.datasource_id, guess_list, obj, x[1])
            except orjson.JSONDecodeError as e:
                guess_list.append((self.user_id, self.datasource_id, x[1], "$", "malformed_json", 0, str(e)))
                continue
        self.logger.info(f"Pushing {len(guess_list)} rows generated from a sample of {len(sample)} messages")
        # encode('utf-8') is needed as the default is 'latin-1'
        self.clickhouse_client.insert_chunk(
            "INSERT INTO data_guess FORMAT CSV",
            csv_from_python_object(guess_list).encode("utf-8"),
            user_agent="tb-data-guess-sampler",
        )


def guess(
    user_id: str, datasource_id: str, guess_list: List[Guess], x: Any, timestamp: Optional[str], path: str = "$"
) -> None:
    if len(path) > MAX_GUESS_STR_SIZE:
        return
    if isinstance(x, str) and path.startswith("csv."):
        try:
            x = float(x)
        except ValueError:
            pass
    if isinstance(x, bool):
        guess_list.append((user_id, datasource_id, timestamp, path, "bool", 0, str(x)[:MAX_GUESS_STR_SIZE]))
    elif isinstance(x, int):
        guess_list.append((user_id, datasource_id, timestamp, path, "number", x, ""))
    elif isinstance(x, float):
        guess_list.append((user_id, datasource_id, timestamp, path, "number", x, "f"))
    elif isinstance(x, decimal.Decimal):
        guess_list.append((user_id, datasource_id, timestamp, path, "number", float(x), "f"))
    elif x is None:
        guess_list.append((user_id, datasource_id, timestamp, path, "null", 0, ""))
    elif isinstance(x, dict):
        guess_list.append((user_id, datasource_id, timestamp, path, "object", 0, ""))
        for key in x.keys():
            guess(user_id, datasource_id, guess_list, x[key], timestamp, jsonpath_add_key(path, key))
    elif isinstance(x, str):
        guess_list.append((user_id, datasource_id, timestamp, path, "string", 0, x))
    elif isinstance(x, bytes):
        guess_list.append((user_id, datasource_id, timestamp, path, "string", 0, x.decode("utf-8", "replace")))
    elif isinstance(x, list):
        # In case there are more than 100 values, we take only 100 samples whose indexes are equally spaced. The other
        # option of using random.sample makes this function to behave non-deterministically. e.g. given a list
        # [1, 1, 1, 1, 1234, 1, 1, 1, 1, 2] if take 3 samples equally spaced, we would get
        # [1, 1234, 2]
        array = (
            x
            if len(x) <= 100 or path.startswith("csv.")
            else [x[i] for i in np.round(np.linspace(0, len(x) - 1, 100)).astype(int)]
        )
        guess_list.append((user_id, datasource_id, timestamp, path, "array", len(array), ""))
        # array items on the analyze query should check that sum(num) at the array path matches the count at their path
        i = 0
        for element in array:
            child_path = f"{path}[:]" if path.startswith("$") else f"{path}.{i}"
            i += 1
            guess(user_id, datasource_id, guess_list, element, timestamp, child_path)
    elif isinstance(x, set):
        x_list = list(x)
        if len(x_list) <= 100 or path.startswith("csv."):
            array = x_list
        else:
            array = x_list[:100]
        guess_list.append((user_id, datasource_id, timestamp, path, "array", len(array), ""))
        for i, element in enumerate(array):
            child_path = f"{path}[:]" if path.startswith("$") else f"{path}.{i}"
            guess(user_id, datasource_id, guess_list, element, timestamp, child_path)
    elif isinstance(x, datetime.datetime) or isinstance(x, datetime.date):
        guess_list.append((user_id, datasource_id, timestamp, path, "string", 0, x.isoformat()))
    else:
        raise Exception(f"Unexpected type of x {type(x)}")


regex_jsonpath_dot_compatible = re.compile(r"\w+")
regex_jsonpath_quote_compatible = re.compile(r"[^']*")


def jsonpath_add_key(path, key):
    """
    >>> jsonpath_add_key("$", "hola")
    '$.hola'
    >>> jsonpath_add_key("$", "bad$idea")
    "$.['bad$idea']"
    >>> jsonpath_add_key("$", "bad/idea")
    "$.['bad/idea']"
    >>> jsonpath_add_key("$", "bad\\idea")
    "$.['bad\\\\idea']"
    """
    if regex_jsonpath_dot_compatible.fullmatch(key):
        return f"{path}.{key}"
    if regex_jsonpath_quote_compatible.fullmatch(key):
        return f"{path}.['{key}']"
    raise Exception(f"JSONPath Unescapable key: {key}")
