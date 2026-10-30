from typing import List

from fastapi import APIRouter

from crud.seller import SellerData, SellerCRUD

router = APIRouter()
crud = SellerCRUD()

@router.post("/seller/create", response_model=int)
def create_seller(data: SellerData):
    """Creates a new seller."""
    return crud.create(data)

@router.put("/seller/update/{seller_id}")
def update_seller(seller_id: int, data: SellerData):
    """Updates an existing seller."""
    return crud.update(seller_id, data)

@router.delete("/seller/delete/{seller_id}")
def delete_seller(seller_id: int):
    """Deletes a seller."""
    return crud.delete(seller_id)

@router.get("/seller/get_by_id/{seller_id}", response_model=SellerData)
def get_seller_by_id(seller_id: int):
    """Gets a seller by ID."""
    return crud.get_by_id(seller_id)

@router.get("/seller/get_all", response_model=List[SellerData])
def get_all_sellers():
    """Gets all sellers."""
    return crud.get_all()

@router.get("/seller/get_by_name/{seller_name}", response_model=List[SellerData])
def get_seller_by_name(seller_name: str):
    """Gets sellers by name."""
    return crud.get_by_name(seller_name)

@router.get("/seller/get_by_rating/{seller_rating}", response_model=List[SellerData])
def get_seller_by_rating(seller_rating: str):
    """Gets sellers by rating."""
    return crud.get_by_rating(seller_rating)