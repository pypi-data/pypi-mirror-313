from pydantic import BaseModel


class Range(BaseModel, frozen=True):

    start: int
    end: int

    def as_string(self, delimiter: str = "-") -> str:
        return f"{self.start}{delimiter}{self.end}"
