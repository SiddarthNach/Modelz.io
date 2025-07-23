import requests
import json
import boto3
from datetime import datetime

# Initialize SQS client
sqs = boto3.client("sqs", region_name="us-east-2")
QUEUE_URL = "https://sqs.us-east-2.amazonaws.com/671476237927/inference-db"

def get_timestamp_info():
    now = datetime.now()
    return {
        'timestamp': now.strftime('%Y-%m-%d_%H:%M:%S'),
        'day': now.strftime('%A'),
        'time': now.strftime('%H:%M:%S'),
        'date': now.strftime('%Y-%m-%d'),
        'month': now.strftime('%B'),
        'week': now.strftime('%U'),
    }

def send_to_sqs(payload):
    try:
        response = sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(payload)
        )
        print(f"Sent message ID: {response['MessageId']}")
    except Exception as e:
        print(f"Failed to send message to SQS: {e}")

def fetch_all_models():
    url = "https://openrouter.ai/api/frontend/models"
    response = requests.get(url)
    response.raise_for_status()
    json_data = response.json()
    return json_data.get('data', [])

def enqueue_model_links():
    models = fetch_all_models()
    for model in models:
        permaslug = model.get('permaslug')
        if not permaslug:
            continue
        model_url = f"https://openrouter.ai/models/{permaslug}"
        payload = {
            "model_id": permaslug,
            "url": model_url,
            **get_timestamp_info()
        }
        send_to_sqs(payload)

if __name__ == "__main__":
    enqueue_model_links()
