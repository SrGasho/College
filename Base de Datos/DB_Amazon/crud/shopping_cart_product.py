from typing import List, Dict
from pydantic import BaseModel
from connections import PostgresDatabaseConnection

class ShoppingCartProductData(BaseModel):
    """Data structure for ShoppingCartProduct."""
    product_id: int
    quantity: int

class ShoppingCartProductCRUD:
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
            print(f"Error en la operación de la base de datos: {e}")
            self.db_connection.connection.rollback()
            return False

    def _get_shopping_cart_products(self, query: str, values: tuple = None) -> List[Dict]:
        """Executes a query and returns a list of shopping cart products as dictionaries."""
        shopping_cart_products = []
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values or ())
            for product in cursor.fetchall():
                shopping_cart_products.append({
                    "cart_id": product[0],
                    "product_id": product[1],
                    "quantity": product[2]
                })
            cursor.close()
            return shopping_cart_products
        except Exception as e:
            print(f"Error al obtener productos del carrito: {e}")
            return []

    def create(self, cart_id: int, data: ShoppingCartProductData) -> bool:
        """Creates a new shopping cart product entry or updates the quantity if it already exists."""
        query = """
            INSERT INTO shopping_cart_product (cart_id, product_id, quantity)
            VALUES (%s, %s, %s)
            ON CONFLICT (cart_id, product_id)
            DO UPDATE SET quantity = shopping_cart_product.quantity + EXCLUDED.quantity;
        """
        values = (cart_id, data.product_id, data.quantity)
        return self._execute_query(query, values)

    def get_by_cart_id(self, cart_id: int) -> List[Dict]:
        """Gets all products in a specific shopping cart."""
        query = """
            SELECT cart_id, product_id, quantity
            FROM shopping_cart_product
            WHERE cart_id = %s;
        """
        return self._get_shopping_cart_products(query, (cart_id,))

    def update(self, cart_id: int, product_id: int, data: ShoppingCartProductData) -> bool:
        """Updates the quantity of a product in a shopping cart."""
        query = """
            UPDATE shopping_cart_product
            SET quantity = %s
            WHERE cart_id = %s AND product_id = %s;
        """
        values = (data.quantity, cart_id, product_id)
        return self._execute_query(query, values)

    def delete(self, cart_id: int, product_id: int) -> bool:
        """Deletes a product from a shopping cart."""
        query = """
            DELETE FROM shopping_cart_product
            WHERE cart_id = %s AND product_id = %s;
        """
        return self._execute_query(query, (cart_id, product_id))

    def delete_by_cart_id(self, cart_id: int) -> bool:
        """Deletes all products from a specific shopping cart."""
        query = """
            DELETE FROM shopping_cart_product
            WHERE cart_id = %s;
        """
        return self._execute_query(query, (cart_id,))