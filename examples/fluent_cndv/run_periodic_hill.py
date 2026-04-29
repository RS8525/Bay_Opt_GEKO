import time
import ansys.fluent.core as pyfluent

CASE_BASE = r"C:\Users\Goncalo\Desktop\TUM\CS\PeriodicHillGeometry_2d.cas.h5"

def run_case(csep=1.75, n_iter=200):

    solver = pyfluent.launch_fluent(
        mode="solver",
        precision="double",
        processor_count=2,
        dimension=2
    )

    solver.file.read_case(file_name=CASE_BASE)

    solver.scheme_eval.scheme_eval(
        f'(ti-menu-load-string "/define/models/viscous/geko-options/csep\\n{csep}\\n")'
    )

    solver.solution.initialization.hybrid_initialize()
    solver.solution.run_calculation.iterate(iter_count=n_iter)

    solver.scheme_eval.scheme_eval(
        r'(ti-menu-load-string "/file/export/ascii C:\Users\Goncalo\Desktop\TUM\CS\Sim\sim.csv surface () yes pressure x-velocity y-velocity turb-kinetic-energy turb-diss-rate ()")'
    )

    solver.file.write_case_data(
        file_name=rf"C:\Users\Goncalo\Desktop\TUM\CS\run_csep_{csep}.cas.h5"
    )

    solver.exit()
    time.sleep(30)


if __name__ == "__main__":
    run_case(csep=1.9, n_iter=200)