from llama_index.core.schema import TextNode
from abc import ABC


class NodeBuilder(ABC):
    def __init__(self, documents, doc_indexes, text_chunks):
        super().__init__()
        self.text_chunks = text_chunks
        self.documents = documents
        self.doc_idxs = doc_indexes

    def build_nodes(self):
        nodes = []
        for idx, text_chunk in enumerate(self.text_chunks):
            node = TextNode(
                text=text_chunk,
            )
            src_doc = self.documents[self.doc_idxs[idx]]
            node.metadata = src_doc.metadata
            nodes.append(node)
        return nodes