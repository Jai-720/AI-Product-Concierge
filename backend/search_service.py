# 1. Import chromadb, BaseModel/Field, load_dotenv, and ChatGoogleGenerativeAI.
# 2. Call load_dotenv().
# 3. Define the 'ProductIntent' Pydantic model (search_query, category, max_price).
# 4. Initialize the LLM (gemini-2.5-flash) and bind it to ProductIntent.
# 5. Initialize the ChromaDB client and get the "products" collection.
# 6. Define a function: def execute_search(user_text: str):
# 7. Inside execute_search: Pass user_text to the LLM to get the intent.
# 8. Inside execute_search: Build the $and filter if conditions exist.
# 9. Inside execute_search: Query the ChromaDB collection and return the results.
import chromadb
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel,Field
from typing import Optional,Literal
import dotenv   
from pathlib import Path

dotenv.load_dotenv()

class ProductIntent(BaseModel):
    search_query: str = Field(description="The is the query of the user")
    # Force the AI to pick one of these three strings, or return None
    category: Optional[Literal["footwear", "gear", "apparel"]] = Field(
        default=None, 
        description="The category of the product. Must be footwear, gear, or apparel."
    )
    max_price: Optional[float] = Field(default=None, description="The maximum price the user want to spend")

# 1. Create the base LLM instance
llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0)
strict_llm = llm.with_structured_output(ProductIntent)

DATABASE_PATH = Path(__file__).resolve().parent / "chroma_db"
client=chromadb.PersistentClient(path=str(DATABASE_PATH))
collection=client.get_or_create_collection("products")

def execute_search(user_text: str):
    intent = strict_llm.invoke(user_text)
    print("Extracted Intent:", intent)
    
    conditions = []
    where_filter = None

    if intent.category:
        conditions.append({"category": intent.category})

    if intent.max_price is not None:
        conditions.append({"price": {"$lte": intent.max_price}})

    if len(conditions) == 1:
        where_filter = conditions[0]
    elif len(conditions) > 1:
        where_filter = {"$and": conditions}

    # Query the database
    results = collection.query(
        query_texts=[intent.search_query],
        n_results=2,
        where=where_filter if where_filter else None
    )

    # 1. Check if the database found anything (using plural 'ids')
    if not results["ids"][0]:
        return []

    # 2. Format the raw database response into a clean list of objects
    clean_output = []
    for item_id, meta in zip(results["ids"][0], results["metadatas"][0]):
        clean_item = {
            "id": item_id,
            "price": meta["price"],
            "category": meta["category"]
        }
        clean_output.append(clean_item)

    return clean_output



