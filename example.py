import requests
import json
import os

API_KEY = os.getenv('OPENAI_API_KEY')
API_ENDPOINT = "https://api.openai.com/v1/chat/completions"

def generate_chat_completion(messages, model="gpt-4", temperature=1, max_tokens=None):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }

    if max_tokens is not None:
        data["max_tokens"] = max_tokens

    response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

messages = [
    {"role": "system", "content": "I am a mental health assistant. How can I help you today?"},
    {"role": "user", "content": "Hi, I feel very lonely"}
]

response_text = generate_chat_completion(messages)
print(response_text)