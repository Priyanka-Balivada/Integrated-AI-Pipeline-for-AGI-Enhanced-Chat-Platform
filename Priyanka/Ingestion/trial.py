# from llama_index import Document
from llama_index.core import VectorStoreIndex
from llama_index.core import SimpleDirectoryReader
from llama_index.embeddings.text_embeddings_inference import TextEmbeddingsInference
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import TokenTextSplitter

# global
from llama_index.core import Settings

# Load documents from directory
reader = SimpleDirectoryReader(input_dir="inputs/", recursive=True, required_exts=[".txt", ".pdf"])
documents = reader.load_data()
print(documents)
# Initialize your local embedding model
local_embed_model = TextEmbeddingsInference(
    model_name="BAAI/bge-large-en-v1.5",
    base_url="http://127.0.0.1:8081",  # Adjust this URL to your inference server
    timeout=60,  # timeout in seconds
    embed_batch_size=10,  # batch size for embedding
)

text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=10)

Settings.text_splitter = text_splitter

# per-index
# index = VectorStoreIndex.from_documents(
#     documents, transformations=[text_splitter], embed_model=local_embed_model
# )
# print(index)


pipeline = IngestionPipeline(transformations=[TokenTextSplitter()])

nodes = pipeline.run(documents=documents)

print(nodes)
# Create a VectorStoreIndex with local embeddings
# vector_index = VectorStoreIndex.from_documents(documents, embed_model=local_embed_model)
# print(vector_index)

# Disable OpenAI LLM entirely by setting `llm=None`
# query_engine = vector_index.as_query_engine(llm=None)

# Now you can query the index without using OpenAI





