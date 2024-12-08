from typing import Any
from pydantic import BaseModel


class DefaultHandler(BaseModel):
    callable: Any
    execution_order: int
    receive_parameters: bool
    args: tuple
    kwargs: dict

    def __gt__(self, other) -> bool:
        return self.execution_order > other.execution_order
