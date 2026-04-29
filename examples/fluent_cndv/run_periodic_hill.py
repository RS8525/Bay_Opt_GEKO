import os
import time
import ansys.fluent.core as pyfluent

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results").replace("\\", "/")
CASE_BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Ansys_projects", "PeriodicHillGeometry_2d.cas.h5")).replace("\\", "/")

def run_case(csep=1.75, n_iter=200):
    os.makedirs(RESULTS_DIR, exist_ok=True)


    solver = pyfluent.launch_fluent(
        mode="solver",
        precision="double",
        processor_count=2,
        dimension=2
    )

    # Use settings.file to avoid deprecation warnings
    solver.settings.file.read_case(file_name=CASE_BASE)

    solver.scheme_eval.scheme_eval(
        f'(ti-menu-load-string "/define/models/viscous/geko-options/csep\\n{csep}\\n")'
    )

    solver.solution.initialization.hybrid_initialize()
    solver.solution.run_calculation.iterate(iter_count=n_iter)

    solver.scheme_eval.scheme_eval(
        f'(ti-menu-load-string "/file/export/ascii {RESULTS_DIR}/sim.csv surface () yes pressure x-velocity y-velocity turb-kinetic-energy turb-diss-rate ()")'
    )

    solver.settings.file.write_case_data(
        file_name=rf"{RESULTS_DIR}/run_csep_{csep}.cas.h5"
    )

    solver.exit()
    time.sleep(30)


if __name__ == "__main__":
    run_case(csep=1.9, n_iter=200)