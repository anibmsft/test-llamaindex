from chunkers.node_builder import NodeBuilder
from chunkers.text_chunker import TextChunker
from database.postgres import PostGresDatabaseBuilder
from embeddings.embedding_builder import EmbeddingBuilder
from readers.text_dir_reader import TextDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

import sys
import os

from vs.postgres_vector_store import PostgresVectorStore

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


db_name = "pg_chunks"
host = "localhost"
password = "123"
user = "aniruddhab_s"
table_name= "pg_knowledge"

text_path = 'data/paul_graham'


def build_v_store(embed_model):
    pgres_db = PostGresDatabaseBuilder(db_name, host, password, user, table_name)
    vector_store = pgres_db.establish_and_get_vector_store()

    data_loader = TextDirectoryReader(text_path)
    documents = data_loader.read_directory()

    doc_ids, doc_chunks = TextChunker().generate_chunks(documents)
    nodes = NodeBuilder(documents, doc_ids, doc_chunks).build_nodes()

    embedding_builder = EmbeddingBuilder(embed_model)
    nodes = embedding_builder.build_embedding(nodes)

    pg_vec_store = PostgresVectorStore(vector_store)
    pg_vec_store.add(nodes)


def main():
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en")
    build_v_store(embed_model)
    print("embeddings build complete")

# from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en")

if __name__ == "__main__":
    print("Starting application...")
    main()