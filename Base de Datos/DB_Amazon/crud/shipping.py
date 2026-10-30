from typing import List, Optional
from pydantic import BaseModel
from datetime import date
from connections import PostgresDatabaseConnection

class ShippingData(BaseModel):
    """Data structure for Shipping."""
    shipping_company: str
    shipping_date: Optional[date] = None  # Date instead of str
    estimated_delivery: Optional[date] = None  # Date instead of str
    shipping_cost: Optional[float] = None

class ShippingCRUD:
    def __init__(self):
        """Initialize the database connection."""
        self.db_connection = PostgresDatabaseConnection()
        self.db_connection.connect()

    def _execute_query(self, query: str, values: tuple = None) -> bool:
        """Executes a query in the database."""
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values if values else ())
            self.db_connection.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error in database operation: {e}")
            self.db_connection.connection.rollback()
            return False

    def _get_shippings(self, query: str, values: tuple = None) -> List[ShippingData]:
        """Executes a query and returns a list of ShippingData objects."""
        shippings = []
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values if values else ())
            shipping_list = cursor.fetchall()
            cursor.close()
            for shipping in shipping_list:
                shipping_dict = {
                    "shipping_company": shipping[0],
                    "shipping_date": shipping[1],
                    "estimated_delivery": shipping[2],
                    "shipping_cost": shipping[3]
                }
                shippings.append(ShippingData(**shipping_dict))
            return shippings
        except Exception as e:
            print(f"Error fetching shipping data: {e}")
            return []

    def create(self, data: ShippingData) -> Optional[int]:
        """Creates a new shipping entry."""
        query = """
            INSERT INTO Shipping (shipping_company, shipping_date, estimated_delivery, shipping_cost)
            VALUES (%s, %s, %s, %s)
            RETURNING shipping_id;
        """
        values = (
            data.shipping_company,
            data.shipping_date.strftime('%Y-%m-%d') if data.shipping_date else None,
            data.estimated_delivery.strftime('%Y-%m-%d') if data.estimated_delivery else None,
            data.shipping_cost
        )
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            shipping_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return shipping_id
        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Error creating shipping entry: {e}")
            return None

    def get_by_id(self, shipping_id: int) -> Optional[ShippingData]:
        """Gets a shipping entry by ID."""
        query = """
            SELECT shipping_company, shipping_date, estimated_delivery, shipping_cost
            FROM Shipping
            WHERE shipping_id = %s;
        """
        shippings = self._get_shippings(query, (shipping_id,))
        return shippings[0] if shippings else None

    def get_all(self) -> List[ShippingData]:
        """Gets all shipping entries."""
        query = """
            SELECT shipping_company, shipping_date, estimated_delivery, shipping_cost
            FROM Shipping;
        """
        return self._get_shippings(query)
    
    def get_by_shipping_company(self, company_name: str) -> List[ShippingData]:
        """Gets all shipping entries by shipping company."""
        query = """
            SELECT shipping_company, shipping_date, estimated_delivery, shipping_cost
            FROM Shipping
            WHERE shipping_company = %s;
        """
        return self._get_shippings(query, (company_name,))
    
    def get_by_shipping_date(self, shipping_date: date) -> List[ShippingData]:
        """Gets all shipping entries by shipping date."""
        query = """
            SELECT shipping_company, shipping_date, estimated_delivery, shipping_cost
            FROM Shipping
            WHERE shipping_date = %s;
        """
        return self._get_shippings(query, (shipping_date.strftime('%Y-%m-%d'),))

    def update(self, shipping_id: int, data: ShippingData) -> bool:
        """Updates a shipping entry."""
        query = """
            UPDATE Shipping
            SET shipping_company = %s, shipping_date = %s, estimated_delivery = %s, shipping_cost = %s
            WHERE shipping_id = %s;
        """
        values = (
            data.shipping_company,
            data.shipping_date.strftime('%Y-%m-%d') if data.shipping_date else None,
            data.estimated_delivery.strftime('%Y-%m-%d') if data.estimated_delivery else None,
            data.shipping_cost,
            shipping_id
        )
        return self._execute_query(query, values)

    def delete(self, shipping_id: int) -> bool:
        """Deletes a shipping entry."""
        query = """
            DELETE FROM Shipping
            WHERE shipping_id = %s;
        """
        return self._execute_query(query, (shipping_id,))