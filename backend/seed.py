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


