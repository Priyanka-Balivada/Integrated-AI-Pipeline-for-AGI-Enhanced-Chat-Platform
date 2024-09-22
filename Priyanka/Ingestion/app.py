from fastapi import FastAPI, HTTPException
from llama_index.readers.google import GoogleDocsReader

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Google Docs Reader API"}

@app.get("/load_documents/{document_id}")
def load_documents(document_id: str):
    loader = GoogleDocsReader()
    try:
        documents = loader.load_data(document_ids=[document_id])
        return {"documents": documents}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/load_documents/{document_id}")
def load_documents(document_id: str):
    from llama_index.core import SimpleDirectoryReader

    documents = SimpleDirectoryReader("./inputs").load_data()
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)




# uvicorn app:app --reload --host 0.0.0.0 --port 8005