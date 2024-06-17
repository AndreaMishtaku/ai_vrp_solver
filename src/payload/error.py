from dataclasses import dataclass

from flask import json

@dataclass
class Error(Exception):
    """Exception raised for 4xx HTTP errors."""

    status_code: int
    message: str

    def __post_init__(self):
        if self.message is None:
            self.message = f"Error: {self.status_code}"
        super().__init__(self.message)

    def __str__(self):
        return f'Message: {self.message}, Status Code: {self.status_code}'

    def to_dict(self):
        return {'status_code': self.status_code, 'message': self.message}
