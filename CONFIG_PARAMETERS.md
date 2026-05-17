# Explanation of `species.yaml` Parameters:

### Special Notes:

Regrading parameters using `"path/to/..."`:

 - If you include the relative path, the file has to be stored in the same folder as the Snakefile and run_snakefile.sh, which is the root directory.
 - If you include the absolute path, Snakefile and run_snakefile.sh will instead depend on the path given to access the file, not its root directory.

Regrading parameters within the _Modules, Languages, and Tools_ :

Depending on what is the best why to activate these, you can choose either to activate and sync the YAML and Snakefile together
   + Option 1) Using the `params` directive with a `"path/to/..."` 
   + Option 2) Using the `envmodules` directive with the last word(s) from `"load module ___"`

 
---

---

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

7. **DEPTH**
    - Allows `rule DNM_Filters:` quick access to the sample's depth from `rule qc2_coverage_estimation:`.
    - DO NOT EDIT: `"{folder}/QC2/{sample}_gwide_coverage.txt"`

8. **DNM_FILTERS**
    - Path to the python script which contains all of the 10 filters and transmission filter
    - Example: `"/path/to/de_novo_filters.py"`
      
9. **DNM_TABLES**
    - Path to the python script which creates three tables:
      a. 
      b. containing that final discovered de novo mutations of the offspring
      c. the transmissions within the grandchild, if the grandchild is present.
    - Example: `"/path/to/de_novo_tables.py"`
  
10. **DNM_GRAPH**
    - Path to the python script which creates a graph to visualize the effects of the filters on the de novo mutations with the offspring and the transmission, if the grandchild is present.
    - Example: `"/path/to/de_novo_graph.py"`

11. **MUT_SPEC**
    - Path to the python script which creates a graph of the the offspring's mutation specturm with 95% CI error bars.
    - Example: `"/path/to/mutation_spectrum_graph.py"`

12. **mutation_types**
    - Nesscary for `rule _`, `rule _`, and `rule _` to calulate all precentages and generate a graph through the python script, **MUT_SPEC**.
    - Default: `["AC", "CT", "CG", "CA", "AT", "AG"]`

_Optional:_

1. **KNOWN_SITES**
    - Path to the vcf file which contains all of the known mutations for your species
    - Example: `"/path/to/known_variants_chr{chr}.vcf"`

_Modules, Languages, and Tools:_

1. **BGZIP**
    - bgzip compresses files as .gz
    - Option 1: `"/path/to/gzip"`
   
2. **TABIX**
    - tabix to take in make index files for newly compressed files
    - Option 1: `"/path/to/tabix"`
  
3. **SEQTK**
    - seqtk to help convert the FASTQ file to a BAM file
    - Option 1: `"/path/to/seqtk"`
  
4. **OLDBWA**
    - oldbwa to help convert the FASTQ file to a BAM file
    - Option 1: `"/path/to/oldBwa"`
  
5. **SAMBLASTER**
    - samblaster to help convert the FASTQ file to a BAM file
    - Option 1: `"/path/to/samblaster"`
  
6. **GATK**
    - Genome Anaylsis Toolkit version 4.1.9.0
    - Option 1: `"/path/to/gatk-4.1.9.0/gatk"`

7. **SAMTOOLS**
    - Samtools helps with converting the FASTQ to BAM, sorting, indexing, and measure depth
    - Option 2: `"bio/samtools"`
  
8. **JAVA**
    - java helps organize the memory for GATK 
    - Option 2: `"java"`
  
9. **BCFTOOLS**
    - bcftools allows us to read and filter information from a vcf file
    - Option 2: `"bcftools"`

10. **BEDTOOLS**
    - bedtools allows us to read and filter information from two vcf files
    - Option 2: `"bedtools2"`

11. **R**
    - R allows us to visualize one of our quality checks 
    - Option 2: `"r"`
   
12. **PYTHON**
    - Using the python packages of `yaml`, `os`, `pandas`, `argparse`, `re`, `numpy`, and `matplotlib.pyplot`
    - Option 2: `"python"`
   
13. **BWAMEMS**
    - *
    - Option 2: `"bwa-mem2"`

---

Snakefile notation to extract the mother's name: `config["SAMPLES"]["mother"]["name"]`
``` yaml
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
```
