import assemblyai as aai

# Replace with your API key
aai.settings.api_key = "cc88dc1603024ea089533cf365cbcc4d"

# URL of the file to transcribe
FILE_URL = "https://assembly.ai/wildfires.mp3"

# You can also transcribe a local file by passing in a file path
# FILE_URL = './path/to/file.mp3'

config = aai.TranscriptionConfig(speaker_labels=True)

transcriber = aai.Transcriber()
transcript = transcriber.transcribe(
  FILE_URL,
  config=config
)

for utterance in transcript.utterances:
  with open('text_files/lesson.txt', 'a') as arc:
    arc.write(f"Speaker {utterance.speaker}: {utterance.text}")
