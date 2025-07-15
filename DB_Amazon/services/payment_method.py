from typing import List, Optional

from fastapi import APIRouter, HTTPException, status

from crud.payment_method import PaymentMethodData, PaymentMethodCRUD

router = APIRouter()
crud = PaymentMethodCRUD()

@router.post("/payment_method/", status_code=status.HTTP_201_CREATED, response_model=int)  # POST a /payment_method/
def create_payment_method(data: PaymentMethodData):
    """Creates a new payment method."""
    payment_method_id = crud.create(data)
    if payment_method_id is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create payment method")
    return payment_method_id

@router.get("/payment_method/{payment_method_id}", response_model=PaymentMethodData)  # GET a /payment_method/{id}
def get_payment_method_by_id(payment_method_id: int):
    """Gets a payment method by ID."""
    payment_method = crud.get_by_id(payment_method_id)
    if payment_method is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment method not found")
    return payment_method

@router.get("/payment_method/", response_model=List[PaymentMethodData])  # GET a /payment_method/
def get_all_payment_methods():
    """Gets all payment methods."""
    return crud.get_all()

@router.get("/payment_method/customer/{customer_id}", response_model=List[PaymentMethodData])  # GET a /payment_method/customer/{id}
def get_payment_methods_by_customer(customer_id: int):
    """Gets payment methods for a specific customer."""
    return crud.get_by_customer(customer_id)

@router.put("/payment_method/update/{payment_method_id}")  # PUT a /payment_method/{id}
def update_payment_method(payment_method_id: int, data: PaymentMethodData):
    """Updates an existing payment method."""
    if not crud.update(payment_method_id, data):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update payment method")
    return {"message": "Payment method updated"}

@router.delete("/payment_method/{payment_method_id}")  # DELETE a /payment_method/{id}
def delete_payment_method(payment_method_id: int):
    """Deletes a payment method."""
    if not crud.delete(payment_method_id):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete payment method")
    return {"message": "Payment method deleted"}
