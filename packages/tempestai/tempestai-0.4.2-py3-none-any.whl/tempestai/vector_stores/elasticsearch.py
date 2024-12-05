import uuid
import logging

from typing import List
from tempestai.core.document import Document, DocumentWithScore
from tempestai.core.embeddings import BaseEmbedding


class ElasticsearchVectorStore:
    """Provides functionality to interact with Elasticsearch for storing and querying document embeddings.

    Args:
        index_name (str): Name of the Elasticsearch index.
        url (str): Elasticsearch instance url.
        user (str): Elasticsearch username.
        password (str): Elasticsearch password.
        dims_length (int): Length of the embedding dimensions.
        embed_model (BaseEmbedding):
        batch_size (int, optional): Batch size for bulk operations. Defaults to ``200``.
        ssl (bool, optional): Whether to use SSL. Defaults to ``False``.
        distance_strategy (str, optional): Distance strategy for similarity search. Defaults to ``cosine``.
        text_field (str, optional): Name of the field containing text. Defaults to ``text``.
        vector_field (str, optional): Name of the field containing vector embeddings. Defaults to ``embedding``.
    """

    def __init__(self,
                 index_name: str,
                 url: str,
                 user: str,
                 password: str,
                 dims_length: int,
                 embed_model: BaseEmbedding,
                 batch_size: int = 200,
                 ssl: bool = False,
                 distance_strategy: str = "cosine",
                 text_field: str = "text",
                 vector_field: str = "embedding",
                 ) -> None:
        try:
            from elasticsearch import Elasticsearch
            from elasticsearch.helpers import bulk

            self._es_bulk = bulk
        except ImportError:
            raise ImportError("elasticsearch package not found, please install it with `pip install elasticsearch`")

        #  TO-DO: Add connections types e.g: cloud
        self._embed_model = embed_model
        self.index_name = index_name
        self.batch_size = batch_size
        self.dims_length = dims_length
        self.distance_strategy = distance_strategy
        self.vector_field = vector_field
        self.text_field = text_field

        self._client = Elasticsearch(
            hosts=[url],
            basic_auth=(
                user,
                password
            ),
            verify_certs=ssl,
            ssl_show_warn=False
        )

        try:
            self._client.info()
        except Exception as e:
            logging.error(f"Error connecting to Elasticsearch: {e}")
            raise

    def _create_index_if_not_exists(self) -> None:
        """Creates the Elasticsearch index if it doesn't already exist."""
        if self._client.indices.exists(index=self.index_name):
            logging.info(f"Index {self.index_name} already exists. Skipping creation.")

        else:
            if self.dims_length is None:
                raise ValueError(
                    "Cannot create index without specifying dims_length. "
                    "When the index doesn't already exist."
                )

            if self.distance_strategy not in ["cosine", "dot_product", "l2_norm"]:
                raise ValueError(f"Similarity {self.distance_strategy} not supported.")

            index_mappings = {
                "properties": {
                    self.text_field: {"type": "text"},
                    self.vector_field: {
                        "type": "dense_vector",
                        "dims": self.dims_length,
                        "index": True,
                        "similarity": self.distance_strategy,
                    },
                    "metadata": {
                        "properties": {
                            "creation_date": {"type": "keyword"},
                            "filename": {"type": "keyword"},
                            "file_type": {"type": "keyword"},
                            "page": {"type": "keyword"},
                        }
                    }
                }
            }

            print(f"Creating index {self.index_name}")

            self._client.indices.create(index=self.index_name, mappings=index_mappings)

    def add_documents(self, documents: List[Document], create_index_if_not_exists: bool = True) -> None:
        """Add documents to the Elasticsearch index.

        Args:
            documents (List[Document]): List of `Document` objects to add to the index.
            create_index_if_not_exists (bool, optional): Whether to create the index if it doesn't exist. Defaults to ``True``.
        """
        if create_index_if_not_exists:
            self._create_index_if_not_exists()

        vector_store_data = []
        for doc in documents:
            _id = doc.doc_id if doc.doc_id else str(uuid.uuid4())
            _metadata = doc.get_metadata()
            vector_store_data.append({
                "_index": self.index_name,
                "_id": _id,
                self.text_field: doc.get_content(),
                self.vector_field: self._embed_model.get_query_embedding(doc.get_content()),
                "metadata": _metadata,
                "metadata.creation_date": _metadata["creation_date"] if _metadata["creation_date"] else None,
                "metadata.filename": _metadata["filename"] if _metadata["filename"] else None,
                "metadata.file_type": _metadata["file_type"] if _metadata["file_type"] else None,
                "metadata.page": _metadata["page"] if _metadata["page"] else None,
            })

        self._es_bulk(self._client, vector_store_data, chunk_size=self.batch_size, refresh=True)
        print(f"Added {len(vector_store_data)} documents to `{self.index_name}`")

    def query(self, query: str, top_k: int = 4) -> List[DocumentWithScore]:
        """Performs a similarity search for top-k most similar documents.

        Args:
            query (str): Query text.
            top_k (int, optional): Number of top results to return. Defaults to ``4``.
        """
        query_embedding = self._embed_model.get_query_embedding(query)
        #  TO-DO: Add elasticsearch `filter` option
        es_query = {"knn": {
            # "filter": filter,
            "field": self.vector_field,
            "query_vector": query_embedding,
            "k": top_k,
            "num_candidates": top_k * 10,
        }}

        results = self._client.search(index=self.index_name,
                                      **es_query,
                                      size=top_k,
                                      _source={"excludes": [self.vector_field]})

        hits = results["hits"]["hits"]

        return [DocumentWithScore(
            document=Document(
                doc_id=hit["_id"],
                text=hit["_source"]["text"],
                metadata=hit["_source"]["metadata"],
            ),
            score=hit["_score"])
            for hit in hits
        ]

    def delete_documents(self, ids: List[str] = None) -> None:
        """Delete documents from the Elasticsearch index.

        Args:
            ids (List[str]): List of `Document` IDs to delete.
        """
        if not ids:
            raise ValueError("No ids provided to delete.")

        for id in ids:
            self._client.delete(index=self.index_name, id=id)
