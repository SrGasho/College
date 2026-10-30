from typing import List

from fastapi import APIRouter, HTTPException, status

from crud.review import ReviewData, ReviewCRUD

router = APIRouter()
crud = ReviewCRUD()

@router.post("/review/", status_code=status.HTTP_201_CREATED, response_model=int)
def create_review(data: ReviewData):
    """Creates a new review."""
    review_id = crud.create(data)
    if review_id is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create review")
    return review_id

@router.get("/review/{review_id}", response_model=ReviewData)
def get_review_by_id(review_id: int):
    """Gets a review by ID."""
    review = crud.get_by_id(review_id)
    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return review

@router.get("/review/", response_model=List[ReviewData])
def get_all_reviews():
    """Gets all reviews."""
    return crud.get_all()

@router.get("/review/product/{product_id}", response_model=List[ReviewData])
def get_reviews_by_product(product_id: int):
    """Gets reviews for a specific product."""
    return crud.get_by_product(product_id)

@router.get("/review/customer/{customer_id}", response_model=List[ReviewData])
def get_reviews_by_customer(customer_id: int):
    """Gets reviews for a specific customer."""
    return crud.get_by_customer(customer_id)

@router.put("/review/{review_id}")
def update_review(review_id: int, data: ReviewData):
    """Updates an existing review."""
    if not crud.update(review_id, data):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update review")
    return {"message": "Review updated"}

@router.delete("/review/{review_id}")
def delete_review(review_id: int):
    """Deletes a review."""
    if not crud.delete(review_id):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete review")
    return {"message": "Review deleted"}

@router.delete("/review/product/{product_id}")
def delete_reviews_by_product(product_id: int):
    """Deletes all reviews for a specific product."""
    if not crud.delete_by_product(product_id):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete reviews for product")
    return {"message": "Reviews for product deleted"}

@router.delete("/review/customer/{customer_id}")
def delete_reviews_by_customer(customer_id: int):
    """Deletes all reviews for a specific customer."""
    if not crud.delete_by_customer(customer_id):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete reviews for customer")
    return {"message": "Reviews for customer deleted"}