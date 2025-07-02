import csv

def parse_cost(dollar_str):
    return float(dollar_str.replace("$", ""))

def parse_tokens(token_str):
    token_str = token_str.upper()
    if token_str.endswith("T"):
        return float(token_str[:-1]) * 1_000_000_000_000
    elif token_str.endswith("B"):
        return float(token_str[:-1]) * 1_000_000_000
    return float(token_str)

models = [
    {
        "model_name": "Google: Gemini 2.0 Flash",
        "tokens": 1048576,
        "input_tokens_cost": "$0.10",
        "output_tokens_cost": "$0.40",
        "total_tokens_used": "1.15T",
    },
    {
        "model_name": "Anthropic: Claude Sonnet 4",
        "tokens": 200000,
        "input_tokens_cost": "$3",
        "output_tokens_cost": "$15",
        "total_tokens_used": "1.04T",
    },
    {
        "model_name": "Google: Gemini 2.5 Flash Preview 05-20",
        "tokens": 1048576,
        "input_tokens_cost": "$0.15",
        "output_tokens_cost": "$0.60",
        "total_tokens_used": "676B",
    },
    {
        "model_name": "DeepSeek: DeepSeek V3 0324 (free)",
        "tokens": 163840,
        "input_tokens_cost": "$0.0",
        "output_tokens_cost": "$0.0",
        "total_tokens_used": "529B",
    },
    {
        "model_name": "OpenAI: GPT-4o-mini",
        "tokens": 128000,
        "input_tokens_cost": "$0.15",
        "output_tokens_cost": "$0.60",
        "total_tokens_used": "518B",
    },
    {
        "model_name": "DeepSeek: DeepSeek V3 0324",
        "tokens": 163840,
        "input_tokens_cost": "$0.28",
        "output_tokens_cost": "$0.88",
        "total_tokens_used": "472B",
    },
    {
        "model_name": "Anthropic: Claude 3.7 Sonnet",
        "tokens": 200000,
        "input_tokens_cost": "$3",
        "output_tokens_cost": "$15",
        "total_tokens_used": "471B",
    },
    {
        "model_name": "Google: Gemini 2.5 Pro",
        "tokens": 1048576,
        "input_tokens_cost": "$1.25",
        "output_tokens_cost": "$10.0",
        "total_tokens_used": "319B",
    },
    {
        "model_name": "Google: Gemini 2.0 Flash Lite",
        "tokens": 1048576,
        "input_tokens_cost": "$0.075",
        "output_tokens_cost": "$0.30",
        "total_tokens_used": "292B",
    },
    {
        "model_name": "Google: Gemini 2.5 Flash Preview 04-17",
        "tokens": 1048576,
        "input_tokens_cost": "$0.15",
        "output_tokens_cost": "$0.60",
        "total_tokens_used": "258B",
    },
    {
        "model_name": "DeepSeek: R1 0528 (free)",
        "tokens": 163840,
        "input_tokens_cost": "$0.0",
        "output_tokens_cost": "$0.0",
        "total_tokens_used": "218B",
    },
    {
        "model_name": "Mistral: Mistral Nemo",
        "tokens": 131072,
        "input_tokens_cost": "$0.01",
        "output_tokens_cost": "$0.011",
        "total_tokens_used": "154B",
    },
    {
        "model_name": "OpenAI: GPT-4.1",
        "tokens": 1047576,
        "input_tokens_cost": "$2",
        "output_tokens_cost": "$8",
        "total_tokens_used": "147B",
    },
    {
        "model_name": "Google: Gemini 2.5 Flash",
        "tokens": 1048576,
        "input_tokens_cost": "$0.30",
        "output_tokens_cost": "$2.50",
        "total_tokens_used": "144B",
    },
    {
        "model_name": "Google: Gemini 2.5 Flash Lite Preview 06-17",
        "tokens": 1048576,
        "input_tokens_cost": "$0.10",
        "output_tokens_cost": "$0.40",
        "total_tokens_used": "142B",
    },
    {
        "model_name": "DeepSeek: R1 (free)",
        "tokens": 163840,
        "input_tokens_cost": "$0.0",
        "output_tokens_cost": "$0.0",
        "total_tokens_used": "135B",
    },
    {
        "model_name": "OpenAI: GPT-4.1 Mini",
        "tokens": 1047576,
        "input_tokens_cost": "$0.40",
        "output_tokens_cost": "$1.60",
        "total_tokens_used": "123B",
    },
    {
        "model_name": "Meta: Llama 3.3 70B Instruct",
        "tokens": 131072,
        "input_tokens_cost": "$0.039",
        "output_tokens_cost": "$0.12",
        "total_tokens_used": "119B",
    },
]

csv_filename = "llm_models_month.csv"

with open(csv_filename, mode="w", newline="") as csv_file:
    fieldnames = [
        "model_name", "tokens", "input_tokens_cost", "output_tokens_cost",
        "total_tokens_used", "usd_per_million_tokens", "usd_spent"
    ]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    csv_file.write("# Top models over month of June\n")
    writer.writeheader()

    for model in models:
        input_cost = parse_cost(model["input_tokens_cost"])
        output_cost = parse_cost(model["output_tokens_cost"])
        total_tokens = parse_tokens(model["total_tokens_used"])
        
        usd_per_million = input_cost + output_cost
        usd_spent = usd_per_million * (total_tokens / 1_000_000)

        model["usd_per_million_tokens"] = f"${usd_per_million:.4f}"
        model["usd_spent"] = f"${usd_spent:,.2f}"

        writer.writerow(model)

print(f"CSV file '{csv_filename}' created successfully.")
