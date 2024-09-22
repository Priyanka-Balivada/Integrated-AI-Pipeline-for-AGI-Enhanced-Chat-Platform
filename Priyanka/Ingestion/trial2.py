# demo pipeline with local model
# from llama_index.core import VectorStoreIndexdem
from llama_index.core import SimpleDirectoryReader
from llama_index.embeddings.text_embeddings_inference import TextEmbeddingsInference
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import TokenTextSplitter

from llama_index.vector_stores.milvus import MilvusVectorStore  # Import MilvusVectorStore

# import milvus  # Ensure milvus is installed

# Initialize Milvus client
# milvus_client = milvus.Milvus(uri="http://localhost:19530/")  # Adjust the URI as needed

# # Create a Milvus vector store
# vector_store = MilvusVectorStore(client=milvus_client, collection_name="test_store")

# Initialize your local embedding model
local_embed_model = TextEmbeddingsInference(
    model_name="BAAI/bge-large-en-v1.5",
    base_url="http://127.0.0.1:8081",  # Adjust this URL to your inference server
    timeout=60,  # timeout in seconds
    embed_batch_size=10,  # batch size for embedding
)

# Load documents from directory
reader = SimpleDirectoryReader(input_dir="inputs/", recursive=True, required_exts=[".txt", ".pdf"])
documents = reader.load_data()

# Create the pipeline with transformations
pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=512, chunk_overlap=10),  # Adjust chunk size and overlap as needed
        TokenTextSplitter()  # Add other transformations as required
    ],
    # vector_store=vector_store,
)

# Run the pipeline on the loaded documents
nodes = pipeline.run(documents=documents)

# Create a VectorStoreIndex using the nodes and the local embedding model
# vector_index = VectorStoreIndex(nodes=nodes, embed_model=local_embed_model)

# Query the index if necessary
# query_engine = vector_index.as_query_engine()

# Optionally: print some output
print("Pipeline run successful, VectorStoreIndex created.")
