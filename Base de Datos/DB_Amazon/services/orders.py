from typing import List

from fastapi import APIRouter

from crud.orders import OrdersData, OrdersCRUD

router = APIRouter()
crud = OrdersCRUD()

@router.post("/orders/create", response_model=int)
def create_order(data: OrdersData):
    """Creates a new order."""
    return crud.create(data)

@router.put("/orders/update/{orders_id}")
def update_order(orders_id: int, data: OrdersData):
    """Updates an existing order."""
    return crud.update(orders_id, data)

@router.delete("/orders/delete/{orders_id}")
def delete_order(orders_id: int):
    """Deletes an order."""
    return crud.delete(orders_id)

@router.get("/orders/get_by_id/{orders_id}", response_model=OrdersData)
def get_order_by_id(orders_id: int):
    """Gets an order by ID."""
    return crud.get_by_id(orders_id)

@router.get("/orders/get_all", response_model=List[OrdersData])
def get_all_orders():
    """Gets all orders."""
    return crud.get_all()