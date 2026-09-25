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
