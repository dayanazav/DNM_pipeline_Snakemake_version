# IMPORTS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
import pandas as pd
import yaml 
import argparse
import os 

def load_config(yaml_path):
    # opening the yaml file
    with open(yaml_path, 'r') as file:
        return yaml.safe_load(file)

def main():
    # INPUTS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    parser = argparse.ArgumentParser("Process input")
    parser.add_argument("--config", \
        help = "Input yaml file, include the whole path (do not include the final backlash)", \
            type = str, required = True)
    parser.add_argument("--table_1", \
        help = "Outputs a csv file of chromosome counts per filter and totals (has to be a csv). ", \
            type = str)
    parser.add_argument("--table_2", \
        help = "Outputs a csv of all discovered known variants (has to be a csv)", \
            type = str)
    parser.add_argument("--grand", \
        help = "Outputs a csv of all transmission mutations from grandchild. True by typing in the grandchild's name. False or None or blank to not create the Transmission table.", \
            type = str, required = True)
    parser.add_argument("--table_3", \
        help = "Outputs a csv of all discovered known variants (has to be a csv)", \
            type = str)

    args = parser.parse_args()
    config_yaml = args.config
    table_1 = args.table_1
    table_2 = args.table_2
    grand = args.grand
    table_3 = args.table_3 # if left blank, it is equaled to None.

    # PARAMETERS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Storing the general input for parameters  
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    # YAML ============================================================
    config = load_config(config_yaml)
    # configfile: config_yaml

    # # locate the species branch
    # species = config['SPECIES']

    # offspring =======================================================
    offspring = config['SAMPLES']['child']['name']
    print(f"Offspring = {offspring}","\n")

    # CHR =============================================================
    chromo = config['CHROMO'] # edit
    print(f"Chromosomes = {chromo}","\n")

    # FOLDER ==========================================================
    folder = config['PATH'] # edit
    print(f"folder = {folder}","\n")
    return table_1, table_2, table_3, offspring, chromo, folder, grand

# PART 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Creating dataframe for each chromosome and total for filters
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def filter_table(offspring = str, chromo = list, folder = str, table_1 = str) -> str:
    # creating table 1
    num = 0
    for i in chromo:
        df = pd.read_table(f"{folder}/DNM/original_dnm_V4_max_01_KNOWN/{offspring}_check_dnm_count_chr{i}.txt", #####EDIT THIS#######################################
                           sep = ":",
                           header = None, 
                           names = ["Filter", f"Chr {i}"])
        if not num: # for chromosome 1
            num += 1
            per_df = pd.DataFrame(columns=["Filter", f"Chr {i}"])
            per_df["Filter"] = df["Filter"]
            per_df[f"Chr {i}"] = df[f"Chr {i}"].values
        else: # all chromosomes, not 1
            per_df[f"Chr {i}"] = df[f"Chr {i}"].values
    per_df["Total"] = per_df.iloc[:, 1:].sum(axis=1)
    per_df.to_csv(table_1)
    return table_1

# PART 2 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Displaying all of our discovered positions from known variants 
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def discovered_table(filter = str, offspring = str, chromo = list, folder = str, table_2or3 = str) -> str:
    # creating table 2 and/or table 3
    print(f"Creating file for the {filter}")
    header = ["CHROMO", "POSITION", "REF", "ALT"]
    mutations = []
    for i in chromo: 
        with open(f"{folder}/DNM/original_dnm_V4_max_01_KNOWN/{offspring}_check_chr{i}_{filter}.vcf",'r') as file: #####EDIT THIS#######################################
            header_line = file.readline()
            while header_line[0:6]!='#CHROM':
                header_line=file.readline()
            for line in file: # this does .readline()
                items = line.split()
                if not line or line.startswith("#"):
                    continue  # skip metadata and empty lines
                chr_position = items[:2]
                ref_alt = items[3:5]
                row = chr_position + ref_alt
                dict = {title : [data] for title, data in zip(header, row)}
                mutations.append(pd.DataFrame(dict))
    combined_df = pd.concat(mutations, ignore_index=True)
    combined_df.to_csv(table_2or3, index=False)
    return table_2or3

if __name__ == '__main__':
    print("Opened de_novo_tables.py")
    ## Managing inputs and parameters
    table_1, table_2, table_3, offspring, chromo, folder, grand = main()


    ## Creating all 2 dataframes
    # Create the complete tables with per and total of all chromosomes from the filters
    ## table 1
    # columns : filters
    # rows : Per chromosome
    table1_name_csv = filter_table(offspring, chromo, folder, table_1)
    
    ## table 2
    # Create the complete table from known variants' positions
    # columns : chr#, position, ref, alt
    # rows : the individual position
    table2_name_csv = discovered_table("known_variants", offspring, chromo, folder, table_2)

    print("Checking paths:")
    print(f"Table 1: \n Path: {table1_name_csv}\n   Exists? {os.path.exists(table1_name_csv)}")
    print(f"Table 2: \n Path: {table2_name_csv}\n   Exists? {os.path.exists(table2_name_csv)}")

    ## OPTIONAL table 3 
    # If there was a grandchild, create the complete table from transmission' positions
    if (grand != "") and (grand != False) and (grand != None): 
       assert table_3 != None, "--table_3's entire was left blank. To make the transmission csv file, you need to fill it with the file name, file type, and optional offspring name and path"
       table3_name_csv = discovered_table("transmitted", offspring, chromo, folder, table_3)
       print(f"Table 3: \n Path: {table3_name_csv}\n    Exists? {os.path.exists(table3_name_csv)}")

    print("- Complete -")

pass
