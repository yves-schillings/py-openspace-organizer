import csv
import os
import json
import pandas as pd
from typing import List, Dict


def create_excel_from_csv(csv_path: str, excel_path: str = "data/colleagues.xlsx") -> None:
    """
    Convert a CSV file into an Excel file and save it.

    :param csv_path: Path to the input CSV file.
    :param excel_path: Path where the output Excel file will be saved.
    """
    names: List[str] = []

    # Read names from the CSV file (assumes one name per row)
    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                names.append(row[0].strip())

    # Create the output directory if it doesn't exist
    os.makedirs(os.path.dirname(excel_path), exist_ok=True)

    # Save names to Excel
    df = pd.DataFrame(names, columns=["Name"])
    df.to_excel(excel_path, index=False)


def load_colleagues_from_excel(excel_path: str) -> List[str]:
    """
    Load colleague names from an Excel file.

    :param excel_path: Path to the Excel file.
    :return: List of colleague names.
    """
    df = pd.read_excel(excel_path)

    # Return the names as a list of strings
    return df["Name"].dropna().astype(str).str.strip().tolist()

def load_config(filepath: str = "config.json") -> Dict:
    """
    Load configuration values from a JSON file.

    :param filepath: Path to the JSON configuration file.
    :return: Dictionary of configuration values.
    """
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)