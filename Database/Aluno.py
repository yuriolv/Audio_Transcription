import sqlite3


db_path = "language_school.db"

def create_aluno(nome, email):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Aluno (Nome, Email) VALUES (?, ?)", (nome, email))
        conn.commit()

def read_alunos():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Aluno")
        return cursor.fetchall()

def get_student(name):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT Id FROM Aluno WHERE Nome = ?", (name,))
        return cursor.fetchall()


def delete_aluno(aluno_id):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Aluno WHERE Id = ?", (aluno_id,))
        conn.commit()