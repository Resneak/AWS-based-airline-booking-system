# Initialize the FastAPI application.
# Create the database tables.
# Define the API endpoints for creating and retrieving payments.

import crud, models, schemas, database
from database import engine
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import boto3
import uuid

# Initialize the FastAPI application
app = FastAPI()

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('Payments')

# Endpoint to create a payment
@app.post("/payments/", response_model=schemas.Payment)
def create_payment(payment: schemas.PaymentCreate):
    try:
        payment_id = str(uuid.uuid4())
        table.put_item(
            Item={
                'payment_id': payment_id,
                'amount': payment.amount,
                'currency': payment.currency,
                'status': payment.status,
                'payment_method': payment.payment_method
            }
        )
        return {
            'payment_id': payment_id,
            'amount': payment.amount,
            'currency': payment.currency,
            'status': payment.status,
            'payment_method': payment.payment_method
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to read a payment by ID
@app.get("/payments/{payment_id}", response_model=schemas.Payment)
def read_payment(payment_id: str):
    try:
        response = table.get_item(Key={'payment_id': payment_id})
        item = response.get('Item')
        if not item:
            raise HTTPException(status_code=404, detail="Payment not found")
        return item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
