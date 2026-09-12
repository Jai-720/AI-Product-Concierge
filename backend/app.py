# 1. Import FastAPI and the Pydantic BaseModel.
# 2. Import the execute_search function from your search_service file.
# 3. Create the FastAPI application instance.
# 4. Define a Pydantic schema named SearchRequest that expects a single string variable named 'query'.
# 5. Create a POST endpoint routed to '/search'.
# 6. Write the function that accepts the SearchRequest as input and returns the result of calling execute_search with the query.


# 1. Import CORSMiddleware from fastapi.middleware.cors
# 2. Add the middleware to the 'app' instance using app.add_middleware()
# 3. Configure the middleware to allow all origins ("*"), all methods ("*"), and all headers ("*").
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI 
from pydantic import BaseModel
from search_service import execute_search

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
class SearchRequest(BaseModel):
    query:str


@app.post("/search")
def query_search(question:SearchRequest):
    return execute_search(question.query)