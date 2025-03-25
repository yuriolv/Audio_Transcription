import sqlite3

db_path = "language_school.db"

def create_class(date, group, teacher_id):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Class (Date, Group, Teacher_Id) VALUES (?, ?, ?)", (date, group, teacher_id))
        conn.commit()

def read_classes():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Class")
        return cursor.fetchall()

def update_class(class_id, date, group, teacher_id):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE Class SET Date = ?, Group = ?, Teacher_Id = ? WHERE Id = ?", (date, group, teacher_id, class_id))
        conn.commit()

def delete_class(class_id):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Class WHERE Id = ?", (class_id,))
        conn.commit()
