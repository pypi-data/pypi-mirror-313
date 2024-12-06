#!/usr/bin/env python3

import time
import pandas as pd
import logging
from transformers import pipeline
from ..config import config as cfg

logger = logging.getLogger("ieee_logger")


classifier = pipeline("zero-shot-classification", model=cfg.DEBERTA_V3_MODEL_NAME)


def classify_text(text: str, timer: bool = False) -> list:
    """
    Classify a single text into multiple categories.

    Parameters:
        text (str): The input text to classify.

    Returns:
        list: A list of tuples (category, confidence).
    """
    if timer:
        start_time = time.time()

    results = classifier(text, candidate_labels=cfg.CATEGORIES, multi_label=True)

    if timer:
        elapsed_time = time.time() - start_time
        logger.debug(f"Paper's classification time: {elapsed_time:.2f}s")

    return [
        (label, score) for label, score in zip(results["labels"], results["scores"])
    ]


def classify_all_papers(df: pd.DataFrame, timer: bool = False) -> pd.DataFrame:
    """
    Classify all papers and return their classifications.

    Parameters:
        df (pd.DataFrame): DataFrame with `paper_id` and `prompt_text`.

    Returns:
        pd.DataFrame: DataFrame with `paper_id`, `category`, and `confidence`.
    """
    classifications = []
    times = []
    for _, row in df.iterrows():

        if timer:
            start_time = time.time()
        classifications.extend(
            [
                {"paper_id": row["paper_id"], "category": cat, "confidence": conf}
                for cat, conf in classify_text(row["prompt_text"], timer=False)
            ]
        )
        if timer:
            elapsed_time = time.time() - start_time
            times.append(elapsed_time)
    if timer:
        mean_classification_time = sum(times) / df.shape[0]
        logger.debug(f"Mean Paper Classification Time: {mean_classification_time:.2f}s")
        logger.debug(f"Total Elapsed Classification Time: {sum(times):.2f}s")
    return pd.DataFrame(classifications)
