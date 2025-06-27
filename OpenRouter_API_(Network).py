import requests
import json

url = "https://openrouter.ai/api/frontend/stats/endpoint?permaslug=deepseek%2Fdeepseek-chat-v3-0324"

response = requests.get(url)
if response.status_code == 200:
    data = response.json()

    with open('output.json', 'w') as f:
        json.dump(data, f, indent=2)
    print("Saved full JSON to output.json")

    providers = data.get('data', [])

    for provider in providers:
        if not isinstance(provider, dict):
            continue  

        name = provider.get('name', 'N/A')
        max_completion_tokens = provider.get('max_completion_tokens', 'N/A')
        context_length = provider.get('context_length', 'N/A')
        pricing_prompt = provider.get('pricing', {}).get('prompt', 'N/A')
        pricing_completion = provider.get('pricing', {}).get('completion', 'N/A')
        p50_throughput = provider.get('stats', {}).get('p50_throughput', 'N/A')
        p50_latency = provider.get('stats', {}).get('p50_latency', 'N/A')

        print(f"Provider: {name}")
        print(f"  Max Completion Tokens: {max_completion_tokens}")
        print(f"  Context Length: {context_length}")
        print(f"  Pricing - Prompt: {pricing_prompt}")
        print(f"  Pricing - Completion: {pricing_completion}")
        print(f"  Throughput: {p50_throughput}")
        print(f"  Latency: {p50_latency}")
        print("-" * 40)

else:
    print("❌ Failed to fetch data")

