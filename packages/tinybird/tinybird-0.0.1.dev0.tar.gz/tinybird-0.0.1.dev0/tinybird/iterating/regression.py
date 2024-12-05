import dataclasses
import logging
import re
import unittest
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Iterable, List, Optional, Tuple, Type, Union
from urllib.parse import urlencode

import orjson as json
import requests
from humanfriendly import format_size

from tinybird.ch import HTTPClient
from tinybird.datafile import PipeChecker, PipeCheckerRunner, PipeCheckerRunnerResponse, itemgetter, normalize_array
from tinybird.iterating.release import Release
from tinybird.job import Job, JobCancelledException, JobExecutor, JobKind, JobStatus
from tinybird.tokens import scopes
from tinybird.user import User, UserAccount, Users, public

LOG_TAG = "[REGRESSION_BRANCH_LOG]"


class RegressionTestError(Exception):
    pass


class RegressionTestType(Enum):
    COVERAGE = "coverage"
    LAST = "last"
    MANUAL = "manual"


@dataclass
class RegressionTestsConfig:
    assert_result: bool = True
    assert_result_no_error: bool = True
    assert_result_rows_count: bool = True
    assert_result_ignore_order: bool = False
    assert_time_increase_percentage: int = 25
    assert_bytes_read_increase_percentage: int = 25
    assert_max_time: float = 0.3
    relative_change: float = 0.01
    failfast: bool = False
    skip: bool = False

    @classmethod
    def from_dict(cls, config_dict: Dict) -> "RegressionTestsConfig":
        try:
            return RegressionTestsConfig(**config_dict) if config_dict else RegressionTestsConfig()
        except TypeError as exc:
            unknown_config = re.findall("'.*'", str(exc))[0]
            raise RegressionTestError(f"unknown config {unknown_config}")


@dataclass
class BaseRegressionTests:
    config: RegressionTestsConfig

    @classmethod
    def from_dict(
        cls, regression_test_dict: Dict
    ) -> Union["CoverageRegressionTests", "LastRegressionTests", "ManualRegressionTests"]:
        RegressionTestsType = Union[
            Type["CoverageRegressionTests"],
            Type["LastRegressionTests"],
            Type["ManualRegressionTests"],
        ]

        test_matrix: Dict[str, Tuple[Optional[str], Optional[RegressionTestsType]]] = {
            RegressionTestType.COVERAGE.value: (
                RegressionTestType.COVERAGE.value,
                CoverageRegressionTests,
            ),
            RegressionTestType.LAST.value: (
                RegressionTestType.LAST.value,
                LastRegressionTests,
            ),
            RegressionTestType.MANUAL.value: (
                RegressionTestType.MANUAL.value,
                ManualRegressionTests,
            ),
        }

        test_type, test_class = test_matrix.get(list(regression_test_dict.keys())[0], (None, None))
        if test_type is not None and test_class is not None:
            try:
                return (
                    test_class.from_dict(regression_test_dict[test_type])
                    if regression_test_dict[test_type]
                    else test_class.from_dict({"config": {}})
                )
            except TypeError as exc:
                unknown_argument = re.findall("'.*'", str(exc))[0]
                raise RegressionTestError(f"unknown test argument for '{test_type}': {unknown_argument}")
        else:
            unknown_test = regression_test_dict.keys() and list(regression_test_dict.keys())[0]
            raise RegressionTestError(f"test unknown: '{str(unknown_test)}'")

    def to_dict(self) -> Dict:
        raise NotImplementedError

    @property
    def test_type(self) -> str:
        return list(self.to_dict().keys())[0]


@dataclass
class CoverageRegressionTests(BaseRegressionTests):
    samples_by_params: int = 1
    matches: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, test_dict: Dict) -> "CoverageRegressionTests":
        test_dict["config"] = RegressionTestsConfig.from_dict(test_dict.get("config", {}))
        return CoverageRegressionTests(**test_dict)

    def to_dict(self) -> Dict:
        return {RegressionTestType.COVERAGE.value: asdict(self)}


@dataclass
class LastRegressionTests(BaseRegressionTests):
    limit: int = 1
    matches: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, test_dict: Dict) -> "LastRegressionTests":
        test_dict["config"] = RegressionTestsConfig.from_dict(test_dict.get("config", {}))
        return LastRegressionTests(**test_dict)

    def to_dict(self) -> Dict:
        return {RegressionTestType.LAST.value: asdict(self)}


@dataclass
class ManualRegressionTests(BaseRegressionTests):
    params: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, test_dict: Dict) -> "ManualRegressionTests":
        test_dict["config"] = RegressionTestsConfig.from_dict(test_dict.get("config", {}))
        return ManualRegressionTests(**test_dict)

    def to_dict(self) -> Dict:
        return {RegressionTestType.MANUAL.value: asdict(self)}


@dataclass
class RegressionTestsCommand:
    pipe: str
    tests: List[Union[CoverageRegressionTests, LastRegressionTests, ManualRegressionTests]] = field(
        default_factory=list
    )

    def get_pipes(self, pipes: List[str]) -> List[str]:
        return [pipe for pipe in pipes if re.fullmatch(self.pipe, pipe)]

    @classmethod
    def from_dict(cls, regression_command_dict: Dict) -> "RegressionTestsCommand":
        try:
            if regression_command_dict["tests"] is None:
                raise RegressionTestError(f"missing 'tests' for {regression_command_dict}")
            copy_regression_command_dict = regression_command_dict.copy()
            copy_regression_command_dict["tests"] = [
                BaseRegressionTests.from_dict(test) for test in copy_regression_command_dict["tests"]
            ]
            return RegressionTestsCommand(**copy_regression_command_dict)
        except KeyError as exc:
            missing_argument = re.findall("'.*'", str(exc))[0]
            raise RegressionTestError(f"missing argument {missing_argument} for {regression_command_dict}")
        except TypeError as exc:
            unknown_argument = re.findall("'.*'", str(exc))[0]
            raise RegressionTestError(f"unknown argument {unknown_argument} for {regression_command_dict}")


class ReleasePipeChecker(PipeChecker):
    def __init__(
        self,
        request: Dict[str, Any],
        pipe_name: str,
        token: str,
        test_type: str,
        assert_result_no_error: bool,
        assert_result_rows_count: bool,
        assert_result: bool,
        assert_result_ignore_order: bool,
        assert_time_increase_percentage: int,
        assert_bytes_read_increase_percentage: int,
        assert_max_time: float,
        relative_change: float,
        skip: bool,
        current_semver: Optional[str] = None,
        checker_semver: Optional[str] = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(
            request,
            pipe_name,
            pipe_name,
            token,
            False,
            False,
            False,
            relative_change,
            *args,
            **kwargs,
        )
        if current_semver:
            self.current_pipe_url += f"{'&' if '?' in self.current_pipe_url else '?'}__tb__semver={current_semver}"
        if checker_semver:
            self.checker_pipe_url += f"{'&' if '?' in self.checker_pipe_url else '?'}__tb__semver={checker_semver}"
        self.test_type = test_type
        self.assert_result_no_error = assert_result_no_error
        self.assert_result_rows_count = assert_result_rows_count
        self.assert_result_ignore_order = assert_result_ignore_order
        self.assert_result = assert_result
        self.assert_time_increase_percentage = assert_time_increase_percentage
        self.assert_bytes_read_increase_percentage = assert_bytes_read_increase_percentage
        self.assert_max_time = assert_max_time
        self.skip = skip
        self.relative_change: float = 0.01
        self.increase_response_time: float = 0.0
        self.increase_read_bytes: float = 0.0
        self.skipped_response_time: bool = False
        self.warning: Optional[str] = None

    def __str__(self):
        test = f"{self.pipe_name}({self.test_type}) - {self.checker_pipe_url}"
        if self.http_method == "POST":
            test += f" - POST Body: {self.pipe_request_params}"
        if self.warning:
            test = f"🚨 Warning: {self.warning}\n\n{test}\n"
        if self.skip:
            test = f"🚨 Skipped: {self.pipe_name}({self.test_type})\n"
        return test

    def _get_request_for_current(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        return requests.get(self.current_pipe_url, headers=headers)

    def _get_request_for_checker(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        return requests.get(self.checker_pipe_url, headers=headers)

    def _post_request_for_current(self):
        headers = {"Authorization": f"Bearer {self.token}", "Content-type": "application/json"}
        try:
            params = json.dumps(self.pipe_request_params)
        except Exception:
            params = b"{}"
        return requests.post(self.current_pipe_url, headers=headers, data=params)

    def _post_request_for_checker(self):
        headers = {"Authorization": f"Bearer {self.token}", "Content-type": "application/json"}
        try:
            params = json.dumps(self.pipe_request_params)
        except Exception:
            params = b"{}"
        return requests.post(self.checker_pipe_url, headers=headers, data=params)

    def _write_performance(self):
        response_time = (
            f"({round(self.increase_response_time, 3)}% skipped < {self.assert_max_time})"
            if self.skipped_response_time
            else f"({round(self.increase_response_time, 3)}%)"
        )
        return f"{round(self.checker_response_time, 3)}s {response_time} {format_size(self.checker_read_bytes)} ({self.increase_read_bytes}%) "

    def _runTest(self) -> None:
        if self.skip:
            return

        if self.http_method == "GET":
            current_r = self._get_request_for_current()
            checker_r = self._get_request_for_checker()
        else:
            current_r = self._post_request_for_current()
            checker_r = self._post_request_for_checker()

        try:
            self.current_response_time = current_r.elapsed.total_seconds()
            self.checker_response_time = checker_r.elapsed.total_seconds()
            self.increase_response_time = (
                round(
                    (self.checker_response_time - self.current_response_time) / self.current_response_time,
                    2,
                )
                * 100
            )

            if self.current_response_time < self.assert_max_time and self.checker_response_time < self.assert_max_time:
                self.increase_response_time = 0
                self.skipped_response_time = True
        except Exception:
            pass

        current_response: Dict[str, Any] = current_r.json()
        checker_response: Dict[str, Any] = checker_r.json()

        current_data: List[Dict[str, Any]] = current_response.get("data", [])
        checker_data: List[Dict[str, Any]] = checker_response.get("data", [])

        self.current_read_bytes = current_response.get("statistics", {}).get("bytes_read", 0)
        self.checker_read_bytes = checker_response.get("statistics", {}).get("bytes_read", 0)
        self.increase_read_bytes = (
            round(
                (self.checker_read_bytes - self.current_read_bytes) / self.current_read_bytes,
                2,
            )
            * 100
            if self.current_read_bytes
            else self.checker_read_bytes
        )

        error_data: Optional[str] = checker_response.get("error", None)

        base_assert_error_feedback = "{message}\n💡 Hint: Use {flag} if it's expected and want to skip the assert.\n\nOrigin Workspace: {current_pipe_url}\nTest Branch: {checker_pipe_url}"

        if self.assert_result_no_error:
            self.assertIsNone(
                error_data,
                base_assert_error_feedback.format(
                    message="Unexpected error in result, this might indicate regression.",
                    flag="`--no-assert-result-no-error`",
                    current_pipe_url=self.current_pipe_url,
                    checker_pipe_url=self.checker_pipe_url,
                ),
            )

        if self.assert_result_rows_count:
            self.assertEqual(
                len(current_data),
                len(checker_data),
                base_assert_error_feedback.format(
                    message="Unexpected number of result rows count, this might indicate regression.",
                    flag="`--no-assert-result-rows-count`",
                    current_pipe_url=self.current_pipe_url,
                    checker_pipe_url=self.checker_pipe_url,
                ),
            )

        if self.assert_result_ignore_order:
            current_data = (
                sorted(
                    normalize_array(current_data),
                    key=itemgetter(*[k for k in current_data[0].keys()]),
                )
                if len(current_data) > 0
                else current_data
            )
            checker_data = (
                sorted(
                    normalize_array(checker_data),
                    key=itemgetter(*[k for k in checker_data[0].keys()]),
                )
                if len(checker_data) > 0
                else checker_data
            )

        # Only assert result with same number of rows
        if self.assert_result_rows_count and self.assert_result:
            base_message = (
                "Expected result differs among pipes, that might indicate there's a regression in the new pipe endpoint"
            )
            for _, (current_data_e, check_fixtures_data_e) in enumerate(zip(current_data, checker_data, strict=True)):
                if self.assert_result or (self.assert_result_ignore_order and self.assert_result):
                    self.assertEqual(list(current_data_e.keys()), list(check_fixtures_data_e.keys()))
                    for x in current_data_e.keys():
                        if isinstance(current_data_e[x], (float, int)):
                            d = abs(current_data_e[x] - check_fixtures_data_e[x])
                            try:
                                self.assertLessEqual(
                                    d / current_data_e[x],
                                    self.relative_change,
                                    base_assert_error_feedback.format(
                                        message=f"{current_data_e[x]} != {check_fixtures_data_e[x]} : {base_message}\nCheck result diff:{self.diff(current_data_e, check_fixtures_data_e)}",
                                        flag="`--no-assert-result`",
                                        current_pipe_url=self.current_pipe_url,
                                        checker_pipe_url=self.checker_pipe_url,
                                    ),
                                )
                            except ZeroDivisionError:
                                self.assertEqual(
                                    d,
                                    0,
                                    f"key {x}. old value: {current_data_e[x]}, new value: {check_fixtures_data_e[x]}\n{self.diff(current_data_e, check_fixtures_data_e)}",
                                )
                        elif (
                            not isinstance(current_data_e[x], (str, bytes))
                            and isinstance(current_data_e[x], Iterable)
                            and self.assert_result_ignore_order
                        ):

                            def flatten(items):
                                """Yield items from any nested iterable; see Reference."""
                                output = []
                                for x in items:
                                    if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
                                        output.extend(flatten(x))
                                    else:
                                        output.append(x)
                                return output

                            self.assertEqual(
                                flatten(current_data_e[x]).sort(),
                                flatten(check_fixtures_data_e[x]).sort(),
                                base_assert_error_feedback.format(
                                    message=f"{base_message}\n\nCheck result diff \n"
                                    + self.diff(current_data_e, check_fixtures_data_e),
                                    flag="`--assert-result-ignore-order`",
                                    current_pipe_url=self.current_pipe_url,
                                    checker_pipe_url=self.checker_pipe_url,
                                ),
                            )
                        else:
                            self.assertEqual(
                                current_data_e[x],
                                check_fixtures_data_e[x],
                                base_assert_error_feedback.format(
                                    message=f"{base_message}\n\nCheck result diff \n"
                                    + self.diff(current_data_e, check_fixtures_data_e),
                                    flag="`--no-assert-result`",
                                    current_pipe_url=self.current_pipe_url,
                                    checker_pipe_url=self.checker_pipe_url,
                                ),
                            )

        base_assert_error_feedback_with_threshold = "{message}\n💡 Hint: Use `--assert-{assert_type}-increase-percentage -1` if it's expected and want to skip the assert. {more_hint}\n\nOrigin Workspace: {current_pipe_url}\nTest Branch: {checker_pipe_url}"

        if self.assert_time_increase_percentage >= 0:
            self.assertLess(
                self.increase_response_time,
                self.assert_time_increase_percentage,
                msg=base_assert_error_feedback_with_threshold.format(
                    message=f"Response time has increased {self.increase_response_time}%",
                    assert_type="time",
                    current_pipe_url=self.current_pipe_url,
                    checker_pipe_url=self.checker_pipe_url,
                    more_hint="Alternatively use `--assert-max-time` to set a max threshold for the response time of the endpoint before taking into account the response time increase percentage.",
                ),
            )

        if self.assert_bytes_read_increase_percentage >= 0:
            self.assertLess(
                self.increase_read_bytes,
                self.assert_bytes_read_increase_percentage,
                msg=base_assert_error_feedback_with_threshold.format(
                    message=f"Processed bytes has increased {self.increase_read_bytes}%",
                    assert_type="bytes-read",
                    current_pipe_url=self.current_pipe_url,
                    checker_pipe_url=self.checker_pipe_url,
                    more_hint="",
                ),
            )


class ReleaseRegressionTestsRunner(PipeCheckerRunner):
    class Stream2Buffer(unittest.runner._WritelnDecorator):
        def __init__(self, stream):
            super().__init__(stream)
            self._buffer = []

        def write(self, message):
            self._buffer.append(message)

        def flush(self):
            pass

    checker_stream_result_class = Stream2Buffer

    def __init__(
        self,
        pipe_name: str,
        host: str,
        config: RegressionTestsConfig,
        test_type: str,
        current_semver: Optional[str] = None,
        checker_semver: Optional[str] = None,
    ):
        super().__init__(pipe_name, host)
        self.config = config
        self.test_type = test_type
        self.current_semver = current_semver
        self.checker_semver = checker_semver

    def _get_checker(
        self,
        request: Dict[str, Any],
        checker_pipe_name: str,
        token: str,
        only_response_times: bool,
        ignore_order: bool,
        validate_processed_bytes: bool,
        relative_change: float,
    ) -> PipeChecker:
        return ReleasePipeChecker(
            request,
            self.pipe_name,
            token,
            self.test_type,
            current_semver=self.current_semver,
            checker_semver=self.checker_semver,
            assert_result_no_error=self.config.assert_result_no_error,
            assert_result_rows_count=self.config.assert_result_rows_count,
            assert_result=self.config.assert_result,
            assert_time_increase_percentage=self.config.assert_time_increase_percentage,
            assert_bytes_read_increase_percentage=self.config.assert_bytes_read_increase_percentage,
            assert_result_ignore_order=self.config.assert_result_ignore_order,
            assert_max_time=self.config.assert_max_time,
            relative_change=self.config.relative_change,
            skip=self.config.skip,
        )


class ReleasePipeRegression:
    def __init__(self, branch: User, host: str):
        self.branch = branch
        self.host = host

    def run(
        self,
        token: str,
        command: RegressionTestsCommand,
        current_semver: Optional[str] = None,
        checker_semver: Optional[str] = None,
    ) -> PipeCheckerRunnerResponse:
        test = command.tests[0]
        if test.config.skip:
            runner_response = PipeCheckerRunnerResponse(
                pipe_name=command.pipe,
                test_type=test.test_type,
                output=f"🚨 Skipped: {command.pipe}({test.test_type})\n",
                metrics_summary={},
                metrics_timing={},
                failed=[],
                was_successfull=True,
            )
            return runner_response
        regression_runner = ReleaseRegressionTestsRunner(
            command.pipe,
            self.host,
            test.config,
            test.test_type,
            current_semver=current_semver,
            checker_semver=checker_semver,
        )
        runner_response = PipeCheckerRunnerResponse(
            pipe_name=command.pipe,
            test_type=test.test_type,
            output="",
            metrics_summary={},
            metrics_timing={},
            failed=[],
            was_successfull=True,
        )

        public_workspace = public.get_public_user()
        pipe_stats_rt = Users.get_datasource(public_workspace, "pipe_stats_rt")
        if pipe_stats_rt is None:
            logging.error("pipe_stats_rt for requests_to_check not found")
            return runner_response
        # default values
        matches: List[str] = []
        sample_by_params = 1
        limit = 0

        if isinstance(test, CoverageRegressionTests):
            sample_by_params = test.samples_by_params or sample_by_params
        if isinstance(test, LastRegressionTests):
            limit = test.limit or limit

        # TODO: this is no longer used for branches
        only_response_times = test.config.assert_time_increase_percentage >= 0
        ignore_order = test.config.assert_result_ignore_order
        failfast = test.config.failfast
        relative_change = test.config.relative_change
        validate_processed_bytes = test.config.assert_bytes_read_increase_percentage >= 0

        pipe_request_to_check: List[Dict[str, Any]] = []

        if isinstance(test, ManualRegressionTests):
            if test.params is None:
                test.params = []
            for req in test.params:
                pipe_request_to_check += [
                    {
                        "endpoint_url": f"{self.host}/v0/pipes/{command.pipe}.json?{urlencode(req)}",
                        "pipe_request_params": req,
                        "http_method": "GET",
                    }
                ]
        else:
            (
                sql_for_coverage,
                sql_latest_requests,
            ) = regression_runner.get_sqls_for_requests_to_check(
                matches,
                sample_by_params,
                limit,
                pipe_stats_rt_table=f"{public_workspace.database}.{pipe_stats_rt.id}",
                extra_where_clause=f" AND user_id = '{self.branch.origin}' ",
            )
            client = HTTPClient(
                public_workspace["database_server"],
                database=public_workspace["database"],
            )
            q = sql_for_coverage if limit == 0 and sample_by_params > 0 else sql_latest_requests
            _, body = client.query_sync(q, read_only=True)
            r = json.loads(body)
            for row in r.get("data", []):
                for i in range(len(row["endpoint_url"])):
                    pipe_request_to_check += [
                        {
                            "endpoint_url": f"{self.host}{row['endpoint_url'][i]}",
                            "pipe_request_params": row["pipe_request_params"][i],
                            "http_method": row["http_method"],
                        }
                    ]
        if pipe_request_to_check:
            runner_response = regression_runner.run_pipe_checker(
                pipe_request_to_check,
                command.pipe,
                token,
                only_response_times,
                ignore_order,
                validate_processed_bytes,
                relative_change,
                failfast,
                custom_output=True,
                debug=True,
            )
        else:
            runner_response = PipeCheckerRunnerResponse(
                pipe_name=command.pipe,
                test_type=test.test_type,
                output=f"🚨 No requests found for the endpoint {command.pipe} - {test.test_type} (Skipping validation).\n💡 See this guide for more info about the regression tests => https://www.tinybird.co/docs/production/implementing-test-strategies.html#testing-strategies\n",
                metrics_summary={},
                metrics_timing={},
                failed=[],
                # For now let's mark is as valid to not have requests and the CLI will mark this meesage as a warning
                was_successfull=True,
            )
        return runner_response


def new_regression_tests_job(
    job_executor: JobExecutor,
    branch_workspace: User,
    user_account: UserAccount,
    api_host: str,
    regression_commands: List[RegressionTestsCommand],
    run_in_main: Optional[bool] = False,
):
    j = RegressionTestsJob(branch_workspace, user_account, api_host, regression_commands, run_in_main)
    j.save()
    checker_semver: Optional[str] = j.get_checker_semver(branch_workspace)
    # mypy shit
    main = Users.get_by_id(branch_workspace.origin) if branch_workspace.origin else None
    current_semver: Optional[str] = j.get_current_semver(main)
    logging.info(
        f"New regression job created: job_id={j.id}, branch={branch_workspace.id}, run_in_main={run_in_main}, checker_semver={checker_semver}, current_semver={current_semver}"
    )
    job_executor.put_job(j)
    return j


class RegressionTestsJob(Job):
    def __init__(
        self,
        branch_workspace: User,
        user_account: UserAccount,
        api_host: str,
        commands: List[RegressionTestsCommand],
        run_in_main: Optional[bool] = False,
    ):
        self.database_server = branch_workspace["database_server"]
        self.database = branch_workspace["database"]
        self.branch_id = branch_workspace.id
        self.main_id = branch_workspace.origin
        self.user_account_id = user_account.id
        self.progress_counter = 0
        self.progress_total = 0
        self.progress_percentage = 0.0
        self.progress: List[Dict[str, Any]] = []
        self.api_host = api_host
        self.commands: List[RegressionTestsCommand] = commands if commands else []
        self.run_in_main = run_in_main
        Job.__init__(self, JobKind.REGRESSION, branch_workspace)

    def _unfold_commands(
        self, commands: List[RegressionTestsCommand], pipe_endpoints: List[str]
    ) -> List[RegressionTestsCommand]:
        new_commands: List[RegressionTestsCommand] = []
        if not commands:
            for pipe in pipe_endpoints:
                config = RegressionTestsConfig.from_dict({})
                new_commands.append(
                    RegressionTestsCommand(
                        pipe=pipe,
                        tests=[CoverageRegressionTests(samples_by_params=1, matches=[], config=config)],
                    )
                )
        else:
            for command in reversed(commands):
                pipes = command.get_pipes(pipe_endpoints)
                for pipe in pipes:
                    if pipe not in [command.pipe for command in new_commands]:
                        for test in command.tests:
                            command_dict = {
                                "pipe": pipe,
                                "tests": [test.to_dict().copy()],
                            }
                            new_commands.append(RegressionTestsCommand.from_dict(command_dict))
        return new_commands

    def to_json(self, u=None, debug=None):
        job = super().to_json(u, debug)
        job["progress"] = self.progress
        job["progress_percentage"] = self.progress_percentage
        job["run_in_main"] = self.run_in_main
        if self.status == JobStatus.ERROR and "error" in self.result:
            job["error"] = self.result["error"]
        return job

    def update_progress(self, response: PipeCheckerRunnerResponse):
        self.progress_counter += 1
        self.progress_percentage = self.progress_counter / self.progress_total * 100
        run = dataclasses.asdict(response)
        self.progress.append(
            {
                "step": self.progress_counter,
                "timestamp": f"{datetime.utcnow()} [UTC]",
                "run": run,
                "percentage": self.progress_percentage,
            }
        )
        logging.info(f"{LOG_TAG} - job => {self.id} branch => {self.branch_id} - main => {self.main_id} - {run}")
        self.save()

    def get_checker_semver(self, branch: User) -> Optional[str]:
        try:
            if self.run_in_main:
                return "regression"
            release = Release.sort_by_date(branch.get_releases())[0]
            if release.is_live:
                return None
            return release.semver
        except Exception as e:
            logging.exception(e)
            return None

    def get_current_semver(self, main: Optional[User]) -> str:
        if self.run_in_main:
            return "regression-main"
        return main.current_release.semver if main and main.current_release else "snapshot"

    def run_regression_tests(self, job):
        branch = Users.get_by_id(self.branch_id)
        # We should never reach this point with a branch without a main
        assert branch.origin is not None
        main = Users.get_by_id(branch.origin)
        token = branch.get_unique_token_for_resource(self.user_account_id, scopes.ADMIN_USER)

        main_pipe_endpoints = {pipe.name for pipe in main.get_pipes() if pipe.endpoint}

        # Avoid regression tests on the pipes that are new (not in main)
        pipe_endpoints = [pipe for pipe in branch.get_pipes() if pipe.endpoint and pipe.name in main_pipe_endpoints]

        commands = self._unfold_commands(self.commands, [pipe.name for pipe in pipe_endpoints])
        branch_pipe_regression = ReleasePipeRegression(branch, self.api_host)
        self.progress_total = len(commands)

        current_semver = self.get_current_semver(main)
        checker_semver = self.get_checker_semver(branch)

        for command in commands:
            job.update_progress(
                branch_pipe_regression.run(token, command, current_semver=current_semver, checker_semver=checker_semver)
            )

    def run(self):
        def function_to_execute(job):
            try:
                self.run_regression_tests(job)
            except JobCancelledException:
                job.save()
                job.mark_as_cancelled()
            except Exception as e:
                logging.exception(str(e))
                job.save()
                job.mark_as_error({"error": str(e)})
            else:
                job.save()
                job.mark_as_done({}, None)

        self.job_executor.submit(function_to_execute, self)
        return self
