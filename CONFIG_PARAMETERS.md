# Explanation of `species.yaml` Parameters:

### Special Note for parameters which use `"path/to/..."`:
 - If you include the relative path, the file has to be stored in the same folder as the Snakefile and run_snakefile.sh, which is the root directory.
 - If you include the absolute path, Snakefile and run_snakefile.sh will instead depend on the path given to access the file, not its root directory.

#### Notation:

1. **SPECIES**
    - Name of the given species
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
    - Path to the output folder.
    - Example: `"/path/to/ape.fa"`
