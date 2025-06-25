
import requests
import json

url = "https://openrouter.ai/api/v1/chat/completions"
api_key = "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" 


headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}


data = {
    
    "model": "mistralai/mistral-small-3.2-24b-instruct:free",
    "messages": [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "Hi! How can I help you?"},
        {"role": "user", "content": "List all the providers in the link "}
    ]
}

response = requests.post(url, headers=headers, json=data)  # Use `json=`, not `data=json.dumps(...)`

# print(response.status_code)
# print(response.json())

response_json = response.json()
if 'error' in response_json:
    print("API error:", response_json['error']['message'])
else:
    answer = response_json['choices'][0]['message']['content']
    print("LLM Answer:")
    print(answer)


#Not enough credits to call the API, tried a "free model" but that did not work as well
#CAP ^^