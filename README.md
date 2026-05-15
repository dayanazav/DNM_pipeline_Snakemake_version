# _De novo_ mutation pipeline based in Snakemake 

Welcome! This repository contains a robust pipeline designed to capture de novo mutation within either 3-or 4-membered family pedigree through  variant calling and genomic analysis, inspired by the standards established in the [Mutationathon](https://elifesciences.org/articles/73577). It leverages Snakemake to ensure reproducible and scalable workflows.

## Prerequisites & Environment

This pipeline is managed via a Conda environment to ensure all dependencies are correctly versioned.

 + Workflow Manager: [Snakemake version 8.14.0](https://snakemake.readthedocs.io/en/v8.14.0/getting_started/installation.html)
 + Languages: Snakemake, Bash Scripting, Python, and YAML.

## Modules and Packages

#### Analysis Tools

 + [GATK(v4.1.9)](https://gatk.broadinstitute.org/hc/en-us/sections/360010932391-4-1-9-0): variant calling and sample analysis.
 + SAMTOOLS: Handles BAM conversion, sorting, indexing, and depth measurement.
 + BCFTOOLS: Used for reading and filtering information within VCF files.
 + BEDTOOLS: Facilitates comparisons and filtering between multiple VCF files.

#### Data Processing & Utilities

 + BGZIP & TABIX: For file compression (.gz) and indexing.
 + SEQTK, OLDBWA, & SAMBLASTER: Essential utilities for converting FASTQ files into BAM format.
 + JAVA: Manages memory allocation specifically for GATK operations.

#### Scripting & Visualization

 + Python: Custom scripts utilize `pandas`, `argparse`, `matplotlib`, `numpy`, and `yaml`.
 + R: Used for generating visualizations for quality control check 3 (QC3).

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

## How to use the Project:

### Snakefile walkthrough
 + Key section: at the top of the snakemake file. This Key section contains the configuration file of our only YAML file. Then, followed by the extracted information from the YAML file.
 + Rule: Rules can house multiple directives to provide the necessary commands for that specific input file(s) to become the output file(s). We used these directives: input, output, envmodules, params, threads, resources, log, benchmark, and shell.
 + 
 +

#### Directive walkthrough
+  Input directive contains the file(s) that we want to analyze.
+  Output directive contains the output file(s) that we wish to generate. Here is where we can perform three reformatting steps: renaming, relocating, and changing the file text. After each edit in the current output directive, always compare and match the current rule’s output file name(s) with corresponding rule’s input file name(s) because these file name(s) need to match to guarantee these rules are paired and continuous.
+  Envmodules directive contains all of the modules needed to load per rule. In order to activate this directive, we have to use the command `--use-envmodules` in the main bash script command. Housing java, samtools, bedtools, bcftools, python, R.
+  Params directive should contain anything that is not in the input files, For our pipeline, the params directive contains GATK, reference genome file, YAML file, wildcards, and non-input files.
+  Log directive has two options. First, produces two files of both output log file and error output file. Second, combine the output and error file as one file. Currently, we are using the option second to save on storage.
+  Benchmark directive allows us to benchmark the time and data usage per output file(s) per rule as a .txt file. Below is an example of a benchmark's content and [for more info and notation](https://snakemake.readthedocs.io/en/v8.14.0/snakefiles/rules.html#benchmark-rules):
```
s h:m:s max_rss max_vms max_uss max_pss io_in io_out mean_load cpu_time

0.9619 0:00:00 14.50 105.73 1.91 3.82 48.00 0.00 0.00 0.96
```
+  Shell directive will tie all of the previous directives to format the complete bash script to pipe our input file(s) into output file(s). This tying process is via wildcards, which will be explained later. Additionally, we can activate our packages (e.g., GATK, Tabix, etc.) using their corresponding paths, which are stored and extracted from the YAML file.
+  Other directives: If you are curious about what other directives are available, feel free to check them out on your own time.

### YAML walkthrough
The YAML file is a configuration file for our snakemake file.

Purpose: store all of our information is because it allows us to switch between samples without the need to edit the main snakemake file.


Need to add:
 + Paste in the species’ name
 + Directory path to your chosen output folder to contain all of the output files, log files, benchmark files, etc.
 + Path to this YAML file, Reference Genome, and Reference Index
 + Packages
     + Paste in their paths for the params directive can load them on to shell directive
     + Paste in the command from the blank in `load module ___`, so envmodules directive can load it 
 + Samples’ names or label IDs
 + The stating the 3 or 4 main relationships (i.e. father, mother, offspring, and grandchild*) in the pedigree
 + Species’ chromosome as an expanded list `[1, …, n]`

Either option works:
 + Known Variant File:
     + Paste in the path to the current list of known variant
     + Leave it blank so snakemake can make its own Known Variant File

Optional:
 + Offspring's gender as Male, Female, or * (default = *)

Do not edit:
 + Mutation Spectrum notation for filing in groups of AC, CT, CG, CA, AT, and AG

### Bash walkthrough

Command Explanations
 1. `-n` / `--dry-run`	: This generates a detailed preview of all rules that will be activated and the number of files to be processed. It allows you to double-check wildcards and ensure no rules are missing without actually executing code.
 2. `-s <file>.smk` :	By default, Snakemake looks for a file named Snakefile or snakefile. If your file is named something else (e.g., `pipeline_v1.smk`), you must use this flag to point to it.
 3. `-R` / `--force-run` :	Forces the re-execution of a specific rule or all rules. Useful if you've updated code but the input files haven't changed.
 4. `--rerun-incomplete`	: Automatically re-runs jobs that were interrupted or terminated before finishing in a previous run.
 5. `--rerun-triggers mtime` :	Tells Snakemake to trigger a re-run only if the modification time of an input file has changed.
 6. `--latency-wait <sec>`	: Defines how many seconds to wait for an output file to appear after a job finishes. Essential for network file systems (like HPC clusters) where file syncing can be slow.
 7. `--summary`	: Prints a table summarizing the status of all files in the pipeline (e.g., modification time, rule used, and if it needs to be updated).

Before submitting a pipeline, always perform a dry run to verify that wildcards are correct and no rules are missing. This generates a preview of the jobs to be executed without actually running them.
```bash
# Run a dry run
snakemake --dry-run

# Run a dry run for a specific file not named 'Snakefile'
snakemake -s type_in_file.smk --dry-run
```

Bash Script Template:
```bash
#!/bin/bash
# (Insert your specific scheduler directives here, e.g., #SBATCH or #PBS)
snakemake \
    -R \
    -s type_in_file_.smk \
    --cores <number_of_cores> \
    --use-envmodules \
    --rerun-incomplete \
    --rerun-triggers mtime \
    --latency-wait <seconds>
```

## Snakemake's Output Structure

Additional Files: species.yaml, all of the 4 python scripts, reference genome, and indexed reference genome
    + Special Note: If these additional files were detailed with their absolute path within the YAML file, then you do not have to switch their current location to the root_directory.
```
# Running with a known_variant.vcf file
root_directory
│
├── Snakefile
├── run_snakefile.sh 
├ ─ Additional Files* 
└── output
    ├── bams
    ├── DNM
    ├── DNM_summary
    ├── CombinedGVCF
    ├── GenotypeGVCF
    ├── HaplotypeCaller
    │    ├── haplotypeCaller_chr1.vcf, etc.
    │    └── benchmark
    ├── log
    ├── make_pedigree
    ├── mutation_spectrum
    ├── QC2
    ├── QC3
    ├── QC4
    └── {species}_{child}_ped.ped
```

```
# Running without a known_variant.vcf file
root_directory
│
├── Snakefile
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
