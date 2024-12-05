import os

from pathlib import Path
from typing import List, Optional

from tempestai.core.document import Document
from tempestai.core.document_loaders import BaseLoader


class DocxLoader(BaseLoader):
    """Microsoft Word (Docx) loader.

    Args:
        input_file (str): File path to load.
    """

    def __init__(self, input_file: str = None):
        if not input_file:
            raise ValueError("You must provide a `input_dir` parameter")

        if not os.path.isfile(input_file):
            raise ValueError(f"File `{input_file}` does not exist")

        self.input_file = str(Path(input_file).resolve())

    def load_data(self, extra_info: Optional[dict] = None) -> List[Document]:
        """Loads data from the specified directory."""
        try:
            import docx2txt  # noqa: F401
        except ImportError:
            raise ImportError("docx2txt package not found, please install it with `pip install docx2txt`")

        text = docx2txt.process(self.input_file)
        metadata = {"source": self.input_file}

        return [Document(text=text, metadata=metadata)]
