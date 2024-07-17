from abc import ABC
class EmbeddingBuilder(ABC):
    def __init__(self, embed_model):
        super().__init__()
        self.embed_model = embed_model
    
    def build_embedding(self, nodes):
        for node in nodes:
            node_embedding = self.embed_model.get_text_embedding(
                node.get_content(metadata_mode="all")
            )
            node.embedding = node_embedding
        return nodes
