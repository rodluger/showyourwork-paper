import exoplanet as xo
import numpy as np
import lightkurve as lk
import matplotlib.pyplot as plt
import pymc3 as pm
import aesara_theano_fallback.tensor as tt
import pymc3_ext as pmx
from celerite2.theano import terms, GaussianProcess
import warnings
import logging


# Suppress exoplanet & theano warnings
logging.getLogger("theano.tensor.opt").setLevel(logging.ERROR)
warnings.filterwarnings(action="ignore", category=UserWarning, module="exoplanet")


# Download the light curve
lcfs = lk.search_lightcurve(
    "TIC 286923464", mission="TESS", author="SPOC"
).download_all(flux_column="pdcsap_flux")
lc = lcfs.stitch().remove_nans().remove_outliers(sigma=7)
x = np.ascontiguousarray(lc.time.value, dtype=np.float64)
y = np.ascontiguousarray(1e3 * (lc.flux - 1), dtype=np.float64)
yerr = np.ascontiguousarray(1e3 * lc.flux_err, dtype=np.float64)
texp = np.min(np.diff(x))

# Run Box Least Squares (BLS) to obtain a guess for the planet period
pg = xo.estimators.bls_estimator(x, y, yerr, min_period=2, max_period=20)
peak = pg["peak_info"]
period_guess = peak["period"]
t0_guess = peak["transit_time"]
depth_guess = peak["depth"]

# Mask out-of-transit data
transit_mask = (
    np.abs((x - t0_guess + 0.5 * period_guess) % period_guess - 0.5 * period_guess)
    < 0.25
)
x = np.ascontiguousarray(x[transit_mask])
y = np.ascontiguousarray(y[transit_mask])
yerr = np.ascontiguousarray(yerr[transit_mask])

# Define our pymc3 model
with pm.Model() as model:

    # Stellar parameters
    mean = pm.Normal("mean", mu=0.0, sigma=10.0)
    u = xo.QuadLimbDark("u")
    star_params = [mean, u]

    # Gaussian process noise model
    sigma = pm.InverseGamma("sigma", alpha=3.0, beta=2 * np.median(yerr))
    log_sigma_gp = pm.Normal("log_sigma_gp", mu=0.0, sigma=10.0)
    log_rho_gp = pm.Normal("log_rho_gp", mu=np.log(10.0), sigma=10.0)
    kernel = terms.SHOTerm(
        sigma=tt.exp(log_sigma_gp), rho=tt.exp(log_rho_gp), Q=1.0 / 3
    )
    noise_params = [sigma, log_sigma_gp, log_rho_gp]

    # Planet parameters
    log_ror = pm.Normal("log_ror", mu=0.5 * np.log(depth_guess * 1e-3), sigma=10.0)
    ror = pm.Deterministic("ror", tt.exp(log_ror))

    # Orbital parameters
    log_period = pm.Normal("log_period", mu=np.log(period_guess), sigma=1.0)
    period = pm.Deterministic("period", tt.exp(log_period))
    t0 = pm.Normal("t0", mu=t0_guess, sigma=1.0)
    log_dur = pm.Normal("log_dur", mu=np.log(0.1), sigma=10.0)
    dur = pm.Deterministic("dur", tt.exp(log_dur))
    b = xo.distributions.ImpactParameter("b", ror=ror)

    # Set up the orbit
    orbit = xo.orbits.KeplerianOrbit(period=period, duration=dur, t0=t0, b=b)

    # Set up the mean transit model
    star = xo.LimbDarkLightCurve(u)
    lc_model = mean + 1e3 * tt.sum(
        star.get_light_curve(orbit=orbit, r=ror, t=x), axis=-1
    )

    # Finally the GP observation model
    gp = GaussianProcess(kernel, t=x, diag=yerr ** 2 + sigma ** 2)
    gp.marginal("obs", observed=y - lc_model)

    # Optimize the model
    map_soln = model.test_point
    map_soln = pmx.optimize(map_soln, [sigma])
    map_soln = pmx.optimize(map_soln, [ror, b, dur])
    map_soln = pmx.optimize(map_soln, noise_params)
    map_soln = pmx.optimize(map_soln, star_params)
    map_soln = pmx.optimize(map_soln)

    # Store our MAP solution
    lc_pred = pmx.eval_in_model(lc_model, map_soln)
    gp_pred = pmx.eval_in_model(gp.predict(y - lc_pred), map_soln)

    # Sample the posterior
    trace = pmx.sample(
        tune=1000,
        draws=10000,
        start=map_soln,
        chains=2,
        cores=2,
        return_inferencedata=False,
        random_seed=[286923464, 464329682],
    )

# Store the results
samples = np.vstack((trace["period"], trace["ror"], trace["b"])).T
np.savez(
    "../data/HD118203.npz",
    x=x,
    y=y,
    gp_pred=gp_pred,
    lc_pred=lc_pred,
    samples=samples,
    map_t0=map_soln["t0"],
    map_period=map_soln["period"],
    map_mean=map_soln["mean"],
)