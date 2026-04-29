import sys

sys.path.append(r"C:\Users\Goncalo\Desktop\TUM\CS\rep\Bay_Opt_GEKO")

import shutil
from pathlib import Path

from run_periodic_hill import run_case
from error_calcs import objective
import file_locations as fl

SIM_PATH = Path(fl.sim)

def run_and_save(csep, label):
    print(f"\n=== Running Csep = {csep} ===")
    run_case(csep=csep, n_iter=200)

    backup_path = SIM_PATH.with_name(f"sim_{label}.csv")
    shutil.copy(SIM_PATH, backup_path)

    score = objective({"csep": csep})

    print(f"Csep = {csep}")
    print(f"CSV saved as: {backup_path}")
    print(f"Score = {score}")

    return score

if __name__ == "__main__":
    #score_15 = run_and_save(1.5, "csep_1p5")
    score_238 = run_and_save(2.3846949, "csep_2p38")

    print("\n=== RESULT ===")
    #print("Csep 1.5       ->", score_15)
    print("Csep 2.3846949 ->", score_238)

    # if score_15 > score_238:
    #     print("✅ Objective está consistente: 1.5 é melhor.")
    # else:
    #     print("❌ Algo está errado: 1.5 deveria ser melhor que 2.3846949.")