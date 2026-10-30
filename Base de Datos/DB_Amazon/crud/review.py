from typing import List, Optional
from pydantic import BaseModel
from datetime import date

from connections import PostgresDatabaseConnection

class ReviewData(BaseModel):
    """Data structure for Review."""
    rating: int
    comment: Optional[str] = None
    review_date: date  # ISO 8601 format is recommended (YYYY-MM-DD)
    customer_id: int    # Foreign key
    product_id: int     # Foreign key

class ReviewCRUD:

    def __init__(self):
        """Initialize the database connection."""
        self.db_connection = PostgresDatabaseConnection()
        self.db_connection.connect()

    def _execute_query(self, query: str, values: tuple = None) -> bool:
        """Execute a query on the database.
        
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
                cursor.execute(query)
            self.db_connection.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error in database operation: {e}")
            self.db_connection.connection.rollback()
            return False

    def _get_reviews(self, query: str, values: tuple = None) -> List[ReviewData]:
        """Executes a query and returns a list of ReviewData objects.
        
        Args:
            query (str): The SQL query to execute.
            values (tuple, optional): The values to use in the query.

        Returns:
            List[ReviewData]: A list of ReviewData objects.
        """
        reviews = []
        try:
            cursor = self.db_connection.connection.cursor()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            review_list = cursor.fetchall()
            cursor.close()
            for review_data in review_list:
                review_dict = {
                    "rating": review_data[0],
                    "comment": review_data[1],
                    "review_date": review_data[2],
                    "customer_id": review_data[3],
                    "product_id": review_data[4]
                }
                reviews.append(ReviewData(**review_dict))
            return reviews
        except Exception as e:
            print(f"Error in query: {e}")
            return []

    def create(self, data: ReviewData) -> Optional[int]:
        """Creates a new review.
        
        Args:
            data (ReviewData): The data for the new review.

        Returns:
            Optional[int]: The ID of the created review, or None if there was an error.
        """
        query = """
            INSERT INTO Review (rating, comment, review_date, customer_id, product_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING review_id;
        """
        values = (data.rating, data.comment, data.review_date, data.customer_id, data.product_id)
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            review_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return review_id
        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Error creating review: {e}")
            return None

    def get_by_id(self, review_id: int) -> Optional[ReviewData]:
        """Gets a review by ID.
        
        Args:
            review_id (int): The ID of the review to retrieve.

        Returns:
            Optional[ReviewData]: The retrieved review, or None if not found.
        """
        query = """
            SELECT rating, comment, review_date, customer_id, product_id
            FROM Review
            WHERE review_id = %s;
        """
        reviews = self._get_reviews(query, (review_id,))
        return reviews[0] if reviews else None  # Return None if no results

    def get_all(self) -> List[ReviewData]:
        """Gets all reviews.
        
        Returns:
            List[ReviewData]: A list of all reviews.
        """
        query = """
            SELECT rating, comment, review_date, customer_id, product_id
            FROM Review;
        """
        return self._get_reviews(query)
    
    def get_by_product(self, product_id: int) -> List[ReviewData]:
        """Gets reviews for a specific product.
        
        Args:
            product_id (int): The ID of the product to retrieve reviews for.

        Returns:
            List[ReviewData]: A list of reviews for the specified product.
        """
        query = """
            SELECT rating, comment, review_date, customer_id, product_id
            FROM Review
            WHERE product_id = %s;
        """
        return self._get_reviews(query, (product_id,))
    
    def get_by_customer(self, customer_id: int) -> List[ReviewData]:
        """Gets reviews for a specific customer.
        
        Args:
            customer_id (int): The ID of the customer to retrieve reviews for.

        Returns:
            List[ReviewData]: A list of reviews for the specified customer.
        """
        query = """
            SELECT rating, comment, review_date, customer_id, product_id
            FROM Review
            WHERE customer_id = %s;
        """
        return self._get_reviews(query, (customer_id,))

    def update(self, review_id: int, data: ReviewData) -> bool:
        """Updates a review.
        
        Args:
            review_id (int): The ID of the review to update.
            data (ReviewData): The new data for the review.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        query = """
            UPDATE Review
            SET rating = %s, comment = %s, review_date = %s, customer_id = %s, product_id = %s
            WHERE review_id = %s;
        """
        values = (data.rating, data.comment, data.review_date, data.customer_id, data.product_id, review_id)
        return self._execute_query(query, values)

    def delete(self, review_id: int) -> bool:
        """Deletes a review.
        
        Args:
            review_id (int): The ID of the review to delete.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        query = """
            DELETE FROM Review
            WHERE review_id = %s;
        """
        return self._execute_query(query, (review_id,))
    
    def delete_by_product(self, product_id: int) -> bool:
        """Deletes all reviews for a specific product.
        
        Args:
            product_id (int): The ID of the product to delete reviews for.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        query = """
            DELETE FROM Review
            WHERE product_id = %s;
        """
        return self._execute_query(query, (product_id,))

    def delete_by_customer(self, customer_id: int) -> bool:
        """Deletes all reviews for a specific customer.
        
        Args:
            customer_id (int): The ID of the customer to delete reviews for.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        query = """
            DELETE FROM Review
            WHERE customer_id = %s;
        """
        return self._execute_query(query, (customer_id,))