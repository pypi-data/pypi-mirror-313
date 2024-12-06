from abc import ABC
from abc import abstractmethod
from typing import Any

from amsdal_utils.query.utils import Q


class QueryableMixin(ABC):
    @abstractmethod
    def to_query(self, *args: Any, **kwargs: Any) -> Q: ...
