import paths
import numpy as np

# Get the seed from the rule parameters
seed = snakemake.params["seed"]

# Write 10 random numbers to 5 different datasets
if not (paths.data / "many_datasets").exists():
    (paths.data / "many_datasets").mkdir()

np.random.seed(seed)
for n in range(1, 6):
    X = np.random.randn(10)
    np.savetxt(str(paths.data / "many_datasets" / f"{n:02d}.dat"), X)