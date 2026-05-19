# Basics of a Rule's Directives and Our Pipeline's Structure 
## Directives:

Directives are sub-headers within a Rule. Each Rule is its own unique job.

1. **`input`**
    +  Input directive contains the file(s) that we want to analyze.

2. **`output`**
    +  Output directive contains the output file(s) that we wish to generate. Here is where we can perform three reformatting steps: renaming, relocating, and changing the file text. After each edit in the current output directive, always compare and match the current rule’s output file name(s) with corresponding rule’s input file name(s) because these file name(s) need to match to guarantee these rules are paired and continuous.

3. **`envmodules`**
    +  Envmodules directive contains all of the modules needed to load per rule. In order to activate this directive, we have to use the command `--use-envmodules` in the main bash script command. Housing java, samtools, bedtools, bcftools, python, R.

4. **`params`**
    +  Params directive should contain anything that is not in the input files, For our pipeline, the params directive contains GATK, reference genome file, YAML file, wildcards, and non-input files.

5. **`log`**
    +  Log directive has two options. First, produces two files of both output log file and error output file. Second, combine the output and error file as one file. Currently, we are using the option second to save on storage.

6. **`benchmark`**
    +  Benchmark directive allows us to benchmark the time and data usage per output file(s) per rule as a .txt file. Below is an example of a benchmark's content and [for more info and notation](https://snakemake.readthedocs.io/en/v8.14.0/snakefiles/rules.html#benchmark-rules):
    ```
    s h:m:s max_rss max_vms max_uss max_pss io_in io_out mean_load cpu_time

    0.9619 0:00:00 14.50 105.73 1.91 3.82 48.00 0.00 0.00 0.96
    ```
    
7. **`message`**
    +  Message directive prints out the command within the `shell` directive. A great way to understand how all of the directives are inneracting to check for syntax.
  
8. **`shell`**
    +  Shell directive will tie all of the previous directives to format the complete bash script to pipe our input file(s) into output file(s). This tying process is via wildcards, which will be explained later. Additionally, we can activate our packages (e.g., GATK, Tabix, etc.) using their corresponding paths, which are stored and extracted from the YAML file.

9. **Others**
    +  Other directives: If you are curious about what other directives are available, feel free to check them out on your own time.
  
## Rules:
