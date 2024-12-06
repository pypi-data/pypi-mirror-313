import sqlite3
import pytest
from endetail_utilities.SQLiteDatabase import SQLiteDatabase  # Adjust the import based on your file structure

class TestSQLiteDatabase:
    @pytest.fixture
    def db(self):
        db = SQLiteDatabase(":memory:")  # Vytvoření databáze v paměti
        yield db
        db.close()

    def test_create_table(self, db):
        db.create_table("users", {"id": "INTEGER PRIMARY KEY", "name": "TEXT"})
        db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        table_exists = db.cursor.fetchone() is not None
        assert table_exists

    def test_insert_data(self, db):
        db.create_table("users", {"id": "INTEGER PRIMARY KEY", "name": "TEXT"})
        db.insert_data("users", (1, "Alice"))
        result = db.fetch_data("users")
        assert result == [(1, "Alice")]

    def test_update_data(self, db):
        db.create_table("users", {"id": "INTEGER PRIMARY KEY", "name": "TEXT"})
        db.insert_data("users", (1, "Alice"))
        db.update_data("users", {"name": "Bob"}, {"id": 1})
        result = db.fetch_data("users")
        assert result == [(1, "Bob")]

    def test_delete_data(self, db):
        db.create_table("users", {"id": "INTEGER PRIMARY KEY", "name": "TEXT"})
        db.insert_data("users", (1, "Alice"))
        db.delete_data("users", {"id": 1})
        result = db.fetch_data("users")
        assert result == []

    def test_fetch_data(self, db):
        db.create_table("users", {"id": "INTEGER PRIMARY KEY", "name": "TEXT"})
        db.insert_data("users", (1, "Alice"))
        db.insert_data("users", (2, "Bob"))
        result = db.fetch_data("users")
        assert result == [(1, "Alice"), (2, "Bob")]

    def test_fetch_data_with_condition(self, db):
        db.create_table("users", {"id": "INTEGER PRIMARY KEY", "name": "TEXT"})
        db.insert_data("users", (1, "Alice"))
        db.insert_data("users", (2, "Bob"))
        result = db.fetch_data("users", {"name": "Alice"})
        assert result == [(1, "Alice")]

    # def test_insert_invalid_data(self, db):
    #     db.create_table("users", {"id": "INTEGER PRIMARY KEY", "name": "TEXT"})
    #     with pytest.raises(sqlite3.IntegrityError):
    #         db.insert_data("users", (None, "Alice"))  # ID cannot be None for PRIMARY KEY

    # def test_update_nonexistent_data(self, db):
    #     db.create_table("users", {"id": "INTEGER PRIMARY KEY", "name": "TEXT"})
    #     with pytest.raises(sqlite3.OperationalError):
    #         db.update_data("users", {"name": "Bob"}, {"id": 999})  # ID 999 does not exist
    #
    # def test_delete_nonexistent_data(self, db):
    #     db.create_table("users", {"id": "INTEGER PRIMARY KEY", "name": "TEXT"})
    #     db.insert_data("users", (1, "Alice"))
    #     with pytest.raises(sqlite3.OperationalError):
    #         db.delete_data("users", {"id": 999})  # ID 999 does not exist
    #
    # def test_insert_into_nonexistent_table(self, db):
    #     with pytest.raises(sqlite3.OperationalError):
    #         db.insert_data("nonexistent_table", (1, "Alice"))  # Table does not exist
