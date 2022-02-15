import paths
import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt(paths.data / "random_numbers.dat")
#
fig = plt.figure()
plt.plot(data)
fig.savefig(paths.figures / "random_numbers.pdf", format="pdf", bbox_inches="tight")