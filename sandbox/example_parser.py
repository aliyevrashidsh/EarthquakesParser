"""Example: Using the ContentParser."""

import sys
from pathlib import Path
from typing import Any

import pandas as pd
from dotenv import load_dotenv

from earthquakes_parser import SupabaseDB
from earthquakes_parser.parser.parser_manager import ParserManager

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


def main():
    df = pd.read_csv("sandbox/data/web_results.csv")
    df.to_csv("sandbox/data/web_results.csv",)
    load_dotenv()
    db = SupabaseDB()
    p_manager = ParserManager(db)
    p_manager.parse_from_dataframe(df)



if __name__ == "__main__":
    main()
