from typing import List, Dict
from fastapi import APIRouter, HTTPException, status
from crud.shopping_cart_product import ShoppingCartProductData, ShoppingCartProductCRUD

router = APIRouter()
crud = ShoppingCartProductCRUD()

@router.post("/shopping_cart_product/{cart_id}/add", status_code=status.HTTP_201_CREATED)
def add_product_to_cart(cart_id: int, data: ShoppingCartProductData):
    if not crud.create(cart_id, data):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al agregar producto al carrito")
    return {"message": "Producto agregado al carrito exitosamente"}

@router.get("/shopping_cart_product/{cart_id}", response_model=List[Dict])
def get_products_in_cart(cart_id: int):
    return crud.get_by_cart_id(cart_id)

@router.put("/shopping_cart_product/{cart_id}/{product_id}")
def update_product_quantity(cart_id: int, product_id: int, data: ShoppingCartProductData):
    if not crud.update(cart_id, product_id, data):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al actualizar cantidad del producto")
    return {"message": "Cantidad de producto actualizada exitosamente"}

@router.delete("/shopping_cart_product/{cart_id}/{product_id}")
def remove_product_from_cart(cart_id: int, product_id: int):
    if not crud.delete(cart_id, product_id):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al eliminar producto del carrito")
    return {"message": "Producto eliminado del carrito exitosamente"}

@router.delete("/shopping_cart_product/{cart_id}")
def clear_shopping_cart(cart_id: int):
    if not crud.delete_by_cart_id(cart_id):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al limpiar carrito")
    return {"message": "Carrito limpiado exitosamente"}