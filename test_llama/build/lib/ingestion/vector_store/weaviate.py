import logging
import sys
import weaviate
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))




# def get_weaviate_client():
#     client = weaviate.("http://localhost:8080")
#     print(client.is_ready())
#     return client

# def main():
#     return get_weaviate_client()

# if __name__ == "__main__":
#     print("Starting application...")
#     main()
