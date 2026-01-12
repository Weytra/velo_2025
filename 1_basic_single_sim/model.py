from dataclasses import dataclass
from typing import Tuple, Dict
import numpy as np
import pandas as pd


@dataclass
class State:
    """Represents the state of bikes at two stations."""
    mailly: int
    moulin: int
    unmet_mailly: int = 0
    unmet_moulin: int = 0


def step(
    state: State,
    p1: float,
    p2: float,
    rng: np.random.Generator,
    metrics: Dict[str, int],
) -> State:
    """Simulate one time step of the bike-sharing system."""

    # Copy state to avoid mutating the original
    mailly = state.mailly
    moulin = state.moulin
    unmet_mailly = state.unmet_mailly
    unmet_moulin = state.unmet_moulin

    # User tries to go from Mailly -> Moulin
    if rng.random() < p1:
        if mailly > 0:
            mailly -= 1
            moulin += 1
        else:
            unmet_mailly += 1
            metrics["unmet_mailly"] += 1

    # User tries to go from Moulin -> Mailly
    if rng.random() < p2:
        if moulin > 0:
            moulin -= 1
            mailly += 1
        else:
            unmet_moulin += 1
            metrics["unmet_moulin"] += 1

    return State(mailly, moulin, unmet_mailly, unmet_moulin)


def run_simulation(
    initial_mailly: int,
    initial_moulin: int,
    steps: int,
    p1: float,
    p2: float,
    seed: int,
) -> Tuple[pd.DataFrame, Dict[str, int]]:

    rng = np.random.default_rng(seed)

    # Initial state
    state = State(initial_mailly, initial_moulin)

    # Metrics
    metrics = {
        "unmet_mailly": 0,
        "unmet_moulin": 0,
    }

    # Time series storage
    records = []

    for t in range(steps + 1):
        records.append({
            "time": t,
            "mailly": state.mailly,
            "moulin": state.moulin,
        })

        state = step(state, p1, p2, rng, metrics)

    df = pd.DataFrame(records)

    # Final metrics
    metrics["mailly"] = state.mailly
    metrics["moulin"] = state.moulin
    metrics["final_imbalance"] = state.mailly - state.moulin

    return df, metrics