from app.parser import parse_document
from app.extractor import extract_invoice_data
from app.validator import validate_llm_output

file_path = "sample_docs/inv_001.pdf"

text = parse_document(file_path)

print("\nTEXT EXTRACTED:\n")
print(text[:1000])

response = extract_invoice_data(text)

print("\nRAW GEMINI RESPONSE:\n")
print(response)

validated = validate_llm_output(response)

print("\nFINAL JSON:\n")
print(validated)