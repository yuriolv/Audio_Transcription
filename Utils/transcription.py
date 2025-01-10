#transcripted = transcript()
#output = errorDetection(transcripted)
#send_message(text, "69d2d1a285494d1ba7e76396fe451f25")
""" from transcription import transcript
from errorDetection import errorDetection """
import assemblyai as aai

def transcript():
  aai.settings.api_key = "cc88dc1603024ea089533cf365cbcc4d"

  FILE_URL = "audios/audio1044392040.m4a"

  config = aai.TranscriptionConfig(speaker_labels=True)

  transcriber = aai.Transcriber()
  transcript = transcriber.transcribe(
    FILE_URL,
    config=config
  )

  return transcript.text

""" import os

from dotenv import load_dotenv
import assemblyai as aai

from zoom import ZoomClient

load_dotenv()

ZOOM_ACCOUNT_ID = os.environ.get('ZOOM_ACCOUNT_ID')
ZOOM_CLIENT_ID = os.environ.get('ZOOM_CLIENT_ID')
ZOOM_CLIENT_SECRET = os.environ.get('ZOOM_CLIENT_SECRET')
aai.settings.api_key = os.environ.get('ASSEMBLYAI_API_KEY')

transcriber = aai.Transcriber()

client = ZoomClient(account_id=ZOOM_ACCOUNT_ID, client_id=ZOOM_CLIENT_ID, client_secret=ZOOM_CLIENT_SECRET)

recs = client.get_recordings()
if recs['meetings']:    
    rec_id = recs['meetings'][0]['id']
    my_url = client.get_download_url(rec_id)
    transcript = transcriber.transcribe(my_url)
    print(transcript.text)
    with open('transcript.txt', 'w') as f:
        f.write(transcript.text)
else:
    print('No meetings to transcribe.') """