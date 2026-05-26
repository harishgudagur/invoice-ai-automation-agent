import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

URL = "https://openrouter.ai/api/v1/chat/completions"


def extract_invoice_data(document_text):

    prompt = f"""
You are an invoice extraction system.

Analyze the invoice carefully.

Classify document into ONLY:

1. standard_invoice
2. credit_note
3. unknown

Extract:

- vendor_name
- invoice_number
- date
- line_items
- total_amount

IMPORTANT RULES:

1. Return ONLY valid JSON
2. No markdown
3. No explanation
4. If document is incomplete, unreadable, or messy -> unknown
5. Prefer FINAL PAYABLE amount
6. Use Net Payable over subtotal
7. If invoice number or vendor missing -> unknown
8. Extract line items properly

Return JSON in this exact format:

{{
    "document_type": "",
    "vendor_name": "",
    "invoice_number": "",
    "date": "",
    "line_items": [],
    "total_amount": 0
}}

Invoice text:

{document_text}
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # fallback models
    models = [
        "openai/gpt-oss-20b:free",
        "qwen/qwen-2.5-72b-instruct:free",
        "deepseek/deepseek-r1:free"
    ]

    for model in models:

        for retry in range(3):

            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }

            try:

                print(f"\nTrying model: {model}")

                response = requests.post(
                    URL,
                    headers=headers,
                    json=payload,
                    timeout=60
                )

                result = response.json()

                # success case
                if "choices" in result:
                    return result["choices"][0]["message"]["content"]

                # failed provider
                print(
                    f"Model failed: {result}"
                )

                wait_time = 5 * (retry + 1)

                print(
                    f"Retrying in {wait_time} sec..."
                )

                time.sleep(wait_time)

            except Exception as e:

                print(
                    f"Retry failed: {str(e)}"
                )

    raise Exception(
        "All LLM providers failed"
    )