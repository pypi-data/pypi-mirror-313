from __future__ import annotations

import logging
import re
import typing
import uuid
from typing import Iterable, List, Optional, Union

from typing_extensions import TypeAlias

from tinybird.constants import FORBIDDEN_WORDS

if typing.TYPE_CHECKING:
    from datasource import Datasource
    from pipe import Pipe

T: TypeAlias = Union["Datasource", "Pipe"]


class ForbiddenWordException(Exception):
    pass


class Resource:
    @staticmethod
    def guid(prefix: str = "t") -> str:
        return prefix + "_" + str(uuid.uuid4()).replace("-", "")

    @staticmethod
    def extract_guid(name: str) -> Optional[str]:
        """
        >>> a = Resource.guid()
        >>> Resource.extract_guid(a) == a
        True
        >>> a = Resource.guid('j')
        >>> Resource.extract_guid(a) == a
        True
        >>> a = Resource.guid('j')
        >>> Resource.extract_guid('j_testing_' + a[2:]) == a
        True
        >>> Resource.extract_guid('abcd')
        >>> Resource.extract_guid('a0123456789012345678901234567890123456789.table_a')
        >>> a = Resource.extract_guid('t_74bb93c2305d4aa887cb5fc9299ec57d_staging')
        >>> 't_74bb93c2305d4aa887cb5fc9299ec57d' == a
        True
        >>> Resource.extract_guid('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab')
        """

        if "_" not in name and "." not in name:
            return None
        p = re.match("(.*)_?([a-f0-9]{32})[^.]*$", name)
        if p:
            return p.groups()[0].split("_")[0] + "_" + p.groups()[1]
        return None

    @staticmethod
    def normalize(name_or_id: str) -> str:
        guid = Resource.extract_guid(name_or_id)
        if guid:
            name_or_id = guid
        return name_or_id

    @staticmethod
    def by_name_or_id(iter: Iterable[T], name_or_id: Optional[str]) -> Optional[T]:
        if not name_or_id:
            return None
        potential_id = Resource.normalize(name_or_id)
        return next((x for x in iter if x.name == name_or_id or x.id == potential_id), None)

    @staticmethod
    def by_names_or_ids(iter: Iterable[T], names_or_ids: List[str]) -> List[T]:
        if not names_or_ids:
            return []
        names_or_ids_set = set(names_or_ids)
        potential_ids = set([Resource.normalize(x) for x in names_or_ids])
        return [x for x in iter if x.name in names_or_ids_set or x.id in potential_ids]

    @staticmethod
    def sanitize_name(name: str) -> str:
        """
        >>> Resource.sanitize_name('-abc')
        'abc'
        >>> Resource.validate_name(Resource.sanitize_name('-abc'))
        True
        >>> Resource.sanitize_name('_abc')
        '_abc'
        >>> Resource.validate_name(Resource.sanitize_name('_abc'))
        True
        >>> Resource.sanitize_name('abc<h2>htmlInjection</h2>')
        'abch2htmlInjectionh2'
        >>> Resource.validate_name(Resource.sanitize_name('abc<h2>htmlInjection</h2>'))
        True
        >>> Resource.sanitize_name('abc http://google.com')
        'abchttpgooglecom'
        >>> Resource.validate_name(Resource.sanitize_name('abc http://google.com'))
        True
        """
        return re.sub(r"[^a-zA-Z0-9_]+", "", name)

    @staticmethod
    def validate_name(name: Optional[str]) -> bool:
        """
        >>> Resource.validate_name('-abc')
        False
        >>> Resource.validate_name('-mv')
        False
        >>> Resource.validate_name('-')
        False
        >>> Resource.validate_name('_')
        True
        >>> Resource.validate_name('1')
        False
        >>> Resource.validate_name('-ab-cd')
        False
        >>> Resource.validate_name('_abc')
        True
        >>> Resource.validate_name('_ab-cd')
        False
        >>> Resource.validate_name('ab_cd')
        True
        >>> Resource.validate_name('_ab_cd')
        True
        >>> Resource.validate_name('ab-cd')
        False
        >>> Resource.validate_name('abcdf-rtyt')
        False
        >>> Resource.validate_name('abcdfrtyt-')
        False
        >>> Resource.validate_name('abc')
        True
        >>> Resource.validate_name('')
        False
        >>> Resource.validate_name(None)
        False
        >>> Resource.validate_name('ab_c_9')
        True
        >>> Resource.validate_name('0ab_c_9')
        False
        >>> Resource.validate_name('a-bc')
        False
        >>> Resource.validate_name('paco paco paco')
        False
        >>> Resource.validate_name('numbers')
        True
        >>> Resource.validate_name('url')
        True
        >>> Resource.validate_name('ñúrl')
        False
        >>> Resource.validate_name('r')
        True
        >>> Resource.validate_name('from')
        Traceback (most recent call last):
        ...
        tinybird.resource.ForbiddenWordException: from is a reserved word. Name must start with a letter and contain only letters, numbers, and underscores. Hint: use from_.
        """
        if not name:
            name = ""
        valid_chars = re.match(r"^[^-]", name, re.I | re.ASCII) is not None
        valid_name = valid_chars and re.match(r"[^\d][\w\d_]*$", name, re.I | re.ASCII) is not None
        if not valid_name:
            logging.warning(f"Detected invalid resource name {name}. reason=invalid")
        if name.lower() in FORBIDDEN_WORDS:
            logging.warning(f"Detected invalid resource name {name}. reason=forbidden")
            raise ForbiddenWordException(f"{name} is a reserved word. {Resource.name_help(name)}")
        return valid_name

    @staticmethod
    def name_help(name: str, force: bool = True) -> str:
        return (
            f"Name must start with a letter and contain only letters, numbers, and underscores."
            f" Hint: use {Resource.normalize_name(name, force=force)}."
        )

    @staticmethod
    def normalize_name(s: str, prefix: str = "t", force: bool = False) -> str:
        """
        >>> Resource.normalize_name('_', force=True)
        't_'
        >>> Resource.normalize_name('-', force=True)
        't_'
        >>> Resource.normalize_name('1', force=True)
        't_1'
        >>> Resource.normalize_name('_')
        't_'
        >>> Resource.normalize_name('-')
        't_'
        >>> Resource.normalize_name('1')
        't_1'
        >>> Resource.normalize_name('_test_without_starting_underscore', force=True)
        'test_without_starting_underscore_'
        >>> Resource.normalize_name('thename')
        'thename'
        >>> Resource.normalize_name('0thename', prefix='work')
        'work_0thename'
        >>> Resource.normalize_name('5othername', force=True)
        't_5othername_'
        >>> Resource.normalize_name('some.email@gmail.com')
        'some_email_gmail_com'
        >>> Resource.normalize_name('')
        ''
        >>> Resource.normalize_name('test_without_starting_underscore', force=True)
        'test_without_starting_underscore_'
        >>> Resource.normalize_name('from', force=True)
        'from_'
        """
        s = re.sub(r"[^0-9a-zA-Z_]", "_", s)
        if len(s) > 1 and force and s[0] in "-_":
            s = f"{s[1:]}_"
        elif len(s) > 1 and force:
            s = f"{s}_"
        if len(s) == 1 and s[0] in "-_":
            return f"{prefix}_"
        elif len(s) > 0 and (s[0] in "0123456789"):
            return f"{prefix}_{s}"
        return s
