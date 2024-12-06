#!/usr/bin/env python3

"""
IEEE Papers Pipeline Script
===========================
This script automates the process of fetching, processing, classifying, and storing research papers from the IEEE Xplore API.

Pipeline Overview:
1. Incrementally fetch new papers based on categories.
2. Preprocess raw data for further analysis.
3. Classify papers into predefined categories.
4. Store results in an SQLite database.
5. Track progress using a JSON file for incremental data retrieval.

Features:
- Handles incremental fetching using the `start_record` parameter.
- Classifies papers using an encoder-based transformer model.
- Stores data persistently in an SQLite database.
- Progress tracking via a JSON file.
"""

import os
import json
import logging
import pandas as pd
from ..config import config as cfg
from data.database import Database
from data.get_papers import get_papers
from data.process_papers import process_papers
from data.classify_papers import classify_all_papers

logger = logging.getLogger("ieee_logger")


def run_pipeline():
    """
    Executes the full data pipeline:
    1. Fetch new papers incrementally.
    2. Preprocess and classify them.
    3. Store final results in the database.

    Returns:
    -------
    bool
        True if new papers were processed, False otherwise.

    TODO: Handle whether query limit has been reached
    """
    db = Database(
        name="ieee_papers",
        filepath=os.path.join(cfg.SRC_DIR),
    )
    logger.debug("Initializing database...")
    db.initialize()  # Handles cases where db doesn't exist or not all tables

    progress = load_progress(cfg.JSON_FILENAME)
    new_papers_retrieved = False

    for category in cfg.CATEGORIES[:-1]:  # Skip last category, assume it's "others"
        # Returns start_record, default to 1 if entry doesn't exist (will be saved)
        start_record = progress.get(category, 1)

        # Get new papers
        while True:
            logger.debug(f"Fetching IEEE data for category '{category}', start_record={start_record}...")
            df_raw = get_papers(
                query=category,
                api_key=cfg.IEEE_API_KEY,
                start_year=cfg.IEEE_API_START_YEAR,
                start_record=start_record,  # Incremental
                max_records=cfg.IEEE_API_MAX_RECORDS,
            )

            # For debug, manually give file, again in DataFrame format
            # df_raw = pd.read_csv("/home/alex-anast/workspace/ieee-papers-mapper/data/raw/machine_learning_small.csv")

            if df_raw.empty:
                logger.info(f"No new papers found for category: '{category}'")
                break
            # True if anything has been returned for any category
            new_papers_retrieved = True

            # Process data
            logger.debug("Processing retrieved papers...")
            df_processed = process_papers(df_raw)

            # Insert new data into the database
            logger.debug("Storing data in SQLite database...")
            for _, row in df_processed.iterrows():
                try:
                    db.insert_full_paper(row)
                except Exception as e:
                    logger.error(
                        f"Error inserting paper with is_number {row['is_number']}: {e}"
                    )

            start_record += cfg.IEEE_API_MAX_RECORDS
            progress[category] = start_record
            save_progress(cfg.JSON_FILENAME, progress)

            if len(df_raw) < cfg.IEEE_API_MAX_RECORDS:
                logger.info(f"Completed retrieval for category '{category}'.")
                break

    # Classify newly retrieved papers by comparing the unique ID
    logger.debug("Classifying unclassified papers...")
    _classify_new_unclassified_papers(db)
    db.close()
    return new_papers_retrieved


def _classify_new_unclassified_papers(db: Database) -> None:
    """
    Classifies unclassified papers and updates the database.

    Parameters:
    ----------
    db : Database
        The active database connection to query and store classified data.
    """
    df_unclassified = pd.read_sql_query(
        sql="""
            SELECT p.paper_id, pr.prompt_text
            FROM papers p
            JOIN prompts pr ON p.paper_id = pr.paper_id
            WHERE NOT EXISTS (
                SELECT 1 FROM classification c WHERE c.paper_id = p.paper_id
            )
        """,
        con=db.connection,
    )
    if df_unclassified.empty:
        logger.warning("No unclassified papers found. Should not have arrived here.")
        return
    else:
        df_classified = classify_all_papers(df_unclassified, timer=True)
        df_classified.to_sql("classification", db.connection, if_exists="append", index=False)
        logger.info(f"Classified and stored {len(df_classified)} papers.")


def load_progress(filename: str):
    """
    Load the progress tracking JSON file.

    Parameters:
    ----------
    filename : str
        The name of the JSON file storing progress data.

    Returns:
    -------
    dict
        A dictionary where each category maps to its last fetched `start_record`.
    """
    fn_path = os.path.join(cfg.CONFIG_DIR, filename)
    if not os.path.exists(fn_path):
        logger.warning(f"File {filename} not found, returning nothing.")
        return {}
    with open(fn_path, "r") as file:
        response = json.load(file)
        return response


def save_progress(filename: str, progress) -> None:
    """
    Save progress tracking data to a JSON file.

    Parameters:
    ----------
    filename : str
        The name of the JSON file to save progress.
    progress : dict
        A dictionary mapping each category to its current `start_record`.
    """
    fn_path = os.path.join(cfg.CONFIG_DIR, filename)
    with open(fn_path, "w") as file:
        json.dump(progress, file, indent=4)
