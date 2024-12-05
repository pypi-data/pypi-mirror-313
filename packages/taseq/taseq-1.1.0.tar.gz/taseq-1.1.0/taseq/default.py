#!/usr/bin/env python3
from taseq.params import Params

pm = Params('default')
args = pm.set_options()

class Default(object):
    def __init__(self, args):
        self.args = args

def main():
    Default(args)

if __name__ == '__main__':
    main()
