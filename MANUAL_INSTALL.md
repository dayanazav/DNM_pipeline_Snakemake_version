## Prerequisites & Environment

This pipeline is managed via a Conda environment to ensure all dependencies are correctly versioned.

 + Workflow Manager: [Snakemake version 8.14.0](https://snakemake.readthedocs.io/en/v8.14.0/getting_started/installation.html)
 + Languages: Snakemake, Bash Scripting, Python, and YAML.

## Modules and Packages

 + [GATK(v4.1.9)](https://gatk.broadinstitute.org/hc/en-us/sections/360010932391-4-1-9-0): variant calling and sample analysis.
 + SAMTOOLS: Handles BAM conversion, sorting, indexing, and depth measurement.
 + BCFTOOLS: Used for reading and filtering information within VCF files.
 + BEDTOOLS: Facilitates comparisons and filtering between multiple VCF files.
 + BGZIP & TABIX: For file compression (.gz) and indexing.
 + SEQTK, OLDBWA, & SAMBLASTER: Essential utilities for converting FASTQ files into BAM format.
 + JAVA: Manages memory allocation specifically for GATK operations.
 + R: Used for generating visualizations for quality control check 3 (QC3).
 + Python (version >= 3.11.6)
     + `pandas` (version >= 2.2.2)
     + `argparse` (version >= 1.1)
     + `matplotlib` (version >= 3.8.4)
     + `numpy` (version >= 1.26.4)
     + `yaml` (version >= 6.0.1)
     + `sys` 
     + `stats` from `scipy` (version >= 1.13.1)
     + `getopt`
