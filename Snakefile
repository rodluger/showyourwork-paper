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


rule v1298tau:
    output:
        "src/figures/v1298tau.pdf"
    shell:
        "curl -L https://github.com/afeinstein20/v1298tau_tess/raw/c670e0/src/static/TESSaperture.pdf --output {output}"