import streaming_form_data
from streaming_form_data.targets import BaseTarget


class CustomMultipartTarget(streaming_form_data.targets.BaseTarget):
    def __init__(self, write_callback):
        self.write_callback = write_callback
        self.written = False
        BaseTarget.__init__(self)

    def on_data_received(self, chunk):
        self.written = True
        self.write_callback(chunk)
