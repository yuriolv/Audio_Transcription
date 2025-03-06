import sqlite3

db_path = "language_school.db"

def create_aula(data, turma, id_professor):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Aula (Data, Turma, idProfessor) VALUES (?, ?, ?)", (data, turma, id_professor))
        conn.commit()

def read_aulas():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Aula")
        return cursor.fetchall()

def update_aula(aula_id, data, turma, id_professor):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE Aula SET Data = ?, Turma = ?, idProfessor = ? WHERE Id = ?", (data, turma, id_professor, aula_id))
        conn.commit()

def delete_aula(aula_id):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Aula WHERE Id = ?", (aula_id,))
        conn.commit()
