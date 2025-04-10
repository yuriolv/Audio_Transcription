import sqlite3


db_path = "language_school.db"

def create_transcription(name, content, class_id=None):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Transcriptions (Class_id, Content, Title) VALUES (?, ?, ?)", (class_id, content, name))
        conn.commit()

def read_transcricoes():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT Content FROM Transcriptions")
        return cursor.fetchall()
    
def get_by_id(student_id):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT Content FROM Transcriptions WHERE Students_Ids LIKE ? ORDER BY Id DESC LIMIT 3", (f'%{student_id}%',))
        return cursor.fetchall()
    
def get_transcription(title):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT Id FROM Transcriptions WHERE title = ?", (title,))
        return cursor.fetchall()

def update_transcription(transcription_id, class_id, content):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE Transcriptions SET Class_id = ?, Content = ? WHERE Id = ?", (class_id, content, transcription_id))
        conn.commit()

def delete_transcription(transcription_id):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Transcriptions WHERE Id = ?", (transcription_id,))
        conn.commit()