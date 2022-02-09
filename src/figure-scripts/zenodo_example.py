import paths
import matplotlib.pyplot as plt

datasets = [
    "A.dat",
    "baz/B.dat",
    "foo/C.dat",
    "foo/bar/H.dat",
    "G.dat",
    "C.dat",
    "bar/H.dat",
    "G_copy.dat",
]

for dataset in datasets:
    assert (paths.data / dataset).exists()

plt.figure().savefig(paths.figures / "zenodo_example.pdf", bbox_inches="tight")