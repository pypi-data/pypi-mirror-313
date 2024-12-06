from typing import Optional


class MlFoundryException(Exception):
    def __init__(self, message, status_code: Optional[int] = None):
        self.message = str(message)
        self.status_code = status_code
        super().__init__(message)
