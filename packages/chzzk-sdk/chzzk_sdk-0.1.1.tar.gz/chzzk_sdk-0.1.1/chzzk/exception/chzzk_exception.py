class ChzzkError(Exception):
    def __init__(self, msg: str):
        self.message = msg

    def __str__(self):
        return self.message


class ChzzkHTTPError(ChzzkError):
    def __init__(self, code: int, msg: str):
        super().__init__(msg)
        self.code = code

    def __str__(self):
        return f"status: {self.code} message: {self.message}"
