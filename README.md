- Task Background and Initiation:
  Begin a task in the background by sending an HTTP request (HTTP 201 response implies successful task creation) and receive a Task ID in return.
- Retrieve Task Status:
  With the provided Task ID, query the API to get the current status of the task using FastAPI.
- Querying API for Results:
  Send a query request to the API, which retrieves node-based results along with associated metadata.
- Caching and Document Store:
  Implement caching mechanisms and utilize a document store to manage the data effectively.
