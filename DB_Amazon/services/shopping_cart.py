from typing import List

from fastapi import APIRouter

from crud.shopping_cart import ShoppingCartData, ShoppingCartCRUD

router = APIRouter()
crud = ShoppingCartCRUD()

@router.post("/shopping_cart/create", response_model=int)
def create_shopping_cart(data: ShoppingCartData):
    """Creates a new shopping cart."""
    return crud.create(data)