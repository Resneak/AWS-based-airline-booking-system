# Initialize the FastAPI application.
# Create the database tables.
# Define the API endpoints for creating and retrieving notifications.

import crud, models, schemas, database
from database import engine, SessionLocal
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import boto3
import json
import time
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Create the database tables
models.Base.metadata.create_all(bind=engine)

# Initialize the FastAPI application
app = FastAPI()

# Initialize the SQS client
sqs_client = boto3.client('sqs')

# SQS queue URL
QUEUE_URL = 'https://sqs.us-east-2.amazonaws.com/767397896582/MyQueue.fifo'

# Function to process messages from the SQS queue
def process_messages():
    while True:
        response = sqs_client.receive_message(
            QueueUrl=QUEUE_URL,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10
        )

        messages = response.get('Messages', [])
        for message in messages:
            body = json.loads(message['Body'])
            print(f"Received message: {body}")

            # just print out whatever is in sqs, could send out emails/sms from here
            send_notification(body)

            sqs_client.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=message['ReceiptHandle']
            )

        time.sleep(5)

# Example function to send a notification (e.g., email, SMS)
def send_notification(message):
    # Implement your notification logic here
    print(f"Sending notification for booking ID: {message['booking_id']}")

# Endpoint to create a notification
@app.post("/notifications/", response_model=schemas.Notification)
def create_notification(notification: schemas.NotificationCreate, db: Session = Depends(database.get_db)):
    return crud.create_notification(db=db, notification=notification)

# Endpoint to read a notification by ID
@app.get("/notifications/{notification_id}", response_model=schemas.Notification)
def read_notification(notification_id: int, db: Session = Depends(database.get_db)):
    db_notification = crud.get_notification(db, notification_id=notification_id)
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return db_notification

if __name__ == "__main__":
    # Start processing messages from the SQS queue
    process_messages()

