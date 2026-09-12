# 1. Import chromadb.
# 2. Initialize a persistent ChromaDB client pointing to "./chroma_db".
# 3. Delete the collection "products" if it already exists, then create a new collection named "products".
# 4. Define a list of at least 3 products with ids, document descriptions, and metadatas (category as string, price as float).
# 5. Add the documents, metadatas, and ids to the collection.
# 6. Print a confirmation message showing the count of items in the collection.

import chromadb
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
client=chromadb.PersistentClient(path=str(BASE_DIR / "chroma_db"))
with open (BASE_DIR / "products.json", 'r') as file:
    products=json.load(file)


try:
    client.delete_collection("products")
except ValueError:
    pass

collection=client.get_or_create_collection(name="products")

ids = []
documents = []
metadatas = []

for product in products:
    ids.append(product["id"])
    documents.append(product["description"])
    metadatas.append({
        "category": product["category"],
        "price": float(product["price"]),
    })


collection.add(
    ids=ids,
    documents=documents,
    metadatas=metadatas,
)


print(f"Number itmes in the collection:{collection.count()}")


