from typing import List, Optional

from fastapi import APIRouter, HTTPException, status

from crud.search_history import SearchHistoryData, SearchHistoryCRUD

router = APIRouter()
crud = SearchHistoryCRUD()

@router.post("/search_history/", status_code=status.HTTP_201_CREATED, response_model=int)  # POST to /search_history/
def create_search_history(data: SearchHistoryData):
    """Creates a new search history entry."""
    search_history_id = crud.create(data)
    if search_history_id is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create search history entry")
    return search_history_id

@router.get("/search_history/{search_history_id}", response_model=SearchHistoryData)  # GET to /search_history/{id}
def get_search_history_by_id(search_history_id: int):
    """Gets a search history entry by ID."""
    search_history_entry = crud.get_by_id(search_history_id)
    if search_history_entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Search history entry not found")
    return search_history_entry


@router.get("/search_history/", response_model=List[SearchHistoryData])  # GET to /search_history/
def get_all_search_history():
    """Gets all search history entries."""
    return crud.get_all()

@router.get("/search_history/customer/{customer_id}", response_model=List[SearchHistoryData]) # GET to /search_history/customer/{id}
def get_search_history_by_customer(customer_id: int):
    """Gets all search history entries for a customer."""
    return crud.get_by_customer(customer_id)

@router.put("/search_history/{search_history_id}")  # PUT to /search_history/{id}
def update_search_history(search_history_id: int, data: SearchHistoryData):
    """Updates an existing search history entry."""
    if not crud.update(search_history_id, data):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update search history entry")
    return {"message": "Search history entry updated"}  # Or return the updated data

@router.delete("/search_history/{search_history_id}")  # DELETE to /search_history/{id}
def delete_search_history(search_history_id: int):
    """Deletes a search history entry."""
    if not crud.delete(search_history_id):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete search history entry")
    return {"message": "Search history entry deleted"}

@router.delete("/search_history/customer/{customer_id}") # DELETE to /search_history/customer/{id}
def delete_search_history_by_customer(customer_id: int):
    """Deletes all search history entries for a customer."""
    if not crud.delete_by_customer(customer_id):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete search history entries for customer")
    return {"message": "Search history entries for customer deleted"}