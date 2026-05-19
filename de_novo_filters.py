## Author: Brian Lui. Modified by Priya Moorjani

import sys					# read chromosome number from bash
from scipy import stats
import getopt

version=4.0
options, remainder = getopt.getopt(sys.argv[1:], 'm:f:c:o', ['mother=','father=','child=','f2=','output=','vcf=','chr=','known_var=','child_DP=','mother_DP=','father_DP='])

for opt, arg in options:
    if opt in ('-m', '--mother'):
        mother = arg
    elif opt in ('-f', '--father'):
        father = arg
    elif opt in ('-f2', '--f2'):
        f2 = arg
    elif opt in ('-c', '--child'):
        child = arg
    elif opt in ('-o', '--output'):
        output = arg
    elif opt == '--chr':
        chr_num = arg
    elif opt == '--vcf':
        raw_variants_file = arg
    elif opt == '--known_var':
        known_variants_list_file = arg
    elif opt == '--child_DP':
        child_avg_depth = float(arg)
    elif opt == '--mother_DP':
         mother_avg_depth = float(arg)
    elif opt == '--father_DP':
        father_avg_depth = float(arg)
    elif opt == '--version':
        version = arg

## set variables 
poisson_threshold = .99  # threshold DP is distribued as a poisson 
binom_threshold = 0.01  # threshold for binomial pvalue for AB filter

#output files
dnm_count_file = output + '_dnm_count_chr' + chr_num + '.txt'
dnm_file = output + '_chr' + chr_num + '_dnm.vcf'
biallelic_file = output + '_chr' + chr_num + '_biallelic.vcf'
hard_filters_file = output + '_chr' + chr_num + '_hard_filters.vcf'
quality_file = output + '_chr' + chr_num + '_quality.vcf'
genotype_quality_file = output + '_chr' + chr_num + '_genotype_quality.vcf'
read_depth_file = output + '_chr' + chr_num + '_read_depth.vcf'
allelic_balance_file = output + '_chr' + chr_num + '_allelic_balance.vcf'
allelic_depth_child_file = output + '_chr' + chr_num + '_allelic_depth_child.vcf'
allelic_depth_parents_file = output + '_chr' + chr_num + '_allelic_depth_parents.vcf'
known_variants_file = output + '_chr' + chr_num + '_known_variants.vcf'
transmission_file = output + '_chr' + chr_num + '_transmitted.vcf'

# functions
def get_value(line, prop):						# find the value of the property within line
	index_start = line.find(prop)				# index where start defining property
	line_prop = line[index_start:]				# line from property to end
	index_end = line_prop.find(';')				# index where end defining property
	return float(line_prop[len(prop) + 1 : index_end])

def depth_filter(event_rate):
        pmf_unscaled = 0                                # Poisson Distribution's Probability Mass Function before / e^(event rate), to reduce accumulation of errors
        cdf_unscaled = 0                                # Poisson Distribution's Cumulative Distribution Function before / e^(event rate), to reduce accumulation of errors
        pmf = 0                                                 # Poisson Distribution's Probability Mass Function
        cdf = 0                                                 # Poisson Distribution's Cumulative Distribution Function
        events = 0                                              # Poisson Distribution's num events = read depth
        while cdf < (1-poisson_threshold):                              # increment depth until cdf reaches 00.01%, to find depth min
                pmf_unscaled = event_rate ** events / math.factorial(events)
                cdf_unscaled = cdf_unscaled + pmf_unscaled
                pmf = pmf_unscaled / math.e**(event_rate)
                cdf = cdf_unscaled / math.e**(event_rate)
                # for testing:  print(events,'\t',pmf,'\t',cdf)
                events = events + 1
        depth_min = events - 1                          # min depth to accept reads, 00.01 %tile
        while cdf < poisson_threshold:                          # increment depth until cdf reaches 99.99%, to find depth max
                pmf_unscaled = event_rate ** events / math.factorial(events)
                cdf_unscaled = cdf_unscaled + pmf_unscaled
                pmf = pmf_unscaled / math.e**(event_rate)
                cdf = cdf_unscaled / math.e**(event_rate)
                # for testing:  print(events,'\t',pmf,'\t',cdf)
                events = events + 1
        depth_max = events -1                   # max depth to accept reads, 99.99 %ile
        return(depth_min, depth_max)

# identify child, parent, offspring columns
raw_variants=open(raw_variants_file,'r')                # IN: raw variants
header_line=raw_variants.readline()                             # copy header until reach data lines
while header_line[0:6] != '#CHROM':
        header_line=raw_variants.readline()
header=header_line.split()
child_column = header.index(child)
father_column = header.index(father)
mother_column = header.index(mother)
try:
    f2
    f2_column = header.index(f2)
except NameError:
    f2="NonExistent"

### 1 Calling DNMs ###
# Homozygous REF in parents (0/0)
# Heterozygous in offspring (0/1)
raw_variants=open(raw_variants_file,'r')		# IN: raw variants
dnm=open(dnm_file,'w')							# OUT: DNMs file
dnm_count=open(dnm_count_file,'w')				# OUT: DNM count
num_pass=0										# append num DNMs count to DNM counts
header_line=raw_variants.readline()				# copy header until reach data lines
while header_line[0:6]!='#CHROM':
	dnm.write(header_line)
	header_line=raw_variants.readline()
dnm.write(header_line)							# write #CHROM line

for variant in raw_variants:
	variant_prop=variant.split()
	# note total col here == <offspring> <father> <mother> <child>
	child_genotype=variant_prop[child_column][0:3]
	mother_genotype=variant_prop[mother_column][0:3]
	father_genotype=variant_prop[father_column][0:3]
	if (child_genotype=='0/1' or child_genotype=='0|1' or child_genotype=='1|0' or child_genotype == '1/0') and (mother_genotype=='0/0' or mother_genotype=='0|0') and (father_genotype=='0/0' or father_genotype=='0|0'):
		dnm.write(variant)					# OUTPUT of DNMs filter, INPUT to biallelic filter
		num_pass += 1
dnm_count.write('DNM : ' + str(num_pass) + '\n')	# write dnm num pass to dnm counts
raw_variants.close()							# close files to save memory
dnm.close()
dnm_count.close()								# comment out if next step uses same script

### 2 Filtering ###
# Require DNM be biallelic SNP (ignore indels, multi-allelic sites)
dnm=open(dnm_file,'r')							# IN: DNMs file
biallelic=open(biallelic_file,'w')				# OUT: biallelic SNPs file
dnm_count=open(dnm_count_file,'a')				# OUT: DNM count
num_pass = 0									# append biallelic SNPs count to DNM counts
header_line=dnm.readline()						# copy header until reach data lines
while header_line[0:6]!='#CHROM':
	biallelic.write(header_line)
	header_line=dnm.readline()
biallelic.write(header_line)					# write #CHROM line
for variant in dnm:
	variant_prop=variant.split()
	ref_allele=variant_prop[3]
	alt_allele=variant_prop[4]
	if len(ref_allele)==1 and len(alt_allele)==1:	# test if ref allele and alt allele are each single nucleotides
		biallelic.write(variant)					# OUTPUT of biallelic filter, INPUT to hard filters
		num_pass += 1
dnm_count.write('biallelic pass: ' + str(num_pass) + '\n')	# write biallelic num pass to dnm counts
dnm.close()											# close files to save memory
biallelic.close()
dnm_count.close()									# comment out if next step uses same script

# GATK hard filters https://gatkforums.broadinstitute.org/gatk/discussion/2806/howto-apply-hard-filters-to-a-call-set
biallelic=open(biallelic_file,'r')				# IN: biallelic SNPs file
hard_filters=open(hard_filters_file,'w')		# OUT: hard filters file
dnm_count=open(dnm_count_file,'a')				# OUT: DNM count
num_pass = 0									# append hard filters count to DNM counts
header_line=biallelic.readline()				# copy header until reach data lines
while header_line[0:6]!='#CHROM':
	hard_filters.write(header_line)
	header_line=biallelic.readline()
hard_filters.write(header_line)					# write #CHROM line
for variant in biallelic:
	errors = []
	variant_prop=variant.split()
	info = variant_prop[7]
	if info.find('QD') != -1 and not (get_value(info,'QD') >= 2.0):		# QualByDepth: variant confidence (quality) / unfiltered depth of non-ref samples
		errors.append('qd2')
	if info.find('FS') != -1 and not (get_value(info,'FS') <= 60.0):	# FisherStrand: more strand bias => false pos calls
		errors.append('fs60')
	if info.find('MQ') != -1 and not (get_value(info,'MQ') >= 40.0):	# RMSMappingQuality: mapping quality of reads across all samples | Root Mean Square
		errors.append('mq40')
	if info.find('MQRankSum') != -1 and not (get_value(info,'MQRankSum') >= -12.5):		# MappingQualityRankSumTest: Rank Sum Test for mapping qualities (reads with ref bases vs. with alt allele)
		errors.append('mqranksum -12.5')
	if info.find('ReadPosRankSum') != -1 and not (get_value(info,'ReadPosRankSum') >= -8.0):	# ReadPosRankSumTest: Rank Sum Test for distance from end of read for reads with alt allele
		errors.append('readposranksum -8.0')
	if info.find('SOR') != -1 and not (get_value(info,'SOR') <= 3.0):	# StrandOddsRatio: higher values => more strand bias
		errors.append('sor3')
	if len(errors)==0:
		hard_filters.write(variant)
		num_pass += 1
dnm_count.write('hard filters pass: ' + str(num_pass) + '\n')	# write hard filters num pass to dnm counts
biallelic.close()										# close files to save memory
hard_filters.close()
dnm_count.close()										# comment out if next step uses same script

# Variant Quality
# QUAL >= 100
hard_filters=open(hard_filters_file,'r')			# IN: hard filters file
quality=open(quality_file,'w')						# OUT: quality filters file
dnm_count=open(dnm_count_file,'a')					# OUT: DNM counts
num_pass = 0										# append variant quality filtered count to DNM counts
header_line=hard_filters.readline()					# copy header until reach data lines
while header_line[0:6]!='#CHROM':
	quality.write(header_line)
	header_line=hard_filters.readline()
quality.write(header_line)							# write #CHROM line
for variant in hard_filters:
	variant_prop=variant.split()
	QUAL = float(variant_prop[5])					# variant quality
	if QUAL >= 100:
		quality.write(variant)
		num_pass += 1
dnm_count.write('quality pass: ' + str(num_pass) + '\n')	# write variant quality num pass to dnm counts
hard_filters.close()								# close files to save memory
quality.close()
dnm_count.close()									# comment out if next step uses same script

# Genotype Quality
# GQ > 40 in all 3 members of trio (mom, dad, child)
quality = open(quality_file,'r')							# IN: quality filters file
genotype_quality = open(genotype_quality_file,'w')			# OUT: genotype quality filters file
dnm_count = open(dnm_count_file,'a')						# OUT: DNM counts
num_pass = 0												# append genotype quality filtered count to DNM counts
header_line = quality.readline()							# copy header until reach data lines
while header_line[0:6] != '#CHROM':
	genotype_quality.write(header_line)
	header_line = quality.readline()
genotype_quality.write(header_line)							# write #CHROM line
for variant in quality:
	variant_prop=variant.split()
	child_GQ = int(variant_prop[child_column].split(':')[3])
	mother_GQ = int(variant_prop[mother_column].split(':')[3])
	father_GQ = int(variant_prop[father_column].split(':')[3])
	if child_GQ > 40 and mother_GQ > 40 and father_GQ > 40:
		genotype_quality.write(variant)
		num_pass += 1
dnm_count.write('genotype quality pass: ' + str(num_pass) + '\n')	# write genotype quality num pass to dnm counts
quality.close()												# close files to save memory
genotype_quality.close()
dnm_count.close()											# comment out if next step uses same script

# Read Depth
# Take the average depth of coverage of child, require DP between 0.01 and 99.99 %ile based on assuming a Poisson-distributed depth (lamba, or event rate, is avg depth as determined by GATK DepthOfCoverage).
import math											# need math.factorial
genotype_quality = open(genotype_quality_file,'r')	# IN: genotype quality filters file
read_depth = open(read_depth_file,'w')				# OUT: read depth filter file
dnm_count = open(dnm_count_file,'a')				# OUT: DNM counts
num_pass = 0										# append read depth filtered count to DNM counts
header_line=genotype_quality.readline()				# copy header until reach data lines
while header_line[0:6] != '#CHROM':
	read_depth.write(header_line)
	header_line = genotype_quality.readline()
read_depth.write(header_line)						# write #CHROM line

for variant in genotype_quality:
	variant_prop=variant.split()
	#child
	child_DP = int(variant_prop[child_column].split(':')[2])			# read depth
	child_dp_min,child_dp_max = depth_filter(child_avg_depth)
	print(child_avg_depth,'\t',child_DP,'\t',child_dp_min,'\t',child_dp_max,'\n')	
	# mother
	mother_DP = int(variant_prop[mother_column].split(':')[2])                        # read depth
	mother_dp_min,mother_dp_max = depth_filter(mother_avg_depth)
	print(mother_avg_depth,'\t',mother_DP,'\t',mother_dp_min,'\t',mother_dp_max,'\n')

	# father
	father_DP = int(variant_prop[father_column].split(':')[2])                        # read depth
	father_dp_min,father_dp_max = depth_filter(father_avg_depth)
	print(father_avg_depth,'\t',father_DP,'\t',father_dp_min,'\t',father_dp_max,'\n')

	# check DP in trio
	if (child_DP >= child_dp_min) and (child_DP <= child_dp_max) and (mother_DP >= mother_dp_min) and (mother_DP <= mother_dp_max) and (father_DP >= father_dp_min) and (father_DP <= father_dp_max):
		read_depth.write(variant)
		num_pass += 1
dnm_count.write('read depth filter count: ' + str(num_pass) + '\n')	# write read depth num pass to dnm counts
genotype_quality.close()										# close files to save memory
read_depth.close()
dnm_count.close()												# comment out if next step uses same script

# Allelic balance in child
# Perform a two-sided binomial test on H0: AB = 50% , HA: AB or 50%; filter if p-value > 0.05
binom_freq = 0.5
read_depth = open(read_depth_file,'r')					# IN: read depth filters file
allelic_balance = open(allelic_balance_file,'w')		# OUT: allelic balance filters file
dnm_count = open(dnm_count_file,'a')					# OUT: DNM counts
num_pass = 0											# append allelic balance filtered count to DNM counts
header_line = read_depth.readline()						# copy header until reach data lines
while header_line[0:6] != '#CHROM':
	allelic_balance.write(header_line)
	header_line = read_depth.readline()
allelic_balance.write(header_line)						# write #CHROM line
for variant in read_depth:
	variant_prop = variant.split()
	DP = int(variant_prop[child_column].split(':')[2])  # using info in DP
	allele_depth_list = variant_prop[child_column].split(':')[1] # using allele depth of non-ref allele
	allele_depth = allele_depth_list.split(',')[1]
	#print(allele_depth,'\t',DP,'\n')
	p_value = stats.binom_test(allele_depth, DP, p=binom_freq, alternative='two-sided')
	#print(p_value,'\n')
	if p_value > binom_threshold:
		allelic_balance.write(variant)
		num_pass += 1
dnm_count.write('allelic balance pass: ' + str(num_pass) + '\n')	# write allelic balance num pass to dnm counts
read_depth.close()										# close files to save memory
allelic_balance.close()
dnm_count.close()										# comment out if next step uses same script

# Allelic depth in child
# Require >= 3 reads supporting DNM in child
allelic_balance = open(allelic_balance_file, 'r')			# IN: allelic balance file
allelic_depth_child = open(allelic_depth_child_file, 'w')	# OUT: allelic depth in child file
dnm_count = open(dnm_count_file, 'a')						# OUT: DNM counts
num_pass = 0												# append allelic depth in child filtered count to DNM counts
header_line = allelic_balance.readline()					# copy header until reach data lines
while header_line[0:6] != '#CHROM':
	allelic_depth_child.write(header_line)
	header_line = allelic_balance.readline()
allelic_depth_child.write(header_line)						# write #CHROM line
for variant in allelic_balance:
	variant_prop = variant.split()
	allelic_depth_dnm = int(variant_prop[child_column].split(':')[1].split(',')[1])
	if allelic_depth_dnm >= 3: 
		allelic_depth_child.write(variant)
		num_pass += 1
dnm_count.write('allelic depth in child pass: ' + str(num_pass) + '\n')	# write allelic depth in child num pass to dnm count file
allelic_balance.close()												# close files to save memory
allelic_depth_child.close()
dnm_count.close()													# comment out if next step uses same script

# Allelic depth in parents
# Require AD = 0 in both one parent
allelic_depth_child = open(allelic_depth_child_file, 'r')		# IN: allelic depth in child file
allelic_depth_parents = open(allelic_depth_parents_file, 'w')	# OUT: allelic depth in parents file
dnm_count = open(dnm_count_file, 'a')							# OUT: DNM counts
num_pass = 0													# append allelic depth in parents filtered count to DNM counts
header_line = allelic_depth_child.readline()
while header_line[0:6] != '#CHROM':
	allelic_depth_parents.write(header_line)
	header_line = allelic_depth_child.readline()
allelic_depth_parents.write(header_line)
for variant in allelic_depth_child:
	variant_prop = variant.split()
	allelic_depth_mother = int(variant_prop[mother_column].split(':')[1].split(',')[1])
	allelic_depth_father = int(variant_prop[father_column].split(':')[1].split(',')[1])
	if allelic_depth_mother == 0 and allelic_depth_father == 0:
		allelic_depth_parents.write(variant)
		num_pass += 1
dnm_count.write('allelic depth in parents pass: ' + str(num_pass) + '\n')	# write allelic depth in parents num pass to dnm count file
allelic_depth_child.close()											# close files to save memory
allelic_depth_parents.close()
dnm_count.close()													# comment out if next step uses same script

# Known variant filter
# Remove all putative DNMs that have previously been seen in an unrelated individual (based on population allele frequency data) (check chromosome and position)
# gorilla: /global/scratch2/m_chintalapati/mutation/gorilla/ref/lifted_gorGor4_known_snps.vcf
# done per chromosome
# compare each variant in allelic_depth_parents to known_snps to filter out known variants

allelic_depth_parents = open(allelic_depth_parents_file, 'r')   # IN: allelic depth in parents file
known_variants_list = open(known_variants_list_file, 'r')       # IN: list of known variants specific to chromosome; without preprocessing 3.5G
known_variants = open(known_variants_file, 'w')                 # OUT: DNMs after filtering out known variants
dnm_count = open(dnm_count_file, 'a')                           # OUT: DNM counts

num_pass = 0                                                    # append known variant filtered count to DNM counts

# --- copy header from allelic_depth_parents to output ---
header_line = allelic_depth_parents.readline()                  # copy header
while not header_line.startswith('#CHROM'):
    known_variants.write(header_line)
    header_line = allelic_depth_parents.readline()
known_variants.write(header_line)                               # write #CHROM line

# --- skip header in known_variants_list ---
line = known_variants_list.readline()
while line.startswith('##'):
    line = known_variants_list.readline()

if line.startswith('#'):  # skip column header
    line = known_variants_list.readline()

# Now line should be first data row
if line.strip():
    fields = line.strip().split('\t')
    known_variants_pos = int(fields[1])   # POS field
else:
    known_variants_pos = ''

# --- main filtering loop ---
for variant in allelic_depth_parents:
    variant_prop = variant.split()
    variant_pos = int(variant_prop[1])

    # Scroll known-variants list until we reach or pass variant_pos
    while known_variants_pos != '' and known_variants_pos < variant_pos:
        line = known_variants_list.readline()
        if not line:
            known_variants_pos = ''
            break
        if line.startswith('#'):  # safety skip
            continue
        fields = line.strip().split('\t')
        known_variants_pos = int(fields[1])

    # If POS does not match → not a known variant → keep it
    if known_variants_pos != variant_pos:
        known_variants.write(variant)
        num_pass += 1

dnm_count.write('known variant filter pass: ' + str(num_pass) + '\n')

allelic_depth_parents.close()
known_variants_list.close()
known_variants.close()
dnm_count.close()

# 3 Estimate Transmission
# Consider transmitted if AD >= 2 in F2
# (Previously, consider transmitted if GT = 0/1 in F2; not much difference between the two)

if f2 != "NonExistent":
    known_variants = open(known_variants_file, 'r')		# IN: known variants file
    transmission = open(transmission_file, 'w')			# OUT: variants transmitted to F2 (not list of DNMs)
    dnm_count = open(dnm_count_file, 'a')				# OUT: DNM count file
    transmitted = 0									# append transmission rate to DNM count file, though not list of DNMs
    header_line = known_variants.readline()				# copy header

    while header_line[0:6] != '#CHROM':
        transmission.write(header_line)
        header_line = known_variants.readline()
    transmission.write(header_line)						# write #CHROM line

    for variant in known_variants:
        variant_prop = variant.split()
        f2 = variant_prop[f2_column]					# data for F2 individual
        AD = int(f2.split(':')[1].split(',')[1])		# allelic depth for F2 individual
        if AD >= 2:										# consider transmitted if AD >= 2 in F2
            transmission.write(variant)
            transmitted += 1
        
    dnm_count.write('transmission (should be ~1/2 filtered variants): ' + str(transmitted) + '\n')	# write transmission to DNM count file, though not a count of DNMs
    known_variants.close()								# close files to save memory
    transmission.close()
    dnm_count.close()									# comment out if next step uses same script
