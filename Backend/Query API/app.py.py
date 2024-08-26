from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymilvus import connections, Collection
from llama_index.embeddings.text_embeddings_inference import TextEmbeddingsInference
from fastapi.responses import HTMLResponse

app = FastAPI()

# Initialize the embedding model
embed_model = TextEmbeddingsInference(
    model_name="BAAI/bge-large-en-v1.5",
    base_url="http://127.0.0.1:8081",
    timeout=60,
    embed_batch_size=10,
)

dim = 768  # Dimension as per your model's output

# Connect to Milvus
def connect_to_milvus():
    try:
        connections.connect("default", host="localhost", port="19530")
        print("Connected to Milvus.")
    except Exception as e:
        print(f"Failed to connect to Milvus: {e}")
        raise

connect_to_milvus()

# Pydantic model for the query input
class QueryRequest(BaseModel):
    query: str

# Search and query Milvus collection
def search_and_query(collection_name, query_text):
    collection = Collection(collection_name)
    query_vector = embed_model.get_text_embedding(query_text)

    collection.load()

    search_params = {
        "metric_type": "L2",
        "params": {"nprobe": 10},
    }

    result = collection.search(
        [query_vector], "embeddings", search_params, limit=1, output_fields=["pk","embeddings"]
    )

    search_results = []
    for hits in result:
        for hit in hits:
            search_results.append({
                "score": hit.distance,
                "embedding": hit.entity.get("embeddings"),
            })
    return search_results

# HTML Frontend
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Milvus Query Interface</title>
</head>
<body>
    <h1>Milvus Query Interface</h1>
    <form id="query-form">
        <label for="query">Enter your query:</label>
        <input type="text" id="query" name="query">
        <button type="submit">Search</button>
    </form>

    <h2>Results:</h2>
    <pre id="results"></pre>

    <script>
        document.getElementById("query-form").addEventListener("submit", async function(event) {
            event.preventDefault();
            const query = document.getElementById("query").value;
            const response = await fetch("/query/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ query: query }),
            });
            const data = await response.json();
            document.getElementById("results").textContent = JSON.stringify(data.results, null, 2);
        });
    </script>
</body>
</html>
"""

# Root endpoint serving HTML
@app.get("/", response_class=HTMLResponse)
async def root():
    return HTMLResponse(content=html_content)

# Query endpoint
@app.post("/query/")
def query_api(request: QueryRequest):
    try:
        results = search_and_query("trial_milvus", request.query)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the app with uvicorn on port 8005
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
