import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
from model import run_simulation


def parse_args():
    parser = argparse.ArgumentParser(description="Run a single bike-sharing simulation.")

    parser.add_argument("--steps", type=int, required=True)
    parser.add_argument("--p1", type=float, required=True)
    parser.add_argument("--p2", type=float, required=True)
    parser.add_argument("--init_mailly", type=int, required=True)
    parser.add_argument("--init_moulin", type=int, required=True)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--out_csv", type=str, required=True)
    parser.add_argument("--plot", action="store_true")

    return parser.parse_args()


def main():
    args = parse_args()

    # Run simulation
    df, metrics = run_simulation(
        args.init_mailly,
        args.init_moulin,
        args.steps,
        args.p1,
        args.p2,
        args.seed,
    )

    # Ensure output directory exists
    out_path = Path(args.out_csv)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Save timeseries
    df.to_csv(out_path, index=False)

    # Save metrics
    metrics_path = out_path.with_suffix(".metrics.tsv")
    with open(metrics_path, "w") as f:
        for k, v in metrics.items():
            f.write(f"{k}\t{v}\n")

    # Optional plot
    if args.plot:
        plt.figure()
        plt.plot(df["time"], df["mailly"], label="Mailly")
        plt.plot(df["time"], df["moulin"], label="Moulin")
        plt.xlabel("Time")
        plt.ylabel("Bikes")
        plt.legend()
        plt.title("Bike counts over time")
        plt.savefig(out_path.with_suffix(".png"))

    print(f"Saved timeseries to {out_path}")
    print(f"Saved metrics to {metrics_path}")


if __name__ == "__main__":
    main()