import sqlite3
import os

class SQLiteDatabase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def create_table(self, table_name, columns):
        columns_with_types = ', '.join(f"{col} {col_type}" for col, col_type in columns.items())
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types})")
        self.connection.commit()


    def insert_data(self, table_name, data):
        if not isinstance(data, (tuple, list)):
            raise TypeError("Data must be a tuple or list.")

        if not data:
            raise ValueError("Data cannot be empty.")

        placeholders = ', '.join('?' * len(data))
        try:
            self.cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", tuple(data))
            self.connection.commit()
        except sqlite3.IntegrityError as e:
            raise ValueError("Integrity error: " + str(e))
        except sqlite3.OperationalError as e:
            raise ValueError("Operational error: " + str(e))



    def update_data(self, table_name, set_values, condition):
        set_clause = ', '.join(f"{col} = ?" for col in set_values.keys())
        condition_clause = ' AND '.join(f"{col} = ?" for col in condition.keys())
        values = list(set_values.values()) + list(condition.values())
        self.cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE {condition_clause}", values)
        self.connection.commit()

    def delete_data(self, table_name, condition):
        condition_clause = ' AND '.join(f"{col} = ?" for col in condition.keys())
        self.cursor.execute(f"DELETE FROM {table_name} WHERE {condition_clause}", tuple(condition.values()))
        self.connection.commit()

    def fetch_data(self, table_name, condition=None):
        if condition:
            condition_clause = ' AND '.join(f"{col} = ?" for col in condition.keys())
            self.cursor.execute(f"SELECT * FROM {table_name} WHERE {condition_clause}", tuple(condition.values()))
        else:
            self.cursor.execute(f"SELECT * FROM {table_name}")
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()

    @staticmethod
    def create_database(db_name):
        if not os.path.exists(db_name):
            open(db_name, 'a').close()

