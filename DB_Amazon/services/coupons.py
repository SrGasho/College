from typing import List
from fastapi import APIRouter
from crud.coupons import CouponsData, CouponsCRUD

router = APIRouter()
crud = CouponsCRUD()

@router.post("/coupons/create", response_model=int)
def create_coupon(data: CouponsData):
    """Creates a new coupon."""
    return crud.create(data)

@router.put("/coupons/update/{coupons_id}")
def update_coupon(coupons_id: int, data: CouponsData):
    """Updates an existing coupon."""
    return crud.update(coupons_id, data)

@router.delete("/coupons/delete/{coupons_id}")
def delete_coupon(coupons_id: int):
    """Deletes a coupon."""
    return crud.delete(coupons_id)

@router.get("/coupons/get_by_id/{coupons_id}", response_model=CouponsData)
def get_coupon_by_id(coupons_id: int):
    """Gets a coupon by ID."""
    return crud.get_by_id(coupons_id)

@router.get("/coupons/get_all", response_model=List[CouponsData])
def get_all_coupons():
    """Gets all coupons."""
    return crud.get_all()

@router.get("/coupons/get_by_code/{discount_code}", response_model=CouponsData)
def get_coupon_by_code(discount_code: str):
    """Gets a coupon by discount code."""
    return crud.get_by_code(discount_code)