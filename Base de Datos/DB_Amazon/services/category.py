from typing import List
from fastapi import APIRouter
from crud.category import CategoryData, CategoryCRUD

router = APIRouter()
crud = CategoryCRUD()

@router.post("/category/create", response_model=int)
def create_category(data: CategoryData):
    """Creates a new category."""
    return crud.create(data)

@router.put("/category/update/{category_id}")
def update_category(category_id: int, data: CategoryData):
    """Updates an existing category."""
    return crud.update(category_id, data)

@router.delete("/category/delete/{category_id}")
def delete_category(category_id: int):
    """Deletes a category."""
    return crud.delete(category_id)

@router.get("/category/get_by_id/{category_id}", response_model=CategoryData)
def get_category_by_id(category_id: int):
    """Gets a category by ID."""
    return crud.get_by_id(category_id)

@router.get("/category/get_all", response_model=List[CategoryData])
def get_all_categories():
    """Gets all categories."""
    return crud.get_all()

@router.get("/category/get_by_name/{category_name}", response_model=List[CategoryData])
def get_category_by_name(category_name: str):
    """Gets categories by name."""
    return crud.get_by_name(category_name)