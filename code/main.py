import argparse
import os

from ingest import load_files
from schema import normalize_schema
from transform import clean
from analysis import compute_kpis, generate_all_plots
from insights import build_prompt, generate_insights
from report import build_pptx


def pipeline(input_paths, out_path):
    # 1. Ingest all files
    dfs, pdf_texts = load_files(input_paths)

    if len(dfs) == 0:
        raise ValueError("No valid tabular files found in --inputs. Provide CSV/XLSX/SQLite files.")

    # 2. Process all dataframes
    df = None
    for d in dfs:
        d = normalize_schema(d)
        d = clean(d)
        df = d if df is None else df._append(d, ignore_index=True)

    if "date" in df.columns:
        df = df.sort_values("date")

    # 3. Compute KPIs
    kpis = compute_kpis(df)

    # 4. Generate Images
    plots_dir = 'outputs/figures'
    images = generate_all_plots(df, plots_dir)

    # 5. LLM Insights
    prompt = build_prompt(kpis)
    insights = generate_insights(prompt)

    # 6. Build PPTX report
    build_pptx(
        title="Automated Marketing Insights Report",
        kpis=kpis,
        insights=insights,
        images=images,
        out_path=out_path
    )
    print("\nReport generated successfully!")
    print(f"Location: {out_path}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", nargs="+", required=True, help="Input files: CSV/XLSX/SQLite/PDF")
    parser.add_argument("--out", required=True, help="Output PPTX path")
    args = parser.parse_args()

    pipeline(args.inputs, args.out)
