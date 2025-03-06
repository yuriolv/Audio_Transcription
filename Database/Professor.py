import sqlite3

db_path = "language_school.db"

def create_professor(nome, email):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Professor (Nome, Email) VALUES (?, ?)", (nome, email))
        conn.commit()

def read_professores():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Professor")
        return cursor.fetchall()

def update_professor(professor_id, nome, email):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE Professor SET Nome = ?, Email = ? WHERE Id = ?", (nome, email, professor_id))
        conn.commit()

def delete_professor(professor_id):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Professor WHERE Id = ?", (professor_id,))
        conn.commit()