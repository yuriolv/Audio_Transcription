import sqlite3

db_path = "language_school.db"

def create_teacher(name, email):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Teachers (Name, Email) VALUES (?, ?)", (name, email))
        conn.commit()

def read_teachers():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Teachers")
        return cursor.fetchall()

def update_teacher(teacher_id, name, email):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE Teachers SET Name = ?, Email = ? WHERE Id = ?", (name, email, teacher_id))
        conn.commit()

def delete_teacher(teacher_id):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Teachers WHERE Id = ?", (teacher_id,))
        conn.commit()