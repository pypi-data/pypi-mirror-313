from starlette.responses import PlainTextResponse


class APIError(Exception):
    def __init__(self, status_code: int, response_text: str):
        self.status_code = status_code
        self.response_text = response_text
        super().__init__(response_text)

    def starlette_response(self):
        return PlainTextResponse(status_code=self.status_code, content=self.response_text)
