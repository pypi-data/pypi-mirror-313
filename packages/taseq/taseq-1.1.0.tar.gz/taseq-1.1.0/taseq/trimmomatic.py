import glob
import sys
import subprocess as sbp
from taseq.utils import prepare_cmd, call_log, time_stamp


class Trimmomatic(object):

    def __init__(self, fqdir, samplename, outdir, crop, minlen, qual, adapter):
        self.fqdir = fqdir
        self.sn = samplename
        self.dir = outdir
        self.crop = crop
        self.minlen = minlen
        self.qual = qual
        self.ad = adapter

    def run(self):
        #Check the input files are pair end
        tmp = ['{}/{}_*R1*'.format(self.fqdir, self.sn), '{}/{}_*R2*'.format(self.fqdir, self.sn)]
        filelist_1 = glob.glob(tmp[0])
        filelist_2 = glob.glob(tmp[1])
        if len(filelist_1) != 1 or len(filelist_2) != 1:
            print(time_stamp(), 
                  '!!ERROR!! Program could not parse the name of input fastq.\n', flush=True)
            sys.exit(1)
            

        if self.ad == 'NONE':
            cmd1 = 'trimmomatic PE -threads 1 -phred33 \
                    {0}/{1}_*R1* \
                    {0}/{1}_*R2* \
                    {2}/fastq/{1}_R1_trimmed.fastq.gz \
                    {2}/fastq/{1}_R1_unpaired.fastq.gz \
                    {2}/fastq/{1}_R2_trimmed.fastq.gz \
                    {2}/fastq/{1}_R2_unpaired.fastq.gz \
                    LEADING:{5} \
                    TRAILING:{5} \
                    CROP:{3} \
                    MINLEN:{4} \
                    >> {2}/log/trimmmomatic.log \
                    2>&1'.format(self.fqdir, self.sn, self.dir, 
                                self.crop, self.minlen, self.qual)
            cmd1 = prepare_cmd(cmd1)

            try:
                sbp.run(cmd1,
                        stdout=sbp.DEVNULL,
                        stderr=sbp.DEVNULL,
                        shell=True,
                        check=True)
            except sbp.CalledProcessError:
                call_log(self.dir, 'trimmmomatic', cmd1)
                sys.exit(1)
        else:
            cmd1 = 'trimmomatic PE -threads 1 -phred33 \
                    {0}/{1}_*R1* \
                    {0}/{1}_*R2* \
                    {2}/fastq/{1}_R1_trimmed.fastq.gz \
                    {2}/fastq/{1}_R1_unpaired.fastq.gz \
                    {2}/fastq/{1}_R2_trimmed.fastq.gz \
                    {2}/fastq/{1}_R2_unpaired.fastq.gz \
                    ILLUMINACLIP:{2}/adapter/adapter.fa:2:30:10 \
                    LEADING:{5} \
                    TRAILING:{5} \
                    CROP:{3} \
                    MINLEN:{4} \
                    >> {2}/log/trimmmomatic.log \
                    2>&1'.format(self.fqdir, self.sn, self.dir, 
                                self.crop, self.minlen, self.qual)
            cmd1 = prepare_cmd(cmd1)

            try:
                sbp.run(cmd1,
                        stdout=sbp.DEVNULL,
                        stderr=sbp.DEVNULL,
                        shell=True,
                        check=True)
            except sbp.CalledProcessError:
                call_log(self.dir, 'trimmmomatic', cmd1)
                sys.exit(1)

