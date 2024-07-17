from abc import ABC


class PostgresVectorStore(ABC):
    def __init__(self, vector_store):
        super().__init__()
        self.vector_store = vector_store
    def add(self, nodes):
        self.vector_store.add(nodes)