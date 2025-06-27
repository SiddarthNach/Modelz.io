import json
import pandas as pd

def json_to_csv(json_file='output.json', csv_file='providers.csv'):
    with open(json_file, 'r') as f:
        data = json.load(f)

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

    df = pd.DataFrame(rows)
    df.to_csv(csv_file, index=False)
    print(f"Saved CSV data to {csv_file}")

if __name__ == "__main__":
    json_to_csv()
