import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from model import run_simulation


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--params", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--plot", action="store_true")
    parser.add_argument("--smooth-window", type=int, default=1)

    return parser.parse_args()


def smooth(series, window):
    if window <= 1:
        return series
    return series.rolling(window, min_periods=1).mean()


def main():
    args = parse_args()

    df_params = pd.read_csv(args.params)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    metrics_rows = []

    for run_id, row in df_params.iterrows():
        res = run_simulation(
        initial_mailly=int(row["init_mailly"]),
        initial_moulin=int(row["init_moulin"]),
        steps=int(row["steps"]),
        p1=float(row["p1"]),
        p2=float(row["p2"]),
        seed=int(row["seed"]),
    )

        metrics_rows.append({
            "run_id": run_id,
            "p1": row["p1"],
            "p2": row["p2"],
            "steps": row["steps"],
            "init_mailly": row["init_mailly"],
            "init_moulin": row["init_moulin"],
            "seed": row["seed"],
            "final_imbalance": res["final_imbalance"],
            "total_unmet_mailly": res["total_unmet_mailly"],
            "total_unmet_moulin": res["total_unmet_moulin"],
        })

        if args.plot:
            df = pd.DataFrame({
                "mailly": res["mailly"],
                "moulin": res["moulin"],
                "imbalance": res["imbalance"],
            })

            df = df.apply(lambda s: smooth(s, args.smooth_window))

            plt.figure(figsize=(10, 6))
            plt.plot(df["mailly"], label="Mailly")
            plt.plot(df["moulin"], label="Moulin")
            plt.plot(df["imbalance"], label="Imbalance")
            plt.legend()
            plt.title(f"Run {run_id}")
            plt.savefig(args.out_dir / f"run_{run_id}.png")
            plt.close()

    df_metrics = pd.DataFrame(metrics_rows)
    df_metrics.to_csv(args.out_dir / "metrics.csv", index=False)

    if args.plot:
        plt.figure(figsize=(10, 6))
        plt.scatter(df_metrics["p1"], df_metrics["final_imbalance"], label="Final imbalance")
        plt.xlabel("p1")
        plt.ylabel("Final imbalance")
        plt.title("Final imbalance vs p1")
        plt.savefig(args.out_dir / "metrics_3plot.png")
        plt.close()


if __name__ == "__main__":
    main()