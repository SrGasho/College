from typing import List, Optional
from pydantic import BaseModel
from datetime import date
from connections import PostgresDatabaseConnection

class CouponsData(BaseModel):
    """Data structure for Coupons."""
    discount_code: str
    discount_value: float
    expiration_date: date

class CouponsCRUD:
    def __init__(self):
        """Initialize the database connection."""
        self.db_connection = PostgresDatabaseConnection()
        self.db_connection.connect()

    def _execute_query(self, query: str, values: tuple = None) -> bool:
        """Executes a query in the database.
        
        Args:
            query (str): The SQL query to execute.
            values (tuple, optional): The values to use in the query.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
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

    def _get_coupons(self, query: str, values: tuple = None) -> List[CouponsData]:
        """Executes a query and returns a list of CouponsData objects.
        
        Args:
            query (str): The SQL query to execute.
            values (tuple, optional): The values to use in the query.

        Returns:
            List[CouponsData]: A list of CouponsData objects.
        """
        coupons = []
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values if values else ())
            coupon_list = cursor.fetchall()
            cursor.close()
            for coupon in coupon_list:
                coupon_dict = {
                    "discount_code": coupon[0],
                    "discount_value": coupon[1],
                    "expiration_date": coupon[2]
                }
                coupons.append(CouponsData(**coupon_dict))
            return coupons
        except Exception as e:
            print(f"Error fetching coupon data: {e}")
            return []

    def create(self, data: CouponsData) -> Optional[int]:
        """Creates a new coupon entry.
        
        Args:
            data (CouponsData): The data for the new coupon.

        Returns:
            Optional[int]: The ID of the created coupon, or None if there was an error.
        """
        query = """
            INSERT INTO Coupons (discount_code, discount_value, expiration_date)
            VALUES (%s, %s, %s)
            RETURNING coupons_id;
        """
        values = (
            data.discount_code,
            data.discount_value,
            data.expiration_date.strftime('%Y-%m-%d')
        )
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            coupons_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return coupons_id
        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Error creating coupon: {e}")
            return None

    def get_by_id(self, coupons_id: int) -> Optional[CouponsData]:
        """Gets a coupon by ID.
        
        Args:
            coupons_id (int): The ID of the coupon to retrieve.

        Returns:
            Optional[CouponsData]: The retrieved coupon, or None if not found.
        """
        query = """
            SELECT discount_code, discount_value, expiration_date
            FROM Coupons
            WHERE coupons_id = %s;
        """
        coupons = self._get_coupons(query, (coupons_id,))
        return coupons[0] if coupons else None

    def get_all(self) -> List[CouponsData]:
        """Gets all coupons.
        
        Returns:
            List[CouponsData]: A list of all coupons.
        """
        query = """
            SELECT discount_code, discount_value, expiration_date
            FROM Coupons;
        """
        return self._get_coupons(query)

    def update(self, coupons_id: int, data: CouponsData) -> bool:
        """Updates a coupon entry.
        
        Args:
            coupons_id (int): The ID of the coupon to update.
            data (CouponsData): The new data for the coupon.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        query = """
            UPDATE Coupons
            SET discount_code = %s, discount_value = %s, expiration_date = %s
            WHERE coupons_id = %s;
        """
        values = (
            data.discount_code,
            data.discount_value,
            data.expiration_date.strftime('%Y-%m-%d'),
            coupons_id
        )
        return self._execute_query(query, values)

    def delete(self, coupons_id: int) -> bool:
        """Deletes a coupon entry.
        
        Args:
            coupons_id (int): The ID of the coupon to delete.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        query = """
            DELETE FROM Coupons
            WHERE coupons_id = %s;
        """
        return self._execute_query(query, (coupons_id,))

    def get_by_code(self, discount_code: str) -> Optional[CouponsData]:
        """Gets a coupon by discount code.
        
        Args:
            discount_code (str): The discount code of the coupon to retrieve.

        Returns:
            Optional[CouponsData]: The retrieved coupon, or None if not found.
        """
        query = """
            SELECT discount_code, discount_value, expiration_date
            FROM Coupons
            WHERE discount_code = %s;
        """
        coupons = self._get_coupons(query, (discount_code,))
        return coupons[0] if coupons else None