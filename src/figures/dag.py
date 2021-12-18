import graphviz
from pathlib import Path
import json
import subprocess


# Make sure we're running this from the workflow
try:
    snakemake
except NameError:
    raise Exception("This script must be run from within a Snakemake workflow.")

# Node border colors
colors = dict(
    zenodo="#1f77b4",
    analysis="black",
    script="black",
    figure="black",
    dataset="#1f77b4",
    other="black",
    edge="black",
)

# Get figure metadata
dependencies = snakemake.config.get("dependencies", {})
zenodo = snakemake.config.get("zenodo", {})
sandbox = snakemake.config.get("zenodo_sandbox", {})
with open(".showyourwork/scripts.json", "r") as f:
    script_info = json.load(f)

# Instantiate the graph
dot = graphviz.Digraph("dag", node_attr={"shape": "box", "penwidth": "2", "width": "1"})

# Figures
png_files = []
for figure in script_info.get("figures", []):

    # Get metadata for this figure
    script = script_info["figures"][figure]["script"]
    files = script_info["figures"][figure]["files"]

    # Figure node
    dot.node(script, label=script.replace("src/", ""), color=colors["script"])

    # Loop through figure dependencies
    for dependency in dependencies.get(script, []):
        if not dependency.endswith(".zenodo"):

            # Dependency node
            if zenodo.get(dependency, {}) or sandbox.get(dependency, {}):
                dot.node(
                    dependency,
                    label=dependency.replace("src/", ""),
                    color=colors["dataset"],
                    shape="box3d",
                )
            else:
                dot.node(
                    dependency,
                    label=dependency.replace("src/", ""),
                    color=colors["other"],
                    style="rounded",
                )

            # Zenodo metadata for this dependency
            for zenodo_info, zenodo_stem in zip(
                [zenodo.get(dependency, {}), sandbox.get(dependency, {})],
                ["10.5281", "10.5072"],
            ):
                if zenodo_info:

                    # Zenodo node
                    zenodo_id = zenodo_info["id"]
                    doi = f"{zenodo_stem}/zenodo.{zenodo_id}"
                    dot.node(
                        doi,
                        label=doi.replace("src/", ""),
                        color=colors["zenodo"],
                        shape="cylinder",
                        height="0.75",
                    )
                    dot.edge(doi, dependency, color=colors["edge"])

                    # Parent script node
                    zenodo_script = zenodo_info.get("script")
                    if zenodo_script:
                        dot.node(
                            zenodo_script,
                            label=zenodo_script.replace("src/", ""),
                            color=colors["analysis"],
                            style="rounded",
                        )
                        dot.edge(zenodo_script, doi, color=colors["edge"])
                        dot.edge(zenodo_script, dependency, color=colors["edge"])

            # Connect stuff
            for file in files:
                dot.edge(dependency, file, color=colors["edge"])

    # Figure images
    for file in files:

        png_file = file.replace(".pdf", ".png")
        subprocess.call(["convert", file, png_file])
        png_files.append(png_file)
        image = str(Path(png_file).relative_to(Path("src") / "figures"))

        dot.node(
            file,
            label="",
            image=image,
            penwidth="4",
            fixedsize="true",
            imagescale="false",
            width="2",
            height="1",
            color=colors["figure"],
        )
        dot.edge(script, file, color=colors["edge"])

        # Invisible edge (to force same rank for all figures)
        dot.edge(file, "anchor", color="#00000000")

# Invisble anchor
dot.node("anchor", label="", color="#00000000")

# Render the graph
dot.render(directory=Path(__file__).absolute().parents[0])

# Remove the png files
for file in png_files:
    if Path(file).exists():
        Path(file).unlink()