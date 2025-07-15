from typing import List, Optional
from pydantic import BaseModel

from connections import PostgresDatabaseConnection

class PaymentMethodData(BaseModel):
    """Data structure for PaymentMethod."""
    payment_type: str
    customer_id: Optional[int] = None  # Foreign key (can be null)

class PaymentMethodCRUD:

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

    def _get_payment_methods(self, query: str, values: tuple = None) -> List[PaymentMethodData]:
        """Executes a query and returns a list of PaymentMethodData objects.
        
        Args:
            query (str): The SQL query to execute.
            values (tuple, optional): The values to use in the query.

        Returns:
            List[PaymentMethodData]: A list of PaymentMethodData objects.
        """
        payment_methods = []
        try:
            cursor = self.db_connection.connection.cursor()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            payment_method_list = cursor.fetchall()
            cursor.close()
            for payment_method_data in payment_method_list:
                payment_method_dict = {
                    "payment_type": payment_method_data[0],
                    "customer_id": payment_method_data[1]
                }
                payment_methods.append(PaymentMethodData(**payment_method_dict))
            return payment_methods
        except Exception as e:
            print(f"Error in query: {e}")
            return []

    def create(self, data: PaymentMethodData) -> Optional[int]:
        """Creates a new payment method.
        
        Args:
            data (PaymentMethodData): The data for the new payment method.

        Returns:
            Optional[int]: The ID of the created payment method, or None if there was an error.
        """
        query = """
            INSERT INTO Payment_Method (payment_type, customer_id)
            VALUES (%s, %s)
            RETURNING payment_method_id;
        """
        values = (data.payment_type, data.customer_id)
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            payment_method_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return payment_method_id
        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Error creating payment method: {e}")
            return None

    def get_by_id(self, payment_method_id: int) -> Optional[PaymentMethodData]:
        """Gets a payment method by ID.
        
        Args:
            payment_method_id (int): The ID of the payment method to retrieve.

        Returns:
            Optional[PaymentMethodData]: The retrieved payment method, or None if not found.
        """
        query = """
            SELECT payment_type, customer_id
            FROM Payment_Method
            WHERE payment_method_id = %s;
        """
        payment_methods = self._get_payment_methods(query, (payment_method_id,))
        return payment_methods[0] if payment_methods else None

    def get_all(self) -> List[PaymentMethodData]:
        """Gets all payment methods.
        
        Returns:
            List[PaymentMethodData]: A list of all payment methods.
        """
        query = """
            SELECT payment_type, customer_id
            FROM Payment_Method;
        """
        return self._get_payment_methods(query)

    def get_by_customer(self, customer_id: int) -> List[PaymentMethodData]:
        """Gets payment methods for a specific customer.
        
        Args:
            customer_id (int): The ID of the customer to retrieve payment methods for.

        Returns:
            List[PaymentMethodData]: A list of payment methods for the specified customer.
        """
        query = """
            SELECT payment_type, customer_id
            FROM Payment_Method
            WHERE customer_id = %s;
        """
        return self._get_payment_methods(query, (customer_id,))

    def update(self, payment_method_id: int, data: PaymentMethodData) -> bool:
        """Updates a payment method.
        
        Args:
            payment_method_id (int): The ID of the payment method to update.
            data (PaymentMethodData): The new data for the payment method.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        query = """
            UPDATE Payment_Method
            SET payment_type = %s, customer_id = %s
            WHERE payment_method_id = %s;
        """
        values = (data.payment_type, data.customer_id, payment_method_id)
        return self._execute_query(query, values)

    def delete(self, payment_method_id: int) -> bool:
        """Deletes a payment method.
        
        Args:
            payment_method_id (int): The ID of the payment method to delete.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        query = """
            DELETE FROM Payment_Method
            WHERE payment_method_id = %s;
        """
        return self._execute_query(query, (payment_method_id,))