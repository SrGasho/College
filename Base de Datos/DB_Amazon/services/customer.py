from typing import List
from fastapi import APIRouter
from crud.customer import CustomerData, CustomerCRUD

router = APIRouter()
crud = CustomerCRUD()

@router.post("/customer/create", response_model=int)
def create_customer(data: CustomerData):
    """Creates a new customer."""
    return crud.create(data)

@router.put("/customer/update/{customer_id}")
def update_customer(customer_id: int, data: CustomerData):
    """Updates an existing customer."""
    return crud.update(customer_id, data)

@router.delete("/customer/delete/{customer_id}")
def delete_customer(customer_id: int):
    """Deletes a customer."""
    return crud.delete(customer_id)

@router.get("/customer/get_by_id/{customer_id}", response_model=CustomerData)
def get_customer_by_id(customer_id: int):
    """Gets a customer by ID."""
    return crud.get_by_id(customer_id)

@router.get("/customer/get_all", response_model=List[CustomerData])
def get_all_customers():
    """Gets all customers."""
    return crud.get_all()

@router.get("/customer/get_by_email/{email}", response_model=CustomerData)
def get_customer_by_email(email: str):
    """Gets a customer by email."""
    return crud.get_by_email(email)

@router.get("/customer/get_by_name/{full_name}", response_model=List[CustomerData])
def get_customer_by_name(full_name: str):
    """Gets customers by name."""
    return crud.get_by_name(full_name)