import mysql.connector
from mysql.connector import Error

class MySQLDatabase:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

        self.connect()

    def connect(self):
        """Establish a connection to the MySQL database."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                db_info = self.connection.get_server_info()
                print("Connected to MySQL database... MySQL Server version: ", db_info)
                self.cursor = self.connection.cursor()
                self.cursor.execute("SELECT DATABASE();")
                record = self.cursor.fetchone()
                print("You're connected to the database: ", record)
        except Error as e:
            print("Error while connecting to MySQL", e)

    def disconnect(self):
        """Close the connection to the MySQL database."""
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("MySQL connection is closed")

    def create_job_list_table(self):
        """Create a new table 'job_list' in the database with the specified schema."""
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS job_list (
              job_role TEXT NOT NULL,
              company TEXT NOT NULL,
              url TEXT NOT NULL,
              location TEXT NOT NULL,
              is_top_candidate BOOLEAN NOT NULL DEFAULT FALSE,
              is_easy_appy BOOLEAN NOT NULL DEFAULT FALSE,
              application_age TEXT NOT NULL,
              description TEXT NOT NULL,
              time_added DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
              PRIMARY KEY (job_role)
            );
            """
            self.cursor.execute(create_table_query)
            print("Table 'job_list' created successfully.")
        except Error as e:
            print("Failed to create table 'job_list'. Error:", e)

    def delete_table(self, table_name):
        """Delete a table from the database."""
        try:
            delete_table_query = f"DROP TABLE IF EXISTS {table_name}"
            self.cursor.execute(delete_table_query)
            print(f"Table '{table_name}' deleted successfully.")
        except Error as e:
            print(f"Failed to delete table {table_name}. Error: {e}")

    def insert_row(self, table_name, columns, values):
        """Insert a row into the table."""
        try:
            insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
            self.cursor.execute(insert_query)
            self.connection.commit()
            print(f"Row inserted into {table_name}.")
        except Error as e:
            print(f"Failed to insert row into {table_name}. Error: {e}")

    def delete_row(self, table_name, condition):
        """Delete a row from the table."""
        try:
            delete_query = f"DELETE FROM {table_name} WHERE {condition}"
            self.cursor.execute(delete_query)
            self.connection.commit()
            print(f"Row deleted from {table_name} where {condition}.")
        except Error as e:
            print(f"Failed to delete row from {table_name}. Error: {e}")

    def update_row(self, table_name, updates, condition):
        """Update a row in the table."""
        try:
            update_query = f"UPDATE {table_name} SET {updates} WHERE {condition}"
            self.cursor.execute(update_query)
            self.connection.commit()
            print(f"Row in {table_name} updated where {condition}.")
        except Error as e:
            print(f"Failed to update row in {table_name}. Error: {e}")

# Example usage:
if __name__ == "__main__":
    db = MySQLDatabase(
        host='sql.freedb.tech',
        port=3306,
        database='freedb_linkedinsites',
        user='freedb_manny',
        password='deK&Uy4%5*XGnRh'
    )

    db.connect()


    # Create the 'job_list' table
    db.create_job_list_table()
