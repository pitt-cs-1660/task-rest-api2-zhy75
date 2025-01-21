# **SQLite Reference Guide for Task Manager API Assignment**

## **What is SQLite?**

**SQLite** is a lightweight, serverless, self-contained SQL database engine that is commonly used for local storage in applications. It stores the entire database in a single file, making it ideal for prototyping and small applications. Unlike traditional databases, SQLite doesn’t require a separate server process.

**sqlite3** is a built-in Python module that provides an interface to interact with SQLite databases. It allows you to execute SQL queries, manage transactions, and work with database connections. You can find more information in the [SQLite Documentation](https://www.sqlite.org/docs.html).
### **Key Features of SQLite:**
- No setup or configuration is required.
- Database is stored as a single `.db` file.
- SQL syntax is similar to other relational databases like MySQL and PostgreSQL.
- Fast, simple, and portable.

---

## **Using SQLite in Your Assignment**
In this assignment, you will interact with an **SQLite** database using SQL queries within the FastAPI routes. The `database.py` file provides utility functions to initialize the database (`init_db()`) and create a connection (`get_db_connection()`). Each route in `server.py` executes **SQL queries** to perform CRUD operations on the `tasks` table.

### **Database Table Structure:**
| **Column**   | **Type**   | **Description**                |
|--------------|------------|---------------------------------|
| `id`         | `INTEGER`  | Auto-incremented primary key    |
| `title`      | `TEXT`     | Title of the task               |
| `description`| `TEXT`     | Detailed description of the task|
| `completed`  | `BOOLEAN`  | Indicates whether the task is complete |

---

## **SQL Queries You Will Use**
Below is a reference to the types of SQL queries you will use for each CRUD operation.

### **1. Create a Task (`POST /tasks/`)**
To insert a new task into the `tasks` table, use the `INSERT INTO` SQL query:
```sql
INSERT INTO tasks (title, description, completed) VALUES (?, ?, ?)
```
- **Parameters:** `(task_data.title, task_data.description, task_data.completed)`
- The `?` placeholders are replaced with the corresponding values to prevent SQL injection.

**Python Code Example:**
```python
from cc_simple_server.database import get_db_connection 
...
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute(
    "INSERT INTO tasks (title, description, completed) VALUES (?, ?, ?)",
    (task_data.title, task_data.description, task_data.completed),
)
conn.commit()
...
conn.close()
```

### **2. Retrieve All Tasks (`GET /tasks/`)**
To fetch all tasks from the database, use the `SELECT` SQL query:
```sql
SELECT * FROM tasks
```
- This query retrieves all columns (`id`, `title`, `description`, `completed`) from the `tasks` table.

**Python Code Example:**
```python
from cc_simple_server.database import get_db_connection 
...
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM tasks")
rows = cursor.fetchall()
...
conn.close()
```
- `fetchall()` returns all rows as a list of dictionaries.

### **3. Update a Task (`PUT /tasks/{task_id}/`)**
To update an existing task by its ID, use the `UPDATE` SQL query:
```sql
UPDATE tasks SET title = ?, description = ?, completed = ? WHERE id = ?
```
- **Parameters:** `(task_data.title, task_data.description, task_data.completed, task_id)`
- The `WHERE id = ?` clause ensures only the specified task is updated.

**Python Code Example:**
```python
from cc_simple_server.database import get_db_connection 
...
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute(
    "UPDATE tasks SET title = ?, description = ?, completed = ? WHERE id = ?",
    (task_data.title, task_data.description, task_data.completed, task_id),
)
...
conn.commit()
```

### **4. Delete a Task (`DELETE /tasks/{task_id}/`)**
To delete a task by its ID, use the `DELETE` SQL query:
```sql
DELETE FROM tasks WHERE id = ?
```
- **Parameters:** `(task_id,)`

**Python Code Example:**
```python
from cc_simple_server.database import get_db_connection 
...
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
...
conn.commit()
```

---

## **Additional Tips:**
- **Database Connection:** Ensure that each database connection (`conn`) is properly closed after executing queries to avoid resource leaks.
- **Transactions:** The `conn.commit()` call is used to save changes (insert, update, delete). Without `commit()`, the changes will not be saved.

---

## **Example SQL Flow for CRUD Operations:**

### **Creating a Task (`POST /tasks/`):**
1. The client sends a `POST` request with the task details.
2. The server runs an `INSERT INTO` SQL query to store the task.
3. The server responds with the created task details.

### **Retrieving All Tasks (`GET /tasks/`):**
1. The server runs a `SELECT * FROM tasks` query.
2. The server formats the results and returns them as a list of tasks.

### **Updating a Task (`PUT /tasks/{task_id}/`):**
1. The client sends a `PUT` request with updated task details.
2. The server checks if the task exists (`SELECT * FROM tasks WHERE id = ?`).
3. If the task exists, the server runs an `UPDATE` SQL query.
4. The server responds with the updated task details.

### **Deleting a Task (`DELETE /tasks/{task_id}/`):**
1. The client sends a `DELETE` request for a task ID.
2. The server checks if the task exists.
3. If the task exists, the server runs a `DELETE FROM tasks WHERE id = ?` query.
4. The server responds with a confirmation message.
