from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import random
from typing import Dict

router = APIRouter(
    prefix="/upi",
    tags=["upi"]
)

class PaymentRequest(BaseModel):
    """
    Request model for initiating a UPI payment.
    
    Attributes:
        payer_vpa: Virtual Payment Address (VPA) of the payer
        payee_vpa: Virtual Payment Address (VPA) of the payee
        amount: Payment amount in INR
        transaction_note: Optional note for the transaction
    """
    payer_vpa: str
    payee_vpa: str
    amount: float
    transaction_note: str = None

class PaymentStatusResponse(BaseModel):
    """
    Response model for payment status.
    
    Attributes:
        transaction_id: Unique transaction identifier
        status: Current payment status (PENDING, SUCCESS, FAILED)
        message: Additional information about the transaction
    """
    transaction_id: str
    status: str
    message: str = None

# Mock database for transactions
transactions_db: Dict[str, str] = {}

@router.post(
    "/payment",
    response_model=PaymentStatusResponse,
    summary="Initiate a UPI payment",
    description="""
    Initiates a new UPI payment transaction between two parties.
    
    This endpoint creates a new payment transaction with the provided details and returns
    a transaction ID that can be used to track the payment status.
    
    **Example Request:**
    ```json
    {
        "payer_vpa": "user@upi",
        "payee_vpa": "merchant@upi",
        "amount": 100.50,
        "transaction_note": "Payment for services"
    }
    ```
    
    **Example Response:**
    ```json
    {
        "transaction_id": "TXN000001",
        "status": "PENDING",
        "message": "Payment initiated successfully"
    }
    ```
    """,
    response_description="Payment initiation response with transaction details"
)
async def initiate_payment(payment: PaymentRequest):
    """
    Initiate a new UPI payment transaction.
    
    Args:
        payment: PaymentRequest object containing payment details
        
    Returns:
        PaymentStatusResponse: Response containing transaction ID and initial status
        
    Raises:
        HTTPException: If payment initiation fails
    """
    # Mock implementation: generate a transaction ID and store status
    transaction_id = f"TXN{len(transactions_db) + 1:06d}"
    transactions_db[transaction_id] = "PENDING"
    return PaymentStatusResponse(
        transaction_id=transaction_id,
        status="PENDING",
        message="Payment initiated successfully"
    )

@router.get(
    "/status/{transaction_id}",
    response_model=PaymentStatusResponse,
    summary="Get payment status",
    description="""
    Retrieves the current status of a UPI payment transaction.
    
    This endpoint allows you to check the status of a previously initiated payment
    using the transaction ID returned from the payment initiation endpoint.
    
    **Example Response:**
    ```json
    {
        "transaction_id": "TXN000001",
        "status": "SUCCESS",
        "message": "Transaction status retrieved successfully"
    }
    ```
    
    **Possible Status Values:**
    - `PENDING`: Payment is being processed
    - `SUCCESS`: Payment completed successfully
    - `FAILED`: Payment failed
    """,
    response_description="Current payment status and transaction details"
)
async def get_payment_status(transaction_id: str):
    """
    Get the current status of a payment transaction.
    
    Args:
        transaction_id: Unique transaction identifier
        
    Returns:
        PaymentStatusResponse: Response containing current transaction status
        
    Raises:
        HTTPException: If transaction ID is not found
    """
    status = transactions_db.get(transaction_id)
    if not status:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    # Simulate status update
    if status == "PENDING":
        new_status = random.choice(["SUCCESS", "FAILED"])
        transactions_db[transaction_id] = new_status
        status = new_status
    
    return PaymentStatusResponse(
        transaction_id=transaction_id,
        status=status,
        message="Transaction status retrieved successfully"
    )
