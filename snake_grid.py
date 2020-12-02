import numpy as np
import pickle

from snake_evo import Population, relu

from tqdm import tqdm


PROBS = 2.**np.arange(-2,3) * 0.05

STRENGTHS = 2.**np.arange(-2,3)

GENERATIONS = 1000

RUN_NAME = "relu"

if __name__ == "__main__":
    for i_p, p in enumerate(PROBS):
        for i_s, s in enumerate(STRENGTHS):
            print(f"testing p={p}, s={s}")
            max_scores = []
            P = Population(
                n_pop = 100,
                blocks_width=15,
                blocks_height = 10,
                hidden_sizes = [10,10]
            )
            for i in tqdm(range(GENERATIONS)):

                P.play(n_trials = 5, threshold = 50, activation=relu)
                max_scores.append(max(P.scores))
                best = P.generation(num_elites = 2, prob= 0.05, strength=1)
            with open(f"./grid_runs_{RUN_NAME}/{i_p}-{i_s}.pkl", "wb") as f:
                pickle.dump((p,s,max_scores,P),f)

