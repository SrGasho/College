from typing import List, Optional
from pydantic import BaseModel, EmailStr, validator
from datetime import date

from connections import PostgresDatabaseConnection

class CustomerData(BaseModel):
    """Data structure for Customer."""
    full_name: str
    email: EmailStr
    shipping_address: str
    phone: str
    registration_date: date

class CustomerCRUD:

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

    def _get_customers(self, query: str, values: tuple = None) -> List[CustomerData]:
        """Executes a query and returns a list of CustomerData objects.
        
        Args:
            query (str): The SQL query to execute.
            values (tuple, optional): The values to use in the query.

        Returns:
            List[CustomerData]: A list of CustomerData objects.
        """
        customers = []
        try:
            cursor = self.db_connection.connection.cursor()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            customer_list = cursor.fetchall()
            cursor.close()
            for customer_data in customer_list:
                customer_dict = {
                    "full_name": customer_data[0],
                    "email": customer_data[1],
                    "shipping_address": customer_data[2],
                    "phone": customer_data[3],
                    "registration_date": customer_data[4]  # No need for strftime here
                }
                customers.append(CustomerData(**customer_dict))
            return customers
        except Exception as e:
            print(f"Error in query: {e}")
            return []  # Or raise the exception if you prefer

    def create(self, data: CustomerData) -> Optional[int]:
        """Creates a new customer.
        
        Args:
            data (CustomerData): The data for the new customer.

        Returns:
            Optional[int]: The ID of the created customer, or None if there was an error.
        """
        query = """
            INSERT INTO Customer (full_name, email, shipping_address, phone, registration_date)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING customer_id;
        """
        values = (data.full_name, data.email, data.shipping_address, data.phone, data.registration_date.strftime('%Y-%m-%d'))
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            customer_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return customer_id
        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Error creating customer: {e}")
            return None

    def get_by_id(self, customer_id: int) -> Optional[CustomerData]:
        """Gets a customer by ID.
        
        Args:
            customer_id (int): The ID of the customer to retrieve.

        Returns:
            Optional[CustomerData]: The retrieved customer, or None if not found.
        """
        query = """
            SELECT full_name, email, shipping_address, phone, registration_date
            FROM Customer
            WHERE customer_id = %s;
        """
        customers = self._get_customers(query, (customer_id,))
        return customers[0] if customers else None

    def get_all(self) -> List[CustomerData]:
        """Gets all customers.
        
        Returns:
            List[CustomerData]: A list of all customers.
        """
        query = """
            SELECT full_name, email, shipping_address, phone, registration_date
            FROM Customer;
        """
        return self._get_customers(query)

    def get_by_email(self, email: str) -> Optional[CustomerData]:
        """Gets a customer by email.
        
        Args:
            email (str): The email of the customer to retrieve.

        Returns:
            Optional[CustomerData]: The retrieved customer, or None if not found.
        """
        query = """
            SELECT full_name, email, shipping_address, phone, registration_date
            FROM Customer
            WHERE email = %s;
        """
        customers = self._get_customers(query, (email,))
        return customers[0] if customers else None

    def get_by_name(self, full_name: str) -> List[CustomerData]:
        """Gets customers by name (case-insensitive search).
        
        Args:
            full_name (str): The name of the customer to search for.

        Returns:
            List[CustomerData]: A list of customers that match the search criteria.
        """
        query = """
            SELECT full_name, email, shipping_address, phone, registration_date
            FROM Customer
            WHERE LOWER(full_name) LIKE LOWER(%s);
        """
        return self._get_customers(query, ("%" + full_name + "%",))

    def update(self, customer_id: int, data: CustomerData) -> bool:
        """Updates a customer.
        
        Args:
            customer_id (int): The ID of the customer to update.
            data (CustomerData): The new data for the customer.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        query = """
            UPDATE Customer
            SET full_name = %s, email = %s, shipping_address = %s, phone = %s, registration_date = %s
            WHERE customer_id = %s;
        """
        values = (data.full_name, data.email, data.shipping_address, data.phone, data.registration_date.strftime('%Y-%m-%d'), customer_id)
        return self._execute_query(query, values)

    def delete(self, customer_id: int) -> bool:
        """Deletes a customer.
        
        Args:
            customer_id (int): The ID of the customer to delete.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        query = """
            DELETE FROM Customer
            WHERE customer_id = %s;
        """
        return self._execute_query(query, (customer_id,))