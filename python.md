# **Python 3.11 Reference Guide for Task Manager API Assignment**

## **What is Python?**
Python is a high-level, general-purpose programming language known for its simplicity and readability. In this assignment, you will use Python 3.11 to implement an API using the FastAPI framework. Below, you'll find examples specific to your `server.py` file to help guide your development process.

---

## **What is FastAPI?**
FastAPI is a modern, high-performance web framework for building APIs with Python. It is designed to be fast and easy to use, featuring automatic generation of API documentation and support for asynchronous programming.

### Key Features of FastAPI:
- **Automatic API Documentation:** FastAPI generates interactive API documentation using Swagger UI.
- **Type Checking:** FastAPI uses Python type hints for data validation and serialization.
- **Performance:** FastAPI is built on top of Starlette and Pydantic, making it one of the fastest Python frameworks.

## **Key Python Concepts for This Assignment**
Below are some essential Python concepts with examples tailored to your Task Manager API.

### **1. Variables and Data Types**
In Python, variables store data values and are dynamically typed.
```python
# Example variables used in your API
id = 1  # Integer
title = "Write documentation"  # String
description = "Detailed instructions for the API"  # String
completed = False  # Boolean (task not completed)
```

---

### **2. Functions in Python and FastAPI Routes**
Functions in Python are defined using the `def` keyword. In FastAPI, functions become routes when decorated with `@app.get()`, `@app.post()`, etc.
```python
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Cloud Computing!"}
```
- **`@app.get("/")`**: Defines a route that responds to `GET /` requests.
- **`async def`**: Indicates the function is asynchronous.
- **`return {"message": ...}`**: Returns a JSON response.

**Tip:** FastAPI functions should be asynchronous (`async def`) for non-blocking I/O operations.

---

### **3. Control Flow and Error Handling**
Control flow helps to decide what code runs based on conditions. Error handling ensures the program handles unexpected input gracefully.

#### Example: Check if a Task Exists
```python
if not existing_task:
    raise HTTPException(status_code=404, detail="Task not found")
```
- If `existing_task` is `None`, a `404 Not Found` error is raised.

#### Try/Except for Error Handling:
```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
```
---

## **Working with Pydantic Models**
Pydantic is used for data validation and serialization. In this assignment, you are provided with the `TaskCreate` and `TaskRead` models.

### **Example of a Pydantic Model:**
```python
from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
```
- **`title: str`**: A required string field for the task title.
- **`description: Optional[str]`**: An optional string field for the task description.
- **`completed: bool`**: A boolean indicating if the task is completed (default is `False`).

**Tip:** Use `task_data.dict()` to convert a Pydantic model to a dictionary.

---

## **Interacting with SQLite**
The database interaction is handled using SQLite through the `sqlite3` module.

### **1. Connecting to the Database**
The `get_db_connection` function in `database.py` returns a connection to the database:
```python
conn = get_db_connection()
cursor = conn.cursor()
```

### **2. SQL Queries**
You will use `execute` to run SQL commands.

#### **Create a Task (POST /tasks/)**
Inserts a new task into the database.
```python
cursor.execute(
    "INSERT INTO tasks (title, description, completed) VALUES (?, ?, ?)",
    (task_data.title, task_data.description, task_data.completed),
)
conn.commit()
```
- `?` placeholders prevent SQL injection.

### **3. Retrieve All Tasks (GET /tasks/)**
Fetches all tasks from the database.
```python
cursor.execute("SELECT * FROM tasks")
rows = cursor.fetchall()
```
- `fetchall()` returns a list of rows.

### **4. Update a Task (PUT /tasks/{task_id}/)**
Updates the details of a specific task.
```python
cursor.execute(
    "UPDATE tasks SET title = ?, description = ?, completed = ? WHERE id = ?",
    (task_data.title, task_data.description, task_data.completed, task_id),
)
conn.commit()
```

### **5. Delete a Task (DELETE /tasks/{task_id}/)**
Deletes a task by its ID.
```python
cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
conn.commit()
```

---

## **Common Python Syntax in Your API**

### **1. String Formatting (f-strings)**
Use f-strings to format strings.
```python
task_id = 42
print(f"Task {task_id} deleted successfully")  # Output: Task 42 deleted successfully
```

### **2. Type Hints for Readability**
Type hints specify the expected types of function parameters and return values.
```python
def format_task(task_id: int, title: str) -> dict:
    return {"id": task_id, "title": title}
```

### **3. Dictionary Comprehensions**
Used for building lists or dictionaries from an iterable.
```python
# Convert rows to TaskRead objects
return [TaskRead(id=row["id"], title=row["title"], description=row["description"], completed=bool(row["completed"])) for row in rows]
```

---

## **FastAPI Error Responses**
FastAPI provides the `HTTPException` class to return custom error responses.
```python
raise HTTPException(status_code=404, detail="Task not found")
```
- `status_code=404`: Indicates a "Not Found" error.
- `detail`: Provides a descriptive error message.

---

## **Running and Testing Your API**

### **1. Run the Development Server**
```bash
poetry run uvicorn cc_simple_server.server:app --reload --host 0.0.0.0 --port 8000
```

### **2. Use `cURL` for Manual Testing**
You can manually test the API using `cURL` commands:

#### **Example: Create a Task**
```bash
curl -X POST "http://localhost:8000/tasks/" -H "Content-Type: application/json" -d '{"title": "Sample Task", "description": "Write documentation", "completed": false}'
```

---

## **Tips for Success**
1. **Indentation Matters:** Python uses indentation to define code blocks.
2. **Close Database Connections:** Always call `conn.close()` to free resources.
