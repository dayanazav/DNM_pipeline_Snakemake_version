# _De novo_ mutation pipeline based in Snakemake 

Welcome! This repository contains a robust pipeline designed to capture de novo mutation within either 3-or 4-membered family pedigree through  variant calling and genomic analysis, inspired by the standards established in the [Mutationathon](https://elifesciences.org/articles/73577). It leverages Snakemake to ensure reproducible and scalable workflows.

## Prerequisites & Environment

This pipeline is managed via a Conda environment to ensure all dependencies are correctly versioned.

 + Workflow Manager: [Snakemake version 8.14.0](https://snakemake.readthedocs.io/en/v8.14.0/getting_started/installation.html)
 + Languages: Snakemake, Bash Scripting, Python, and YAML.

## Installation
Steps to install dependencies and set up the environment.

 1. Install Conda: Ensure you have [Miniconda](https://docs.anaconda.com/free/miniconda/index.html) or [Anaconda](https://www.anaconda.com/download) installed.
 2. Set up the Environment: 
```bash
conda create -c conda-forge -c bioconda -n pipeline snakemake=8.14.0
conda activate pipeline
```
 3. Once snakemake is uplod a properly, activate the environment.
```bash
conda activate snakemake
```

## Overview

### Snakefile
 + Key section: at the top of the snakemake file. This Key section contains the configuration file of our only YAML file. Then, followed by the extracted information from the YAML file.
 + Rule: Rules can house multiple directives to provide the necessary commands for that specific input file(s) to become the output file(s). We used these directives: input, output, envmodules, params, threads, resources, log, benchmark, and shell.

### YAML 
The YAML file is a configuration file for our snakemake file.

Purpose: to run different species through its own unique YAML file without the need to directly edit the snakemake file to allow for quick reproducible.

### Bash Script

Before submitting a pipeline, always perform a dry run to verify that wildcards are correct and no rules are missing. This generates a preview of the jobs to be executed without actually running them.
```bash
# Run a dry run
snakemake --dry-run

# Run a dry run for a specific file not named 'Snakefile'
snakemake -s snakefile_dnm --dry-run
```

Bash Script Template:
```bash
#!/bin/bash
# (Insert your specific scheduler directives here, e.g., #SBATCH or #PBS)
snakemake \
    -R \
    -s snakefile_dnm \
    --cores <number_of_cores> \
    --use-envmodules \
    --rerun-incomplete \
    --rerun-triggers mtime \
    --latency-wait <seconds>
```

Command Explanations:
 1. `-n` / `--dry-run`	: This generates a detailed preview of all rules that will be activated and the number of files to be processed. It allows you to double-check wildcards and ensure no rules are missing without actually executing code.
 2. `-s <file>.smk` :	By default, Snakemake looks for a file named `Snakefile` or `snakefile`. If your file is named something else (e.g., `pipeline_v1.smk`), you must use this flag to point to it.
 3. `-R` / `--force-run` :	Forces the re-execution of a specific rule or all rules. Useful if you've updated code but the input files haven't changed.
 4. `--rerun-incomplete`	: Automatically re-runs jobs that were interrupted or terminated before finishing in a previous run.
 5. `--rerun-triggers mtime` :	Tells Snakemake to trigger a re-run only if the modification time of an input file has changed.
 6. `--latency-wait <sec>`	: Defines how many seconds to wait for an output file to appear after a job finishes. Essential for network file systems (like HPC clusters) where file syncing can be slow.
 7. `--summary`	: Prints a table summarizing the status of all files in the pipeline (e.g., modification time, rule used, and if it needs to be updated).

### Directed Acyclic Graph (DAG)

Purpose: The DAG display how the rules are connected to provide an overview of which rules will be activated when submitted.

```bash
snakemake --forceall --rulegraph | dot -Tpdf > path/to/workflow_dag.pdf.
```

[More Info.](https://snakemake.readthedocs.io/en/v8.4.1/executing/cli.html#visualization)

## Usage Instructions

Once you have:

- Downloaded any required pre-built indices, modules, and packages 
- Built the human reference genome index
- Built the clean FASTQ files or bams for each individual
- Downloaded our 4 python scripts and `snakefile_dnm`
- The file sturcture looks like this:
    - Additional Files: species.yaml, all of the 4 python scripts, reference genome, indexed reference genome, and if you have it the known variant vcf file. If these additional files were detailed with their absolute path within the YAML file, then you do not have to switch their current location to the root_directory.

```
# Running without a known_variant.vcf file
root_directory
│
├── snakefile_dnm
├── run_snakefile.sh 
├ ─ Additional Files* 
└── output
    └── fastq or bams
        ├── 
        └── 
```

You can run *snakefile_dnm*:
   1. Update the `species.yaml` file to set parameters (see [details](./CONFIG_PARAMETERS.md)).
   2. Check the workflow within the root_directory either with... 
      + testing out a dry run (see [details](https://github.com/dayanazav/DNM_pipeline_Snakemake_version/blob/main/README.md#bash-script))
      + visualizing with a DAG (see [details](https://github.com/dayanazav/DNM_pipeline_Snakemake_version/blob/main/README.md#directed-acyclic-graph-dag))
   3. Execute the workflow within the run directory (see [details](https://github.com/dayanazav/DNM_pipeline_Snakemake_version/blob/main/README.md#bash-script))


Then after running, your file setup should become like this:
```
# Running without a known_variant.vcf file
root_directory
│
├── snakefile_dnm
├── run_snakefile.sh 
├ ─ Additional Files* 
└── output
    ├── bams
    ├── BaseRecal
    ├── DNM
    ├── DNM_summary
    ├── CombinedGVCF
    ├── GATKfilters
    ├── GenotypeGVCF
    ├── HaplotypeCaller
    ├── known_variants
    ├── log
    ├── make_pedigree
    ├── mutation_spectrum
    ├── QC2
    ├── QC3
    ├── QC4
    ├── unknown_CombinedGVCF
    ├── unknown_GenotypeGVCF
    ├── unknown_HaplotypeCaller
    │    ├── unknown_haplotypeCaller_chr1.vcf, etc.
    │    └── benchmark
    ├── vio_mend
    └── {species}_{child}_ped.ped
```

## Contributing

Guidelines for pull requests, issues, and coding style.

## License

Specify your license here.
