#!/usr/bin/env python3

"""
IEEE Papers Data Extraction Script
==================================
This script retrieves research papers from the IEEE Xplore API based on a specified query.
It supports command-line arguments to customize the query and output file name.

Features:
- Fetch papers from the IEEE Xplore API.
- Save the fetched data as a CSV file.
- Handle API rate limits and errors gracefully.

Dependencies:
- Requests for API calls.
- Pandas for data manipulation.
- Argparse for command-line argument parsing.
"""

import requests
import pandas as pd
import argparse
from ..config import config as cfg
import logging
from typing import Optional

logger = logging.getLogger("ieee_logger")


def get_papers(
    query: str,
    start_year: str,
    api_key: str,
    max_records: int,
    start_record: int,
) -> Optional[pd.DataFrame]:
    """
    Fetches research papers from the IEEE Xplore API.

    Parameters:
    ----------
    query : str
        The search query for the API.
    start_year : str
        The starting year for the search.
    api_key : str
        The API key for authenticating the request.
    max_records : int
        Maximum number of records to fetch per request (maximum allowed: 200).
    start_record : int
        The starting record for pagination.

    Returns:
    -------
    Optional[pd.DataFrame]
        A DataFrame containing the retrieved articles if successful, otherwise None.

    Raises:
    ------
    requests.exceptions.HTTPError
        If the HTTP request returns an unsuccessful status code.
    requests.exceptions.RequestException
        For other network-related errors.
    """
    params = {
        "apikey": api_key,
        "format": "json",
        "content_type": "Journals",
        "start_year": start_year,
        "max_records": max_records,
        "sort_field": "article_number",
        "sort_order": "asc",
        "querytext": query,
        "start_record": start_record,
    }

    try:
        response = requests.get(cfg.BASE_URL, params=params)
        response.raise_for_status()
        papers = response.json().get("articles", [])
        if not papers:
            logger.info(f"No data fetched for query: {query}")
            return None

        # Convert the list of articles to a DataFrame
        df = pd.json_normalize(papers)
        logger.info(f"Successfully fetched {len(df)} articles for query: {query}")
        return df

    except requests.exceptions.HTTPError as http_err:
        logger.warning(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.warning(f"Request error occurred: {req_err}")
    except KeyError:
        logger.warning("No articles found in the API response.")
    return None


if __name__ == "__main__":
    """
    Main entry point for the script.

    Allows users to specify a query and optionally a filename via command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Extract research papers from IEEE Xplore API."
    )
    parser.add_argument(
        "-q",
        "--query",
        required=True,
        type=str,
        help="The search query for the data extraction (e.g., 'energy', 'machine learning').",
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="Optional: The name of the CSV file to save the results. Defaults to the query name.",
    )
    args = parser.parse_args()
