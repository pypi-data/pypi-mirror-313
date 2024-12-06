#!/usr/bin/env python3


"""
Database Module for IEEE Papers Mapper
======================================

This module manages the SQLite database used by the IEEE Papers Mapper project.
It provides functionality to initialize the database, create tables, and insert
data such as papers, authors, index terms, prompts, and classification results.

Classes:
    Database: A class that handles all database operations, including table
              creation, data insertion, and connection management.

Functions:
    - initialize: Creates tables in the database if they don't exist.
    - insert_paper: Inserts paper metadata into the `papers` table.
    - insert_authors: Inserts authors associated with a paper into the `authors` table.
    - insert_index_terms: Adds index terms for a paper into the `index_terms` table.
    - insert_prompt: Stores prompts related to a paper.
    - insert_full_paper: Inserts a complete paper along with its associated data.
"""


import os
import sqlite3
import logging
import pandas as pd
from typing import Optional
from ..config import config as cfg

logger = logging.getLogger("ieee_logger")


class Database:
    def __init__(self, name: str, filepath: Optional[str] = None):
        if filepath is None:
            self.db_name = f"{name}.db"
        else:
            self.db_name = os.path.join(filepath, f"{name}.db")
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.expected_tables = cfg.DB_TABLES

    @property
    def file_exists(self) -> bool:
        """
        Check if the database exists.

        Returns:
            bool: True if the database exists, False otherwise.
        """
        return os.path.exists(os.path.join(cfg.SRC_DIR, self.db_name))

    def get_existing_tables(self):
        if not self.file_exists:
            return []
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        existing_tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return existing_tables

    def initialize(self):
        if not self.file_exists:
            # Create new database file and all tables
            logger.info("Database file doesn't exist, creating from scratch...")
            self.create_all_tables()
        else:
            # Database file exists, check for missing tables
            existing_tables = self.get_existing_tables()
            missing_tables = set(self.expected_tables) - set(existing_tables)
            logger.info(
                f"Database file exists, creating missing tables: {missing_tables}"
            )
            if missing_tables:
                self.create_tables(missing_tables)

    def create_all_tables(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Create all tables
        self.create_tables(self.expected_tables, cursor)

        conn.commit()
        conn.close()

    def create_tables(self, tables, cursor=None):
        if cursor is None:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
        else:
            conn = None

        for table in tables:
            if table == "papers":
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS papers (
                        paper_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        is_number TEXT,
                        insert_date DATE,
                        publication_year INTEGER,
                        download_count INTEGER,
                        citing_patent_count INTEGER,
                        title TEXT,
                        abstract TEXT
                    )
                """
                )
            elif table == "authors":
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS authors (
                        author_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        paper_id INTEGER,
                        name TEXT,
                        affiliation TEXT,
                        FOREIGN KEY(paper_id) REFERENCES papers(paper_id)
                    )
                """
                )
            elif table == "index_terms":
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS index_terms (
                        index_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        paper_id INTEGER,
                        term_type TEXT,
                        term TEXT,
                        FOREIGN KEY(paper_id) REFERENCES papers(paper_id)
                    )
                """
                )
            elif table == "prompts":
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS prompts (
                        prompt_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        paper_id INTEGER,
                        prompt_text TEXT,
                        FOREIGN KEY(paper_id) REFERENCES papers(paper_id)
                    )
                """
                )
            elif table == "classification":
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS classification (
                        classification_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        paper_id INTEGER,
                        category TEXT,
                        confidence REAL,
                        FOREIGN KEY(paper_id) REFERENCES papers(paper_id)
                    )
                    """
                )

        if conn:
            conn.commit()
            conn.close()
            logger.info(f"Database '{self.db_name}' initialized successfully.")

    @property
    def is_connected(self) -> bool:
        if self.connection is None:
            return False
        return True

    def connect(self) -> bool:
        """
        Connect to the database if not already connected.
        """
        if not self.is_connected:
            self.connection = sqlite3.connect(self.db_name)
        return self.connection is not None

    def close(self) -> None:
        """
        Close the database connection.
        """
        if self.is_connected:
            self.connection.close()
            self.connection = None
            logger.info("Database connection closed.")

    def paper_exists(self, is_number: str) -> bool:
        """
        Check if a paper with the given is_number exists in the database.

        Parameters:
            is_number (str): Unique identifier for the paper.

        Returns:
            bool: True if the paper exists, False otherwise.
        """
        query = "SELECT 1 FROM papers WHERE is_number = ?"
        self.cursor.execute(query, (is_number,))
        return self.cursor.fetchone() is not None

    def insert_paper(self, paper_data: dict) -> int:
        """
        Insert a paper into the papers table and return its paper_id.

        Parameters:
            paper_data (dict): Dictionary containing paper metadata.

        Returns:
            int: The paper_id of the inserted paper.
        """
        query = """
        INSERT INTO papers (is_number, insert_date, publication_year, download_count,
                            citing_patent_count, title, abstract)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(
            query,
            (
                paper_data["is_number"],
                paper_data["insert_date"],
                paper_data["publication_year"],
                paper_data["download_count"],
                paper_data["citing_patent_count"],
                paper_data["title"],
                paper_data["abstract"],
            ),
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def insert_authors(self, paper_id: int, authors: list):
        """
        Insert authors into the authors table.

        Parameters:
            paper_id (int): The ID of the associated paper.
            authors (list): List of dictionaries containing author data.
        """
        query = """
        INSERT INTO authors (paper_id, name, affiliation)
        VALUES (?, ?, ?)
        """
        for author in authors:
            self.cursor.execute(
                query,
                (paper_id, author["author_full_name"], author["author_affiliation"]),
            )
        self.connection.commit()

    def insert_index_terms(self, paper_id: int, term_type: str, terms: list):
        """
        Insert index terms into the index_terms table.

        Parameters:
            paper_id (int): The ID of the associated paper.
            term_type (str): The type of index term (e.g., 'author', 'ieee', 'dynamic').
            terms (list): List of terms.
        """
        query = """
        INSERT INTO index_terms (paper_id, term_type, term)
        VALUES (?, ?, ?)
        """
        for term in terms:
            self.cursor.execute(query, (paper_id, term_type, term))
        self.connection.commit()

    def insert_prompt(self, paper_id: int, prompt: str):
        """
        Insert a prompt into the prompts table.

        Parameters:
            paper_id (int): The ID of the associated paper.
            prompt (str): The prompt text.
        """
        query = "INSERT INTO prompts (paper_id, prompt_text) VALUES (?, ?)"
        self.cursor.execute(query, (paper_id, prompt))
        self.connection.commit()

    def insert_full_paper(self, row: pd.Series):
        """
        Insert a full paper, including all related data, into the database.

        Parameters:
            row (pd.Series): A row from the processed DataFrame.
        """
        if self.paper_exists(row["is_number"]):
            logger.warning(
                f"Paper with is_number {row['is_number']} already exists. Skipping."
            )
            return

        # Insert main paper metadata
        paper_data = row[
            [
                "is_number",
                "insert_date",
                "publication_year",
                "download_count",
                "citing_patent_count",
                "title",
                "abstract",
            ]
        ].to_dict()
        paper_id = self.insert_paper(paper_data)

        # Insert authors
        authors = row["authors"]
        self.insert_authors(paper_id, authors)

        # Insert index terms
        index_terms_types = ["author", "ieee", "dynamic"]
        index_terms_columns = [
            # "index_terms_author",
            "index_terms_ieee",
            "index_terms_dynamic",
        ]
        for term_type, terms_column in zip(index_terms_types, index_terms_columns):
            terms = row[terms_column]
            self.insert_index_terms(paper_id, term_type, terms)

        # Insert prompt
        self.insert_prompt(paper_id, row["prompt"])
