# taseq
Data analysis tools for targeted amplicon sequencing (TA-seq)
(Renamed from 'tasdos')
#### version 1.1.0 (2024.12.3)

![sample.png](./fig/fig01.png)

## Outline

'taseq' is a set of tools for down stream analysis of targeted amplicon sequencing (TA-seq),
which is one of the most efficient genotyping method.
Input files are paired end fastq and VCF containing target SNP which was made by 'mkdesigner'.
We can get genotype file which is suitable to QTL analysis using R/qtl software just in few steps.

#### Citation
- Comming soon.

#### Update
- 2024.12.3: 1.1.0 Output folder name can now be specified. Test data provided.

## Install

### Install via PyPI
```
pip install taseq
```

#### Dependencies
 - python >=3.12
 - pandas >=2.2.2
 - matplotlib-base
 - samtools >=1.20
 - gatk4 >=4.5.0.0
 - picard >=3.1.1
 - bwa >=0.7.18

These must be installed manually.

## Usage
#### Tutorial
(1) Haplotype calling   
```
taseq_hapcall -I [directory_of_input_fastq] \
              -R reference_genome.fasta \
              -V target_VCF_made_by_mkdesigner.vcf \
              -n taseq_hapcall_1
```
Result file will be located as   
'./taseq_hapcall_1/result_taseq_hapcall.vcf'    

(2) Analyzing genotypes of each samples    
```
taseq_genotype -I taseq_hapcall_1/result_taseq_hapcall.vcf \
               -p1 (Name of parent A in the input VCF of 'taseq_hapcall') \
               -p2 (Name of parent B in the input VCF of 'taseq_hapcall') \
               -n taseq_genotype_1
```
Result file will be located as    
'./taseq_genotype_1/result_taseq_genotype.tsv'    

(3) Filter markers by designaetd thresholds    
```
taseq_filter -I taseq_genotype_1/result_taseq_genotype.tsv \
             --parent_sample1 (Name of a sample of parent A, if included) \
             --parent_sample2 (Name of a sample of parent B, if included) \
             -n taseq_filter_1
```
Result file will be located as
'./taseq_filter_1/result_taseq_filter.tsv'     
'./taseq_filter_1/result_taseq_filter_formated_for_Rqtl.csv'    
This file can be used as input file of R/qtl.    

(4) Draw genotype visually    
```
taseq_draw -I taseq_filter_1/result_taseq_filter.tsv \
           -F reference_genome.fasta.fai \
           -n taseq_draw_1
```
Result figures are located in
'./taseq_draw_1/'    

#### Commands
```
taseq_hapcall -h
usage: taseq_hapcall -I <Directory containing input FASTQ>
                     -R <File of reference FASTA>
                     -V <File of target VCF>
                     -n <Name of output directory>
                     ... 
options:
  -h, --help            show this help message and exit
  -I , --input          Directory containing input FASTQ.
                        This directory must contain only fastq file used in genotyping.
                        The names of fastq files must be unique for each [Name]_*R1* and [Name]_*R2*.
                        The string to the left of the first underscore is considered the sample name.
                        gzip (fastq.gz) supported.
  -R , --ref            File of reference genome (fasta).
  -V , --vcf            VCF File containing only target SNPs.
                        (VCF made by mkselect is recommended.)
  -n , --name           Name of output directory.
                        Already existing directory name is not allowed.
                        Default: taseq_hapcall.
  --cpu                 Number of CPUs to use.
                        Default: 2.
  --adapter             Adapter sequences used for trimming fastq.
                        NONE means the input fastq has already trimmed.
                        When CUSTOM designated, --adapterfile must be specified.
                        Choose from [NONE, NEXTERA, TRUSEQ, CUSTOM].
                        Default: NONE.
  --adapterfile         This is valid when --adapter = CUSTOM.
  --seqlen              Sequence length of fastq.
                        3 dash bases over this length will be cut.
                        Default: 150.
  --minlen              Ignore reads which are shorter than this value after trimming.
                        Default: 60.
  --quality_threshold   If the quality of the bases at both ends of a read
                        is below this threshold, it is deleted.
                        Default: 30.
  -v, --version         show program's version number and exit
```

```
taseq_genotype -h
usage: taseq_genotype -I <VCF file which is the output of taseq_hapcall>
                      -p1 <Parent name genotyped as A>
                      -p2 <Parent name genotyped as B>
                      -n <Name of output directory>
                      ... 
options:
  -h, --help        show this help message and exit
  -I , --input      VCF file which is the output of taseq_hapcall.
  -p1 , --parent1   Parent name genotyped as A.
                    Use the name of vcf column in the input file of taseq_hapcall.
  -p2 , --parent2   Parent name genotyped as B.
                    Use the name of vcf column in the input file of taseq_hapcall.
  -n , --name       Name of output directory.
                    Already existing directory name is not allowed.
                    Default: taseq_genotype.
  --mindep          Minimum depth to genotype.
                    Variants with depth lower than this
                    will be genotyped as missing.
                    Default: 6.
  --hetero_chi      Threshold value of chi-square when genotyping as hetero.
                    Default value is 3.84 (the threshold for p=0.05).
  --noise_level     When genotyping as homozygous, minor reads below this ratio will be ignored.
                    Default: 0.1.
  -v, --version     show program's version number and exit
```

```
taseq_filter -h
usage: taseq_filter -I <TSV file which is the output of taseq_genotype>
                    --parent_sample1 <Parent sample expected to be A>
                    --parent_sample2 <Parent sample expected to be B>
                    -n <Name of output directory>
                    ... 
options:
  -h, --help         show this help message and exit
  -I , --input       TSV file which is the output of taseq_genotype.
  --parent_sample1   Parent sample expected to be genotype A.
                     This must be specified if parental lines are included in your samples.
  --parent_sample2   Parent sample expected to be genotype B.
                     This must be specified if parental lines are included in your samples.
  -n , --name        Name of output directory.
                     Already existing directory name is not allowed.
                     Default: taseq_filter.
  --missing_rate     Markers with more missing than this
                     value will be removed
                     Default: 0.2.
  --check_parents    Test the genotype of the parent line.
                     If they are inconsistent with the predicted genotype, the marker will be removed.
                     This is invalid if -p1 and -p2 are not specified.
  --minor_freq       Threshold of minor allele frequency (MAF).
                     Markers whose MAF are lower than this,
                     they are removed.
                     Default: 0.
  -v, --version      show program's version number and exit
```

```
taseq_draw -h
usage: taseq_draw -I <TSV file which is the output of taseq_filter>
                  -F <FASTA Index file to draw chromosome>
                  -n <Name of output directory>
                  ... 
options:
  -h, --help     show this help message and exit
  -I , --input   TSV file which is the output of taseq_filter.
  -F , --fai     FASTA Index file to draw chromosome.
  -n , --name    Name of output directory.
                 Already existing directory name is not allowed.
                 Default: taseq_draw.
  --color_A      Color of genotype A (Default: orange).
                 Limited to color names that can be specified in matplotlib.
                 (The same applies below.)
  --color_B      Color of genotype B (Default: blue).
  --color_het    Color of heterozygous (Default: cyan).
  --color_miss   Color of missing genotype (Default: gray).
  --name_A       Name of line A (Default: A).
  --name_B       Name of line B (Default: B).
  -v, --version  show program's version number and exit
```
