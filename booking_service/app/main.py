# Initialize the FastAPI application.
# Create and manage database tables.
# Define endpoints for the booking service.

import crud, models, schemas, database
from database import engine, SessionLocal
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.responses import StreamingResponse
import io
from sqlalchemy.orm import Session
import requests
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import json
from pydantic import BaseModel
from datetime import datetime

class Booking(BaseModel):
    booking_id: int
    customer_name: str
    flight_number: str
    seat_number: str
    flight_id: int
    booking_time: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# Create the database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Initialize S3 client
s3_client = boto3.client('s3', region_name='us-east-2')

# Initialize SQS client
sqs_client = boto3.client('sqs', region_name='us-east-2')

# bucket name
BUCKET_NAME = 'my-enhanced-project-bucket'
# SQS queue URL (replace with your queue URL)
QUEUE_URL = 'https://sqs.us-east-2.amazonaws.com/767397896582/MyQueue.fifo'

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Interact with the Flight Management Service
def get_flight_details(flight_id: int):
    response = requests.get(f"http://flight_management_service:80/flights/{flight_id}")
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Flight not found")
    
# Function that removes available seats (via flight_number) by -1 once user has a confirmed booking (via bookings/ POST request)
def decrement_flight_seats(flight_details):
    if flight_details["total_seats"] > 0:
        flight_details["total_seats"] -= 1
        return flight_details["total_seats"]
    else:
        raise HTTPException(status_code=400, detail="No seats available")
    




# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Booking Service"} # returns message to user when user hits homepage

# upload file to S3 bucket
@app.post("/upload/{booking_id}")
async def upload_file(booking_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Ensure booking exists
        booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        # Upload file to S3
        s3_client.upload_fileobj(file.file, BUCKET_NAME, file.filename)
        
        # could save file to database?
        
        return {"filename": file.filename}
    except Exception as e:
        return {"error": str(e)}

# download file from S3 bucket
@app.get("/download/{filename}")
async def download_file(filename: str):
    try:
        # Download the file from S3
        s3_response = s3_client.get_object(Bucket=BUCKET_NAME, Key=filename)
        file_stream = io.BytesIO(s3_response['Body'].read())
        return StreamingResponse(file_stream, media_type='application/octet-stream', headers={'Content-Disposition': f'attachment; filename={filename}'})
    except Exception as e:
        return {"error": str(e)}


# Create a new booking and decrement available seats by -1 (include in response json)
@app.post("/bookings/", response_model=schemas.BookingResponse)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(database.get_db)):
    try:
        flight_details = get_flight_details(booking.flight_id)
        remaining_seats = decrement_flight_seats(flight_details)
        created_booking = crud.create_booking(db=db, booking=booking)
        
        # Send message to SQS
        message = {
            "booking_id": created_booking.id,
            "customer_name": created_booking.customer_name,
            "flight_number": created_booking.flight_number,
            "seat_number": created_booking.seat_number,
            "flight_id": created_booking.flight_id,
            "booking_time": str(created_booking.booking_time)
        }
        # Convert the booking to a dictionary and handle datetime serialization
        booking_dict = booking.dict(by_alias=True)
        booking_dict['booking_time'] = booking.booking_time.isoformat()

        # Send the booking message to the SQS queue
        response = sqs_client.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(booking_dict),  # Ensure the message is properly formatted as JSON
            MessageGroupId='booking_group',  # Required for FIFO queues
            MessageDeduplicationId=str(booking.booking_id)  # Use a unique identifier for deduplication
        )
        print(f"Message sent to SQS: {response['MessageId']}")
        
        
        return {
            "id": created_booking.id,
            "customer_name": created_booking.customer_name,
            "flight_number": created_booking.flight_number,
            "seat_number": created_booking.seat_number,
            "flight_id": created_booking.flight_id,
            "booking_time": created_booking.booking_time,
            "remaining_seats": remaining_seats
        }
    except Exception as e:
        print(f"Error: {e}")  # Log the error for debugging
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Read a booking by ID
@app.get("/bookings/{booking_id}", response_model=schemas.BookingBase)
def read_booking(booking_id: int, db: Session = Depends(get_db)):
    db_booking = crud.get_booking(db, booking_id=booking_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_booking
