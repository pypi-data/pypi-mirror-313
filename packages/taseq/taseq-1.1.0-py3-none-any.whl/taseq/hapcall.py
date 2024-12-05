#!/usr/bin/env python3
from multiprocessing import Pool
import sys
import subprocess as sbp
import os

import pandas as pd
from taseq.adapter import Adapter
from taseq.extractref import ExtractRef
from taseq.mapping import Mapping
from taseq.mergevcf import MergeVcf
from taseq.params import Params
from taseq.refindex import RefIndex
from taseq.trimmomatic import Trimmomatic
from taseq.utils import prepare_cmd, read_vcf, time_for_filename, time_stamp

pm = Params('hapcall')
args = pm.set_options()


class Hapcall(object):
    def __init__(self, args):
        pm.hapcall_check_args(args)
        self.args = args
        self.ref = args.ref
        self.input = args.input #fastq directry
        self.seqlen =  args.seqlen
        self.minlen = args.minlen
        self.qual = args.quality_threshold
        self.adapter = args.adapter
        self.cpu = args.cpu

        #This is the name of output directory
        self.dir = args.name

        #get sample list
        tmp_fqlist = os.listdir(self.input)
        self.slist = [] #list of sample names
        for f in tmp_fqlist:
            #The strings left of 1st '_' are considered to be sample name
            self.slist.append(f.split('_')[0])
        self.slist = list(set(self.slist)) #extract unique values
        self.slist.sort()
        print(time_stamp(), 
              '{} samples are processing.'.format(len(self.slist)), flush=True)
        
        #get VCF as dataframe
        tmp_vcf = read_vcf(args.vcf)
        self.vcf_head = tmp_vcf[0] #List
        self.vcf_col = tmp_vcf[1] #List
        self.vcf = pd.DataFrame(tmp_vcf[2], columns=self.vcf_col) #dataframe

    def setdir(self):
        cmd1 = ('mkdir {0} {0}/log {0}/bam {0}/vcf '
                '{0}/adapter {0}/fastq {0}/ref').format(self.dir)
        cmd1 = prepare_cmd(cmd1)
        try:
            sbp.run(cmd1,
                    stdout=sbp.DEVNULL,
                    stderr=sbp.DEVNULL,
                    shell=True,
                    check=True)
        except sbp.CalledProcessError:
            print(time_stamp(), 
                  '!!ERROR!! Makeing output directory was failed.\n', flush=True)
            sys.exit(1)

    def command(self):
        #Output command info
        command = ' '.join(sys.argv)
        fn = '{}/command.txt'.format(self.dir)
        with open(fn, 'w') as f:
            f.write('{}\n'.format(command))

    def refindex(self):
        ri = RefIndex(self.ref, self.dir)
        ri.run()

    def setadapter(self):
        ad = Adapter(self.dir, self.adapter, self.args.adapterfile)
        ad.run()

    def trimmomatic(self, num):
        ri = Trimmomatic(self.input, self.slist[num], self.dir, 
                        self.seqlen, self.minlen, self.qual, self.adapter)
        ri.run()

    def extractref(self):
        er = ExtractRef(self.ref, self.vcf, self.dir)
        er.run()

    def mapping(self, num):
        ma = Mapping(self.dir, self.slist[num])
        ma.run()

    def mergevcf(self):
        ma = MergeVcf(self.dir, self.slist)
        ma.run()

def main():
    print(time_stamp(), 'taseq_hapcall started.', flush=True)

    prog = Hapcall(args)
    prog.setdir()
    prog.command()
    prog.refindex()
    prog.setadapter()

    print(time_stamp(), 'Trimming sequences...', flush=True)
    with Pool(prog.cpu) as p:
        p.map(prog.trimmomatic, range(len(prog.slist)))
    print(time_stamp(), 'Done.', flush=True)
        
    prog.extractref()

    print(time_stamp(), 'Mapping fastq to target sequences...', flush=True)
    with Pool(prog.cpu) as p:
        p.map(prog.mapping, range(len(prog.slist)))
    print(time_stamp(), 'Done.', flush=True)

    prog.mergevcf()

    print(time_stamp(), 'taseq_hapcall successfully finished.\n', flush=True)

if __name__ == '__main__':
    main()
