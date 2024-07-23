

import sys
import os

from retriever.retriever import VectorDBRetriever
from vector_store.vs.postgres_vector_store import PostgresVectorStore
from vector_store.chunkers.node_builder import NodeBuilder
from vector_store.chunkers.text_chunker import TextChunker
from vector_store.database.postgres import PostGresDatabaseBuilder
from vector_store.embeddings.embedding_builder import EmbeddingBuilder
from vector_store.readers.text_dir_reader import TextDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.vector_stores import VectorStoreQuery

from llama_index.core.schema import NodeWithScore
from llama_index.core.query_engine import RetrieverQueryEngine

from llama_index.llms.llama_cpp import LlamaCPP


db_name = "pg_chunks"
host = "localhost"
password = "123"
user = "aniruddhab_s"
table_name= "pg_knowledge"
port =  '5432'
text_path = 'data/paul_graham'


model_url = "https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/resolve/main/llama-2-13b-chat.Q4_0.gguf"


def build_v_store(embed_model):
    pgres_db = PostGresDatabaseBuilder(db_name = db_name, host = host, password = password, user = user, 
                                       table_name = table_name, port =port)
    vector_store = pgres_db.establish_and_get_vector_store()

    data_loader = TextDirectoryReader(text_path)
    documents = data_loader.read_directory()


    tx_chunker = TextChunker()
    doc_ids, doc_chunks = tx_chunker.generate_chunks(documents)
    nodes = NodeBuilder(documents, doc_ids, doc_chunks).build_nodes()

    embedding_builder = EmbeddingBuilder(embed_model)
    nodes = embedding_builder.build_embedding(nodes)

    pg_vec_store = PostgresVectorStore(vector_store)
    pg_vec_store.add(nodes)
    return pg_vec_store


def main():
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en")
    pg_vec_store = build_v_store(embed_model)
    print("embeddings build complete")
    print(pg_vec_store)

    print("set up LLM")
    llm = LlamaCPP(
    # You can pass in the URL to a GGML model to download it automatically
        model_url=model_url,
        # optionally, you can set the path to a pre-downloaded model instead of model_url
        model_path=None,
        temperature=0.1,
        max_new_tokens=256,
        # llama2 has a context window of 4096 tokens, but we set it lower to allow for some wiggle room
        context_window=1000,
        # kwargs to pass to __call__()
        generate_kwargs={},
        # kwargs to pass to __init__()
        # set to at least 1 to use GPU
        model_kwargs={"n_gpu_layers": 0},
        verbose=True
        )
    
    print("LLM build complete")
    while True:
        user_input = input("Enter your input: ")
        # Process the user input here
        print("User input: ", user_input)

        query_embedding = embed_model.get_query_embedding(user_input)

        query_mode = "default"
        # query_mode = "sparse"
        # query_mode = "hybrid"

        vector_store_query = VectorStoreQuery(
            query_embedding=query_embedding, similarity_top_k=2, mode=query_mode
            )
        
        query_result = pg_vec_store.query(vector_store_query)
        print(query_result.nodes[0].get_content())

        nodes_with_scores = []
        for index, node in enumerate(query_result.nodes):
            score = None
            if query_result.similarities is not None:
                score = query_result.similarities[index]
            nodes_with_scores.append(NodeWithScore(node=node, score=score))

        retriever = VectorDBRetriever(
        pg_vec_store, embed_model, query_mode="default", similarity_top_k=2
        )

        query_engine = RetrieverQueryEngine.from_args(retriever, llm=llm)

        response = query_engine.query(user_input)

        print("Response is : " + str(response))
        print("Response source nodes: " + response.source_nodes[0].get_content())

# from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en")

if __name__ == "__main__":
    print("Starting application...")
    main()