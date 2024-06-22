# Initialize the FastAPI application.
# Create the database tables.
# Define the API endpoints for creating and retrieving payments.

import boto3
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

# Initialize the FastAPI application
app = FastAPI()

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('Payments')

class PaymentCreate(BaseModel):
    payment_id: str
    amount: float
    status: str

class Payment(PaymentCreate):
    pass

# Endpoint to create a payment
@app.post("/payments/", response_model=Payment)
def create_payment(payment: PaymentCreate):
    try:
        table.put_item(
            Item={
                'payment_id': payment.payment_id,
                'amount': payment.amount,
                'status': payment.status
            }
        )
        return payment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to read a payment by ID
@app.get("/payments/{payment_id}", response_model=Payment)
def read_payment(payment_id: str):
    try:
        response = table.get_item(Key={'payment_id': payment_id})
        if 'Item' in response:
            return response['Item']
        else:
            raise HTTPException(status_code=404, detail="Payment not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
