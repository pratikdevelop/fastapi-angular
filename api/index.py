from sqlalchemy.orm import Session
from schemas import ItemCreate, ItemUpdate
from database import SessionLocal, engine
import models
from typing_extensions import Annotated
from fastapi import FastAPI, File, UploadFile, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from tempfile import NamedTemporaryFile
import shutil
import os
from fastapi.responses import FileResponse
from pathlib import Path

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# Path to store uploaded files
UPLOAD_FOLDER = Path("uploads")

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
async def create_user_item(todo_name: str = Form(...), todo_description: str = Form(...), todo_image:UploadFile = Form(...), db: Session = Depends(get_db)):
    filename = upload_file(todo_image)
    print(filename)
    item = {
        "todo_name": todo_name,
        "todo_description": todo_description,
        "todo_image": filename,
    }
    db_item = models.Item(**item)
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

# Function to save file to database
# def save_file_to_db(file_id: str, file_name: str, db: Session):
#     db_file = models.UploadedFile(file_name=file_name)
#     db.add(db_file)
#     db.commit()
#     db.refresh(db_file)
#     db.close()

# FastAPI endpoint to handle file upload
# @app.post("/upload/")


def upload_file(file: UploadFile = File(...)):
    try:
        # Alternatively, you can directly write the file to disk
        file_path = os.path.join("uploads", file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        print("File uploaded:", file.filename)
        # save_file_to_db(file_id, file_path, db)
        return file.filename
    finally:
        file.file.close()


@app.get("/files/{file_name}")
async def get_file(file_name: str):
    try:
        filepath = UPLOAD_FOLDER / file_name
        return FileResponse(filepath, media_type="application/octet-stream")
    except FileNotFoundError:
        return {"error": "File not found"}

