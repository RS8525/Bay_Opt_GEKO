import sys
import os

# Add directorys to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from turborans.bayes_io import optimizer
from turborans.utilities.json_io import load_json
from run_periodic_hill import run_case
from error_calcs import objective
import file_locations as fl


N_RUNS = 10

opt = optimizer(
    turborans_directory=fl.tuner,
    settings={
        "json_mode": True,
        "random_state": 7,
        "n_samples": 5
    }
)

for run_ind in range(N_RUNS):
    opt.suggest()
    coeff = load_json(fl.tuner, "suggestion.json")

    csep = coeff["csep"]

    print(f"\n=== Run {run_ind} | Csep = {csep} ===")

    run_case(csep=csep, n_iter=250)

    score = objective(coeff)

    print(f"Score = {score}")

    opt.register_score(score=score)