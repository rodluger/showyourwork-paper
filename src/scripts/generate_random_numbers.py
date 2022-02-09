import paths
import numpy as np

# Get the seed from the rule parameters
seed = snakemake.params["seed"]

# Write 10 random numbers to the dataset
np.random.seed(seed)
X = np.random.randn(10)
np.savetxt(str(paths.data / "random_numbers.dat"), X)
