import math
from typing import Any, Dict, Optional, Union

from tinybird.model import RedisModel


class DynamoDBStreamsShard(RedisModel):
    __namespace__ = "dynamodbstreams"
    __owner__ = "linker_id"
    __ttl__ = 24 * 60 * 60
    __owner_max_children__ = math.inf

    __props__ = [
        "linker_id",
        "stream_arn",
        "shard_id",
        "parent_shard_id",
        "last_sequence_number",
        "finished",
        "closed",
    ]

    def __init__(
        self,
        linker_id: str,
        stream_arn: str,
        shard_id: str,
        last_sequence_number: Optional[str],
        finished: bool,
        closed: bool,
        parent_shard_id: str = "",
        is_dirty=True,
        shard_iterator=None,
        **shard_dict: Union[str, Dict[str, Any]],
    ):
        self.linker_id = linker_id
        self.stream_arn = stream_arn
        self.shard_id = shard_id
        self.last_sequence_number = last_sequence_number
        # This variable represents the current version of the last_sequence_number
        # that's stored in redis. Useful to perform a rollback without performing a read
        # access to redis.
        self.saved_last_sequence_number = last_sequence_number
        self.finished = finished
        self.closed = closed
        self.parent_shard_id = parent_shard_id

        # Those variables are not stored in redis but are part of the class
        self.shard_iterator = shard_iterator
        self.is_dirty = is_dirty

        super().__init__(**shard_dict)

    def __eq__(self, other):
        if not isinstance(other, DynamoDBStreamsShard):
            return False

        return (
            self.id == other.id
            and self.linker_id == other.linker_id
            and self.stream_arn == other.stream_arn
            and self.shard_id == other.shard_id
            and self.parent_shard_id == other.parent_shard_id
            and self.last_sequence_number == other.last_sequence_number
            and self.finished == other.finished
            and self.closed == other.closed
            and self.shard_iterator == other.shard_iterator
        )

    def __repr__(self) -> str:
        return (
            f"DynamoDBStreamsShard({self.id}, {self.linker_id}, {self.stream_arn}, {self.shard_id}, "
            f"{self.parent_shard_id}, {self.last_sequence_number}, {self.finished}, {self.closed}, "
            f"{self.shard_iterator}, {self.is_dirty}, {self.created_at}, {self.updated_at})"
        )

    # sets the shard iterator, does not mark shard as dirty as
    # this variable does not get propagated
    def set_shard_iterator(self, shard_iterator: Optional[str]) -> None:
        self.shard_iterator = shard_iterator

    def set_last_sequence_number(self, last_sequence_number: Optional[str]) -> None:
        if self.last_sequence_number != last_sequence_number:
            self.is_dirty = True
        self.last_sequence_number = last_sequence_number

    def set_finished(self, finished: bool) -> None:
        if self.finished != finished:
            self.is_dirty = True
        self.finished = finished

    def set_closed(self, closed: bool) -> None:
        if self.closed != closed:
            self.is_dirty = True
        self.closed = closed

    def save(self) -> None:
        if self.is_dirty:
            super().save()
            self.saved_last_sequence_number = self.last_sequence_number
            self.is_dirty = False

    def delete(self) -> None:
        DynamoDBStreamsShard._delete(self.id)

    def to_json(self):
        return {
            "id": self.id,
            "linker_id": self.linker_id,
            "stream_arn": self.stream_arn,
            "shard_id": self.shard_id,
            "parent_shard_id": self.parent_shard_id,
            "last_sequence_number": self.last_sequence_number,
            "finished": self.finished,
            "closed": self.closed,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
            "shard_iterator": self.shard_iterator,
            "is_dirty": self.is_dirty,
        }
