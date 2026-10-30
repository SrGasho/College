from typing import List, Optional
from pydantic import BaseModel

from connections import PostgresDatabaseConnection

class ProductRecommendationsData(BaseModel):
    """Data structure for ProductRecommendations."""
    customer_id: int             # Foreign key
    recommended_product_id: int  # Foreign key

class ProductRecommendationsCRUD:

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
        
    def _get_product_recommendations(self, query: str, values: tuple = None) -> List[ProductRecommendationsData]:
        """Executes a query and returns a list of ProductRecommendationsData objects.
        
        Args:
            query (str): The SQL query to execute.
            values (tuple, optional): The values to use in the query.

        Returns:
            List[ProductRecommendationsData]: A list of ProductRecommendationsData objects.
        """
        product_recommendations = []
        try:
            cursor = self.db_connection.connection.cursor()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            product_recommendation_list = cursor.fetchall()
            cursor.close()
            for product_recommendation in product_recommendation_list:
                product_recommendation_dict = {
                    "customer_id": product_recommendation[0],
                    "recommended_product_id": product_recommendation[1]
                }
                product_recommendations.append(ProductRecommendationsData(**product_recommendation_dict))
            return product_recommendations
        except Exception as e:
            print(f"Error in query: {e}")
            return []

    def create(self, data: ProductRecommendationsData) -> Optional[int]:
        """Creates a new product recommendation.
        
        Args:
            data (ProductRecommendationsData): The data for the new product recommendation.

        Returns:
            Optional[int]: The ID of the created product recommendation, or None if there was an error.
        """
        query = """
            INSERT INTO Product_Recommendations (customer_id, recommended_product_id)
            VALUES (%s, %s)
            RETURNING product_Recommendation_id;
        """
        values = (data.customer_id, data.recommended_product_id)
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            product_recommendation_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return product_recommendation_id
        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Error creating product recommendation: {e}")
            return None

    def get_by_id(self, product_recommendation_id: int) -> Optional[ProductRecommendationsData]:
        """Gets a product recommendation by ID.
        
        Args:
            product_recommendation_id (int): The ID of the product recommendation to retrieve.

        Returns:
            Optional[ProductRecommendationsData]: The retrieved product recommendation, or None if not found.
        """
        query = """
            SELECT customer_id, recommended_product_id
            FROM Product_Recommendations
            WHERE product_Recommendation_id = %s;
        """
        product_recommendations = self._get_product_recommendations(query, (product_recommendation_id,))
        return product_recommendations[0] if product_recommendations else None

    def get_by_customer(self, customer_id: int) -> List[ProductRecommendationsData]:
        """Gets recommendations for a specific customer.
        
        Args:
            customer_id (int): The ID of the customer to retrieve recommendations for.

        Returns:
            List[ProductRecommendationsData]: A list of recommendations for the specified customer.
        """
        query = """
            SELECT customer_id, recommended_product_id
            FROM Product_Recommendations
            WHERE customer_id = %s;
        """
        return self._get_product_recommendations(query, (customer_id,))

    def get_recommendations_for_product(self, product_id: int) -> List[ProductRecommendationsData]:
        """Gets recommendations that include a specific product.
        
        Args:
            product_id (int): The ID of the product to retrieve recommendations for.

        Returns:
            List[ProductRecommendationsData]: A list of recommendations that include the specified product.
        """
        query = """
            SELECT customer_id, recommended_product_id
            FROM Product_Recommendations
            WHERE recommended_product_id = %s;
        """
        return self._get_product_recommendations(query, (product_id,))

    def update(self, product_recommendation_id: int, data: ProductRecommendationsData) -> bool:
        """Updates a product recommendation.
        
        Args:
            product_recommendation_id (int): The ID of the product recommendation to update.
            data (ProductRecommendationsData): The new data for the product recommendation.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        query = """
            UPDATE Product_Recommendations
            SET customer_id = %s, recommended_product_id = %s
            WHERE product_Recommendation_id = %s;
        """
        values = (data.customer_id, data.recommended_product_id, product_recommendation_id)
        return self._execute_query(query, values)

    def delete(self, product_recommendation_id: int) -> bool:
        """Deletes a product recommendation.
        
        Args:
            product_recommendation_id (int): The ID of the product recommendation to delete.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        query = """
            DELETE FROM Product_Recommendations
            WHERE product_Recommendation_id = %s;
        """
        return self._execute_query(query, (product_recommendation_id,))