import paths
import matplotlib.pyplot as plt
import numpy as np

datasets = (paths.data / "many_datasets").glob("*.dat")
fig = plt.figure()

for dataset in datasets:
    data = np.loadtxt(dataset)
    plt.plot(data)

fig.savefig(paths.figures / "many_datasets.pdf", format="pdf", bbox_inches="tight")