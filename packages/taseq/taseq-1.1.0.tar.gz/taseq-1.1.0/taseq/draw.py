#!/usr/bin/env python3
import math
import os
import sys

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from taseq.params import Params
from taseq.utils import time_for_filename, time_stamp

pm = Params('draw')
args = pm.set_options()

class Draw(object):
    def __init__(self, args):
        self.args = args
        self.input = args.input
        self.fai = args.fai
        self.col_a = args.color_A
        self.col_b = args.color_B
        self.col_h = args.color_het
        self.col_m = args.color_miss
        self.name_a = args.name_A
        self.name_b = args.name_B

        #This is the name of output directory
        self.dir = args.name
        os.mkdir(self.dir)

        #make input TSV to dataframe
        self.data = pd.read_csv(args.input, sep='\t') #dataframe
        self.data = self.data[self.data['JUDGE']]

        #Prepare chromosome information
        self.fai_data = []
        with open(self.fai, 'r') as f:
            for row in f:
                row = row.strip()
                self.fai_data.append(row.split('\t'))
        self.fai_col = ['chr', 'len', 'A', 'B', 'C']
        self.fai_data = pd.DataFrame(self.fai_data, columns=self.fai_col)
        self.fai_data['len'] = self.fai_data['len'].astype(int)
        
    def command(self):
        #Output command info
        command = ' '.join(sys.argv)
        fn = '{}/command.txt'.format(self.dir)
        with open(fn, 'w') as f:
            f.write('{}\n'.format(command))
            
    def run(self):
        print(time_stamp(),
              'Drawing positions of selected markers.',
              flush=True)

        #number of digits in the length of the longest chromosome
        digits = math.floor(math.log10(max(self.fai_data['len'])))
        standard = 10**(digits)
        #if the longest chr length is 23098790,
        #digits = 7
        #standard = 10000000

        if(max(self.fai_data['len']) / standard < 2):
            standard = standard / 5
        elif(max(self.fai_data['len']) / standard < 5):
            standard = int(standard / 2)
        #if the longest chr length is 23098790,
        #standard = 5000000

        y_axis_at = range(0, standard*11, standard)
        y_axis_lab = []
        if(standard >= 100000):
            st_lab = standard/1000000
            sign = 'M'
        elif(standard >= 100):
            st_lab = standard/1000
            sign = 'K'
        else:
            st_lab = standard
            sign = 'bp'

        for i in range(11):
            y_axis_lab.append('{}{}'.format(round(st_lab * i, 1), sign))

        longest_len = max(self.fai_data['len'])



        sample_col = range(3, len(self.data.columns) - 12)
        for h in sample_col:
            # Create a figure
            fig = plt.figure(figsize=(5, 5), dpi=144)
            ax = fig.add_subplot(111,
                                xlim=[-1, len(self.fai_data['chr'])],
                                xticks=range(len(self.fai_data['chr'])),
                                xticklabels=self.fai_data['chr'],
                                xlabel="Chromosome",
                                ylim=[longest_len*1.05, -longest_len*0.05],
                                yticks=y_axis_at,
                                yticklabels=y_axis_lab,
                                ylabel="Position")
            plt.subplots_adjust(left=0.15, right=0.95, bottom=0.15, top=0.95)
            plt.xticks(rotation=45)
            plt.xlim(-1, len(self.fai_data['chr']))
            plt.ylim(longest_len*1.05, -longest_len*0.05)

            legends = []
            legends.append(patches.Patch(color=self.col_a, label=self.name_a))
            legends.append(patches.Patch(color=self.col_b, label=self.name_b))
            legends.append(patches.Patch(color=self.col_h, label='Hetero'))
            legends.append(patches.Patch(color=self.col_m, label='Missing'))
            ax.legend(handles=legends, loc="lower right")


            for i in range(len(self.fai_data['chr'])):
                #Draw rectangle of chromosome
                r = patches.Rectangle(xy=(i-0.4, 0), width=0.8,
                    height=self.fai_data['len'][i], ec=None, fc='lightgray', fill=True)
                ax.add_patch(r)

                ##make data matrix
                data_select = self.data[self.data['CHR'] == self.fai_data['chr'][i]]
                data_select.reset_index(inplace=True, drop=True)

                #Draw rectangle
                for j in range(len(data_select)):
                    pos = data_select['POS'][j]
                    geno = data_select[data_select.columns[h]][j]

                    if(j == 0):
                        sta = 0
                    else:
                        sta = (data_select['POS'][j-1] + pos) / 2
                    if(j == len(data_select) - 1):
                        end = self.fai_data['len'][i]
                    else:
                        end = (data_select['POS'][j+1] + pos) / 2

                    if(geno == 'A'):
                        r = patches.Rectangle(xy=(i-0.4, sta), width=0.8, height=end - sta,
                                ec=None, fc=self.col_a, fill=True)
                    elif(geno == 'B'):
                        r = patches.Rectangle(xy=(i-0.4, sta), width=0.8, height=end - sta,
                                ec=None, fc=self.col_b, fill=True)
                    elif(geno == 'H'):
                        r = patches.Rectangle(xy=(i-0.4, sta), width=0.8, height=end - sta,
                                ec=None, fc=self.col_h, fill=True)
                    else:
                        r = patches.Rectangle(xy=(i-0.4, sta), width=0.8, height=end - sta,
                                ec=None, fc=self.col_m, fill=True)
                    ax.add_patch(r)
                    plt.hlines(pos, i-0.4, i+0.4, color='black', lw=1)

                #Draw rectangle of chromosome
                r = patches.Rectangle(xy=(i-0.4, 0), width=0.8,
                    height=self.fai_data['len'][i], ec='black', fill=False)
                ax.add_patch(r)

            # Save figure
            file = '{}/{}.png'.format(self.dir, self.data.columns[h])
            fig.savefig(file, dpi=144)

            # Release memory
            plt.clf()
            plt.close()

        print(time_stamp(),
              'Done.',
              flush=True)

def main():
    prog = Draw(args)
    prog.command()
    prog.run()


if __name__ == '__main__':
    main()
