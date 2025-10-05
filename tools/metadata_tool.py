from pathlib import Path
import pandas as pd
from langchain_core.tools import tool
from common.config import load_config

_cfg = load_config()
_METADATA_CSV = Path(_cfg["metadata"]["csv_path"])

def _load_df() -> pd.DataFrame:
    if not _METADATA_CSV.exists():
        raise FileNotFoundError(f"Metadata CSV not found at: {_METADATA_CSV}")
    return pd.read_csv(_METADATA_CSV)

@tool("lookup_policy_metadata")
def lookup_policy_metadata(query: str) -> str:
    """
    Retrieve policy metadata for a given query (usually a policy title).
    Matches on policy_title first; also searches managers/business_owner.
    """
    df = _load_df()
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

    sub = df.loc[mask, ["policy_title","published_status","managers","business_owner","review_cycle"]]
    lines = []
    for _, row in sub.iterrows():
        mgr = row["managers"] if isinstance(row["managers"], str) and row["managers"].strip() else "—"
        lines.append(
            f"- {row['policy_title']} | status: {row['published_status']} | "
            f"manager(s): {mgr} | owner: {row['business_owner']} | review: {row['review_cycle']}"
        )
    print("[TOOL] lookup_policy_metadata called.")
    return "\n".join(lines)
