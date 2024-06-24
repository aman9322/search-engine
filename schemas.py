from fastapi import FastAPI
from pydantic import BaseModel


class query(BaseModel):
    query: str