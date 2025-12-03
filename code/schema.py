import pandas as pd

COLUMN_MAP = {
    "impr": "impressions",
    "impressions": "impressions",
    "clicks": "clicks",
    "spend": "spend",
    "cost": "spend",
    "date": "date",
    "day": "date",
    "campaign": "campaign",
    "campaign_name": "campaign",
    "revenue": "revenue",
    "conversions": "conversions"
}

def normalize_schema(df):
    df = df.rename(columns={c: c.lower().strip() for c in df.columns})

    rename_map = {}
    for c in df.columns:
        for key, target in COLUMN_MAP.items():
            if c == key or c.startswith(key):
                rename_map[c] = target
    df = df.rename(columns=rename_map)

    if "date" in df.columns:
        try:
            df["date"] = pd.to_datetime(df["date"])
        except:
            pass

    return df
