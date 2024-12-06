class BaseError(Exception):
    def __init__(self, message: str, status: int, code: str, title: str):
        self.message = message
        self.status = status
        self.code = code
        self.title = title
        super().__init__(self.message)
