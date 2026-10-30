import psycopg2

class PostgresDatabaseConnection:
    """This class is responsible for connecting to the PostgreSQL database."""

    def __init__(self):
        """Initialize the database connection parameters."""
        self._dbname = "amazon"
        self._duser = "postgres"
        self._dpass = "admin123"
        self._dhost = "localhost"
        self._dport = "5432"
        self.connection = None

    def connect(self):
        """This method connects to the PostgreSQL database."""
        try:
            self.connection = psycopg2.connect(
                dbname=self._dbname,
                user=self._duser,
                password=self._dpass,
                host=self._dhost,
                port=self._dport
            )
            print("✅ Connection successful!")
        except Exception as e:
            print(f"❌ Connection failed: {e}")

    def test_query(self):
        """This method tests a simple query to check the connection."""
        if self.connection:
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
                    tables = cursor.fetchall()
                    print("📋 Tables in 'public' schema:", tables)
            except Exception as e:
                print(f"❌ Query failed: {e}")
        else:
            print("⚠️ No active connection.")

    def close(self):
        """This method closes the database connection."""
        if self.connection:
            self.connection.close()
            print("🔌 Connection closed.")

# Test the connection
if __name__ == "__main__":
    db = PostgresDatabaseConnection()
    db.connect()
    db.test_query()
    db.close()