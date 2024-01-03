import mysql.connector

class Kontrol_Acara:
    def __init__(self, db_config):
        self.db_config = db_config
        self.connection = None

    def connect_to_database(self):
        try:
            self.connection = mysql.connector.connect(**self.db_config)
        except mysql.connector.Error as err:
            print(f"Error connecting to the database: {err}")

    def close_database_connection(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect_to_database()

            with self.connection.cursor() as cursor:
                if params is not None:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

                data = cursor.fetchall()
                if not data:
                    print("No data matching the filter criteria.")
                return data

        except mysql.connector.Error as err:
            print(f"MySQL error: {err}")
            print(f"Failed query: {query}")
            return None
        except Exception as e:
            print(f"Error: {str(e)}")
            return None
        finally:
            self.close_database_connection()

    def get_acara_by_filter_type(self, filter_type):
        if filter_type == "Harian":
            query = "SELECT * FROM acara WHERE Tanggal = CURDATE()"
        elif filter_type == "Mingguan":
            query = "SELECT * FROM acara WHERE Tanggal BETWEEN CURDATE() AND CURDATE() + INTERVAL 6 DAY"
        elif filter_type == "Bulanan":
            query = "SELECT * FROM acara WHERE Tanggal BETWEEN CURDATE() AND CURDATE() + INTERVAL 29 DAY"
        else:
            query = "SELECT * FROM acara"

        return self.execute_query(query)

    def get_data_database(self, nama_acara):
        query = "SELECT * FROM acara WHERE Nama_Acara = %s"
        return self.execute_query(query, (str(nama_acara),))

    def update_data_in_database(self, nama_acara, updated_data):
        query = "UPDATE acara SET Nama_Acara = %s, Tanggal = %s, Waktu = %s, Deskripsi_Acara = %s WHERE Nama_Acara = %s"

        # Ensure that the values are properly formatted for SQL
        updated_values = (
            updated_data.get("Nama_Acara", ""),
            updated_data.get("Tanggal", ""),
            updated_data.get("Waktu", ""),
            updated_data.get("Deskripsi_Acara", "")
        )
        # Print the data before the update
        select_query = "SELECT * FROM acara WHERE Nama_Acara = %s"
        selected_data = self.get_data_from_database(select_query, (str(nama_acara),))
        print(f"Selected data before update: {selected_data}")

        try:
            if not self.connection or not self.connection.is_connected():
                self.connect_to_database()

            with self.connection.cursor() as cursor:
                print(f"Executing query: {query} with values: {updated_values!r}")
                cursor.execute(query, updated_values + (str(nama_acara),))  # Concatenate the nama_acara to the tuple
            self.connection.commit()
            print("Data updated successfully.")
        except mysql.connector.Error as err:
            print(f"MySQL error: {err}")
            print(f"Failed query: {query} with values: {updated_values!r}")
            raise  # Reraise the exception to see the full traceback
        finally:
            # Always close the connection in the finally block
            self.close_database_connection()

    def delete_data_in_database(self, nama_acara):
        query = "DELETE FROM acara WHERE Nama_Acara = %s"

        try:
            if not self.connection or not self.connection.is_connected():
                self.connect_to_database()

            with self.connection.cursor() as cursor:
                cursor.execute(query, (str(nama_acara),))
            self.connection.commit()
            print("Data deleted successfully.")
        except mysql.connector.Error as err:
            print(f"MySQL error: {err}")
            print(f"Failed query: {query} with value: {nama_acara!r}")
            raise  # Reraise the exception to see the full traceback
        finally:
            self.close_database_connection()

    def get_data_for_detail_acara(self, event_name):
        # Fungsi khusus untuk mendapatkan data untuk Detail Acara
        query = "SELECT * FROM acara WHERE Nama_Acara = %s"
        return self.execute_query(query, (event_name,))

    def get_data_from_database(self, query, query_params=None):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect_to_database()

            with self.connection.cursor() as cursor:
                print(f"Executing query: {query} with params: {query_params}")
                if query_params is not None:
                    cursor.execute(query, query_params)
                else:
                    cursor.execute(query)

                data = cursor.fetchall()
                if not data:
                    print("No data matching the filter criteria.")
                return data

        except mysql.connector.Error as err:
            print(f"MySQL error: {err}")
            print(f"Failed query: {query}")
            return None
        except Exception as e:
            print(f"Error: {str(e)}")
            return None
        finally:
            self.close_database_connection()