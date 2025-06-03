from typing import List, Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
import asyncio
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import logging


# Initialize FastAPI app
app = FastAPI()


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database file path
DB_FILE_PATH = "../syslogs.db"

# Pydantic Models
class Log(BaseModel):
    id: int
    timestamp: str
    source_ip: str
    severity: int
    log_message: str

class LogsResponse(BaseModel):
    logs: List[Log]

class MessageResponse(BaseModel):
    message: str

status_flag = False  # Change this to True or False to control the message

# Root endpoint
@app.get("/", response_model=MessageResponse)
def read_root():
    return {"message": "Welcome to the FastAPI syslog service."}

@app.post("/db_updated")
async def set_status_true():
    global status_flag
    status_flag = True
    return {"message": "status_flag set to True"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global status_flag
    await websocket.accept()
    try:
        while True:
            
            if status_flag:
                message = "Status is True"
                await websocket.send_text(message)
                status_flag = False  
            else:
                message = "Status is False"
                #await websocket.send_text(message)
            await asyncio.sleep(2)  # Send update every 2 seconds
    except WebSocketDisconnect:
        print("Client disconnected")

# Fetch all logs
@app.get("/logs", response_model=LogsResponse)
def read_logs():
    try:
        with sqlite3.connect(DB_FILE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, timestamp, source_ip, syslog_severity, log_message FROM logs")
            rows = cursor.fetchall()

        if not rows:
            raise HTTPException(status_code=404, detail="No logs found in the database.")

        logs = [Log(id=row[0], timestamp=row[1], source_ip=row[2], severity=row[3], log_message=row[4]) for row in rows]
        return {"logs": logs}

    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Fetch logs by severity
@app.get("/logs/severity/{level}", response_model=LogsResponse)
def filter_logs_by_severity(level: int):
    if level < 1 or level > 5:
        raise HTTPException(status_code=400, detail="Severity level must be between 1 and 5.")

    try:
        with sqlite3.connect(DB_FILE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, timestamp, source_ip, syslog_severity, log_message FROM logs WHERE syslog_severity = ?", (level,))
            rows = cursor.fetchall()

        if not rows:
            raise HTTPException(status_code=404, detail=f"No logs found with severity level {level}.")

        logs = [Log(id=row[0], timestamp=row[1], source_ip=row[2], severity=row[3], log_message=row[4]) for row in rows]
        return {"logs": logs}

    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Delete a log entry
@app.delete("/logs/{log_id}", response_model=MessageResponse)
def delete_log(log_id: int):
    try:
        with sqlite3.connect(DB_FILE_PATH) as conn:
            cursor = conn.cursor()

            # Check if log exists
            cursor.execute("SELECT * FROM logs WHERE id = ?", (log_id,))
            log = cursor.fetchone()

            if not log:
                raise HTTPException(status_code=404, detail=f"Log with ID {log_id} not found.")

            # Delete log
            cursor.execute("DELETE FROM logs WHERE id = ?", (log_id,))
            conn.commit()

        logger.info(f"Log {log_id} deleted successfully.")
        return {"message": f"Log with ID {log_id} deleted successfully."}

    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.delete("/clearlogs", response_model=MessageResponse)
def clear_logs():
    try:
        with sqlite3.connect(DB_FILE_PATH) as conn:
            cursor = conn.cursor()

            # Delete all logs
            cursor.execute("DELETE FROM logs")
            conn.commit()

        logger.info("All logs cleared successfully.")
        return MessageResponse(message="All logs cleared successfully.")

    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
