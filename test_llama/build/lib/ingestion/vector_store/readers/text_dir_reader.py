from llama_index.core import  SimpleDirectoryReader
from abc import ABC

class TextDirectoryReader(ABC):
    def __init__(self, path):
        super().__init__()
        self.path = path
    def read_directory(self):
        directory =  SimpleDirectoryReader(self.path).load_data()
        return directory