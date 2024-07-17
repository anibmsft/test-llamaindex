from llama_index.core.node_parser import SentenceSplitter
from abc import ABC

class TextChunker(ABC):
    def __init__(self, chunk_size = 1024):
        super().__init()
        self.chunk_size = chunk_size
        self.text_parser = SentenceSplitter(
            chunk_size=chunk_size
            )
    def generate_chunks(self, documents):
        text_chunks = []
        # maintain relationship with source doc index, to help inject doc metadata in (3)
        doc_idxs = []
        for doc_idx, doc in enumerate(documents):
            cur_text_chunks = self.text_parser.split_text(doc.text)
            text_chunks.extend(cur_text_chunks)
            doc_idxs.extend([doc_idx] * len(cur_text_chunks))

        return doc_idxs, text_chunks
    





