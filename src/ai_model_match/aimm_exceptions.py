class AIMMHTTPException(Exception):
    def __init__(self, status_code, errors: list[str]):
        self.status_code = status_code
        self.errors = errors
        super().__init__(f"HTTP error occurred: {self.status_code}")

class AIMMHTTPGenericException(Exception):
    def __init__(self, message: str, err: str):
        self.err = err
        self.message = message
        super().__init__(message)