import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

def ensure(path):
    os.makedirs(path, exist_ok=True)

def clean_numeric(df, cols):
    for c in cols:
        if c in df.columns:
            df[c] = (
                df[c]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.replace("%", "", regex=False)
            )
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

def compute_kpis(df):
    k = {}
    if "impressions" in df.columns: 
        k["total_impressions"] = int(df["impressions"].sum())
    if "clicks" in df.columns: 
        k["total_clicks"] = int(df["clicks"].sum())
    if "spent" in df.columns or "spend" in df.columns: 
        col = "spent" if "spent" in df.columns else "spend"
        k["total_spend"] = float(df[col].sum())
    if "ctr" in df.columns: 
        k["mean_ctr"] = round(df["ctr"].mean(), 4)
    if "cpc" in df.columns: 
        k["mean_cpc"] = round(df["cpc"].mean(), 4)
    return k


def plot_timeseries(df, date_col, metric, out_path):
    ensure(os.path.dirname(out_path))
    plt.figure(figsize=(9, 3))
    sns.lineplot(data=df.sort_values(date_col), x=date_col, y=metric)
    plt.title(f"{metric.capitalize()} Over Time")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


def plot_top_campaigns(df, metric, out_path):
    ensure(os.path.dirname(out_path))
    if "campaign" not in df.columns:
        return None
    
    top = df.groupby("campaign")[metric].sum().nlargest(8)

    plt.figure(figsize=(6, 4))
    sns.barplot(y=top.index, x=top.values)
    plt.title(f"Top Campaigns by {metric.capitalize()}")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

    return out_path


# Generate all plots at once
def generate_all_plots(df, out_dir):
    ensure(out_dir)

    df = clean_numeric(df, ["impressions", "clicks", "spent", "spend", "ctr"])
    plots = []

    # Timeseries plots
    if "reporting_start" in df.columns:
        date_col = "reporting_start"

        for metric in ["impressions", "clicks", "spent", "ctr"]:
            if metric in df.columns:
                p = os.path.join(out_dir, f"{metric}_timeseries.png")
                plot_timeseries(df, date_col, metric, p)
                plots.append(p)

    # Top campaigns
    for metric in ["impressions", "clicks", "spent", "ctr"]:
        if metric in df.columns:
            p = os.path.join(out_dir, f"top_campaigns_{metric}.png")
            res = plot_top_campaigns(df, metric, p)
            if res: plots.append(p)

    return plots
