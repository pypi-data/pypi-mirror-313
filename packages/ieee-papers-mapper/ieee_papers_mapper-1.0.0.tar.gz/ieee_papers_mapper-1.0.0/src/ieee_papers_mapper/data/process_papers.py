#!/usr/bin/env python3

"""
IEEE Paper Preprocessor
=======================
This script processes raw CSV files containing IEEE paper data to prepare them for analysis and classification.

Key Functions:
1. Selects relevant columns from the raw data.
2. Converts date formats and processes structured fields (e.g., index terms, authors).
3. Creates a 'prompt' column combining title, abstract, and keywords.
4. Saves the processed data to a specified output directory.

Usage:
    python process_papers.py -f <input_file.csv> [-o <output_directory>]

The processed data is saved with a 'processed_' prefix in the output directory.
"""

import os
import ast
import logging
import pandas as pd
from ..config import config as cfg

logger = logging.getLogger("ieee_logger")


def process_papers(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocesses a DataFrame of IEEE paper data to retain relevant information for classification.

    Parameters:
    ----------
    df_raw : pd.DataFrame
        The raw DataFrame containing IEEE paper data.

    Returns:
    -------
    pd.DataFrame
        A processed DataFrame ready for classification and storage.
    """
    keep_columns = [
        "is_number",
        "insert_date",
        "publication_year",
        "download_count",
        "citing_patent_count",
        "title",
        "abstract",
        # "index_terms.author_terms.terms",
        "index_terms.ieee_terms.terms",
        "index_terms.dynamic_index_terms.terms",
        "authors.authors",
    ]

    # Retain only the columns that exist in df_raw
    existing_columns = [col for col in keep_columns if col in df_raw.columns]
    missing_columns = set(keep_columns) - set(existing_columns)

    if missing_columns:
        logger.warning(f"(!) Missing columns in input data: {missing_columns}")

    df_processed = df_raw[existing_columns].copy()

    # Convert 'insert_date' to ISO8601 format
    df_processed["insert_date"] = pd.to_datetime(
        df_processed["insert_date"], errors="coerce", format="%Y%m%d"
    ).dt.strftime("%Y-%m-%d")

    # Ensure publication_year is str for consistency
    df_processed["publication_year"] = df_processed["publication_year"].astype(str)

    # Transform index_terms columns
    for col in [
        # "index_terms.author_terms.terms",
        "index_terms.ieee_terms.terms",
        "index_terms.dynamic_index_terms.terms",
    ]:
        # TODO: This needs to be replaced. Crashes if data format is not perfect
        df_processed[col] = df_processed[col].apply(_safe_parse_list)

    # Rename index_terms columns
    df_processed.rename(
        columns={
            # "index_terms.author_terms.terms": "index_terms_author",
            "index_terms.ieee_terms.terms": "index_terms_ieee",
            "index_terms.dynamic_index_terms.terms": "index_terms_dynamic",
        },
        inplace=True,
    )

    df_processed["authors"] = df_processed["authors.authors"].apply(_extract_author_info)
    df_processed.drop("authors.authors", axis=1, inplace=True)

    df_processed["prompt"] = df_processed.apply(_create_prompt, axis=1)

    # Reorder columns
    column_order = [
        "is_number",
        "insert_date",
        "publication_year",
        "download_count",
        "citing_patent_count",
        # "index_terms_author",
        "index_terms_ieee",
        "index_terms_dynamic",
        "authors",
        "title",
        "abstract",
        "prompt",
    ]
    df_processed = df_processed[column_order]

    return df_processed


def _safe_parse_list(value: str) -> list:
    """
    Safely parses a string representation of a list into an actual list.

    Parameters:
    ----------
    value : str
        The string to be parsed.

    Returns:
    -------
    list
        Parsed list, or an empty list if parsing fails.
    """
    try:
        return ast.literal_eval(value) if isinstance(value, str) else []
    except (ValueError, SyntaxError) as e:
        logger.warning(f"Failed to parse list: {value}. Error: {e}")
        return []


def _extract_author_info(authors_str: str) -> list:
    """
    Extracts author information from a stringified list.

    Parameters:
    ----------
    authors_str : str
        Stringified list of author dictionaries.

    Returns:
    -------
    list
        A list of dictionaries containing author details.
    """
    authors = _safe_parse_list(authors_str)
    return [
        {
            # Only keeping the "order=1" author
            "author_id": author["id"],
            "author_full_name": author["full_name"],
            "author_affiliation": author["affiliation"],
            # 'author_url': author['authorUrl'],
            # 'author_order': author['author_order'],
            # 'author_affiliations': author['authorAffiliations']['authorAffiliation']
        }
        for author in authors
    ]


def _create_prompt(row: pd.Series) -> str:
    """
    Creates a prompt from a paper's title, abstract, and index terms.

    Parameters:
    ----------
    row : pd.Series
        A row of the DataFrame.

    Returns:
    -------
    str
        A formatted prompt string.
    """
    title = row["title"]
    abstract = row["abstract"]
    # all_terms = row["index_terms_author"] + row["index_terms_ieee"] + row["index_terms_dynamic"]
    all_terms = row["index_terms_ieee"] + row["index_terms_dynamic"]
    index_terms = ", ".join(all_terms)
    return f"title: {title} - abstract: {abstract} - index_terms: {index_terms}"


if __name__ == "__main__":
    """
    If this script is specifically executed, it should be directed to a specific
    `csv` file. To select it, argparse is used.
    """

    import argparse as ag

    parser = ag.ArgumentParser(description="Preprocess IEEE CSV files.")
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        required=True,
        help="The path to the raw CSV file to preprocess",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=os.path.join(cfg.ROOT_DIR, cfg.DATA_PROCESSED_DIR),
        help="The directory to save the processed CSV file",
    )
    args = parser.parse_args()

    if not os.path.exists(args.file):
        raise FileNotFoundError(f"File '{args.file}' does not exist.")

    # Read the input CSV file
    df_raw = pd.read_csv(args.file)

    # Process the papers
    df_processed = process_papers(df_raw)

    # Create the output filename
    input_filename = os.path.basename(args.file)
    output_filename = f"processed_{input_filename}"
    output_path = os.path.join(args.output, output_filename)

    # Ensure the output directory exists
    os.makedirs(args.output, exist_ok=True)

    # Save the processed DataFrame to a CSV file
    df_processed.to_csv(output_path, index=False)

    logger.info(f"Processed file saved to: {output_path}")
