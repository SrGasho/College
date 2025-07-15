from typing import List
from datetime import date 
from fastapi import APIRouter

from crud.shipping import ShippingData, ShippingCRUD

router = APIRouter()
crud = ShippingCRUD()

@router.post("/shipping/create", response_model=int)
def create_shipping(data: ShippingData):
    """Creates a new shipping entry."""
    return crud.create(data)

@router.put("/shipping/update/{shipping_id}")
def update_shipping(shipping_id: int, data: ShippingData):
    """Updates an existing shipping entry."""
    return crud.update(shipping_id, data)

@router.delete("/shipping/delete/{shipping_id}")
def delete_shipping(shipping_id: int):
    """Deletes a shipping entry."""
    return crud.delete(shipping_id)

@router.get("/shipping/get_by_id/{shipping_id}", response_model=ShippingData)
def get_shipping_by_id(shipping_id: int):
    """Gets a shipping entry by ID."""
    return crud.get_by_id(shipping_id)

@router.get("/shipping/get_all", response_model=List[ShippingData])
def get_all_shipping():
    """Gets all shipping entries."""
    return crud.get_all()

@router.get("/shipping/get_by_shipping_company/{shipping_company}", response_model=List[ShippingData])
def get_shipping_by_shipping_company(shipping_company: str):
    """Gets all shipping entries."""
    return crud.get_by_shipping_company(shipping_company)

@router.get("/shipping/get_by_shipping_date/{shipping_date}", response_model=List[ShippingData])
def get_shipping_by_shipping_date(shipping_date: date):
    """Gets all shipping entries."""
    return crud.get_by_shipping_date(shipping_date)