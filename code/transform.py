import pandas as pd

def clean(df):
    num_cols = df.select_dtypes(include="object").columns
    for c in num_cols:
        df[c] = df[c].str.replace(",", "", regex=False)

    for c in df.columns:
        try:
            df[c] = pd.to_numeric(df[c])
        except:
            pass

    # Derived metrics
    if "impressions" in df.columns and "clicks" in df.columns:
        df["ctr"] = df["clicks"] / df["impressions"].replace(0, pd.NA)

    if "clicks" in df.columns and "spend" in df.columns:
        df["cpc"] = df["spend"] / df["clicks"].replace(0, pd.NA)

    if "spend" in df.columns and "impressions" in df.columns:
        df["cpm"] = (df["spend"] / df["impressions"].replace(0, pd.NA)) * 1000

    return df
