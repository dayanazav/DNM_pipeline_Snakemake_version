
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
