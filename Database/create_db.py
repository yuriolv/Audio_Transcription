import sqlite3

# Conectar ao banco de dados (ou criar se não existir)
conn = sqlite3.connect("language_school.db")
cursor = conn.cursor()

cursor.executescript('''
CREATE TABLE IF NOT EXISTS Aluno (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Nome TEXT NOT NULL,
    Email TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Professor (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Nome TEXT NOT NULL,
    Email TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Aula (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Data TEXT NOT NULL,
    Turma TEXT,
    idProfessor INTEGER,
    FOREIGN KEY (idProfessor) REFERENCES Professor(Id)
);

CREATE TABLE IF NOT EXISTS Transcricao (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    idAula INTEGER,
    Hora TEXT,
    Frase TEXT NOT NULL,
    FOREIGN KEY (idAula) REFERENCES Aula(Id)
);

CREATE TABLE IF NOT EXISTS Correcao (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Correcao TEXT NOT NULL,
    idAluno INTEGER,
    idTranscricao INTEGER,
    FOREIGN KEY (idAluno) REFERENCES Aluno(Id),
    FOREIGN KEY (idTranscricao) REFERENCES Transcricao(Id)
);
''')

conn.commit()
conn.close()
