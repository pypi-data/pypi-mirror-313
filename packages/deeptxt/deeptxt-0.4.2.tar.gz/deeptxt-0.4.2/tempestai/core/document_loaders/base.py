from typing import List, Optional
from abc import ABC, abstractmethod

from tempestai.core.document import Document


class BaseLoader(ABC):
    """An interface for document loader."""

    @classmethod
    def class_name(cls) -> str:
        return "BaseLoader"

    @abstractmethod
    def load_data(self, extra_info: Optional[dict] = None) -> List[Document]:
        """Loads data."""

    def load(self) -> List[Document]:
        return self.load_data()

    def lazy_load(self) -> List[Document]:
        return self.load_data()
