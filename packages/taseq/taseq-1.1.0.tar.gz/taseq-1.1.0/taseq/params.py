import argparse
import os
import sys
from taseq.__init__ import __version__

class Params(object):

    def __init__(self, program_name):
        self.program_name = program_name

    def set_options(self):
        if self.program_name == 'hapcall':
            parser = self.hapcall_options()
        elif self.program_name == 'genotype':
            parser = self.genotype_options()
        elif self.program_name == 'filter':
            parser = self.filter_options()
        elif self.program_name == 'draw':
            parser = self.draw_options()
        elif self.program_name == 'default':
            parser = self.default_options()

        if len(sys.argv) == 1:
            args = parser.parse_args(['-h'])
        else:
            args = parser.parse_args()
        return args
    
    def hapcall_options(self):
        parser = argparse.ArgumentParser(description='taseq version {}'.format(__version__),formatter_class=argparse.RawTextHelpFormatter)
        parser.usage = ('taseq_hapcall -I <Directory containing input FASTQ>\n'
                        '              -R <File of reference FASTA>\n'
                        '              -V <File of target VCF>\n'
                        '              -n <Name of output directory>\n'
                        '              ... \n')

        # set options
        parser.add_argument('-I', '--input',
                            action='store',
                            required=True,
                            type=str,
                            help=('Directory containing input FASTQ.\n'
                                  'This directory must contain only fastq file used in genotyping.\n'
                                  'The names of fastq files must be unique for each [Name]_*R1* and [Name]_*R2*.\n'
                                  'The string to the left of the first underscore is considered the sample name.\n'
                                  'gzip (fastq.gz) supported.\n'),
                            metavar='')
        
        parser.add_argument('-R', '--ref',
                            action='store',
                            required=True,
                            type=str,
                            help='File of reference genome (fasta).',
                            metavar='')
        
        parser.add_argument('-V', '--vcf',
                            action='store',
                            required=True,
                            type=str,
                            help=('VCF File containing only target SNPs.\n'
                                  '(VCF made by mkselect is recommended.)\n'),
                            metavar='')
        
        parser.add_argument('-n', '--name',
                            action='store',
                            default='taseq_hapcall',
                            type=str,
                            help=('Name of output directory.\n'
                                  'Already existing directory name is not allowed.\n'
                                  'Default: taseq_hapcall.\n'),
                            metavar='')

        parser.add_argument('--cpu',
                            action='store',
                            default=2,
                            type=int,
                            help=('Number of CPUs to use.\n'
                                  'Default: 2.\n'),
                            metavar='')
        
        parser.add_argument('--adapter',
                            action='store',
                            default='NONE',
                            choices=['NONE', 'NEXTERA', 'TRUSEQ', 'CUSTOM'],
                            help=('Adapter sequences used for trimming fastq.\n'
                                  'NONE means the input fastq has already trimmed.\n'
                                  'When CUSTOM designated, --adapterfile must be specified.\n'
                                  'Choose from [NONE, NEXTERA, TRUSEQ, CUSTOM].\n'
                                  'Default: NONE.\n'),
                            metavar='')
        
        parser.add_argument('--adapterfile',
                            action='store',
                            type=str,
                            help=('This is valid when --adapter = CUSTOM.\n'),
                            metavar='')
        
        parser.add_argument('--seqlen',
                            action='store',
                            default=150,
                            type=int,
                            help=('Sequence length of fastq.\n'
                                  '3 dash bases over this length will be cut.\n'
                                  'Default: 150.\n'),
                            metavar='')
        
        parser.add_argument('--minlen',
                            action='store',
                            default=60,
                            type=int,
                            help=('Ignore reads which are shorter than this value after trimming.\n'
                                  'Default: 60.\n'),
                            metavar='')
        
        parser.add_argument('--quality_threshold',
                            action='store',
                            default=30,
                            type=int,
                            help=('If the quality of the bases at both ends of a read\n'
                                  'is below this threshold, it is deleted.\n'
                                  'Default: 30.\n'),
                            metavar='')
        
        # set version
        parser.add_argument('-v', '--version',
                            action='version',
                            version='%(prog)s {}'.format(__version__))
        return parser

    def genotype_options(self):
        parser = argparse.ArgumentParser(description='taseq version {}'.format(__version__),formatter_class=argparse.RawTextHelpFormatter)
        parser.usage = ('taseq_genotype -I <VCF file which is the output of taseq_hapcall>\n'
                        '               -p1 <Parent name genotyped as A>\n'
                        '               -p2 <Parent name genotyped as B>\n'
                        '               -n <Name of output directory>\n'
                        '               ... \n')

        # set options
        parser.add_argument('-I', '--input',
                            action='store',
                            required=True,
                            type=str,
                            help='VCF file which is the output of taseq_hapcall.',
                            metavar='')
        
        parser.add_argument('-p1', '--parent1',
                            action='store',
                            required=True,
                            type=str,
                            help=('Parent name genotyped as A.\n'
                                  'Use the name of vcf column in the input file of taseq_hapcall.\n'),
                            metavar='')
        
        parser.add_argument('-p2', '--parent2',
                            action='store',
                            required=True,
                            type=str,
                            help=('Parent name genotyped as B.\n'
                                  'Use the name of vcf column in the input file of taseq_hapcall.\n'),
                            metavar='')
        
        parser.add_argument('-n', '--name',
                            action='store',
                            default='taseq_genotype',
                            type=str,
                            help=('Name of output directory.\n'
                                  'Already existing directory name is not allowed.\n'
                                  'Default: taseq_genotype.\n'),
                            metavar='')
        
        parser.add_argument('--mindep',
                            action='store',
                            default=6,
                            type=int,
                            help=('Minimum depth to genotype.\n'
                                  'Variants with depth lower than this\n'
                                  'will be genotyped as missing.\n'
                                  'Default: 6.\n'),
                            metavar='')

        parser.add_argument('--hetero_chi',
                            action='store',
                            default=3.84,
                            type=float,
                            help=('Threshold value of chi-square when genotyping as hetero.\n'
                                  'Default value is 3.84 (the threshold for p=0.05).\n'),
                            metavar='')
        
        parser.add_argument('--noise_level',
                            action='store',
                            default=0.1,
                            type=float,
                            help=('When genotyping as homozygous, minor reads below this ratio will be ignored.\n'
                                  'Default: 0.1.\n'),
                            metavar='')

        # set version
        parser.add_argument('-v', '--version',
                            action='version',
                            version='%(prog)s {}'.format(__version__))
        return parser

    def filter_options(self):
        parser = argparse.ArgumentParser(description='taseq version {}'.format(__version__),formatter_class=argparse.RawTextHelpFormatter)
        parser.usage = ('taseq_filter -I <TSV file which is the output of taseq_genotype>\n'
                        '             --parent_sample1 <Parent sample expected to be A>\n'
                        '             --parent_sample2 <Parent sample expected to be B>\n'
                        '             -n <Name of output directory>\n'
                        '             ... \n')

        # set options
        parser.add_argument('-I', '--input',
                            action='store',
                            required=True,
                            type=str,
                            help='TSV file which is the output of taseq_genotype.',
                            metavar='')
        
        parser.add_argument('--parent_sample1',
                            action='store',
                            default=None,
                            type=str,
                            help=('Parent sample expected to be genotype A.\n'
                                  'This must be specified if parental lines are included in your samples.\n'),
                            metavar='')
        
        parser.add_argument('--parent_sample2',
                            action='store',
                            default=None,
                            type=str,
                            help=('Parent sample expected to be genotype B.\n'
                                  'This must be specified if parental lines are included in your samples.\n'),
                            metavar='')
        
        parser.add_argument('-n', '--name',
                            action='store',
                            default='taseq_filter',
                            type=str,
                            help=('Name of output directory.\n'
                                  'Already existing directory name is not allowed.\n'
                                  'Default: taseq_filter.\n'),
                            metavar='')
        
        parser.add_argument('--missing_rate',
                            action='store',
                            default=0.2,
                            type=float,
                            help=('Markers with more missing than this\n'
                                  'value will be removed\n'
                                  'Default: 0.2.\n'),
                            metavar='')

        parser.add_argument('--check_parents',
                            action='store_true',
                            help=('Test the genotype of the parent line.\n'
                                  'If they are inconsistent with the predicted genotype, the marker will be removed.\n'
                                  'This is invalid if -p1 and -p2 are not specified.\n'))

        parser.add_argument('--minor_freq',
                            action='store',
                            default=0,
                            type=float,
                            help=('Threshold of minor allele frequency (MAF).\n'
                                  'Markers whose MAF are lower than this,\n'
                                  'they are removed.\n'
                                  'Default: 0.\n'),
                            metavar='')

        # set version
        parser.add_argument('-v', '--version',
                            action='version',
                            version='%(prog)s {}'.format(__version__))
        return parser
    
    def draw_options(self):
        parser = argparse.ArgumentParser(description='taseq version {}'.format(__version__),formatter_class=argparse.RawTextHelpFormatter)
        parser.usage = ('taseq_draw -I <TSV file which is the output of taseq_filter>\n'
                        '           -F <FASTA Index file to draw chromosome>\n'
                        '           -n <Name of output directory>\n'
                        '           ... \n')

        # set options
        parser.add_argument('-I', '--input',
                            action='store',
                            required=True,
                            type=str,
                            help='TSV file which is the output of taseq_filter.',
                            metavar='')

        parser.add_argument('-F', '--fai',
                            action='store',
                            required=True,
                            type=str,
                            help='FASTA Index file to draw chromosome.',
                            metavar='')
        
        parser.add_argument('-n', '--name',
                            action='store',
                            default='taseq_draw',
                            type=str,
                            help=('Name of output directory.\n'
                                  'Already existing directory name is not allowed.\n'
                                  'Default: taseq_draw.\n'),
                            metavar='') 
        
        parser.add_argument('--color_A',
                            action='store',
                            default='orange',
                            type=str,
                            help='Color of genotype A (Default: orange).\n'
                                 'Limited to color names that can be specified in matplotlib.\n'
                                 '(The same applies below.)',
                            metavar='')
        
        parser.add_argument('--color_B',
                            action='store',
                            default='blue',
                            type=str,
                            help='Color of genotype B (Default: blue).',
                            metavar='')

        parser.add_argument('--color_het',
                            action='store',
                            default='cyan',
                            type=str,
                            help='Color of heterozygous (Default: cyan).',
                            metavar='')

        parser.add_argument('--color_miss',
                            action='store',
                            default='gray',
                            type=str,
                            help='Color of missing genotype (Default: gray).\n',
                            metavar='')

        parser.add_argument('--name_A',
                            action='store',
                            default='A',
                            type=str,
                            help='Name of line A (Default: A).',
                            metavar='')
        
        parser.add_argument('--name_B',
                            action='store',
                            default='B',
                            type=str,
                            help='Name of line B (Default: B).',
                            metavar='')

        # set version
        parser.add_argument('-v', '--version',
                            action='version',
                            version='%(prog)s {}'.format(__version__))
        return parser

    def default_options(self):
        parser = argparse.ArgumentParser(description='taseq version {}'.format(__version__),formatter_class=argparse.RawTextHelpFormatter)
        parser.usage = ('Commands that can be executed with taseq are as follows:\n'
                        '  taseq_hapcall\n'
                        '  taseq_genotype\n'
                        '  taseq_filter\n'
                        '  taseq_draw\n')
        # set version
        parser.add_argument('-v', '--version',
                            action='version',
                            version='%(prog)s {}'.format(__version__))
        return parser

    def hapcall_check_args(self, args):
        #Does the same name directory exist?
        if os.path.isdir(args.name):
            sys.stderr.write(('  Output directory already exist.\n'
                              '  Please rename the --name.\n'))
            sys.exit(1)
        
        #input fastq
        if not os.path.isdir(args.input):
            sys.stderr.write(('  Input fastq directory does not exist.\n'))
            sys.exit(1)
        #input reference genome
        if not os.path.isfile(args.ref):
            sys.stderr.write(('  Input reference genome does not exist.\n'))
            sys.exit(1)
        #input vcf
        if not os.path.isfile(args.vcf):
            sys.stderr.write(('  Input VCF does not exist.\n'))
            sys.exit(1)

