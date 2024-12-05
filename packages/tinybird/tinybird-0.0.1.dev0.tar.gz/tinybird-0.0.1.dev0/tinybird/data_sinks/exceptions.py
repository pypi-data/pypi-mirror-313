class DataSinkException(Exception):
    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args)
        self.status = kwargs.get("status", 500)
