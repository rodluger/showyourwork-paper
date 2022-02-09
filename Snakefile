rule random_numbers:
    output:
        "src/data/random_numbers.dat"
    conda:
        "environment.yml"
    params:
        seed=0
    script:
        "src/scripts/generate_random_numbers.py"