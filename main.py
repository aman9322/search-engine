from fastapi import FastAPI

app = FastAPI()
from schemas import query
from ranking import get_scores

# add cors
from fastapi.middleware.cors import CORSMiddleware

@app.post("/")
def read_root(query:query):
    return get_scores(query.query)  

# add cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




