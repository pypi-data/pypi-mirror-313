#!/usr/bin/env python3

import pytest
import pandas as pd
from src.ieee_papers_mapper.data.classify_papers import classify_text, classify_all_papers


@pytest.fixture
def mock_prompt_data():
    data = {"paper_id": [1], "prompt_text": ["Sample Title and Abstract"]}
    return pd.DataFrame(data)


def test_classify_text(mocker):
    mocker.patch(
        "src.ieee_papers_mapper.data.classify_papers.classifier",
        return_value={"labels": ["Category 1", "Category 2"], "scores": [0.9, 0.1]},
    )
    result = classify_text("Sample prompt")
    assert result[0][0] == "Category 1"
    assert result[0][1] == 0.9


def test_classify_all_papers(mock_prompt_data, mocker):
    mocker.patch(
        "src.ieee_papers_mapper.data.classify_papers.classify_text", return_value=[("Category 1", 0.95)]
    )
    df_classified = classify_all_papers(mock_prompt_data)
    assert len(df_classified) == 1
    assert df_classified["category"].iloc[0] == "Category 1"
