import os

from pathlib import Path
from typing import List, Optional, Type, Callable

from tempestai.core.document import Document
from tempestai.core.document_loaders import BaseLoader

from langchain_community.document_loaders import DirectoryLoader as LangChainDirectoryLoader


def _loading_default_file_loaders():
    from tempestai.document_loaders import DocxLoader
    from tempestai.document_loaders import HTMLLoader
    from tempestai.document_loaders import PDFLoader

    default_file_loader_cls: dict[str, Type[BaseLoader]] = {
        ".docx": DocxLoader,
        ".html": HTMLLoader,
        ".pdf": PDFLoader,
    }

    return default_file_loader_cls


class DirectoryLoader(BaseLoader):
    """Simple directory loader.

    Args:
        input_dir (str): Directory path from which to load the documents.
        recursive (str, optional): Whether to recursively search for files. Defaults to ``False``.
    """

    input_dir: Callable = _loading_default_file_loaders

    def __init__(self, input_dir: str = None,
                 file_loader: Optional[dict[str, Type[BaseLoader]]] = None,
                 recursive: Optional[bool] = False):

        if not input_dir:
            raise ValueError("You must provide a `input_dir` parameter")

        if not os.path.isdir(input_dir):
            raise ValueError(f"Directory `{input_dir}` does not exist")

        if file_loader is not None:
            self.file_loader = file_loader
        else:
            self.file_loader = {}

        self.input_dir = Path(input_dir)
        self.recursive = recursive

    def load_data(self, extra_info: Optional[dict] = None) -> List[Document]:
        """Loads data from the specified directory."""
        documents = []
        default_file_loader_cls = DirectoryLoader.default_file_loader_cls()

        file_loader = self.file_loader | default_file_loader_cls
        file_loader_suffix = list(file_loader.keys())

        for file_suffix in file_loader_suffix:
            print(file_suffix)
            #TO-DO add `file_loader_kwargs`
            docs = LangChainDirectoryLoader(self.input_dir, glob=f"**/*{file_suffix}",
                                   loader_cls=file_loader[file_suffix]).load()

            documents.extend(docs)
            # TO-DO extend `doc.metadata` with `extra_info`
        return documents
