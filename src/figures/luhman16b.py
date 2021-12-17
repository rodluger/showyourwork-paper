import numpy as np
import matplotlib.pyplot as plt
import pickle


# Load the dataset
with open("../data/luhman16b.pickle", "rb") as f:
    data = pickle.load(f, encoding="latin1")

# Timestamps (from Ian Crossfield)
t = np.array(
    [
        0.0,
        0.384384,
        0.76825872,
        1.15339656,
        1.5380364,
        1.92291888,
        2.30729232,
        2.69268336,
        3.07654752,
        3.46219464,
        3.8473428,
        4.23171624,
        4.61583456,
        4.99971048,
    ]
)

# Use the first epoch's wavelength array
lams = data["chiplams"][0]

# Interpolate onto that array
observed = np.empty((14, 4, 1024))
template = np.empty((14, 4, 1024))
broadened = np.empty((14, 4, 1024))
for k in range(14):
    for c in range(4):
        observed[k][c] = np.interp(
            lams[c],
            data["chiplams"][k][c],
            data["obs1"][k][c] / data["chipcors"][k][c],
        )
        template[k][c] = np.interp(
            lams[c],
            data["chiplams"][k][c],
            data["chipmodnobroad"][k][c] / data["chipcors"][k][c],
        )
        broadened[k][c] = np.interp(
            lams[c],
            data["chiplams"][k][c],
            data["chipmods"][k][c] / data["chipcors"][k][c],
        )

# Get the final data arrays
wav = data["chiplams"][:, 2]
flux = data["obs1"][:, 2] / data["chipcors"][:, 2]
model = data["chipmods"][:, 2] / data["chipcors"][:, 2]

# Plot the spectra
fig, ax = plt.subplots(1, figsize=(8, 5))
fig.subplots_adjust(wspace=0.1)
for k in range(14):
    ax.plot(wav[k], 0.65 * k + flux[k], "k.", ms=2, alpha=0.5, zorder=-1)
    ax.plot(wav[k], 0.65 * k + model[k], "C1-", lw=1)

# Appearance hacks
ax.spines["left"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.margins(0, None)
for tick in ax.get_xticklabels():
    tick.set_fontsize(12)
for tick in ax.get_yticklabels():
    tick.set_fontsize(10)
ax.xaxis.set_major_formatter("{x:.3f}")
ax.set_rasterization_zorder(0)

ax.set_ylim(0.3, 10)
ax.set_yticks([0, 0.5, 1.0])
ax.set_xlim(ax.get_xlim()[0] - 0.0001, ax.get_xlim()[1])
x0 = ax.get_xlim()[0]
y0 = ax.get_ylim()[0]
ax.plot([x0, x0], [y0, 1.25], "k-", clip_on=False, lw=0.75)
ax.set_xticks([2.320, 2.322, 2.324, 2.326, 2.328, 2.330])
ax.set_xlabel(r"wavelength [$\mu$m]", fontsize=16, labelpad=10)
fig.savefig("luhman16b.pdf", bbox_inches="tight", dpi=300)
