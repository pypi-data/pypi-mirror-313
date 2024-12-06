#!/usr/bin/env python3

import pytest
import pandas as pd
from src.ieee_papers_mapper.data.process_papers import process_papers


@pytest.fixture
def sample_raw_data():
    data = {
        "is_number": ["12345"],
        "insert_date": ["20240101"],
        "publication_year": ["2020"],
        "download_count": [10],
        "citing_patent_count": [2],
        "title": ["Sample Title"],
        "abstract": ["Sample Abstract"],
        # "index_terms.author_terms.terms": ['["term1", "term2"]'],
        "index_terms.ieee_terms.terms": ['["term3", "term4"]'],
        "index_terms.dynamic_index_terms.terms": ['["term5"]'],
        "authors.authors": [
            '[{"id": "1", "full_name": "Author 1", "affiliation": "Affiliation 1"}]'
        ],
    }
    return pd.DataFrame(data)


def test_process_papers(sample_raw_data):
    df_processed = process_papers(sample_raw_data)
    assert "prompt" in df_processed.columns
    assert df_processed["prompt"].iloc[0].startswith("title: Sample Title")
    # assert df_processed["index_terms_author"].iloc[0] == ["term1", "term2"]
