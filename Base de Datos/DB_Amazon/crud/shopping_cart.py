from typing import List, Optional, Dict
from pydantic import BaseModel

from connections import PostgresDatabaseConnection

class ShoppingCartData(BaseModel):
    """Data structure for ShoppingCart."""
    customer_id: int    # Foreign key

class ShoppingCartCRUD:
    def __init__(self):
        """Initialize the database connection."""
        self.db_connection = PostgresDatabaseConnection()
        self.db_connection.connect()

    def _execute_query(self, query: str, values: tuple = None) -> bool:
        """Execute a query on the database."""
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values or ())
            self.db_connection.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error in database operation: {e}")
            self.db_connection.connection.rollback()
            return False

    def _get_shopping_cart(self, query: str, values: tuple = None) -> List[Dict]:
        """Executes a SELECT query and returns shopping carts as a list of dictionaries."""
        shopping_carts = []
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values or ())
            for cart in cursor.fetchall():
                shopping_carts.append({
                    "shopping_cart_id": cart[0],
                    "customer_id": cart[1]
                })
            cursor.close()
            return shopping_carts
        except Exception as e:
            print(f"Error fetching shopping carts: {e}")
            return []

    def create(self, data: ShoppingCartData) -> int:
        """Creates a new shopping cart and returns its ID."""
        query = """
            INSERT INTO shopping_cart (customer_id)
            VALUES (%s)
            RETURNING shopping_cart_id;
        """
        values = (data.customer_id,)
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            result = cursor.fetchone()
            self.db_connection.connection.commit()
            cursor.close()

            if result is None:
                raise ValueError("Failed to retrieve shopping_cart_id after insertion.")

            return result[0]

        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Error creating shopping cart: {e}")
            raise ValueError("Could not create shopping cart.")

    def get_by_id(self, shopping_cart_id: int) -> Optional[Dict]:
        """Gets a shopping cart by ID."""
        query = """
            SELECT shopping_cart_id, customer_id
            FROM shopping_cart
            WHERE shopping_cart_id = %s;
        """
        shopping_carts = self._get_shopping_cart(query, (shopping_cart_id,))
        return shopping_carts[0] if shopping_carts else None

    def get_all(self) -> List[Dict]:
        """Gets all shopping carts."""
        query = """
            SELECT shopping_cart_id, customer_id
            FROM shopping_cart;
        """
        return self._get_shopping_cart(query)

    def get_by_customer_id(self, customer_id: int) -> List[Dict]:
        """Gets all shopping carts for a specific customer."""
        query = """
            SELECT shopping_cart_id, customer_id
            FROM shopping_cart
            WHERE customer_id = %s;
        """
        return self._get_shopping_cart(query, (customer_id,))

    def update(self, shopping_cart_id: int, data: ShoppingCartData) -> bool:
        """Updates a shopping cart."""
        query = """
            UPDATE shopping_cart
            SET customer_id = %s
            WHERE shopping_cart_id = %s;
        """
        values = (data.customer_id, shopping_cart_id)
        return self._execute_query(query, values)

    def delete(self, shopping_cart_id: int) -> bool:
        """Deletes a shopping cart."""
        query = """
            DELETE FROM shopping_cart
            WHERE shopping_cart_id = %s;
        """
        return self._execute_query(query, (shopping_cart_id,))