from typing import Optional


class BadRequestException(Exception):
    def __init__(self, status_code: int, message: Optional[str] = None):
        super().__init__()
        self.status_code = status_code
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return self.message
