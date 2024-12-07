import base64
import json
from typing import Any, Dict, List, Tuple
import uuid
from dataclasses import dataclass

# For type hinting
try:
    import numpy as np
    from langchain.callbacks.manager import CallbackManagerForRetrieverRun
    from langchain.pydantic_v1 import BaseModel
    from langchain.schema.document import Document
    from langchain.schema.embeddings import Embeddings
    from langchain.schema.retriever import BaseRetriever
    from langchain.schema.vectorstore import VectorStoreRetriever
except ModuleNotFoundError:
    pass

from antimatter.errors import MissingDependency
from antimatter.extra_helper import COL_TYPE_KEY
from antimatter.fieldtype.fieldtypes import FieldType
from antimatter.fieldtype.infer import infer_fieldtype
from antimatter.handlers import DataHandler


class EmbeddingClient:
    OPEN_AI = "openai"
    HUGGING_FACE = "huggingface"


@dataclass
class BaseDocument:
    """
    BaseDocument is a wrapper around the langchain Document.
    It is used to store the page content of the document.
    """

    content: Any
    embedding: List[float]


class LangchainHandler(DataHandler):
    """
    The LangchainHandler DataHandler supports an implementation of a langchain
    Retriever. This handler assumes that the underlying data is a list of
    two-dimensional data.
    """

    def from_generic(self, cols: List[str], generic_data: List[List[bytes]], extra: Dict[str, Any]) -> Any:
        """
        from_generic loads the generic data into an implementation of a
        langchain Retriever with langchain Embeddings.

        :param cols: the column names for the underlying data
        :param generic_data: the capsule's generic data format that is loaded into a langchain Retriever
        :param extra: extra data for the DataHandler, containing information for the Embeddings
        :return: the langchain Retriever built with the dataset
        """
        data = []
        for generic_row in generic_data:
            row = {}
            for col, field in zip(cols, generic_row):
                row[col] = self.field_converter_from_generic(FieldType.String)(field)
            data.append(row)
        return LangchainHandler.Retriever(data=data, extra=extra)

    def to_generic(self, data: Any) -> Tuple[List[str], List[List[bytes]], Dict[str, Any]]:
        """
        to_generic converts a langchain Retriever with langchain Embeddings
        into the generic data format.

        :param data: the langchain Retriever
        :return: the data in its generic format
        """
        assert isinstance(data, LangchainHandler.Retriever)

        cols = set()
        rows = []
        extra = {}

        col_ft_cache = {}
        if data.vectors:
            extra[COL_TYPE_KEY] = {}

        # First pass: get column names
        [cols.add(key) for _, docs in data.vectors.items() for key in docs.content]

        # Second pass: flatten dicts into rows
        cols = list(cols)
        for _, docs in data.vectors.items():
            d = docs.content
            row = []
            for cname in cols:
                # TODO: Handle 'missing' values using 'extras' dict
                val = d.get(cname)
                if val is None:
                    val = ""
                else:
                    ft = col_ft_cache.get(cname)
                    if ft is None:
                        ft = infer_fieldtype(val)
                    extra[COL_TYPE_KEY][cname] = ft.value
                    col_ft_cache[cname] = ft
                    val = self.field_converter_to_generic(ft)(val)
                row.append(val)
            rows.append(row)

        return cols, rows, data.extra or {}

    try:

        class Retriever(BaseRetriever):
            """
            Retriever is a wrapper around the langchain Retriever.
            It is used to store and retrieve data from the langchain Retriever.
            """

            vectors: Dict[str, BaseDocument] = {}
            k: int = 10
            embeddings: Embeddings = None
            extra: Dict[str, Any] = None

            def encrypt(self, data):
                return base64.b64encode(str(data).encode("utf-8")).decode("utf-8")

            def decrypt(self, data):
                return base64.b64decode(data).decode("utf-8")

            def __init__(self, data: List[Dict[str, bytes]], extra: Dict[str, Any] = None):
                try:
                    import numpy as np
                    from langchain.callbacks.manager import CallbackManagerForRetrieverRun
                    from langchain.pydantic_v1 import BaseModel
                    from langchain.schema.document import Document
                    from langchain.schema.embeddings import Embeddings
                    from langchain.schema.retriever import BaseRetriever
                except ModuleNotFoundError as me:
                    raise MissingDependency(me)

                super().__init__()
                if extra is None:
                    extra = {}
                self.embeddings = LangchainHandler.Embed(extra=extra)
                self.extra = extra
                for row in data:
                    embedding = self.embeddings.embed_documents([json.dumps(row)])
                    self.vectors[uuid.uuid4().hex] = BaseDocument(content=row, embedding=embedding[0])

            def _get_relevant_documents(
                self, query: str, *, run_manager: CallbackManagerForRetrieverRun
            ) -> List[Document]:
                """Return the first k documents from the list of documents"""
                distances = {
                    id: np.linalg.norm(docs.embedding - self.embeddings.embed_query(query))
                    for id, docs in self.vectors.items()
                }
                return [
                    Document(page_content=json.dumps(self.vectors[id].content))
                    for id, _ in sorted(distances.items(), key=lambda x: x[1])[: self.k]
                ]

            async def _aget_relevant_documents(self, query: str) -> List[Document]:
                return self._get_relevant_documents(query)

        class Embed(BaseModel, Embeddings):
            """
            Embed is a wrapper around the embedding client.
            Currently, it supports the following embedding clients:
            - OpenAI
            - Huggingface flan-t5-base (default)

            The embedding client can be set in the extra of the Retriever.
            To use the OpenAI embedding client, set the extra of the Retriever to:
            extra = {
                "embedding_client": "openai",
                "openai_api_key": "YOUR_API_KEY"
            }
            """

            client: Any

            def __init__(self, extra: Dict[str, Any], **kwargs: Any) -> None:
                super().__init__(**kwargs)
                if extra is None:
                    extra = {}
                # Check if openai is set as the embedding client in the extra
                embedding_client = extra.get("embedding_client", None)
                if embedding_client == EmbeddingClient.OPEN_AI:
                    from langchain.embeddings.openai import OpenAIEmbeddings

                    # Check if the openai api key is set in the extra
                    if extra.get("openai_api_key") is None:
                        raise Exception("OpenAI API key not set in extra")

                    model = OpenAIEmbeddings(openai_api_key=extra.get("openai_api_key"))

                    def embed(text):
                        return model.embed_documents([text])[0]

                else:
                    try:
                        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
                        import torch
                    except ModuleNotFoundError as me:
                        raise MissingDependency(me)

                    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                    tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
                    model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base").to(device)

                    def embed(text):
                        input_ids = tokenizer.encode(text, return_tensors="pt").to(device)
                        outputs = model.encoder(input_ids)
                        return outputs.last_hidden_state.mean(dim=1).detach().cpu().numpy()[0]

                self.client = embed

            def embed_documents(self, texts: List[str]) -> List[List[float]]:
                texts = list(map(lambda x: x.replace("\n", " "), texts))
                return [self.client(text) for text in texts]

            def embed_query(self, text: str) -> List[float]:
                return self.client(text)

    except (ModuleNotFoundError, NameError):
        # If we hit this point, the langchain dependencies have not been imported
        # yet. We only want to fail or warn if the caller attempts to use langchain,
        # so swallow the error for now
        pass
