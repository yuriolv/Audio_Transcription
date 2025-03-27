import sqlite3

class ReportsCRUD:
    def __init__(self, db_path):
        self.db_path = db_path
    
    def execute_query(self, query, params=None, fetch=False):
        """Executa uma consulta no banco de dados."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            if fetch:
                return cursor.fetchall()
            conn.commit()

    def create_report(self, name, class_participation, report_date, repeated_mistakes, english_percentage, behavioral_state):
        """Insere um novo relatório na tabela Reports."""
        query = """
        INSERT INTO Reports (Name, Class_participation, Report_date, Repeated_mistakes, English_percentage, Behavioral_state)
        VALUES (?, ?, ?, ?, ?, ?)"""
        params = (name, class_participation, report_date, repeated_mistakes, english_percentage, behavioral_state)
        self.execute_query(query, params)
    
    def read_reports(self):
        """Retorna todos os relatórios armazenados."""
        query = "SELECT Name, Class_participation, Report_date, Repeated_mistakes, English_percentage, Behavioral_state FROM Reports"
        return self.execute_query(query, fetch=True)
    
    def get_report(self, student_id):
        """Retorna todos os relatórios armazenados."""
        query = "SELECT Name, Class_participation, Report_date, Repeated_mistakes, English_percentage, Behavioral_state FROM Reports WHERE Student_id = ?"
        return self.execute_query(query, (student_id,), fetch=True)
    
    def update_report(self, report_id, name=None, class_participation=None, report_date=None, repeated_mistakes=None, english_percentage=None, behavioral_state=None):
        """Atualiza um relatório com base no ID."""
        fields = []
        params = []
        
        if name:
            fields.append("Name = ?")
            params.append(name)
        if class_participation:
            fields.append("Class_participation = ?")
            params.append(class_participation)
        if report_date:
            fields.append("Report_date = ?")
            params.append(report_date)
        if repeated_mistakes:
            fields.append("Repeated_mistakes = ?")
            params.append(repeated_mistakes)
        if english_percentage:
            fields.append("English_percentage = ?")
            params.append(english_percentage)
        if behavioral_state:
            fields.append("Behavioral_state = ?")
            params.append(behavioral_state)
        
        params.append(report_id)
        query = f"UPDATE Reports SET {', '.join(fields)} WHERE Id = ?"
        self.execute_query(query, params)
    
    def delete_report(self, report_id):
        """Remove um relatório com base no ID."""
        query = "DELETE FROM Reports WHERE Id = ?"
        self.execute_query(query, (report_id,))
