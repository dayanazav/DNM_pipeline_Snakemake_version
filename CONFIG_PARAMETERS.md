# Explanation of `species.yaml` Parameters:

### Special Note for parameters which use `"path/to/..."`:
 - If you include the relative path, the file has to be stored in the same folder as the Snakefile and run_snakefile.sh, which is the root directory.
 - If you include the absolute path, Snakefile and run_snakefile.sh will instead depend on the path given to access the file, not its root directory.

#### Notation:

1. **SPECIES**
    - Name of the given species. Used to title files and graphs.
    - Example: `"ape"`
  
2. **YAML**
    - Used as input for the python scripts
    - Example: `"/path/to/ape.yaml"`

3. **CHROMO**
    - An expanded list of all of the chromosomes, excluding the sex chromosomes.
    - Example: `[1,2A,2B,3,4,5,6,7,8,9,10]`
  
4. **PATH**
    - Path to the output folder.
    - Example: `"/path/to/output"`

5. **REF_GENOME**
    - Path to the species' reference genome.
    - Example: `"/path/to/ape.fa"`

6. **REF_INDEX***
    - Path to the species' indexed reference genome.
    - Example: `"/path/to/species.fa.fai"`
  
7. **DNM_FILTERS**
    - Path to the python script which contains all of the 10 filters and transmission filter
    - Example: `"/path/to/de_novo_filters.py"`
      
8. **DNM_TABLES**
    - Path to the python script which creates two tables containing that final discovered de novo mutations of the offspring and the transmissions within the grandchild, if the grandchild is present.
    - Example: `"/path/to/de_novo_tables.py"`
  
9. **DNM_GRAPH**
    - Path to the python script which creates a graph to visualize the effects of the filters on the de novo mutations with the offspring and the transmission, if the grandchild is present.
    - Example: `"/path/to/de_novo_graph.py"`

10. **MUT_SPEC**
    - Path to the python script which creates a graph of the the offspring's mutation specturm with 95% CI error bars.
    - Example: `"/path/to/mutation_spectrum_graph.py"`

11. **mutation_types**
    - Nesscary for rules `_`, `_`, and **MUT_SPEC** to calulate all precentages and generate a graph through the python script, **MUT_SPEC**.
    - Default: `["AC", "CT", "CG", "CA", "AT", "AG"]`

Optional:

1. **KNOWN_SITES**
    - Path to the vcf file which contains all of the known mutations for your species
    - Example: `"/path/to/known_variants_chr{chr}.vcf"`
  
#########
# These are all of the modules, tools, and apps used in the snakefile
# and snakefile is able to extract the below packages as config["BGZIP"]
# NOTE: You can change the between these two formats, path or envmodules, in both YAML file and snakefile. 
#########
#> Paste the paths to the packages for bash script activation
BGZIP: "/path/to/gzip" # bgzip compresses files as .gz
TABIX: "/path/to/tabix" # tabix to take in make index files for newly compressed files
SEQTK: "/path/to/seqtk" # seqtk to help convert the FASTQ file to a BAM file
OLDBWA: "/path/to/oldBwa" # oldbwa to help convert the FASTQ file to a BAM file
SAMBLASTER: "/path/to/samblaster" # samblaster to help convert the FASTQ file to a BAM file
GATK: "/path/to/gatk-4.1.9.0/gatk" # Genome Anaylsis Toolkit version 4.1.9.0
#> Paste in the last word(s) from "load module ___" and these will be activated within the envmodules directive 
SAMTOOLS: "/path/to/samtools" # samtools helps with converting the FASTQ to BAM, sorting, indexing, and measure depth
JAVA: "/path/to/java" # java helps organize the memory for GATK 
BCFTOOLS: "/path/to/bcftools" # bcftools allows us to read and filter information from a vcf file
BEDTOOLS: "/path/to/bedtools2" # bedtools allows us to read and filter information from two vcf files
R: "/path/to/r" # R allows us to visualize one of our quality checks
PYTHON: "/path/to/python" # Using the python packages of yaml, os, pandas, argparse, re, numpy, and matplotlib.pyplot
BWAMEMS: "/path/to/bwa-mem2"

# Snakefile extracts the family's information as config["SAMPLES"]["mother"]["name"]
SAMPLES:
   mother: 
     name: &mom "A" # Mother Name or label
   father: 
     name: &dad "B" # Father Name or label
   child:
     gender: "*" # Optional: Offspring Gender as either Male, Female, or *
     name: &kid "C" # Offspring Name or label
   f2: 
     name: &grand "D" # Required: (Grandchild's Name or label) OR (False or None or "")
   quad:
     - *dad
     - *mom
     - *kid
     - *grand
   family:
     - *dad
     - *mom
     - *kid
     - *grand
     - "Extra grandchildern" # Add extra grandchildern by their Name or label to the pedigree 

   
