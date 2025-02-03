import sqlite3
import datetime

class Task:
    def __init__(self, name, description, due_date):
        self.name = name
        self.description = description
        self.due_date = due_date

    def __str__(self):
        return f"{self.name}: {self.description} (Due: {self.due_date})"

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                due_date TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def add_task(self, name, description, due_date):
        try:
            self.cursor.execute("INSERT INTO tasks (name, description, due_date) VALUES (?, ?, ?)",
                                (name, description, due_date))
            self.conn.commit()
            print(f"Task '{name}' added successfully.")
        except sqlite3.IntegrityError:
            print(f"Task '{name}' already exists.")

    def view_tasks(self):
        try:
            self.cursor.execute("SELECT * FROM tasks")
            rows = self.cursor.fetchall()
            for row in rows:
                task = Task(row[1], row[2], row[3])
                print(task)
        except sqlite3.Error as e:
            print(f"Error: {e}")

    def delete_task(self, name):
        try:
            self.cursor.execute("DELETE FROM tasks WHERE name = ?", (name,))
            self.conn.commit()
            print(f"Task '{name}' deleted successfully.")
        except sqlite3.IntegrityError:
            print(f"Task '{name}' does not exist.")

    def update_task(self, name, new_name=None, new_description=None, new_due_date=None):
        try:
            if new_name is not None:
                self.cursor.execute("UPDATE tasks SET name = ? WHERE name = ?", (new_name, name))
            if new_description is not None:
                self.cursor.execute("UPDATE tasks SET description = ? WHERE name = ?", (new_description, name))
            if new_due_date is not None:
                self.cursor.execute("UPDATE tasks SET due_date = ? WHERE name = ?", (new_due_date, name))
            self.conn.commit()
            print(f"Task '{name}' updated successfully.")
        except sqlite3.Error as e:
            print(f"Error: {e}")

class TimeManagementApp:
    def __init__(self):
        self.db = Database('tasks.db')

    def run(self):
        while True:
            print("\nTime Management App")
            print("1. Add Task")
            print("2. View Tasks")
            print("3. Delete Task")
            print("4. Update Task")
            print("5. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                name = input("Enter task name: ")
                description = input("Enter task description: ")
                due_date = datetime.datetime.strptime(input("Enter due date (YYYY-MM-DD): "), "%Y-%m-%d")
                self.db.add_task(name, description, due_date)
            elif choice == "2":
                self.db.view_tasks()
            elif choice == "3":
                name = input("Enter task name: ")
                self.db.delete_task(name)
            elif choice == "4":
                name = input("Enter task name: ")
                new_name = input("Enter new task name (optional): ")
                new_description = input("Enter new task description (optional): ")
                new_due_date = datetime.datetime.strptime(input("Enter new due date (YYYY-MM-DD) (optional): "), "%Y-%m-%d")
                self.db.update_task(name, new_name or None, new_description or None, new_due_date or None)
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    app = TimeManagementApp()
    app.run()