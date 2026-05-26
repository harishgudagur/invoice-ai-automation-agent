import csv
import os


CSV_FILE = "invoice_sheet.csv"
SLACK_FILE = "slack_mock/slack_messages.txt"
HUMAN_REVIEW_FILE = "outputs/human_review.log"


def route_invoice(data, filename):

    document_type = data.get(
        "document_type",
        "unknown"
    )

    total = data.get(
        "total_amount",
        0
    )

    vendor = data.get(
        "vendor_name",
        ""
    )

    invoice_number = data.get(
        "invoice_number",
        ""
    )

    # Human review routing
    if (
        document_type == "unknown"
        or not vendor
        or not invoice_number
    ):

        with open(
            HUMAN_REVIEW_FILE,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(
                f"{filename} -> Human Review Required\n"
            )

        return "human_review"

    # High-value invoice
    if total > 50000:

        slack_message = f"""
HIGH VALUE INVOICE

Vendor: {vendor}
Invoice: {invoice_number}
Amount: ₹{total}
Date: {data.get('date')}
"""

        with open(
            SLACK_FILE,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(slack_message)
            f.write(
                "\n" + "=" * 50 + "\n"
            )

        return "slack"

    # CSV Routing
    file_exists = os.path.exists(
        CSV_FILE
    )

    with open(
        CSV_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as csvfile:

        writer = csv.writer(
            csvfile
        )

        if not file_exists:

            writer.writerow([
                "Vendor",
                "Invoice Number",
                "Date",
                "Amount",
                "Type"
            ])

        writer.writerow([
            vendor,
            invoice_number,
            data.get("date"),
            total,
            document_type
        ])

    return "csv"