import numpy as np
import matplotlib.pyplot as plt

# Load the results
data = np.load("../data/HD118203.npz")
x = data["x"]
y = data["y"]
gp_pred = data["gp_pred"]
lc_pred = data["lc_pred"]
map_t0 = data["map_t0"]
map_period = data["map_period"]
map_mean = data["map_mean"]

# Plot the transit
fig = plt.figure(figsize=(8, 4))
x_fold = (x - map_t0 + 0.5 * map_period) % map_period - 0.5 * map_period
inds = np.argsort(x_fold)
plt.scatter(x_fold, y - gp_pred - map_mean, c="k", s=3, alpha=0.5)
plt.plot(x_fold[inds], lc_pred[inds] - map_mean, "C0")
plt.xlabel("time since transit [days]")
plt.ylabel("relative flux [ppt]")
_ = plt.xlim(-0.25, 0.25)
fig.savefig("HD118203_transit.pdf", bbox_inches="tight")