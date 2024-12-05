import gzip

from .model import RedisModel


class Snapshot(RedisModel):
    """like a Gist but for data
    >>> from .pipe import Pipe
    >>> from tinybird_shared.redis_client.redis_client import  TBRedisClientSync, TBRedisConfig
    >>> client = TBRedisClientSync(TBRedisConfig())
    >>> pipe = Pipe('test', [{'name': 'test_0', 'sql': 'select * from test_ds'}])
    >>> t = Snapshot(id='idsnap', token='token', parent_pipe_id=pipe.id, pipe_owner_id='owner_id', pipe=pipe.clone_with_new_ids())
    >>> t.save()
    >>> t2 = Snapshot.get_by_id(t.id)
    >>> t2.pipe.pipeline.nodes[0].sql
    'select * from test_ds'
    >>> [x[0] for x in Snapshot.get_items_for('parent_pipe_id', pipe.id)]
    ['idsnap']
    """

    __namespace__ = "snapshot"
    __props__ = ["id", "token", "parent_pipe_id", "pipe_owner_id", "pipe", "description", "name"]
    __sets__ = {"parent_pipe_id"}
    __pre_deserialize__ = gzip.decompress
    __post_serialize__ = gzip.compress

    def __init__(self, id, token, parent_pipe_id, pipe_owner_id, pipe, description=None, name=None, **kwargs):
        kwargs.update(
            {
                "id": id,
                "token": token,
                "parent_pipe_id": parent_pipe_id,
                "pipe_owner_id": pipe_owner_id,
                "pipe": pipe,
                "description": description,
                "name": name,
            }
        )
        super().__init__(**kwargs)

    def to_json(self):
        return {"id": self.id, "description": self.description, "name": self.name}  # type: ignore[attr-defined]


def migration_add_name(m):
    m["name"] = f"Snapshot #{m['id'][:5]}"
    return m


Snapshot.__migrations__ = {1: migration_add_name}
