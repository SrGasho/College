from typing import List, Optional, Dict
from pydantic import BaseModel

from connections import PostgresDatabaseConnection

class ProductData(BaseModel):
    """Data structure for Product."""
    product_name: str
    description: Optional[str] = None
    price: float
    quantity_available: int
    category_id: int
    seller_id: int

class ProductCRUD:

    def __init__(self):
        """Initialize the database connection."""
        self.db_connection = PostgresDatabaseConnection()
        self.db_connection.connect()

    def _execute_query(self, query: str, values: tuple = None) -> bool:
        """Executes an SQL query that modifies the database.
        
        Args:
            query (str): The SQL query to execute.
            values (tuple, optional): The values to use in the query.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values or ())
            self.db_connection.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Database error: {e}")
            self.db_connection.connection.rollback()
            return False

    def _get_products(self, query: str, values: tuple = None) -> List[Dict]:
        """Executes a SELECT query and returns products as a list of dictionaries.
        
        Args:
            query (str): The SQL query to execute.
            values (tuple, optional): The values to use in the query.

        Returns:
            List[Dict]: A list of products as dictionaries.
        """
        products = []
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values or ())
            for product in cursor.fetchall():
                products.append({
                    "product_name": product[0],
                    "description": product[1],
                    "price": product[2],
                    "quantity_available": product[3],
                    "category_id": product[4],
                    "seller_id": product[5],
                })
            cursor.close()
            return products
        except Exception as e:
            print(f"Error fetching products: {e}")
            return []

    def create(self, data: ProductData) -> Optional[int]:
        """Creates a new product.
        
        Args:
            data (ProductData): The data for the new product.

        Returns:
            Optional[int]: The ID of the created product, or None if there was an error.
        """
        query = """
            INSERT INTO Product (product_name, description, price, quantity_available, category_id, seller_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING product_id;
        """
        values = (data.product_name, data.description, data.price, data.quantity_available, data.category_id, data.seller_id)
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            product_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return product_id
        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Error creating product: {e}")
            return None

    def update(self, product_id: int, data: ProductData) -> bool:
        """Updates a product.
        
        Args:
            product_id (int): The ID of the product to update.
            data (ProductData): The new data for the product.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        query = """
            UPDATE Product
            SET product_name = %s, description = %s, price = %s, quantity_available = %s, category_id = %s, seller_id = %s
            WHERE product_id = %s;
        """
        values = (data.product_name, data.description, data.price, data.quantity_available, data.category_id, data.seller_id, product_id)
        return self._execute_query(query, values)

    def delete(self, product_id: int) -> bool:
        """Deletes a product.
        
        Args:
            product_id (int): The ID of the product to delete.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        query = "DELETE FROM Product WHERE product_id = %s;"
        return self._execute_query(query, (product_id,))

    def get_by_id(self, product_id: int) -> Optional[Dict]:
        """Gets a product by ID.
        
        Args:
            product_id (int): The ID of the product to retrieve.

        Returns:
            Optional[Dict]: The retrieved product as a dictionary, or None if not found.
        """
        query = """
            SELECT product_name, description, price, quantity_available, category_id, seller_id
            FROM Product
            WHERE product_id = %s;
        """
        products = self._get_products(query, (product_id,))
        return products[0] if products else None

    def get_all(self) -> List[Dict]:
        """Gets all products.
        
        Returns:
            List[Dict]: A list of all products.
        """
        query = "SELECT product_name, description, price, quantity_available, category_id, seller_id FROM Product;"
        return self._get_products(query)

    def get_by_name(self, product_name: str) -> List[Dict]:
        """Gets products by name (case-insensitive search).
        
        Args:
            product_name (str): The name of the product to search for.

        Returns:
            List[Dict]: A list of products that match the search criteria.
        """
        query = """
            SELECT product_name, description, price, quantity_available, category_id, seller_id
            FROM Product
            WHERE LOWER(product_name) LIKE LOWER(%s);
        """
        return self._get_products(query, ("%" + product_name + "%",))

    def get_by_category(self, category_id: int) -> List[Dict]:
        """Gets products by category.
        
        Args:
            category_id (int): The ID of the category to retrieve products for.

        Returns:
            List[Dict]: A list of products in the specified category.
        """
        query = """
            SELECT product_name, description, price, quantity_available, category_id, seller_id
            FROM Product
            WHERE category_id = %s;
        """
        return self._get_products(query, (category_id,))

    def get_by_price_ascendent(self) -> List[Dict]:
        """Gets products ordered by price in ascending order.
        
        Returns:
            List[Dict]: A list of products ordered by price in ascending order.
        """
        query = """
            SELECT product_name, description, price, quantity_available, category_id, seller_id
            FROM Product
            ORDER BY price ASC;
        """
        return self._get_products(query)

    def get_by_price_descendent(self) -> List[Dict]:
        """Gets products ordered by price in descending order.
        
        Returns:
            List[Dict]: A list of products ordered by price in descending order.
        """
        query = """
            SELECT product_name, description, price, quantity_available, category_id, seller_id
            FROM Product
            ORDER BY price DESC;
        """
        return self._get_products(query)

    def get_cheaper(self, max_price: float) -> List[Dict]:
        """Gets products with a price lower than or equal to the given value.
        
        Args:
            max_price (float): The maximum price to filter products by.

        Returns:
            List[Dict]: A list of products with a price lower than or equal to the given value.
        """
        query = """
            SELECT product_name, description, price, quantity_available, category_id, seller_id
            FROM Product
            WHERE price <= %s;
        """
        return self._get_products(query, (max_price,))

    def get_expensive(self, min_price: float) -> List[Dict]:
        """Gets products with a price higher than or equal to the given value.
        
        Args:
            min_price (float): The minimum price to filter products by.

        Returns:
            List[Dict]: A list of products with a price higher than or equal to the given value.
        """
        query = """
            SELECT product_name, description, price, quantity_available, category_id, seller_id
            FROM Product
            WHERE price >= %s;
        """
        return self._get_products(query, (min_price,))