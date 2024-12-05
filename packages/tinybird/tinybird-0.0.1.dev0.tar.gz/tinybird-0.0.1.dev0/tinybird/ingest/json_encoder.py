import base64
import datetime
import decimal
import json
from uuid import UUID

# This class comes from djanjo JsonEncoder:
# https://github.com/django/django/blob/dde2537fbb04ad78a673092a931b449245a2d6ae/django/core/serializers/json.py#L77-L106


class ExtendedJsonEncoder(json.JSONEncoder):
    """
    JSONEncoder that supports to encode date/time, decimal and UUID types.
    """

    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime.datetime):
            r = o.isoformat()
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith("+00:00"):
                r = r[:-6] + "Z"
            return r
        elif isinstance(o, datetime.date):
            return o.isoformat()
        elif isinstance(o, datetime.time):
            if is_aware(o):
                raise ValueError("JSON can't represent timezone-aware times.")
            r = o.isoformat()
            if o.microsecond:
                r = r[:12]
            return r
        elif isinstance(o, decimal.Decimal):
            return str(o)
        elif isinstance(o, UUID):
            return o.hex

        try:
            return super().default(o)
        except Exception as e:
            if isinstance(o, bytes):
                return base64.b64encode(o).decode("utf-8")
            else:
                raise e


def is_aware(value):
    """
    Determines if a given datetime.datetime is aware.

    The logic is described in Python's docs:
    http://docs.python.org/library/datetime.html#datetime.tzinfo
    """
    return value.tzinfo is not None and value.tzinfo.utcoffset(value) is not None
