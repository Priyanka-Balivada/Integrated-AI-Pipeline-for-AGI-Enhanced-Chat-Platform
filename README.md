**22nd September 2024**
- Task Background and Initiation:
  Begin a task in the background by sending an HTTP request (HTTP 201 response implies successful task creation) and receive a Task ID in return.
- Retrieve Task Status:
  With the provided Task ID, query the API to get the current status of the task using FastAPI.
- Querying API for Results:
  Send a query request to the API, which retrieves node-based results along with associated metadata.
- Caching and Document Store:
  Implement caching mechanisms and utilize a document store to manage the data effectively.
- https://jalammar.github.io/illustrated-transformer/
- https://arxiv.org/abs/1706.03762
- Model Quantization
- Text Generation Inference
- https://huggingface.co/microsoft/phi-2
- https://eval.ai/web/challenges/challenge-page/1897/leaderboard/4475
- Sparse Vector Store and Retrieval (BM25): BM25 is a traditional sparse retrieval method based on term frequency and relevance. The task involves using BM25 to retrieve documents based on sparse representations of text.
- Dense Vector Retrieval (SPLADE): SPLADE is a transformer-based model that generates sparse vectors but uses deep learning techniques to enhance retrieval performance. The task is to generate sparse vectors using SPLADE, store them in a vector store (like Milvus or FAISS), and use them for dense retrieval.
- Combining BM25 and SPLADE for Hybrid Retrieval: The task requires combining results from BM25 (sparse retrieval) and SPLADE (dense retrieval) into a single result set. This could be done by merging, ranking, or using a weighted combination of the results from both retrieval methods.
- Hybrid Retrieval Setup with BGE-M3 and SPLaDe-v2
- BGE-M3 Model for Sparse Vectors: BGE-M3 is another model that can be used for sparse vector generation, typically for search or retrieval tasks. It requires storing these sparse vectors and retrieving relevant documents based on a query.
- SPLaDe-v2 for Dense Representations: SPLaDe-v2 is an advanced model from Naver Labs that is focused on sparse-dense representations for efficient retrieval. It generates sparse vectors that can be stored in a vector database for fast retrieval.
- https://milvus.io/docs/sparse_vector.md
