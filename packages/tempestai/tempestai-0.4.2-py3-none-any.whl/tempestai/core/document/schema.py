import uuid

from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, Optional
from pydantic.v1 import BaseModel, Field, validator

if TYPE_CHECKING:
    from langchain_core.documents import Document as LangChainDocument


class BaseDocument(ABC, BaseModel):
    """Generic abstract interface for retrievable documents."""

    doc_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique ID of the document.")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="A flat dictionary of metadata fields.")

    @validator("metadata", pre=True)
    def _validate_metadata(cls, v) -> Dict:
        if v is None:
            return {}
        return v

    @abstractmethod
    def get_content(self) -> str:
        """Get document content."""

    @abstractmethod
    def get_metadata(self) -> str:
        """Get metadata."""


class Document(BaseDocument):
    """Generic interface for data document."""

    text: str = Field(default="", description="Text content of the document.")

    @classmethod
    def class_name(cls) -> str:
        return "Document"

    def get_content(self) -> str:
        """Get the text content."""
        return self.text

    def get_metadata(self) -> dict:
        """Get metadata."""
        return self.metadata

    @classmethod
    def from_langchain_format(cls, doc: "LangChainDocument") -> "Document":
        """
        Convert a document from LangChain  format.

        Args:
            doc (LangChainDocument): Document in LangChain format.
        """
        return cls(text=doc.page_content, metadata=doc.metadata)


@dataclass
class DocumentWithScore:
    document: BaseDocument
    score: Optional[float] = None

    @classmethod
    def class_name(cls) -> str:
        return "DocumentWithScore"

    def get_score(self) -> float:
        """Get score."""
        if self.score is None:
            return 0.0
        else:
            return self.score

    # #### pass through methods to BaseDocument ####
    @property
    def doc_id(self) -> str:
        return self.document.doc_id

    @property
    def text(self) -> str:
        if isinstance(self.document, Document):
            return self.document.text
        else:
            raise ValueError("Must be a Document to get text")

    def get_content(self) -> str:
        return self.document.get_content()

    def get_metadata(self) -> str:
        return self.document.get_metadata()
