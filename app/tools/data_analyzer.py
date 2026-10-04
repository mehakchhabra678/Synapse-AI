import pandas as pd


def analyze_dataset(file_path: str) -> dict:
    """
    Analyze a CSV dataset without using an LLM.
    """

    df = pd.read_csv(file_path)

    result = {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "numeric_summary": df.describe().round(2).to_dict(),
    }

    return result