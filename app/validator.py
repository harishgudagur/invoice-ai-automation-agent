import json


def validate_llm_output(response_text):
    """
    Validate Gemini response.
    Retry-safe JSON parsing.
    """

    try:
        cleaned = (
            response_text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        parsed = json.loads(cleaned)

        required_fields = [
            "document_type",
            "vendor_name",
            "invoice_number",
            "date",
            "line_items",
            "total_amount"
        ]

        for field in required_fields:
            if field not in parsed:
                raise Exception(f"Missing field: {field}")

        return parsed

    except Exception as e:
        raise Exception(f"Invalid JSON Output: {str(e)}")