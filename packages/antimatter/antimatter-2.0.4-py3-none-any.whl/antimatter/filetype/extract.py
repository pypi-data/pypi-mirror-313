import csv
import json
from typing import Any, Dict, List

from antimatter.errors import DataFormatError, MissingDependency


def extract_from_file(path: str, hint: str) -> Any:
    """
    Extracts data from a file based on the provided hint about the file's format.

    :param path: The path to the file.
    :param hint: A hint about the file format. Supported hints are 'csv', 'json', 'parquet', and 'txt'.
    :return: The extracted data.
    :raises errors.DataFormatError: If the file format hinted is not supported.
    """
    if hint == "csv":
        return extract_from_csv(path)
    elif hint == "json":
        # assume ndjson format first
        try:
            return extract_from_ndjson(path)
        except:
            return extract_from_json(path)
    elif hint == "parquet":
        return extract_from_parquet(path)
    elif hint == "txt":
        return extract_from_txt(path)
    else:
        raise DataFormatError(f"file format with hint '{hint}' is not supported")


def extract_from_csv(path: str) -> List[Dict]:
    """
    Extracts data from a CSV file.

    This function sniffs the dialect of the CSV file and reads it into a list of dictionaries,
    where each dictionary represents a row with column headers as keys.

    :param path: The path to the CSV file.
    :return: A list of dictionaries representing the rows of the CSV file.
    """
    with open(path, newline="") as csvfile:
        try:
            dialect = csv.Sniffer().sniff(csvfile.read(1024))
            csvfile.seek(0)
        except csv.Error:
            # fallback to default dialect if sniffing fails
            dialect = "excel"

        reader = csv.DictReader(csvfile, dialect=dialect)
        return [row for row in reader]


def extract_from_json(path: str) -> Any:
    """
    Extracts data from a JSON file.

    :param path: The path to the JSON file.
    :return: The data parsed from the JSON file.
    """
    with open(path, "r") as file:
        return json.load(file)


def extract_from_ndjson(path: str) -> List:
    """
    Extracts data from an NDJSON (Newline Delimited JSON) file.

    Each line of the file is a JSON object. The function reads each line and
    parses it as JSON.

    :param path: The path to the NDJSON file.
    :return: A list where each element is the data parsed from one line of the
             NDJSON file.
    """
    data = []
    with open(path, "r") as file:
        for line in file:
            data.append(json.loads(line))
    return data


def extract_from_parquet(path: str):
    """
    Extracts data from a Parquet file.

    :param path: The path to the Parquet file.
    :return: The data parsed from the Parquet file as a pandas DataFrame.
    """
    try:
        import pandas as pd
    except ModuleNotFoundError as me:
        raise MissingDependency(me)

    return pd.read_parquet(path)


def extract_from_txt(path: str) -> str:
    """
    Extracts data from a text file.

    :param path: The path to the text file.
    :return: The content of the text file as a string.
    """
    with open(path, "r") as f:
        return f.read()
