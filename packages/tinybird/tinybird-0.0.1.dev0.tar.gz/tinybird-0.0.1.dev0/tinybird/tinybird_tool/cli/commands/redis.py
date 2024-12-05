import json
import time

import click

from tinybird.integrations.dynamodb.shard import DynamoDBStreamsShard
from tinybird.model import RedisModel

from ... import common
from ..cli_base import cli


class DynamoDBStreamsStateExtractor:
    def __init__(self, linker_id) -> None:
        self.linker_id = linker_id

    def get_state(self):
        state = {}
        status = ""
        shards = DynamoDBStreamsShard.get_all_by_owner(self.linker_id, limit=1000)
        if len(shards) >= 1000:
            status = "Warning: More than 1000 shards found. Only the first 1000 will be shown."
        for shard in shards:
            shard_state = shard.to_json()
            del shard_state["shard_iterator"]
            del shard_state["is_dirty"]
            del shard_state["linker_id"]
            del shard_state["stream_arn"]
            state[shard.id] = shard_state

        return state, status


@cli.command()
@click.argument("model", nargs=1)
@click.argument("owner", nargs=1)
@click.option("--forward", is_flag=True, default=False)
@click.option("--diff", is_flag=True, default=False)
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
def get_redis(model, owner, forward, diff, config):
    # Setup redis config
    conf, redis_client = common.setup_redis_client(config)
    RedisModel.config(redis_client)

    state_extractor = None
    if model == "dynamodbstreams":
        state_extractor = DynamoDBStreamsStateExtractor(owner)
    else:
        raise Exception("Model not supported")

    current_state, status = state_extractor.get_state()
    for shard in current_state.values():
        print(json.dumps(shard))
    # Print status at the end to improve readability
    if status:
        print(status)

    while forward:
        new_state, status = state_extractor.get_state()
        changes = False
        for shard_id, new_shard_state in new_state.items():
            current_shard_state = current_state.get(shard_id)
            if new_shard_state != current_shard_state:
                # In case of just wanting to see the diff, remove
                # keys that don't change
                shown_shard_state = new_shard_state.copy()
                if diff:
                    for key, new_value in new_shard_state.items():
                        if key == "id":
                            continue

                        if key in current_shard_state and current_shard_state[key] == new_value:
                            del shown_shard_state[key]

                print(json.dumps(shown_shard_state))

                changes = True

        # Print status at the end to improve readability
        if status and changes:
            print(status)

        current_state = new_state
        time.sleep(2)
