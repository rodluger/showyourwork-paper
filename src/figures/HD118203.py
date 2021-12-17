import numpy as np
import matplotlib.pyplot as plt
import corner

# Load the results
data = np.load("../data/HD118203.npz")
x = data["x"]
y = data["y"]
gp_pred = data["gp_pred"]
lc_pred = data["lc_pred"]
map_t0 = data["map_t0"]
map_period = data["map_period"]
map_mean = data["map_mean"]
samples = data["samples"]

# Plot the transit
fig = plt.figure(figsize=(8, 4))
x_fold = (x - map_t0 + 0.5 * map_period) % map_period - 0.5 * map_period
inds = np.argsort(x_fold)
plt.scatter(x_fold, y - gp_pred - map_mean, c="k", s=3, alpha=0.5)
plt.plot(x_fold[inds], lc_pred[inds] - map_mean, "C0")
plt.xlabel("time since transit [days]", fontsize=12)
plt.ylabel("relative flux [ppt]", fontsize=12)
_ = plt.xlim(-0.25, 0.25)
fig.savefig("HD118203_transit.pdf", bbox_inches="tight")

# Plot the corner plot (with some appearance tweaks)
samples[:, 0] -= 6.13498
samples[:, 0] *= 1e5
fig = corner.corner(
    samples,
    labels=[
        "$\mathrm{period} - 6.13498$ [days]",
        "planet/star radius ratio",
        "impact parameter",
    ],
    truths=[0, 0.05538, 0.125],
)
fig.axes[6].set_xticks([-4, -2, 0, 2, 4])
fig.axes[6].set_xticklabels(
    [
        r"$-4 \times 10^{-5}$",
        r"$-2 \times 10^{-5}$",
        0,
        r"$2 \times 10^{-5}$",
        r"$4 \times 10^{-5}$",
    ]
)
for axis in fig.axes:
    for tick in axis.xaxis.get_major_ticks() + axis.yaxis.get_major_ticks():
        tick.label.set_fontsize(6)
    axis.set_xlabel(axis.get_xlabel(), fontsize=12)
    axis.set_ylabel(axis.get_ylabel(), fontsize=12)
fig.savefig("HD118203_corner.pdf", bbox_inches="tight")