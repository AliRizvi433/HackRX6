from pydantic import BaseModel
from typing import List

class QueryInput(BaseModel):
    documents: str
    questions: List[str]