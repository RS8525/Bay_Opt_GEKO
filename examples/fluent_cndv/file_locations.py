import os

BASE_DIR = os.path.dirname(__file__)

#file locations

#Journal File data
#journal_file = os.path.join(BASE_DIR, "journal_20h_rerun.wbjn")

#Rans tuning directory 
tuner = os.path.join(BASE_DIR, "tuner")

#figure saves
figs = os.path.join(BASE_DIR, "results", "graficos")

#dns file location (adjust this depending on where fakeDNS actually is)
dns = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "Ansys_projects", "PeriodicHillGeometry_fakeDNS.csv"))

#sim data location 
sim = os.path.join(BASE_DIR, "results", "sim.csv")

#Default coeff file location
baseline = sim
