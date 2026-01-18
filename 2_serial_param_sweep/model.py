from dataclasses import dataclass
from typing import Dict
import numpy as np


@dataclass
class State:
    mailly: int
    moulin: int
    unmet_mailly: int = 0
    unmet_moulin: int = 0


def step(state: State, p1: float, p2: float, rng: np.random.Generator, metrics: Dict[str, int]) -> State:
    u = rng.random()

    # Mailly -> Moulin
    if u < p1:
        if state.mailly > 0:
            state.mailly -= 1
            state.moulin += 1
        else:
            state.unmet_mailly += 1
            metrics["unmet_mailly"] += 1

    # Moulin -> Mailly
    elif u < p1 + p2:
        if state.moulin > 0:
            state.moulin -= 1
            state.mailly += 1
        else:
            state.unmet_moulin += 1
            metrics["unmet_moulin"] += 1

    return state


def run_simulation(initial_mailly: int, initial_moulin: int, steps: int,
                   p1: float, p2: float, seed: int) -> Dict[str, list]:

    rng = np.random.default_rng(seed)
    state = State(initial_mailly, initial_moulin)

    metrics = {"unmet_mailly": 0, "unmet_moulin": 0}

    mailly_hist = []
    moulin_hist = []
    unmet_mailly_hist = []
    unmet_moulin_hist = []
    imbalance_hist = []

    for _ in range(steps):
        mailly_hist.append(state.mailly)
        moulin_hist.append(state.moulin)
        unmet_mailly_hist.append(state.unmet_mailly)
        unmet_moulin_hist.append(state.unmet_moulin)
        imbalance_hist.append(state.mailly - state.moulin)

        state = step(state, p1, p2, rng, metrics)

    return {
        "mailly": mailly_hist,
        "moulin": moulin_hist,
        "unmet_mailly": unmet_mailly_hist,
        "unmet_moulin": unmet_moulin_hist,
        "imbalance": imbalance_hist,
        "final_imbalance": imbalance_hist[-1],
        "total_unmet_mailly": metrics["unmet_mailly"],
        "total_unmet_moulin": metrics["unmet_moulin"],
    }