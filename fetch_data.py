import requests
import json

def fetch_and_save_json(filename='output.json'):
    url = "https://openrouter.ai/api/frontend/stats/endpoint?permaslug=deepseek%2Fdeepseek-chat-v3-0324"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Saved JSON data to {filename}")
    else:
        print("Failed to fetch data. Status code:", response.status_code)

if __name__ == "__main__":
    fetch_and_save_json()
