import sqlite3

db_path = "language_school.db"

def create_student(name, email):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Students (Name, Email) VALUES (?, ?)", (name, email))
        conn.commit()

def read_students():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Students")
        return cursor.fetchall()

def get_id(name):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT Id FROM Students WHERE Name = ?", (name,))
        return cursor.fetchall()
    
def get_name(student_id):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT Name FROM Students WHERE Id = ?", (student_id,))
        return cursor.fetchall()

def delete_student(student_id):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Students WHERE Id = ?", (student_id,))
        conn.commit()

def update_student(student_id, new_name, new_email):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM Students WHERE Id = ?", (student_id,))
        exists = cursor.fetchone()[0] > 0
        
        if not exists:
            raise ValueError(f"Students with ID {student_id} not found.")

        cursor.execute("""
            UPDATE Student
            SET Name = ?, Email = ?
            WHERE Id = ?
        """, (new_name, new_email, student_id))
        conn.commit()
        print(f"Student with ID {student_id} updated succesfully.")
