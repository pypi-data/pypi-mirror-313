from typing import List

from tempestai.core.document import Document

from tempestai.core.text_splitters.utils import (
    split_by_regex,
    split_by_sep,
    split_by_sentence_tokenizer,
    split_by_char,
    split_by_fns,
    merge_splits,
    tokenizer
)


class SentenceSplitter:
    """Designed to split input text into smaller chunks,
    particularly useful for processing large documents or texts, tries to keep sentences and paragraphs together.

    Args:
        chunk_size (int, optional): Size of each chunk. Default is ``512``.
        chunk_overlap (int, optional): Amount of overlap between chunks. Default is ``256``.
        separator (str, optional): Separators used for splitting into words. Default is ``" "``

    **Example**

    .. code-block:: python

        from tempestai.text_splitters import SentenceSplitter

        splitter = SentenceSplitter()
    """

    def __init__(self,
                 chunk_size: int = 512,
                 chunk_overlap: int = 256,
                 separator=" "
                 ) -> None:

        if chunk_overlap > chunk_size:
            raise ValueError(
                f"Got a larger `chunk_overlap` ({chunk_overlap}) than `chunk_size` "
                f"({chunk_size}). `chunk_overlap` should be smaller."
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self._split_fns = [
            split_by_sep("\n\n\n"),
            split_by_sentence_tokenizer()
        ]
        self._sub_split_fns = [
            split_by_regex("[^,.;？！]+[,.;？！]?"),
            split_by_sep(separator),
            split_by_char()
        ]

    def from_text(self, text: str) -> List[str]:
        """Split text into chunks.
        
        Args:
            text (str): Input text to split.

        **Example**

        .. code-block:: python

            chunks = splitter.from_text("tempestai is a data framework to build context-aware AI applications")
        """
        splits = self._split(text)

        return merge_splits(splits, self.chunk_size, self.chunk_overlap)

    def from_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks.

        Args:
            documents (List[Document]): List of `Document` objects to split.
        """
        chunks = []

        for document in documents:
            texts = self.from_text(document.get_content())

            for text in texts:
                chunks.append(Document(text=text, metadata=document.get_metadata()))

        return chunks

    def _split(self, text: str) -> List[dict]:

        text_len = len(tokenizer(text))
        if text_len <= self.chunk_size:
            return [{"text": text, "is_sentence": True, "token_size": text_len}]

        text_splits = []
        text_splits_by_fns, is_sentence = split_by_fns(text, self._split_fns, self._sub_split_fns)

        for text_split_by_fns in text_splits_by_fns:
            split_len = len(tokenizer(text_split_by_fns))
            if split_len <= self.chunk_size:
                text_splits.append({"text": text_split_by_fns, "is_sentence": is_sentence, "token_size": split_len})
            else:
                recursive_text_splits = self._split(text_split_by_fns)
                text_splits.extend(recursive_text_splits)

        return text_splits
