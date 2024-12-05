import base64
from decimal import Decimal
from typing import Any

from boto3.dynamodb.types import Binary, TypeDeserializer

dynamodbstreams_deserializer = TypeDeserializer()


def from_dynamodb_to_json_raw(item):
    def _deserialize_raw(value):
        dynamodb_type = list(value.keys())[0]

        deserialized_value = None

        # DynamoDB stream base64-encodes all binary types, must base64 decode first for consistency
        if dynamodb_type == "B" and isinstance(value["B"], str):
            value = {"B": base64.b64decode(value["B"])}
            deserialized_value = dynamodbstreams_deserializer.deserialize(value)
        elif dynamodb_type == "B":
            deserialized_value = base64.b64encode(value["B"]).decode("utf-8")
        elif dynamodb_type == "BS":
            deserialized_value = set([base64.b64encode(v).decode("utf-8") for v in value["BS"]])
        else:
            deserialized_value = dynamodbstreams_deserializer.deserialize(value)

        return {dynamodb_type: deserialized_value}

    def decode_value(dynamodb_value: Any) -> Any:
        if isinstance(dynamodb_value, set):
            decoded_value_set = set()
            for v in dynamodb_value:
                decoded_value_set.add(decode_value(v))
            return decoded_value_set
        if isinstance(dynamodb_value, list):
            decoded_value_list = []
            for v in dynamodb_value:
                decoded_value_list.append(decode_value(v))
            return decoded_value_list
        if isinstance(dynamodb_value, dict):
            decoded_value_dict = {}
            for k, v in dynamodb_value.items():
                decoded_value_dict[k] = decode_value(v)
            return decoded_value_dict
        if isinstance(dynamodb_value, Decimal):
            # Decimal is a float if exponent is negative
            if dynamodb_value.as_tuple().exponent < 0:  # type: ignore
                return float(dynamodb_value)
            return int(dynamodb_value)
        elif isinstance(dynamodb_value, Binary):
            # DynamoDB stream base64-encodes all binary types, must base64 decode first
            return base64.b64encode(dynamodb_value.value).decode("utf-8")
        elif isinstance(dynamodb_value, bytes):
            return base64.b64encode(dynamodb_value).decode("utf-8")
        return dynamodb_value

    def decode_type(value: Any) -> Any:
        dynamodb_value = list(value.values())[0]

        return decode_value(dynamodb_value)

    if not item:
        return {}

    return {k: decode_type(_deserialize_raw(v)) for k, v in item.items()}


def from_dynamodb_to_json_with_strings(item):
    def _deserialize(value):
        dynamodb_type = list(value.keys())[0]

        if dynamodb_type == "NULL":
            return None
        elif dynamodb_type == "BOOL":
            return value["BOOL"]
        elif dynamodb_type == "N":
            return value["N"]
        elif dynamodb_type == "S":
            return value["S"]
        if dynamodb_type == "B":
            return base64.b64encode(value["B"]).decode("utf-8")
        elif dynamodb_type == "NS":
            return value["NS"]
        elif dynamodb_type == "SS":
            return value["SS"]
        elif dynamodb_type == "BS":
            return [base64.b64encode(v).decode("utf-8") for v in value["BS"]]
        elif dynamodb_type == "L":
            return [_deserialize(v) for v in value["L"]]
        elif dynamodb_type == "M":
            return {k: _deserialize(v) for k, v in value["M"].items()}

        return None

    if not item:
        return {}

    return {k: _deserialize(v) for k, v in item.items()}
