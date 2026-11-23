
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Literal
from pathlib import Path
from uuid import uuid4

from database import create_table
from alert_engine import save_alert
from alert_service import (
    get_all_alerts,
    get_alert_by_id,
    update_alert_status
)
from detection_service import analyze_record
from dataset_service import inspect_dataset


app = FastAPI(
    title="AI Network Intrusion Detection System",
    description="Dataset-Based Network Threat Analysis Platform",
    version="1.0"
)


# Initialize database

@app.on_event("startup")
def startup():
    create_table()


# Request models

class AlertInput(BaseModel):
    attack_type: str
    severity: Literal["Low", "Medium", "High"]
    score: int
    reason: str
    record_index: int | None = None


class StatusInput(BaseModel):
    status: Literal[
        "New",
        "Investigating",
        "Resolved",
        "False Positive"
    ]


class RecordInput(BaseModel):
    record: dict[str, float]
    record_index: int | None = None


# Home

@app.get("/")
def home():
    return {
        "message": "Intrusion Detection Backend is running"
    }


# Health check

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Intrusion Detection Backend"
    }


# Create alert

@app.post("/alerts")
def create_alert(alert: AlertInput):

    alert_id = save_alert(
        alert.dict(exclude={"record_index"}),
        alert.record_index
    )

    return {
        "message": "Alert created successfully",
        "alert_id": alert_id
    }


# Get all alerts

@app.get("/alerts")
def list_alerts():

    alerts = get_all_alerts()

    return {
        "total": len(alerts),
        "alerts": alerts
    }


# Get alert by ID

@app.get("/alerts/{alert_id}")
def alert_details(alert_id: int):

    alert = get_alert_by_id(alert_id)

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    return alert


# Update alert status

@app.patch("/alerts/{alert_id}/status")
def change_alert_status(
    alert_id: int,
    data: StatusInput
):

    updated = update_alert_status(
        alert_id,
        data.status
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    return {
        "message": "Alert status updated",
        "alert_id": alert_id,
        "status": data.status
    }


# Dashboard statistics

@app.get("/stats")
def get_statistics():

    alerts = get_all_alerts()

    return {
        "total_alerts": len(alerts),
        "high": sum(a["severity"] == "High" for a in alerts),
        "medium": sum(a["severity"] == "Medium" for a in alerts),
        "low": sum(a["severity"] == "Low" for a in alerts),
        "new": sum(a["status"] == "New" for a in alerts),
        "resolved": sum(a["status"] == "Resolved" for a in alerts)
    }


# Analyze a single network record

@app.post("/analyze-record")
def analyze_network_record(data: RecordInput):

    result = analyze_record(
        data.record,
        data.record_index
    )

    return {
        "message": "Record analysis completed",
        "result": result
    }


# Upload and inspect CSV dataset

@app.post("/dataset/upload")
async def upload_dataset(file: UploadFile = File(...)):

    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed"
        )

    data_directory = Path("data")
    data_directory.mkdir(exist_ok=True)

    file_path = data_directory / f"{uuid4().hex}.csv"

    max_size = 50 * 1024 * 1024
    total_size = 0

    try:
        with file_path.open("wb") as destination:

            while True:
                chunk = await file.read(1024 * 1024)

                if not chunk:
                    break

                total_size += len(chunk)

                if total_size > max_size:
                    raise HTTPException(
                        status_code=413,
                        detail="CSV file exceeds 50 MB limit"
                    )

                destination.write(chunk)

        if total_size == 0:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty"
            )

        summary = inspect_dataset(file_path)

        return {
            "message": "Dataset uploaded successfully",
            "filename": file.filename,
            "dataset_summary": summary
        }

    except HTTPException:
        file_path.unlink(missing_ok=True)
        raise

    except (ValueError, UnicodeDecodeError) as error:
        file_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=400,
            detail=f"Invalid CSV file: {error}"
        )

    except Exception:
        file_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=500,
            detail="Dataset processing failed"
        )

    finally:
        await file.close()
