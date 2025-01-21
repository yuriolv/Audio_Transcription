from Models.Transcription import Transcription
from pathlib import Path
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_Transcription(file_name):
  main_directory = Path("Assets/Transcriptions")

  for item in main_directory.iterdir():
      absolute = item.name.split()
      name = f'{absolute[0]} {absolute[1]}'

      if name == file_name:
          for i in item.iterdir():
            path = i

          transcripted = Transcription(path)

          transcripted.getTranscription()
          transcripted.getStudents()

          return transcripted.students
