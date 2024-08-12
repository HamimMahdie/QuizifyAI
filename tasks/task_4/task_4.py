from langchain_google_vertexai import VertexAIEmbeddings
from chromadb.utils import embedding_functions

class EmbeddingClient(embedding_functions.EmbeddingFunction):
    def __init__(self, model_name, project, location):
        self.client = VertexAIEmbeddings(
            model_name=model_name,
            project=project,
            location=location
        )

    def __call__(self, input):
        texts = input  # The input parameter is the texts to be embedded
        if isinstance(texts, str):
            return self.client.embed_query(texts)
        return self.client.embed_documents(texts)

    def embed(self, texts):
        # Alias for __call__ to ensure compatibility
        return self.__call__(texts)

if __name__ == "__main__":
    model_name = "textembedding-gecko@003"
    project = "quizzify-428916"
    location = "us-central1"

    embedding_client = EmbeddingClient(model_name, project, location)
    vectors = embedding_client.embed("Hello World!")
    if vectors:
        print(vectors)
        print("Successfully used the embedding client!")
