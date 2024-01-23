from fastapi import FastAPI, File, Form, UploadFile, HTTPException, status, Path
from os import makedirs, getcwd, remove
from typing import Annotated
from nanoid import generate
from bson import ObjectId
from db.database import database as db
from db.models.post import Post, PostUpdate
from db.schemas.post import post_schema, posts_schema

BASE_URL = "http://127.0.0.1:8000/"

UPLOADS_DIR = getcwd() + "/uploads/"
makedirs(UPLOADS_DIR, exist_ok=True)

app = FastAPI()


@app.post("/create", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(
    name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    image: Annotated[UploadFile, File()],
):
    try:
        ext_image = image.filename.split(".")[1]
        filename_server = f"{generate(size=10)}.{ext_image}"

        with open(UPLOADS_DIR + filename_server, "wb") as image_file:
            image_file.write(image.file.read())

        post = {
            "name": name,
            "description": description,
            "filename_server": filename_server
        }

        id = db.posts.insert_one(post).inserted_id
        new_post = post_schema(db.posts.find_one({"_id": id}))

        return Post(**new_post)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/posts", response_model=list[Post])
async def read_posts():
    return posts_schema(db.posts.find())


@app.put("/update/{post_id}", response_model=Post)
async def update_post(post_id: str, post_data: PostUpdate):
    try:
        updated_data = {
            "$set": {
                "name": post_data.name,
                "description": post_data.description
            }
        }

        db.posts.find_one_and_update(
            {"_id": ObjectId(post_id)}, updated_data)

        post = db.posts.find_one({"_id": ObjectId(post_id)})

        return post_schema(post)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found")


@app.delete("/delete/{post_id}", response_model=Post)
async def delete_post(post_id: Annotated[str, Path(title="Id Post")]):
    post = db.posts.find_one_and_delete({"_id": ObjectId(post_id)})

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found")

    image_path = UPLOADS_DIR + post["filename_server"]
    remove(image_path)

    return post_schema(post)
