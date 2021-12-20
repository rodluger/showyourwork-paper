#!/usr/bin/env python
# coding: utf-8
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from helpers.sun import sun

# McQuillan et al. 2014
mcq = pd.read_csv("../data/McQuillan2014.csv")
mcq = mcq.add_prefix("mcq_")

# LAMOST-Kepler
lam = pd.read_csv("../data/KeplerRot-LAMOST.csv")

# Drop duplicate sources, keeping the one with the brighter G magnitude
lam = lam.sort_values(["KIC", "Gmag"], ascending=(True, True))
lam = lam.merge(mcq, how="left", left_on="KIC", right_on="mcq_KIC")
lam = lam.drop_duplicates(subset=["KIC"], keep="first")
lam_mask = lam["Teff_lam"] > 3000
lam_mask = lam["Teff_lam"] < 8000
lam_mask &= lam["logg_lam"] > 3
lam_mask &= lam["logg_lam"] < 5
lam_mask &= abs(lam["feh_lam"]) < 2
lam = lam[lam_mask]

# Plot
fig, ax = plt.subplots(1, figsize=(4, 4))
ax.scatter(lam["Teff_lam"], lam["mcq_Prot"], marker=".", rasterized=True, s=0.1)
ax.set_xlabel("Effective temperature [K]")
ax.set_xlim(7250, 3250)
ax.set_ylim(-2, 60)
ax.plot(sun["teff"], sun["prot"], "o", color="C1")
ax.errorbar(
    sun["teff"],
    sun["prot"],
    yerr=np.vstack([sun["e_prot"], sun["E_prot"]]),
    fmt="o",
    color="C1",
    mec="white",
    ms=6,
)
ax.set_ylabel("Rotation period [d]")
fig.savefig("rossbyridge.pdf", bbox_inches="tight", dpi=100)