from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4  # Unique Identifier

# Created an instance of FastAPI
app = FastAPI()

class Task(BaseModel):
    id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    completed: bool = False

tasks = []  # In-memory database kind. When server turns off, all data is cleared.


# function to return responses
def response(success: bool, message: str, data=None):
    return {
        "success": success,
        "message": message,
        "data": data if data is not None else []
    }


@app.post("/tasks/")
def create_task(task: Task):  # Input to the API. Pass this info with the POST request to create a new task.
    task.id = uuid4()
    tasks.append(task)
    return response(True, "Task created successfully", task.model_dump())

# Set up basic route. GET request to the /URL
@app.get("/tasks/")
def read_tasks():
    return response(True, "Tasks retrieved successfully", [task.model_dump() for task in tasks])

@app.get("/tasks/{task_id}")
def read_task(task_id: UUID):
    for task in tasks:
        if task.id == task_id:
            return response(True, "Task retrieved successfully", task.model_dump())
    return response(False, "Task not found")

@app.put("/tasks/{task_id}")
def update_task(task_id: UUID, task_update: Task):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            updated_task = task.model_copy(update=task_update.model_dump(exclude_unset=True))  # Replaced deprecated `.copy()` and `.dict()`
            tasks[idx] = updated_task
            return response(True, "Task updated successfully", updated_task.model_dump())

    return response(False, "Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: UUID):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            deleted_task = tasks.pop(idx)
            return response(True, "Task deleted successfully", deleted_task.model_dump())

    return response(False, "Task not found")

# To check if this Python file is running and not some other
if __name__ == "__main__":
    import uvicorn  # Simple web server, allows running this API
    
    uvicorn.run(app, host="127.0.0.1", port=8000)  # 0.0.0.0 not working. 127.0.0.1 used for localhost.
    
    # Insert /docs or /redoc at the end of URL to open API documentation in Swagger UI. To end use ctrl+c on terminal.
