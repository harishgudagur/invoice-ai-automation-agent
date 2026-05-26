from fastapi import FastAPI
import subprocess

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Invoice AI Automation Pipeline Running"
    }


@app.get("/run-pipeline")
def run_pipeline():

    result = subprocess.run(
        ["python", "run.py"],
        capture_output=True,
        text=True
    )

    return {
        "status": "completed",
        "output": result.stdout
    }