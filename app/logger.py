import json
import os

SUCCESS_LOG = "outputs/success_log.json"
FAILED_LOG = "outputs/failed_log.json"


def log_success(filename, route):

    log_data = {
        "file": filename,
        "status": "success",
        "route": route
    }

    logs = []

    if os.path.exists(SUCCESS_LOG):
        with open(SUCCESS_LOG, "r") as f:
            try:
                logs = json.load(f)
            except:
                logs = []

    logs.append(log_data)

    with open(SUCCESS_LOG, "w") as f:
        json.dump(logs, f, indent=4)


def log_failure(filename, reason):

    log_data = {
        "file": filename,
        "status": "failed",
        "reason": reason
    }

    logs = []

    if os.path.exists(FAILED_LOG):
        with open(FAILED_LOG, "r") as f:
            try:
                logs = json.load(f)
            except:
                logs = []

    logs.append(log_data)

    with open(FAILED_LOG, "w") as f:
        json.dump(logs, f, indent=4)