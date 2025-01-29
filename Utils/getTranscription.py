from Models.Transcription import Transcription
from pathlib import Path
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_Transcription(file_name):
  main_directory = Path("Assets/Transcriptions")

  for item in main_directory.iterdir():
      absolute = item.name.split()

      date_str = f'{absolute[0]} {absolute[1]}'
      date_obj = datetime.strptime(date_str, f"%Y-%m-%d %H:%M:%S")
      formated_date = date_obj.strftime(f'%d/%m/%y %H:%M')

      name = f'{absolute[2]} {absolute[3]} - {formated_date}'

      if name == file_name:
          for i in item.iterdir():
            path = i

          transcripted = Transcription(path)

          transcripted.getTranscription()
          transcripted.getStudents()

          return transcripted.students
