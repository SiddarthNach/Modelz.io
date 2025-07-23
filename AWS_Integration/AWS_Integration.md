# ⚙️ Automated Data Pipeline for LLM Model Inference Data

This repository contains the code for an automated data pipeline that ingests, processes, and stores inference metadata from external model providers (e.g., OpenRouter). The system is designed to be **serverless, scalable**, and **resilient**, using **AWS Lambda** and **DynamoDB**, with Python handling orchestration.

## 🧪 Motivation

The goal of this project was to build a fully automated, cloud-native system to collect and persist inference metadata with minimal manual intervention. Along the way, I faced several challenges that led to deeper understanding of serverless architectures and data integrity in distributed systems.

## 🛠️ Tech Stack

- **AWS Lambda** – Serverless compute to handle scraping and data ingestion  
- **AWS DynamoDB** – NoSQL database for fast, scalable, and low-latency data storage  
- **boto3** – AWS SDK for Python to interact with DynamoDB  
- **Python 3.9+** – Core scripting and logic implementation  
- **Requests** – To interact with external HTTP APIs  
- **uuid / datetime / decimal** – For ID generation and type-safe storage in DynamoDB

## 🔁 Pipeline Workflow

1. **Lambda function** fetches inference data from provider APIs (e.g., OpenRouter).
2. The data is **cleaned and normalized**, ensuring proper typing and formatting.
3. The cleaned data is **stored directly in DynamoDB**, using a carefully structured key to avoid duplication.

## ⚠️ Challenges Faced

### 🧯 Duplicate Key Handling
Ran into `ConditionalCheckFailedException` due to duplicate entries in DynamoDB. Resolved by:
- Designing a composite primary key using a `uuid` and timestamp fields
- Implementing idempotent write logic

### 🔢 Type Conversion
Faced serialization issues when dealing with:
- Floats (converted to `Decimal`)
- `datetime` objects
- Nested JSON needing precise typing for DynamoDB

### 🧵 Error Handling & Idempotency
Ensured:
- Graceful handling of API errors
- Retry-safe logic to prevent overwriting or duplicate records

### 🧊 Lambda Cold Starts
Tuned memory and timeout settings to:
- Minimize latency
- Handle high-frequency scraping more efficiently

## 📈 Future Improvements

- [ ] Integrate logging and alerting via **CloudWatch**
- [ ] Schedule scraping intervals using **CloudWatch Events** or **EventBridge**
- [ ] Add local testing with **moto** or **localstack**
- [ ] Explore batch ingestion optimizations

---

## 📂 Folder Structure

