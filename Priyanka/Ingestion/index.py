from llama_index.core import SimpleDirectoryReader

# def get_meta(file_path):
#     return {"foo": "bar", "file_path": file_path}

# reader = SimpleDirectoryReader(input_dir="inputs/", recursive=True, required_exts=[".txt",".pdf", ".docx"],file_metadata=get_meta)
reader = SimpleDirectoryReader(input_dir="inputs/", recursive=True, required_exts=[".txt",".pdf", ".docx"])

# SimpleDirectoryReader(input_dir="path/to/directory", recursive=True)
documents = reader.load_data()

for doc in documents:
    print("\n\n")
    print(doc)

print("\n\n\n\n****************************************************************************\n\n\n\n")
all_docs = []
#better data extraction
for docs in reader.iter_data():
    # <do something with the documents per file>
    print("\n\n")
    print(docs)
    all_docs.extend(docs)



