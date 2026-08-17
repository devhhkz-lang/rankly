# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from uuid import uuid4
import uvicorn

app = FastAPI(title="Rankly API")

# ---------- Models ----------
class ItemIn(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    score: float = 0.0

class Item(ItemIn):
    id: str

# ---------- In-memory storage ----------
db: dict[str, Item] = {}

# ---------- Routes ----------
@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/items", response_model=Item)
def create_item(item: ItemIn):
    item_id = str(uuid4())
    new_item = Item(id=item_id, **item.model_dump())
    db[item_id] = new_item
    return new_item

@app.get("/items", response_model=list[Item])
def list_items():
    return list(db.values())

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: str):
    item = db.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: str, item: ItemIn):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    updated = Item(id=item_id, **item.model_dump())
    db[item_id] = updated
    return updated

@app.delete("/items/{item_id}")
def delete_item(item_id: str):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    del db[item_id]
    return {"status": "deleted"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)