from Model.Transcription import Transcription
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#transcripted = transcript()
#output = errorDetection(transcripted)
#send_message(text, "69d2d1a285494d1ba7e76396fe451f25")
""" from transcription import transcript
from errorDetection import errorDetection """

def get_Transcription():
  transcripted = Transcription()
  
  transcripted.getTranscription()
  transcripted.getStudents()

  return transcripted.students
