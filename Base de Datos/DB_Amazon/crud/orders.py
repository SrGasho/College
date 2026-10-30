from typing import List, Optional, Dict
from pydantic import BaseModel

from connections import PostgresDatabaseConnection

class OrderItem(BaseModel):
    """Data structure for Order Items."""
    product_id: int
    product_name: str
    quantity: int
    price_at_purchase: float
    coupon_discount: float
    offer_discount: float
    total_price: float

class OrdersData(BaseModel):
    """Data structure for Orders."""
    total_amount: float
    order_status: str
    customer_id: int       # Foreign key
    payment_method_id: int  # Foreign key
    shipping_id: int       # Foreign key
    order_items: List[OrderItem] = []  # List of products in the order
    calculated_total: Optional[float] = None  # Optional if you don't want to validate it always

class OrdersCRUD:

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
            cursor.execute(query, values or ())
            self.db_connection.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error in database operation: {e}")
            self.db_connection.connection.rollback()
            return False

    def _get_orders(self, query: str, values: tuple = None) -> List[Dict]:
        """Executes a SELECT query and returns orders as a list of dictionaries.
        
        Args:
            query (str): The SQL query to execute.
            values (tuple, optional): The values to use in the query.

        Returns:
            List[Dict]: A list of orders as dictionaries.
        """
        orders = []
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values or ())
            for order in cursor.fetchall():
                orders.append({
                    "total_amount": order[0],
                    "order_status": order[1],
                    "customer_id": order[2],
                    "payment_method_id": order[3],
                    "shipping_id": order[4],
                })
            cursor.close()
            return orders
        except Exception as e:
            print(f"Error fetching orders: {e}")
            return []

    def create(self, data: OrdersData) -> Optional[int]:
        """Creates a new order.
        
        Args:
            data (OrdersData): The data for the new order.

        Returns:
            Optional[int]: The ID of the created order, or None if there was an error.
        """
        query = """
            INSERT INTO Orders (total_amount, order_status, customer_id, payment_method_id, shipping_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING orders_id;
        """
        values = (data.total_amount, data.order_status, data.customer_id, data.payment_method_id, data.shipping_id)
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            orders_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return orders_id
        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Error creating order: {e}")
            return None

    def get_by_id(self, orders_id: int) -> Dict:
        """Gets an order by ID, including order items with product names and total price calculation.
        
        Args:
            orders_id (int): The ID of the order to retrieve.

        Returns:
            Dict: The order data including items and calculated total.
        """
        query = """
            SELECT 
                o.total_amount, 
                o.order_status, 
                o.customer_id, 
                o.payment_method_id, 
                o.shipping_id, 
                oi.product_id, 
                p.product_name, 
                oi.quantity, 
                oi.price_at_purchase, 
                COALESCE(c.discount_value, 0) AS coupon_discount, 
                COALESCE(ofr.discount, 0) AS offer_discount
            FROM Orders o
            LEFT JOIN Order_Items oi ON o.orders_id = oi.orders_id
            LEFT JOIN Product p ON oi.product_id = p.product_id
            LEFT JOIN Coupons c ON oi.coupon_id = c.coupons_id
            LEFT JOIN Offer ofr ON oi.offer_id = ofr.offer_id
            WHERE o.orders_id = %s;
        """
        
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, (orders_id,))
            order_items = cursor.fetchall()
            cursor.close()
            
            if not order_items:
                print(f"No data found for order {orders_id}.")
                return {"error": f"Order {orders_id} not found"}  # Return valid response in case of error

            # Extract general order data
            order_data = {
                "total_amount": order_items[0][0],
                "order_status": order_items[0][1],
                "customer_id": order_items[0][2],
                "payment_method_id": order_items[0][3],
                "shipping_id": order_items[0][4],
                "order_items": []  # Initialize the list before the loop
            }
            
            total_real = 0  # To calculate the total with discounts

            for item in order_items:
                product_id = item[5]
                product_name = item[6]
                quantity = item[7]
                price_at_purchase = item[8]
                coupon_discount = item[9]
                offer_discount = item[10]
                
                if product_id is None:  # Case where there are no Order_Items
                    continue  # Avoid adding empty products, but continue processing other items

                total_price = (price_at_purchase * quantity) - (coupon_discount + offer_discount)
                total_real += total_price  # Add to the total of the order
                
                order_data["order_items"].append({  # Add the item inside the loop
                    "product_id": product_id,
                    "product_name": product_name,
                    "quantity": quantity,
                    "price_at_purchase": price_at_purchase,
                    "coupon_discount": coupon_discount,
                    "offer_discount": offer_discount,
                    "total_price": total_price  # Total price per product
                })
            
            order_data["calculated_total"] = total_real  # Total adjusted with discounts
            
            return order_data

        except Exception as e:
            print(f"Error getting order by ID {orders_id}: {e}")
            return {"error": f"Internal error retrieving order {orders_id}"}

    def get_all(self) -> List[OrdersData]:
        """Gets all orders.
        
        Returns:
            List[OrdersData]: A list of all orders.
        """
        query = """
            SELECT total_amount, order_status, customer_id, payment_method_id, shipping_id
            FROM Orders;
        """
        return self._get_orders(query) or []

    def update(self, orders_id: int, data: OrdersData) -> bool:
        """Updates an order.
        
        Args:
            orders_id (int): The ID of the order to update.
            data (OrdersData): The new data for the order.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        query = """
            UPDATE Orders
            SET total_amount = %s, order_status = %s, customer_id = %s, payment_method_id = %s, shipping_id = %s
            WHERE orders_id = %s;
        """
        values = (data.total_amount, data.order_status, data.customer_id, data.payment_method_id, data.shipping_id, orders_id)
        return self._execute_query(query, values)

    def delete(self, orders_id: int) -> bool:
        """Deletes an order.
        
        Args:
            orders_id (int): The ID of the order to delete.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        query = """
            DELETE FROM Orders
            WHERE orders_id = %s;
        """
        return self._execute_query(query, (orders_id,))