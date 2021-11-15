import numpy as np
import matplotlib.pyplot as plt
import corner

# Load the results
data = np.load("../data/HD118203.npz")
samples = data["samples"]

# Plot the corner
fig = corner.corner(
    samples, labels=["period", "ror", "b"], truths=[6.134980, 0.05538, 0.125]
)
fig.savefig("HD118203_corner.pdf", bbox_inches="tight")