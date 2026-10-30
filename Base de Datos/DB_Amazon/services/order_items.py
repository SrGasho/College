from typing import List, Dict, Optional

from fastapi import APIRouter

from crud.order_items import OrderItemData, OrderItemCRUD  # Import the CRUD and the model

router = APIRouter()
crud = OrderItemCRUD()

@router.post("/order_items/create", response_model=int)
def create_order_item(data: OrderItemData):
    """Creates a new order item."""
    return crud.create(data)

@router.put("/order_items/update/{order_item_id}")
def update_order_item(order_item_id: int, data: OrderItemData):
    """Updates an existing order item."""
    return crud.update(order_item_id, data)

@router.delete("/order_items/delete/{order_item_id}")
def delete_order_item(order_item_id: int):
    """Deletes an order item."""
    return crud.delete(order_item_id)

@router.get("/order_items/get_by_order/{order_id}", response_model=List[Dict])
def get_order_items_by_order(order_id: int):
    """Gets all order items for a specific order with product name and discounts."""
    return crud.get_by_order(order_id)

@router.get("/order_items/get_one_from_order/{order_id}/{product_id}", response_model=Optional[Dict])
def get_one_order_item_from_order(order_id: int, product_id: int):
    """Gets a single order item from a specific order with product name and discounts."""
    return crud.get_one_from_order(order_id, product_id)
