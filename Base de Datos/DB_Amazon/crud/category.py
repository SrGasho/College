from typing import List, Optional
from pydantic import BaseModel, EmailStr, validator

from connections import PostgresDatabaseConnection

class CategoryData(BaseModel):
    """Data structure for Category."""
    category_name: str
    description: Optional[str] = None  # Optional description

class CategoryCRUD:
    """CRUD operations for Category."""

    def __init__(self):
        """Initialize the database connection."""
        self.db_connection = PostgresDatabaseConnection()
        self.db_connection.connect()

    def _execute_query(self, query: str, values: tuple = None) -> bool:
        """Execute a query and commit the changes.
        
        Args:
            query (str): The SQL query to execute.
            values (tuple, optional): The values to use in the query.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        try:
            cursor = self.db_connection.connection.cursor()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)  # For queries without values.
            self.db_connection.connection.commit()
            cursor.close()
            return True  # Indicate that the operation was successful.
        except Exception as e:
            print(f"Error in database operation: {e}")
            self.db_connection.connection.rollback()  # Revert changes in case of error.
            return False
        
    def _get_categories(self, query: str, values: tuple = None) -> List[CategoryData]:
        """Execute a query and create a list of CategoryData objects.
        
        Args:
            query (str): The SQL query to execute.
            values (tuple, optional): The values to use in the query.

        Returns:
            List[CategoryData]: A list of CategoryData objects.
        """
        categories = []
        try:
            cursor = self.db_connection.connection.cursor()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            category_list = cursor.fetchall()
            cursor.close()
            for category_data in category_list:
                category_dict = {
                    "category_name": category_data[0],
                    "description": category_data[1]
                }
                categories.append(CategoryData(**category_dict))
            return categories
        except Exception as e:
            print(f"Error en la consulta: {e}")
            return []

    def create(self, data: CategoryData) -> Optional[int]:
        """Create a new category.
        
        Args:
            data (CategoryData): The data for the new category.

        Returns:
            Optional[int]: The ID of the created category, or None if there was an error.
        """
        query = """
            INSERT INTO Category (category_name, description)
            VALUES (%s, %s)
            RETURNING category_id;
        """
        values = (data.category_name, data.description)
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            category_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return category_id
        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Error creating category: {e}")
            return None

    def get_by_id(self, category_id: int) -> Optional[CategoryData]:
        """Get a category by ID.
        
        Args:
            category_id (int): The ID of the category to retrieve.

        Returns:
            Optional[CategoryData]: The retrieved category, or None if not found.
        """
        query = """
            SELECT category_name, description
            FROM Category
            WHERE category_id = %s;
        """
        categories = self._get_categories(query, (category_id,))
        return categories[0] if categories else None

    def get_all(self) -> List[CategoryData]:
        """Get all categories.
        
        Returns:
            List[CategoryData]: A list of all categories.
        """
        query = """
            SELECT category_name, description
            FROM Category;
        """
        return self._get_categories(query)
    
    def get_by_name(self, category_name: str) -> List[CategoryData]:
        """Get categories by name (case-insensitive search).
        
        Args:
            category_name (str): The name of the category to search for.

        Returns:
            List[CategoryData]: A list of categories that match the search criteria.
        """
        query = """
            SELECT category_name, description
            FROM Category
            WHERE LOWER(category_name) LIKE LOWER(%s);
        """
        return self._get_categories(query, ("%" + category_name + "%",))

    def update(self, category_id: int, data: CategoryData) -> bool:
        """Update a category.
        
        Args:
            category_id (int): The ID of the category to update.
            data (CategoryData): The new data for the category.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        query = """
            UPDATE Category
            SET category_name = %s, description = %s
            WHERE category_id = %s;
        """
        values = (data.category_name, data.description, category_id)
        return self._execute_query(query, values)

    def delete(self, category_id: int) -> bool:
        """Delete a category.
        
        Args:
            category_id (int): The ID of the category to delete.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        query = """
            DELETE FROM Category
            WHERE category_id = %s;
        """
        return self._execute_query(query, (category_id,))