import os
import json

from app.parser import parse_document
from app.extractor import extract_invoice_data
from app.validator import validate_llm_output
from app.router import route_invoice
from app.logger import (
    log_success,
    log_failure
)
from app.acknowledgement import (
    send_acknowledgement
)

SAMPLE_FOLDER = "sample_docs"
OUTPUT_FOLDER = "outputs/extracted_json"


def process_document(file_path):

    filename = os.path.basename(file_path)

    print("\n" + "=" * 60)
    print(f"Processing: {filename}")
    print("=" * 60)

    try:
        # Step 1: Parse document
        text = parse_document(file_path)

        # Step 2: LLM extraction
        raw_response = extract_invoice_data(text)

        # Step 3: Validate JSON
        validated_data = validate_llm_output(
            raw_response
        )

        # Step 4: Save JSON output
        output_file = os.path.join(
            OUTPUT_FOLDER,
            filename.replace(".pdf", ".json")
            .replace(".jpg", ".json")
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                validated_data,
                f,
                indent=4,
                ensure_ascii=False
            )

        # Step 5: Route invoice
        route = route_invoice(
            validated_data,
            filename
        )

        # Handle human review
        if route == "human_review":

            log_success(
                filename,
                "human_review"
            )

            print(
                f"HUMAN REVIEW: {filename}"
            )

            return

        # Step 6: Success log
        log_success(
            filename,
            route
        )

        # Step 7: Send acknowledgement
        send_acknowledgement(
            validated_data.get(
                "vendor_name",
                "Unknown Vendor"
            ),
            validated_data.get(
                "invoice_number",
                "N/A"
            ),
            "Processed Successfully"
        )

        print(
            f"SUCCESS: {filename}"
        )

    except Exception as e:

        reason = str(e)

        log_failure(
            filename,
            reason
        )

        print(
            f"FAILED: {filename}"
        )
        print(
            f"Reason: {reason}"
        )


def main():

    files = os.listdir(
        SAMPLE_FOLDER
    )

    supported_extensions = (
        ".pdf",
        ".jpg",
        ".jpeg",
        ".png"
    )

    invoice_files = [
        file for file in files
        if file.lower().endswith(
            supported_extensions
        )
    ]

    print(
        f"\nFound {len(invoice_files)} invoices\n"
    )

    for file in invoice_files:

        file_path = os.path.join(
            SAMPLE_FOLDER,
            file
        )

        process_document(
            file_path
        )

    print("\nDONE")
    print(
        "Check outputs folder"
    )


if __name__ == "__main__":
    main()