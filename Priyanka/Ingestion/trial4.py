from pymilvus import connections # type: ignore
from llama_index.core import SimpleDirectoryReader
from llama_index.embeddings.text_embeddings_inference import TextEmbeddingsInference
from llama_index.core.node_parser import SentenceSplitter, TokenTextSplitter # type: ignore
from llama_index.core.ingestion import IngestionPipeline # type: ignore
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.milvus import MilvusVectorStore # type: ignore

# Connect to Milvus
# connections.connect("default", host='localhost', port='19530')

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

# Set up the Milvus vector store
vector_store = MilvusVectorStore(
    uri="http://localhost:19530",  # Adjust as needed
    dim=1024,  # Adjust dimension based on your embedding model
    overwrite=True
)

# wroks Create a StorageContext with the Milvus vector store
# storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Create the pipeline with transformations
pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=512, chunk_overlap=10),  # Adjust chunk size and overlap as needed
        TokenTextSplitter()  # Add other transformations as required
    ],
    vector_store=vector_store,
)

# Run the pipeline on the loaded documents to generate nodes
nodes = pipeline.run(documents=documents)

# Create a VectorStoreIndex using the nodes and the local embedding model
index = VectorStoreIndex.from_documents(
    documents, 
    # storage_context=storage_context, #works
    embed_model=local_embed_model,
)

# Optionally: Query the index if necessary
# query_engine = index.as_query_engine()
# results = query_engine.query("Sample query")

# Optionally: print some output
print("Pipeline run successful, VectorStoreIndex created and documents stored in Milvus.")
