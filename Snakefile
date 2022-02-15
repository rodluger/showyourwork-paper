rule random_numbers:
    output:
        "src/data/random_numbers.dat"
    conda:
        "environment.yml"
    cache:
        True
    params:
        seed=0
    script:
        "src/scripts/generate_random_numbers.py"


rule many_datasets:
    output:
        directory("src/data/many_datasets")
    conda:
        "environment.yml"
    cache:
        True
    params:
        seed=0
    script:
        "src/scripts/generate_many_datasets.py"