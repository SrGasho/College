from typing import List, Optional
from pydantic import BaseModel

from connections import PostgresDatabaseConnection

class SellerData(BaseModel):
    """Data structure for Seller."""
    seller_name: str
    seller_type: Optional[str] = None
    seller_rating: Optional[float] = None

class SellerCRUD:

    def __init__(self):
        """Initialize the database connection."""
        self.db_connection = PostgresDatabaseConnection()
        self.db_connection.connect()

    def _execute_query(self, query: str, values: tuple = None) -> bool:
        """Execute a query on the database."""
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
        
    def _get_sellers(self, query: str, values: tuple = None) -> List[SellerData]:
        """Executes a query and returns a list of SellerData objects."""
        sellers = []
        try:
            cursor = self.db_connection.connection.cursor()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            seller_list = cursor.fetchall()
            cursor.close()
            for seller in seller_list:
                sellers.append(SellerData(
                    seller_name=seller[0],
                    seller_type=seller[1],
                    seller_rating=seller[2]
                ))
            return sellers
        except Exception as e:
            print(f"Error in query: {e}")
            return []

    def create(self, data: SellerData) -> Optional[int]:
        """Creates a new seller."""
        query = """
            INSERT INTO Seller (seller_name, seller_type, seller_rating)
            VALUES (%s, %s, %s)
            RETURNING seller_id;
        """
        values = (data.seller_name, data.seller_type, data.seller_rating)
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            seller_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return seller_id
        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Error creating seller: {e}")
            return None

    def get_by_id(self, seller_id: int) -> Optional[SellerData]:
        """Get a seller by ID."""
        query = """
            SELECT seller_name, seller_type, seller_rating
            FROM Seller
            WHERE seller_id = %s;
        """
        sellers = self._get_sellers(query, (seller_id,))
        return sellers[0] if sellers else None

    def get_all(self) -> List[SellerData]:
        """Gets all sellers."""
        query = """
            SELECT seller_name, seller_type, seller_rating
            FROM Seller;
        """
        return self._get_sellers(query)

    def update(self, seller_id: int, data: SellerData) -> bool:
        """Updates a seller."""
        query = """
            UPDATE Seller
            SET seller_name = %s, seller_type = %s, seller_rating = %s
            WHERE seller_id = %s;
        """
        values = (data.seller_name, data.seller_type, data.seller_rating, seller_id)
        return self._execute_query(query, values)

    def delete(self, seller_id: int) -> bool:
        """Deletes a seller."""
        query = """
            DELETE FROM Seller
            WHERE seller_id = %s;
        """
        return self._execute_query(query, (seller_id,))

    def get_by_name(self, seller_name: str) -> List[SellerData]:
        """Gets sellers by name."""
        query = """
            SELECT seller_name, seller_type, seller_rating
            FROM Seller
            WHERE LOWER(seller_name) LIKE LOWER(%s);
        """
        return self._get_sellers(query, ("%" + seller_name + "%",))
    
    def get_by_rating(self, seller_rating: float) -> List[SellerData]:
        """Gets sellers by rating (greater than or equal to)."""
        try:
            seller_rating = float(seller_rating)  # Convert to float in case it comes as a string
        except ValueError:
            raise ValueError("seller_rating must be a number between 0 and 5")

        if not (0 <= seller_rating <= 5):
            raise ValueError("seller_rating must be between 0 and 5")

        query = """
            SELECT seller_name, seller_type, seller_rating
            FROM Seller
            WHERE seller_rating >= %s;
        """
        return self._get_sellers(query, (seller_rating,))  # Pass the float value directly