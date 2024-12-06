#!/usr/bin/env python3

import pytest
from src.ieee_papers_mapper.data.database import Database


@pytest.fixture
def db(tmp_path):
    """Fixture to create a temporary database for testing."""
    db_path = tmp_path / "test_ieee_papers.db"
    db = Database(name="test_ieee_papers", filepath=str(tmp_path))
    db.initialize()
    return db


def test_create_tables(db):
    db.create_all_tables()
    existing_tables = db.get_existing_tables()
    assert "papers" in existing_tables
    assert "authors" in existing_tables
    assert "classification" in existing_tables

def test_insert_paper(db):
    paper_data = {
        "is_number": "12345",
        "insert_date": "2024-01-01",
        "publication_year": "2023",
        "download_count": 10,
        "citing_patent_count": 2,
        "title": "Sample Paper",
        "abstract": "Sample Abstract",
    }
    paper_id = db.insert_paper(paper_data)
    assert paper_id > 0
    result = db.cursor.execute(
        "SELECT * FROM papers WHERE paper_id = ?", (paper_id,)
    ).fetchone()
    assert result[1] == "12345"
