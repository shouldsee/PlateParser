#!/usr/bin/env python2
# -*- coding: utf-8 -*-
def file2dfs(fname):
    with open(fname,'r') as f:
        mcount = -1
        buf = ''
        lst = []
        header = [None]*2
        OUTPUT = []
        while True:
            line = next(f,'Read')
    #     for line in f:
    #         buf += []        
            if line.startswith('Read'):
                newheader = [line, next(f,None)]
                if newheader[0] != header[0] or newheader[1] is None:
                    print 'newheader is：',newheader
                    if lst:
                        name = header[0].strip()
                        df = pd.concat(lst,axis=0)
                        OUTPUT += [(name,df)]
                    lst = []
                    if newheader[1] is None:
                        break
                header = newheader
                mcount += 1
                if mcount >= 1:                
    #                 break
                    time = timePTN.findall(''.join(header) )[0]
                    dfc = buffer2data(buf)
                    if mcount == 1:
                        col = paste0(dfc.iloc[:,:2].values.T)
                    dfc = dfc[['value']].T;
                    dfc.columns = col
                    dfc = dfc.set_index([[time]])
                    lst += [dfc]
                    buf = ''
    #                 if mcount == 5:
    #                     dfc = pd.concat(lst,axis=0)
    #                     break
            else:
                if not buf:
                    buf = line
                else:
                    buf = '%s\n%s' %(buf, line)
    return OUTPUT

def buffer2data(buf):
    df = pd.read_table(StringIO.StringIO(buf))
    dfc = df.iloc[:,:12]
    dfc.columns = np.arange(0,12)
    # .reset_index()
    # dfc

    dfc= pd.melt(dfc.reset_index(), 
                id_vars='index', 
                value_vars=list(dfc.columns), # list of days of the week
                value_name='value',
           )
    return dfc

def paste0(ss,sep=None,na_rep=None):
    '''Analogy to R paste0
    '''
    if sep is None:
        sep=''
    res = [sep.join(str(s) for s in x) for x in zip(*ss)]
    res = pd.Series(res)
    return res

import argparse
import pandas as pd
import numpy as np
import StringIO
import re
timePTN = re.compile('\((.*)\)')

parser = argparse.ArgumentParser()
parser.add_argument('filename',nargs='+',help='raw txt file containing 96 well data')

if __name__=='__main__':
    args =  parser.parse_args()
    OUTPUT = file2dfs(args.filename[0])
    for k,df in OUTPUT:
        k = k.replace(' ','_').replace('/','-')
        outname = '%s.csv'%k
        print '[OUTPUT] to %s' % outname
        df.to_csv(outname,index_label = 'time')
    