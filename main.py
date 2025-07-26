from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class TodoItem(BaseModel):
    id: int
    item: str
    due_date: str

todos: List[TodoItem] = []
next_id = 1

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})

@app.post("/create-todo")
def create_todo(item: str = Form(...), due_date: str = Form(...)):
    global next_id
    todos.append(TodoItem(id=next_id, item=item, due_date=due_date))
    next_id += 1
    return RedirectResponse("/", status_code=303)

@app.get("/delete-todo/{todo_id}")
def delete_todo(todo_id: int):
    global todos
    todos = [todo for todo in todos if todo.id != todo_id]
    return RedirectResponse("/", status_code=303)
