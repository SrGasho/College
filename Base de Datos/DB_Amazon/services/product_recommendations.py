from typing import List

from fastapi import APIRouter

from crud.product_recommendations import ProductRecommendationsData, ProductRecommendationsCRUD

router = APIRouter()
crud = ProductRecommendationsCRUD()

@router.post("/product_recommendations/create", response_model=int)
def create_product_recommendation(data: ProductRecommendationsData):
    """Creates a new product recommendation."""
    return crud.create(data)

@router.put("/product_recommendations/update/{product_recommendation_id}")
def update_product_recommendation(product_recommendation_id: int, data: ProductRecommendationsData):
    """Updates an existing product recommendation."""
    return crud.update(product_recommendation_id, data)

@router.delete("/product_recommendations/delete/{product_recommendation_id}")
def delete_product_recommendation(product_recommendation_id: int):
    """Deletes a product recommendation."""
    return crud.delete(product_recommendation_id)

@router.get("/product_recommendations/get_by_id/{product_recommendation_id}", response_model=ProductRecommendationsData)
def get_product_recommendation_by_id(product_recommendation_id: int):
    """Gets a product recommendation by ID."""
    return crud.get_by_id(product_recommendation_id)

@router.get("/product_recommendations/customer/{customer_id}", response_model=List[ProductRecommendationsData])
def get_product_recomendation_by_customer_(customer_id : int):
    """Gets all product recommendations."""
    return crud.get_by_customer(customer_id)

@router.get("/product_recommendations/product/{product_id}", response_model=List[ProductRecommendationsData])
def get_product_recomendation_by_product_(product_id : int):
    """Gets all product recommendations."""
    return crud.get_recommendations_for_product(product_id)