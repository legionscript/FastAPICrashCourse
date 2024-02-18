from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
	title="Todo App",
	description="Our Basic Todo App",
	version='0.0.1'
)

class Category(Enum):
	"""Categories for a Todo"""
	PERSONAL = 'personal'
	WORK = 'work'

class Todo(BaseModel):
	title: str
	completed: bool
	id: int
	category: Category

todos = {
	0: Todo(title='test1', completed=True, id=0, category=Category.PERSONAL),
	1: Todo(title='test2', completed=False, id=1, category=Category.WORK)
}

@app.get('/')
def index() -> dict[str, dict[int, Todo]]:
	return {'todos': todos}

@app.get('/todos/{todo_id}')
def get_todo_by_id(todo_id: int) -> Todo:
	if todo_id not in todos:
		raise HTTPException(status_code=404, detail=f'ID {todo_id} does not exist.')
	return todos[todo_id]

@app.get('/todos/')
def query_todo_by_completed(completed: bool | None=None) -> dict[str, list[Todo]]:
	filtered_todos = [todo for todo in todos.values() if todo.completed is completed]
	return {'todos': filtered_todos}

@app.post('/')
def create_todo(todo: Todo) -> dict[str, Todo]:
	if todo.id in todos:
		raise HTTPException(status_code=400, detail=f'ID {todo.id} already exists.')

	todos[todo.id] = todo
	return {'todo': todo}

@app.put('/todos/{todo_id}')
def update_todo(todo_id, todo: Todo) -> dict[str, Todo]:
	todos[todo_id] = todo
	return {'todo': todo}

@app.delete('/todos/{todo_id}')
def delete_todo(todo_id: int) -> dict[str, Todo]:
	if todo_id not in todos:
		raise HTTPException(status_code=404, detail=f'ID {todo_id} does not exist')

	todo = todos.pop(todo_id)
	return {'todo': todo}	