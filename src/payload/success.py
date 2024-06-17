from dataclasses import dataclass

@dataclass
class Success:
    """Class representing a success response."""
    status_code: int = 200
    message: str = "Success"


    def __str__(self):
        return f"Success: {self.message}, Status Code: {self.status_code}"
    

    def to_dict(self):
        return {'status_code': self.status_code, 'message': self.message}