#!/usr/bin/env python
# coding: utf-8
import numpy as np
import astropy.constants as c


__all__ = ["sun"]


# Data for the Sun
sun = {
    "teff": 5772,
    "prot": 25.4,
    "e_prot": 25.4 - 24.5,
    "E_prot": 36 - 25.4,
    "logg": np.log10(c.GM_sun.cgs.value / c.R_sun.cgs.value ** 2),
}