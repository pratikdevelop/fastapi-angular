from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from schemas import ItemCreate, ItemUpdate
from database import SessionLocal, engine
import models

from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to the appropriate origins for your Angular frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root(db: Session = Depends(get_db)):
    items = db.query(models.Item).all()
    return {"items": items} 

@app.post("/todo", response_model=None)
async def create_user_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.put("/todo/{item_id}", response_model=None)
async def update_item(item_id: int, item_update: ItemUpdate, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in item_update.dict().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return item_update


@app.delete("/todo/{item_id}", response_model=None)
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted successfully"}