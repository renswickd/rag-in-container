import pandas as pd
from pathlib import Path
from langchain_core.tools import tool

# Constants
METADATA_CSV_PATH = "data/metadata/pr_metadata.csv"

def load_metadata_df() -> pd.DataFrame:
    """Load policy metadata from CSV file"""
    path = Path(METADATA_CSV_PATH)
    print(f"[INFO] Loading metadata from {path}")
    return pd.read_csv(path)

@tool("lookup_policy_metadata")
def lookup_policy_metadata(query: str) -> str:
    """
    Retrieve policy metadata for a given query (usually a policy title).
    """
    try:
        df = load_metadata_df()
        q = (query or "").strip().lower()
        mask = df["policy_title"].str.lower().str.contains(q, na=False)

        if not mask.any():
            mask = (
                df["business_owner"].fillna("").str.lower().str.contains(q)
                | df["managers"].fillna("").str.lower().str.contains(q)
            )

        if not mask.any():
            titles = ", ".join(df["policy_title"].tolist())
            return f"No direct metadata match. Available policies: {titles}"

        sub = df.loc[mask, ["policy_title", "published_status", "managers", "business_owner", "review_cycle"]]
        lines = []
        for _, row in sub.iterrows():
            mgr = row["managers"] if isinstance(row["managers"], str) and row["managers"].strip() else "—"
            lines.append(
                f"- {row['policy_title']} | status: {row['published_status']} | "
                f"manager(s): {mgr} | owner: {row['business_owner']} | review: {row['review_cycle']}"
            )
        return "\n".join(lines)
    except Exception as e:
        print(f"[ERROR] Metadata lookup failed: {e}")
        return "Unable to retrieve metadata at this time."