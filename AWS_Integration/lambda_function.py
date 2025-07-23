import requests
import json
import boto3
from datetime import datetime
from decimal import Decimal
from uuid import uuid4

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = 'OpenRouterModelScrapedData'

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

def fetch_all_models():
    url = "https://openrouter.ai/api/frontend/models"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get('data', [])
    except requests.exceptions.RequestException as e:
        print(f"error fetching model list: {e}")
        return []

def fetch_model_provider_data(permaslug):
    url = f"https://openrouter.ai/api/frontend/stats/endpoint?permaslug={permaslug}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"failed to fetch stats for {permaslug}: {e}")
        return None

def to_decimal_or_none(value):
    if value in (None, '', 'N/A'):
        return None
    try:
        return Decimal(str(value))
    except (ValueError, TypeError):
        return None

def upload_to_dynamodb(data_list):
    if not data_list:
        print("no data to upload to dynamodb.")
        return

    table = dynamodb.Table(TABLE_NAME)
    print(f"uploading {len(data_list)} items to dynamodb")

    try:
        with table.batch_writer() as batch:
            for item in data_list:
                batch.put_item(Item=item)
        print("upload successful.")
    except Exception as e:
        print(f"upload failed: {e}")
        raise

def lambda_handler(event, context):
    print(f"lambda triggered at {datetime.now()}")

    all_provider_data_for_dynamodb = []
    models = fetch_all_models()

    if not models:
        print("no models found.")
        return {
            'statusCode': 500,
            'body': json.dumps('failed to fetch models.')
        }

    current_timestamp_info = get_timestamp_info()

    for model in models:
        permaslug = model.get('permaslug')
        if not permaslug:
            continue

        print(f"processing model: {permaslug}")
        stats_data = fetch_model_provider_data(permaslug)

        if stats_data and stats_data.get('data'):
            for provider in stats_data['data']:
                if not isinstance(provider, dict):
                    continue

                provider_name = provider.get('name', 'N/A')
                unique_sort_key = f"{provider_name}#{current_timestamp_info['timestamp']}#{uuid4().hex[:6]}"

                item = {
                    'ModelId': permaslug,
                    'ProviderNameTimestamp': unique_sort_key,
                    'ProviderName': provider_name,
                    'MaxCompletionTokens': to_decimal_or_none(provider.get('max_completion_tokens')),
                    'ContextLength': to_decimal_or_none(provider.get('context_length')),
                    'PricingPrompt': to_decimal_or_none(provider.get('pricing', {}).get('prompt')),
                    'PricingCompletion': to_decimal_or_none(provider.get('pricing', {}).get('completion')),
                    'P50Throughput': to_decimal_or_none(provider.get('stats', {}).get('p50_throughput')),
                    'P50Latency': to_decimal_or_none(provider.get('stats', {}).get('p50_latency')),
                    **current_timestamp_info
                }
                all_provider_data_for_dynamodb.append(item)
        else:
            print(f"no stats for {permaslug}")

    if all_provider_data_for_dynamodb:
        upload_to_dynamodb(all_provider_data_for_dynamodb)
    else:
        print("nothing to upload")

    print("lambda done.")
    return {
        'statusCode': 200,
        'body': json.dumps('scrape + upload done')
    }
