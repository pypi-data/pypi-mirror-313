import uuid
from datetime import datetime, timezone


class NDJSONBlockLogTracker:
    def __init__(self, job_url=None):
        self.block_status_log = []
        self.blocks = {}
        self.offset = 0
        self.current_block_id = None
        self.job_url = job_url
        self.next_block()

    def next_block(self):
        self.current_block_id = str(uuid.uuid4())
        block = {"block_id": self.current_block_id, "start_offset": self.offset, "end_offset": self.offset}
        self.blocks[self.current_block_id] = block
        return block

    def get_current_block(self):
        return self.blocks[self.current_block_id]

    def on_data_received(self):
        self.block_status_log.append(
            {"block_id": self.current_block_id, "status": "receiving", "timestamp": datetime.now(timezone.utc)}
        )
        return self.blocks[self.current_block_id]

    def on_decompressing(self):
        self.block_status_log.append(
            {"block_id": self.current_block_id, "status": "decompressing", "timestamp": datetime.now(timezone.utc)}
        )

    def track_offset(self, block, chunk_length):
        block["end_offset"] += chunk_length
        self.blocks[block["block_id"]] = block
        self.offset = block["end_offset"]
        return self.next_block()

    def on_done(self, block_id=None):
        self.block_status_log.append(
            {"block_id": block_id or self.current_block_id, "status": "done", "timestamp": datetime.now(timezone.utc)}
        )

    def on_fetching(self):
        block_id = self.current_block_id
        block = self.blocks[block_id]
        block = {
            **block,
            **{
                "block_id": block_id,
                "url": self.job_url,
            },
        }
        self.blocks[block_id] = block
        self.block_status_log.append(
            {"block_id": block_id, "status": "fetching", "timestamp": datetime.now(timezone.utc)}
        )
        return block

    def on_incomplete_read(self):
        self.block_status_log.append(
            {"block_id": self.current_block_id, "status": "fetching", "timestamp": datetime.now(timezone.utc)}
        )
        return self.blocks[self.current_block_id]

    def on_processing(self, block):
        block_id = block["block_id"]
        self.blocks[block_id] = block
        self.block_status_log.append(
            {"block_id": block_id, "status": "processing", "timestamp": datetime.now(timezone.utc)}
        )
        return block

    def on_queued(self, block_id):
        self.block_status_log.append(
            {"block_id": block_id, "status": "queued", "timestamp": datetime.now(timezone.utc)}
        )

    def on_error(
        self,
        block_id,
        error,
        total_rows=None,
        quarantine_rows=None,
        processing_time=None,
        ch_summaries=None,
        quarantine_ch_summaries=None,
        parser="python",
    ):
        if not block_id:
            block_id = self.get_current_block()["block_id"]
        self.blocks[block_id]["processing_error"] = str(error)
        # Although error we need to track if anything was inserted in CH
        # to track related materializations
        # Track block with CH Summary header as done in 'on_done_inserting_chunk'
        # https://gitlab.com/tinybird/analytics/-/issues/14368
        if total_rows is not None:
            self.blocks[block_id]["process_return"] = [
                {
                    "lines": total_rows - quarantine_rows,
                    "quarantine": quarantine_rows,
                    "empty": 0,
                    "parser": parser,
                    "bytes": self.blocks[block_id].get("end_offset", 0) - self.blocks[block_id].get("start_offset", 0),
                    "db_stats": [summary.to_dict() for summary in ch_summaries],
                    "quarantine_db_stats": [summary.to_dict() for summary in quarantine_ch_summaries],
                }
            ]
            self.blocks[block_id]["processing_time"] = processing_time

    def on_inserting_chunk(self, block_id):
        self.block_status_log.append(
            {"block_id": block_id, "status": "inserting_chunk", "timestamp": datetime.now(timezone.utc)}
        )

    def on_done_inserting_chunk(
        self,
        block_id,
        total_rows,
        quarantine_rows,
        processing_time,
        ch_summaries,
        quarantine_ch_summaries,
        parser="python",
    ):
        block = self.blocks[block_id]
        block["process_return"] = [
            {
                "lines": total_rows - quarantine_rows,
                "quarantine": quarantine_rows,
                "empty": 0,
                "parser": parser,
                "bytes": block.get("end_offset", 0) - block.get("start_offset", 0),
                "db_stats": [summary.to_dict() for summary in ch_summaries],
                "quarantine_db_stats": [summary.to_dict() for summary in quarantine_ch_summaries],
            }
        ]
        block["processing_time"] = processing_time
        self.blocks[block_id] = block
        self.block_status_log.append(
            {"block_id": block_id, "status": "done_inserting_chunk", "timestamp": datetime.now(timezone.utc)}
        )

    @property
    def block_ids(self):
        return list(self.blocks.keys())[:-1]


class DummyBlockLogTracker:
    def __init__(self, job_url=None):
        self.block_ids = []

    def next_block(self):
        pass

    def get_current_block(self):
        pass

    def on_data_received(self):
        pass

    def on_decompressing(self):
        pass

    def track_offset(self, block, chunk_length):
        pass

    def on_done(self, block_id=None):
        pass

    def on_fetching(self):
        pass

    def on_incomplete_read(self):
        pass

    def on_processing(self, block):
        pass

    def on_queued(self, block_id):
        pass

    def on_error(
        self,
        block_id,
        error,
        total_rows=None,
        quarantine_rows=None,
        processing_time=None,
        ch_summaries=None,
        quarantine_ch_summaries=None,
        parser="python",
    ):
        pass

    def on_inserting_chunk(self, block_id):
        pass

    def on_done_inserting_chunk(
        self, block_id, total_rows, quarantine_rows, processing_time, db_stats, quarantine_db_stats, parser="python"
    ):
        pass
