from typing import List, Optional
from pydantic import BaseModel
from datetime import date
from connections import PostgresDatabaseConnection  # Ensure you import your connection class

class SearchHistoryData(BaseModel):
    """Data structure for SearchHistory."""
    search_term: str
    search_date: date  # ISO 8601 format is recommended (YYYY-MM-DD)
    customer_id: int    # Foreign key

class SearchHistoryCRUD:

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

    def _get_search_history(self, query: str, values: tuple = None) -> List[SearchHistoryData]:
        """Executes a query and returns a list of SearchHistoryData objects."""
        search_history_entries = []
        try:
            cursor = self.db_connection.connection.cursor()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            search_history_list = cursor.fetchall()
            cursor.close()
            for search_history_entry in search_history_list:
                search_history_dict = {
                    "search_term": search_history_entry[0],
                    "search_date": search_history_entry[1],
                    "customer_id": search_history_entry[2]
                }
                search_history_entries.append(SearchHistoryData(**search_history_dict))
            return search_history_entries
        except Exception as e:
            print(f"Error in query: {e}")
            return []  # Or raise the exception if you prefer

    def create(self, data: SearchHistoryData) -> Optional[int]:
        """Creates a new search history entry."""
        query = """
            INSERT INTO search_history (search_term, search_date, customer_id)
            VALUES (%s, %s, %s)
            RETURNING search_history_id;
        """
        values = (data.search_term, data.search_date, data.customer_id)
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            search_history_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return search_history_id
        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Error creating search history entry: {e}")
            return None

    def get_by_id(self, search_history_id: int) -> Optional[SearchHistoryData]:
        """Gets a search history entry by ID."""
        query = """
            SELECT search_term, search_date, customer_id
            FROM search_history
            WHERE search_history_id = %s;
        """
        results = self._get_search_history(query, (search_history_id,))
        return results[0] if results else None  # Returns None if no result, the SearchHistoryData object otherwise

    def get_all(self) -> List[SearchHistoryData]:
        """Gets all search history entries."""
        query = """
            SELECT search_term, search_date, customer_id
            FROM search_history;
        """
        return self._get_search_history(query)

    def get_by_customer(self, customer_id: int) -> List[SearchHistoryData]:
        """Gets search history entries for a specific customer."""
        query = """
            SELECT search_term, search_date, customer_id
            FROM search_history
            WHERE customer_id = %s;
        """
        return self._get_search_history(query, (customer_id,))

    def update(self, search_history_id: int, data: SearchHistoryData) -> bool:
        """Updates a search history entry."""
        query = """
            UPDATE search_history
            SET search_term = %s, search_date = %s, customer_id = %s
            WHERE search_history_id = %s;
        """
        values = (data.search_term, data.search_date, data.customer_id, search_history_id)
        return self._execute_query(query, values)

    def delete(self, search_history_id: int) -> bool:
        """Deletes a search history entry."""
        query = """
            DELETE FROM search_history
            WHERE search_history_id = %s;
        """
        return self._execute_query(query, (search_history_id,))

    def delete_by_customer(self, customer_id: int) -> bool:
        """Deletes all search history entries for a specific customer."""
        query = """
            DELETE FROM search_history
            WHERE customer_id = %s;
        """
        return self._execute_query(query, (customer_id,))