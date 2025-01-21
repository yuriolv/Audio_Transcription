from Models.Transcription import Transcription
from pathlib import Path
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_Transcription(file):
  main_directory = Path("Audios")

  for item in main_directory.iterdir():
      path = item.name.split()
      name = f'{path[0]} {path[1]}'

      if name == file:
          for i in item.iterdir():
            relative = i.relative_to()

          transcripted = Transcription(relative)

          transcripted.getTranscription()
          transcripted.getStudents()

          print(transcripted.students)
          return transcripted.students
