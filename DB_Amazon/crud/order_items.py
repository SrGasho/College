from typing import List, Optional, Dict
from pydantic import BaseModel

from connections import PostgresDatabaseConnection

class OrderItemData(BaseModel):
    """Data structure for Order_Items."""
    orders_id: int
    product_id: int
    quantity: int
    price_at_purchase: float
    coupon_id: Optional[int] = None
    offer_id: Optional[int] = None

class OrderItemCRUD:

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

    def create(self, data: OrderItemData) -> Optional[int]:
        """Creates a new order item.
        
        Args:
            data (OrderItemData): The data for the new order item.

        Returns:
            Optional[int]: The ID of the created order item, or None if there was an error.
        """
        query = """
            INSERT INTO Order_Items (orders_id, product_id, quantity, price_at_purchase, coupon_id, offer_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING order_item_id;
        """
        values = (data.orders_id, data.product_id, data.quantity, data.price_at_purchase, data.coupon_id, data.offer_id)
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            order_item_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return order_item_id
        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Error creating order item: {e}")
            return None

    def _get_order_items(self, query: str, values: tuple = None) -> List[Dict]:
        """Executes a SELECT query and returns order items as a list of dictionaries.
        
        Args:
            query (str): The SQL query to execute.
            values (tuple, optional): The values to use in the query.

        Returns:
            List[Dict]: A list of order items as dictionaries.
        """
        order_items = []
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values or ())
            for order_item in cursor.fetchall():
                order_items.append({
                    "orders_id": order_item[0],
                    "product_id": order_item[1],
                    "product_name": order_item[2],  # Product name from Product table
                    "quantity": order_item[3],
                    "price_at_purchase": order_item[4],
                    "coupon_discount": order_item[5],  # Discount from coupon
                    "offer_discount": order_item[6],  # Discount from offer
                })
            cursor.close()
            return order_items
        except Exception as e:
            print(f"Error fetching order items: {e}")
            return []

    def get_by_order(self, order_id: int) -> List[Dict]:
        """Gets all order items for a specific order with product name and discounts.
        
        Args:
            order_id (int): The ID of the order to retrieve items for.

        Returns:
            List[Dict]: A list of order items for the specified order.
        """
        query = """
            SELECT oi.orders_id, oi.product_id, p.product_name, oi.quantity, oi.price_at_purchase,
                COALESCE(c.discount_value, 0) AS discount_value, 
                COALESCE(o.discount, 0) AS discount
            FROM Order_Items oi
            JOIN Product p ON oi.product_id = p.product_id
            LEFT JOIN Coupons c ON oi.coupon_id = c.coupons_id
            LEFT JOIN Offer o ON oi.offer_id = o.offer_id
            WHERE oi.orders_id = %s;
        """
        return self._get_order_items(query, (order_id,))

    def get_one_from_order(self, order_id: int, product_id: int) -> Optional[Dict]:
        """Gets a single order item from a specific order with product name and discounts.
        
        Args:
            order_id (int): The ID of the order to retrieve the item from.
            product_id (int): The ID of the product to retrieve.

        Returns:
            Optional[Dict]: The order item if found, otherwise None.
        """
        query = """
            SELECT oi.orders_id, oi.product_id, p.product_name, oi.quantity, oi.price_at_purchase,
                COALESCE(c.discount_value, 0) AS discount_value, 
                COALESCE(o.discount, 0) AS discount
            FROM Order_Items oi
            JOIN Product p ON oi.product_id = p.product_id
            LEFT JOIN Coupons c ON oi.coupon_id = c.coupons_id
            LEFT JOIN Offer o ON oi.offer_id = o.offer_id
            WHERE oi.orders_id = %s AND oi.product_id = %s;
        """
        order_items = self._get_order_items(query, (order_id, product_id))
        return order_items[0] if order_items else None

    def update(self, order_item_id: int, data: OrderItemData) -> bool:
        """Updates an order item.
        
        Args:
            order_item_id (int): The ID of the order item to update.
            data (OrderItemData): The new data for the order item.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        query = """
            UPDATE Order_Items
            SET orders_id = %s, product_id = %s, quantity = %s, price_at_purchase = %s, coupon_id = %s, offer_id = %s
            WHERE order_item_id = %s;
        """
        values = (data.orders_id, data.product_id, data.quantity, data.price_at_purchase, data.coupon_id, data.offer_id, order_item_id)
        return self._execute_query(query, values)

    def delete(self, order_item_id: int) -> bool:
        """Deletes an order item.
        
        Args:
            order_item_id (int): The ID of the order item to delete.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        query = """
            DELETE FROM Order_Items
            WHERE order_item_id = %s;
        """
        return self._execute_query(query, (order_item_id,))