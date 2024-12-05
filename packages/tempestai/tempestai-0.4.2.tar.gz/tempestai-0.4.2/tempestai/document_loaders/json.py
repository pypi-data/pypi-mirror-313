import os

from pathlib import Path
from typing import List, Optional

from tempestai.core.document import Document
from tempestai.core.document_loaders import BaseLoader

from langchain_community.document_loaders import JSONLoader as LangChainJSONLoader


class JSONLoader(BaseLoader):
    """JSON loader.

    Args:
        input_file (str): File path to load.
        jq_schema (str, optional): jq schema to use to extract the data from the JSON.
        text_content (bool, optional): Flag to indicate whether the content is in string format. Default is ``False``
    """

    def __init__(self, input_file: str = None,
                 jq_schema: Optional[str] = None,
                 text_content: Optional[bool] = False):
        try:
            import jq  # noqa: F401
        except ImportError:
            raise ImportError("jq package not found, please install it with `pip install jq`")

        if not input_file:
            raise ValueError("You must provide a `input_dir` parameter")

        if not os.path.isfile(input_file):
            raise ValueError(f"File `{input_file}` does not exist")

        self.input_file = str(Path(input_file).resolve())
        self.jq_schema = jq_schema
        self.text_content = text_content

    def load_data(self, extra_info: Optional[dict] = None) -> List[Document]:
        """Loads data from the specified directory."""
        lc_documents = LangChainJSONLoader(file_path=self.input_file,
                                  jq_schema=self.jq_schema,
                                  text_content=self.text_content).load()

        return [Document().from_langchain_format(doc=doc) for doc in lc_documents]
