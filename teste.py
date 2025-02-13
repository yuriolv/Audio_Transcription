# This example is the new way to use the OpenAI lib for python
from openai import OpenAI

client = OpenAI(
api_key = "LA-246e09a0a1fe47dc9d04f21ec6708b85e8997f2645714d6e914f6ad7ca1cadba",
base_url = "https://api.llama-api.com"
)

response = client.chat.completions.create(
model="llama3.1-70b",
messages=[
    {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
    {"role": "user", "content": "Who were the founders of Microsoft?"}
],


)

#print(response)
print(response.model_dump_json(indent=2))
print(response.choices[0].message.content)

