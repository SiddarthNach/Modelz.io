import requests
from supabase import create_client
import apis  

url = "https://fidoxszrgnzwutnpkekr.supabase.co"
key = apis.supabase_key
supabase = create_client(url, key)

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

def process_and_insert_supabase(data, model_slug):
    rows = []
    for provider in data.get('data', []):
        if not isinstance(provider, dict):
            continue
        row = {
            'provider_name': provider.get('name', 'N/A'),
            'model_slug': model_slug,
            'max_completion_tokens': provider.get('max_completion_tokens', None),
            'context_length': provider.get('context_length', None),
            'pricing_prompt': provider.get('pricing', {}).get('prompt', None),
            'pricing_completion': provider.get('pricing', {}).get('completion', None),
            'p50_throughput': provider.get('stats', {}).get('p50_throughput', None),
            'p50_latency': provider.get('stats', {}).get('p50_latency', None),
        }
        rows.append(row)

    if not rows:
        print(f"No data to insert for {model_slug}")
        return

    response = supabase.table("model_metadata").insert(rows).execute()

    if response.data:
        print(f"✅ Inserted data for model: {model_slug}")
    else:
        print(f"❌ Failed to insert data for {model_slug}")

def main():
    models = fetch_all_models()

    for model in models:
        permaslug = model.get('permaslug')
        if not permaslug:
            continue

        print(f"Processing model: {permaslug}")
        stats_data = fetch_model_provider_data(permaslug)
        if stats_data:
            process_and_insert_supabase(stats_data, permaslug)

if __name__ == "__main__":
    main()
