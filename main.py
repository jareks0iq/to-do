from uuid import uuid4

from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
)

class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool

class TaskCreateSchema(BaseModel):
    title: str

class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None

class Category(BaseModel):
    id: str
    name: str

tasks: list[TaskSchema] = []
categories: list[Category] = []

class CategoryCreate(BaseModel):
    name: str

class CategoryUpdate(BaseModel):
    name: str

@app.get("/categories")
def get_categories() -> list[Category]:
    return categories

@app.post("/categories", status_code=status.HTTP_201_CREATED)
def create_categories(payload: CategoryCreate):
    new_category = Category(id=str(uuid4()), name=payload.name)
    categories.append(new_category)

    return new_category

@app.patch("/categories/{id}")
def update_task(id: str, payload: CategoryUpdate):
    for category in categories:
        if category.id == id:
            category.name = payload.name
            return category

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Category not found",
    )

@app.delete("/categories/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(id: str):
    for category in categories:
        if category.id == id:
            categories.remove(category)
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Category not found",
    )


@app.get("/tasks")
def get_tasks() -> list[TaskSchema]:
    return tasks

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateSchema) -> TaskSchema:
    new_task = TaskSchema(id=str(uuid4()), title=payload.title, completed=False)

    tasks.append(new_task)
    return new_task

@app.patch("/tasks/{task_id}")
def update_task(task_id: str, payload: TaskUpdateSchema):
    for task in tasks:
        if task.id == task_id:
            if payload.title:
                task.title = payload.title
            if payload.completed is not None:
                task.completed = payload.completed
            return task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return
