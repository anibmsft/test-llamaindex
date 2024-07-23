from abc import ABC
import psycopg2
from sqlalchemy import make_url
from llama_index.vector_stores.postgres import PGVectorStore

class PostGresDatabaseBuilder(ABC):
    def __init__(self, **kwargs):
        super().__init__()
        self.kwargs = kwargs
    
    def establish_and_get_vector_store(self):
        conn = psycopg2.connect(
            dbname=self.kwargs['db_name'],
            host=self.kwargs['host'],
            password=self.kwargs['password'],
            port=self.kwargs['port'],
            user=self.kwargs['user']
            )
        conn.autocommit = True

        with conn.cursor() as c:
            # Check if the database exists
            c.execute(f"SELECT 1 FROM pg_database WHERE datname = '{self.kwargs['db_name']}'")
            exists = c.fetchone()

            if not exists:
                # Create the database if it does not exist
                c.execute(f"CREATE DATABASE {self.kwargs['db_name']}")

        # Close the initial connection
        conn.close()

        # Connect to the newly created or existing database
        conn = psycopg2.connect(
            dbname=self.kwargs['db_name'],
            host=self.kwargs['host'],
            password=self.kwargs['password'],
            port=self.kwargs['port'],
            user=self.kwargs['user']
        )
        conn.autocommit = True

        # Initialize the vector store
        vector_store = PGVectorStore.from_params(
            database=self.kwargs['db_name'],
            host=self.kwargs['host'],
            password=self.kwargs['password'],
            port=self.kwargs['port'],
            user=self.kwargs['user'],
            table_name=self.kwargs['table_name'],
            embed_dim=384,  # openai embedding dimension
        )
        return vector_store
# conn = psycopg2.connect(connection_string)






