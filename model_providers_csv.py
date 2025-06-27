import requests
import json
import pandas as pd
import os

def fetch_all_models():
    url = "https://openrouter.ai/api/frontend/models"
    response = requests.get(url)
    response.raise_for_status()
    json_data = response.json()
    
    return json_data.get('data', [])

def fetch_model_provider_data(permaslug):
    url = f"https://openrouter.ai/api/frontend/stats/endpoint?permaslug={permaslug}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch stats for {permaslug}")
        return None

def process_and_save_csv(data, model_slug):
    rows = []
    for provider in data.get('data', []):
        if not isinstance(provider, dict):
            continue
        rows.append({
            'name': provider.get('name', 'N/A'),
            'max_completion_tokens': provider.get('max_completion_tokens', 'N/A'),
            'context_length': provider.get('context_length', 'N/A'),
            'pricing_prompt': provider.get('pricing', {}).get('prompt', 'N/A'),
            'pricing_completion': provider.get('pricing', {}).get('completion', 'N/A'),
            'p50_throughput': provider.get('stats', {}).get('p50_throughput', 'N/A'),
            'p50_latency': provider.get('stats', {}).get('p50_latency', 'N/A'),
        })

    if not rows:
        print(f"No data for {model_slug}, skipping CSV.")
        return

    df = pd.DataFrame(rows)
    filename = f"csv_output/{model_slug.replace('/', '_')}.csv"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    df.to_csv(filename, index=False)
    print(f"✅ Saved: {filename}")


def main():
    models = fetch_all_models()

    for model in models:
        permaslug = model.get('permaslug')
        if not permaslug:
            continue

        print(f"Processing model: {permaslug}")
        stats_data = fetch_model_provider_data(permaslug)
        if stats_data:
            process_and_save_csv(stats_data, permaslug)

if __name__ == "__main__":
    main()
