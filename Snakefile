# User config
configfile: "showyourwork.yml"
    

# Import the showyourwork module
module showyourwork:
    snakefile:
        "showyourwork/workflow/Snakefile"
    config:
        config


# Use all default rules
use rule * from showyourwork



rule dag:
    input:
        "src/figures/dag.py",
        showyourwork.figures
    output:
        "src/figures/dag.gv.pdf",
        temp("src/figures/dag.gv")
    conda:
        "environment.yml"
    script:
        "src/figures/dag.py"


showyourwork.rules.pdf.rule._input.append(workflow._rules["dag"].output[0])