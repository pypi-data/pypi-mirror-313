from abc import ABC
from typing import Any
from typing_extensions import Self

from spiderpy3.utils.logger import logger


class Object(ABC):
    logger = logger

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

    @classmethod
    def create_instance(cls, *args: Any, **kwargs: Any) -> Self:
        return cls(*args, **kwargs)
