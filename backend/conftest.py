import pytest
import database


@pytest.fixture
def test_db(tmp_path, monkeypatch):
    test_database = tmp_path / "test_intrusion.db"

    monkeypatch.setattr(
        database,
        "DATABASE_NAME",
        str(test_database)
    )

    database.create_table()

    return test_database
