# half ingestion pipeline with vector store and 3 models
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
from llama_index.core import SimpleDirectoryReader
from llama_index.embeddings.text_embeddings_inference import TextEmbeddingsInference
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline

# Connect to Milvus
connections.connect("default", host='localhost', port='19530')

# Define schema for the collection
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1024)  # Adjust dimension based on your embedding model
]

schema = CollectionSchema(fields, description="Test collection for storing embeddings",enable_dynamic_field=True)
collection_name = "test_store_new"

# Create a collection if it doesn't exist
if not utility.has_collection(collection_name):
    collection = Collection(name=collection_name, schema=schema,consistency_level="Eventually")
    print(f"Collection '{collection_name}' created.")
else:
    collection = Collection(name=collection_name)
    print(f"Collection '{collection_name}' already exists.")

# Initialize your local embedding model
local_embed_model = TextEmbeddingsInference(
    # model_name="WhereIsAI/UAE-Large-V1",
    model_name="intfloat/multilingual-e5-large-instruct",
    # model_name="BAAI/bge-large-en-v1.5",
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
        SentenceSplitter(chunk_size=512, chunk_overlap=10)  # Adjust chunk size and overlap as needed
    ]
)

# Run the pipeline on the loaded documents
nodes = pipeline.run(documents=documents)

# Prepare vectors for insertion into Milvus
embeddings = [local_embed_model.get_text_embedding(node.text) for node in nodes]  # Replace with your actual embedding method
# ids = [node.id_ for node in nodes]  # Assuming your nodes have an id attribute

# Insert vectors into Milvus
collection.insert([embeddings])

# Optionally: print some output
print("Documents inserted into Milvus successfully.")
