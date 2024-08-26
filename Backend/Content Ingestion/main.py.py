from typing import Optional, List
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
from llama_index.readers.web import SimpleWebPageReader, BeautifulSoupWebReader, RssReader, WholeSiteReader
from llama_index.core import SummaryIndex
from llama_index.readers.file import (
    DocxReader,
    PDFReader,
    FlatReader,
    HTMLTagReader,
    ImageReader,
    IPYNBReader,
    PptxReader,
    PandasCSVReader,
    PyMuPDFReader,
    XMLReader,
    CSVReader,
)
from llama_index.embeddings.text_embeddings_inference import TextEmbeddingsInference
from pymilvus import connections, utility, FieldSchema, CollectionSchema, DataType, Collection
import os

app = FastAPI()

# Initialize embedding model
embed_model = TextEmbeddingsInference(
    model_name="BAAI/bge-large-en-v1.5",
    base_url="http://127.0.0.1:8081",
    timeout=60,  # timeout in seconds
    embed_batch_size=10,  # batch size for embedding
)

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <body>
            <h1>Data Loaders</h1>
            <form action="/read" method="post">
                <label for="format">Format:</label>
                <select id="format" name="format">
                    <option value="web">Web Reader</option>
                    <option value="html_tags">HTML Tags Reader</option>
                    <option value="beautiful_soup">BeautifulSoup Reader</option>
                    <option value="rss">RSS Reader</option>
                    <option value="pdf">PDF Reader</option>
                    <option value="docx">DOCX Reader</option>
                    <option value="txt">TXT Reader</option>
                    <option value="image">Image Reader</option>
                    <option value="ipynb">IPYNB Reader</option>
                    <option value="pptx">PPTX Reader</option>
                    <option value="csv">CSV Reader</option>
                    <option value="xml">XML Reader</option>
                    <option value="whole_site">Whole Site Reader</option>
                </select><br><br>
                
                <div id="web-fields" style="display:none;">
                    <label for="url_web">URL:</label>
                    <input type="text" id="url_web" name="url_web"><br><br>
                </div>
                
                <div id="html-tags-fields" style="display:none;">
                    <label for="url_html">URL:</label>
                    <input type="text" id="url_html" name="url_html"><br><br>
                    <label for="tag">Tag:</label>
                    <input type="text" id="tag" name="tag" value="section"><br><br>
                    <label for="ignore_no_id">Ignore No ID:</label>
                    <input type="checkbox" id="ignore_no_id" name="ignore_no_id" checked><br><br>
                </div>
                
                <div id="beautiful-soup-fields" style="display:none;">
                    <label for="url_soup">URL:</label>
                    <input type="text" id="url_soup" name="url_soup"><br><br>
                </div>
                
                <div id="whole-site-fields" style="display:none;">
                    <label for="url_whole">Base URL:</label>
                    <input type="text" id="url_whole" name="url_whole"><br><br>
                    <label for="prefix">Prefix:</label>
                    <input type="text" id="prefix" name="prefix"><br><br>
                    <label for="max_depth">Max Depth:</label>
                    <input type="number" id="max_depth" name="max_depth" value="10"><br><br>
                </div>
                
                <div id="file-path-fields" style="display:none;">
                    <label for="url_file">File Path:</label>
                    <input type="text" id="url_file" name="url_file"><br><br>
                </div>
                
                <input type="submit" value="Submit">
            </form>
            <script>
                document.getElementById('format').addEventListener('change', function() {
                    document.getElementById('web-fields').style.display = this.value === 'web' ? 'block' : 'none';
                    document.getElementById('html-tags-fields').style.display = this.value === 'html_tags' ? 'block' : 'none';
                    document.getElementById('beautiful-soup-fields').style.display = this.value === 'beautiful_soup' ? 'block' : 'none';
                    document.getElementById('whole-site-fields').style.display = this.value === 'whole_site' ? 'block' : 'none';
                    document.getElementById('file-path-fields').style.display = ['pdf', 'docx', 'txt', 'image', 'ipynb', 'pptx', 'csv', 'xml'].includes(this.value) ? 'block' : 'none';
                });
            </script>
        </body>
    </html>
    """

@app.post("/read")
async def read_data(
    format: str = Form(...),
    url_web: Optional[str] = Form(None),
    url_html: Optional[str] = Form(None),
    url_soup: Optional[str] = Form(None),
    url_whole: Optional[str] = Form(None),
    url_file: Optional[str] = Form(None),
    tag: Optional[str] = Form("section"),
    ignore_no_id: Optional[bool] = Form(True),
    prefix: Optional[str] = Form(None),
    max_depth: Optional[int] = Form(10)
):
    # Load the documents based on the format
    documents = []
    
    if format == "web":
        if url_web is None:
            raise HTTPException(status_code=400, detail="URL must be provided for web reader")
        documents = SimpleWebPageReader(html_to_text=True).load_data([url_web])
    
    elif format == "html_tags":
        if url_html is None:
            raise HTTPException(status_code=400, detail="URL must be provided for HTML tag reader")
        if not os.path.exists(url_html):
            raise HTTPException(status_code=400, detail="File not found")
        with open(url_html, "r", encoding="utf-8") as f:
            content = f.read()
        reader = HTMLTagReader(tag=tag, ignore_no_id=ignore_no_id)
        documents = reader.load_data(content)
    
    elif format == "beautiful_soup":
        if url_soup is None:
            raise HTTPException(status_code=400, detail="URL must be provided for BeautifulSoup reader")
        loader = BeautifulSoupWebReader()
        documents = loader.load_data(urls=[url_soup])
    
    elif format == "rss":
        reader = RssReader()
        documents = reader.load_data(
            [
                "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
                "https://roelofjanelsinga.com/atom.xml",
            ]
        )
    
    elif format == "whole_site":
        if url_whole is None or prefix is None:
            raise HTTPException(status_code=400, detail="Base URL and prefix must be provided for Whole Site Reader")
        scraper = WholeSiteReader(prefix=prefix, max_depth=max_depth)
        documents = scraper.load_data(base_url=url_whole)
    
    elif format in ["pdf", "docx", "txt", "image", "ipynb", "pptx", "csv", "xml"]:
        if url_file is None:
            raise HTTPException(status_code=400, detail="URL must be provided for the selected format")
        if not os.path.exists(url_file):
            raise HTTPException(status_code=400, detail="File not found")
        
        parser_map = {
            "pdf": PyMuPDFReader(),
            "docx": DocxReader(),
            "txt": FlatReader(),
            "image": ImageReader(),
            "ipynb": IPYNBReader(),
            "pptx": PptxReader(),
            "csv": CSVReader(),
            "xml": XMLReader()
        }
        
        parser = parser_map.get(format)
        documents = parser.load_data(url_file)
    
    else:
        raise HTTPException(status_code=400, detail="Unsupported format. Use one of the available formats.")
    
    # Debug: Print the documents to verify their structure
    print(f"Documents: {documents[0].text}")

    # Extract text from the documents for embedding
    # Convert list of document texts into a single string with newline separator
    document_texts = '\n'.join(doc.text for doc in documents)
    
    # Debug: Print the document texts to ensure they are correctly extracted
    print(f"Document Texts: {document_texts}")

    # Generate embeddings for the documents
    try:
        embeddings = embed_model.get_text_embedding(document_texts)
    except Exception as e:
        # Debug: Print the error if the embedding fails
        print(f"Error generating embeddings: {e}")
        raise HTTPException(status_code=500, detail="Error generating embeddings")
    
    # # Chunk documents using SummaryIndex
    # index = SummaryIndex(docs=documents)
    # chunks = index.as_chunks()
    
    # # Debug: Print the chunks to verify their structure
    # print(f"Chunks: {chunks}")
    milvus_store(embeddings)

    return {"embeddings": embeddings}


def connect_to_milvus():
    try:
        connections.connect("default", host="localhost", port="19530")
        print("Connected to Milvus.")
    except Exception as e:
        print(f"Failed to connect to Milvus: {e}")
        raise


def create_collection(name, fields, description, consistency_level="Eventually"):
    schema = CollectionSchema(fields, description)
    collection = Collection(name, schema, consistency_level=consistency_level)
    return collection

def insert_data(collection, entities):
    insert_result = collection.insert(entities)
    collection.flush()
    print(
        f"Inserted data into '{collection.name}'. Number of entities: {collection.num_entities}")
    return insert_result

def create_index(collection, field_name, index_type, metric_type, params):
    index = {"index_type": index_type,
             "metric_type": metric_type, "params": params}
    collection.create_index(field_name, index)
    print(f"Index '{index_type}' created for field '{field_name}'.")

def milvus_store(embeddings):
    try:
        print(embeddings)
        dim = 1024  # Adjust the dimension as per your model's output

        connect_to_milvus()

        # Define the schema for the Milvus collection
        fields = [
            FieldSchema(name="pk", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=dim)
            # FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=500)
        ]
        collection_name = "trial_milvus"

        # Create or get the collection
        if utility.has_collection(collection_name):
            collection = Collection(collection_name)
        else:
            collection = create_collection(collection_name, fields, "Collection for demo purposes")

        # Ensure embeddings is a list of vectors
        if not isinstance(embeddings[0], list):
            embeddings = [embeddings]

        # if not isinstance(text[0], list):
        #     text = [text]

        # Convert embeddings to a format suitable for Milvus
        entities = [
            embeddings  # Embedding vectors
            # text
        ]

        # Insert data into the collection
        insert_result = insert_data(collection, entities)

        print(f"Inserted data into '{collection.name}'. Number of entities: {insert_result.insert_count}")

        create_index(collection, "embeddings", "IVF_FLAT", "L2", {"nlist": 128})

        return insert_result

    except Exception as e:
        print(f"Milvus Store Error: {e}")
        raise HTTPException(status_code=500, detail=f"Milvus Store Error: {e}")
