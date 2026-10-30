from typing import List, Optional
from pydantic import BaseModel
from datetime import date
from connections import PostgresDatabaseConnection

class OfferData(BaseModel):
    """Data structure for Offer."""
    discount: float
    start_date: date
    end_date: date

class OfferCRUD:
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

    def _get_offers(self, query: str, values: tuple = None) -> List[OfferData]:
        """Executes a query and returns a list of OfferData objects.
        
        Args:
            query (str): The SQL query to execute.
            values (tuple, optional): The values to use in the query.

        Returns:
            List[OfferData]: A list of OfferData objects.
        """
        offers = []
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values if values else ())
            offer_list = cursor.fetchall()
            cursor.close()
            for offer in offer_list:
                offer_dict = {
                    "discount": offer[0],
                    "start_date": offer[1],
                    "end_date": offer[2]
                }
                offers.append(OfferData(**offer_dict))
            return offers
        except Exception as e:
            print(f"Error fetching offer data: {e}")
            return []

    def create(self, data: OfferData) -> Optional[int]:
        """Creates a new offer.
        
        Args:
            data (OfferData): The data for the new offer.

        Returns:
            Optional[int]: The ID of the created offer, or None if there was an error.
        """
        query = """
            INSERT INTO Offer (discount, start_date, end_date)
            VALUES (%s, %s, %s)
            RETURNING offer_id;
        """
        values = (data.discount, data.start_date.strftime('%Y-%m-%d'), data.end_date.strftime('%Y-%m-%d'))
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            offer_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return offer_id
        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Error creating offer: {e}")
            return None

    def get_by_id(self, offer_id: int) -> Optional[OfferData]:
        """Gets an offer by ID.
        
        Args:
            offer_id (int): The ID of the offer to retrieve.

        Returns:
            Optional[OfferData]: The retrieved offer, or None if not found.
        """
        query = """
            SELECT discount, start_date, end_date
            FROM Offer
            WHERE offer_id = %s;
        """
        offers = self._get_offers(query, (offer_id,))
        return offers[0] if offers else None

    def get_all(self) -> List[OfferData]:
        """Gets all offers.
        
        Returns:
            List[OfferData]: A list of all offers.
        """
        query = """
            SELECT discount, start_date, end_date
            FROM Offer;
        """
        return self._get_offers(query)

    def update(self, offer_id: int, data: OfferData) -> bool:
        """Updates an offer.
        
        Args:
            offer_id (int): The ID of the offer to update.
            data (OfferData): The new data for the offer.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        query = """
            UPDATE Offer
            SET discount = %s, start_date = %s, end_date = %s
            WHERE offer_id = %s;
        """
        values = (data.discount, data.start_date.strftime('%Y-%m-%d'), data.end_date.strftime('%Y-%m-%d'), offer_id)
        return self._execute_query(query, values)

    def delete(self, offer_id: int) -> bool:
        """Deletes an offer.
        
        Args:
            offer_id (int): The ID of the offer to delete.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        query = """
            DELETE FROM Offer
            WHERE offer_id = %s;
        """
        return self._execute_query(query, (offer_id,))