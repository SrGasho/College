from typing import List

from fastapi import APIRouter, HTTPException, status

from crud.returns import ReturnsData, ReturnsCRUD

router = APIRouter()
crud = ReturnsCRUD()

@router.post("/returns/", status_code=status.HTTP_201_CREATED, response_model=int)
def create_return(data: ReturnsData):
    """Creates a new return."""
    return_id = crud.create(data)
    if return_id is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create return")
    return return_id

@router.get("/returns/{returns_id}", response_model=ReturnsData)
def get_return_by_id(returns_id: int):
    """Gets a return by ID."""
    return_item = crud.get_by_id(returns_id)
    if return_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Return not found")
    return return_item

@router.get("/returns/", response_model=List[ReturnsData])
def get_all_returns():
    """Gets all returns."""
    return crud.get_all()

@router.get("/returns/order_item/{order_item_id}", response_model=List[ReturnsData])
def get_returns_by_order_item(order_item_id: int):
    """Gets returns for a specific order item."""
    return crud.get_by_order_item(order_item_id)

@router.get("/returns/status/{return_status}", response_model=List[ReturnsData])
def get_returns_by_status(return_status: str):
    """Gets returns by status."""
    return crud.get_by_status(return_status)

@router.put("/returns/update/{returns_id}")
def update_return(returns_id: int, data: ReturnsData):
    """Updates an existing return."""
    if not crud.update(returns_id, data):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update return")
    return {"message": "Return updated"}

@router.delete("/returns/status/{return_status}")
def delete_returns_by_status(return_status: str):
    """Deletes returns by status."""
    if not crud.delete_by_status(return_status):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete returns by status")
    return {"message": "Returns by status deleted"}