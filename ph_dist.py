from zrst import asr
from zrst import std
from zrst import hmm
import os
import numpy as np
ph_dist_path = r'/home/c2tao/asru_2015/ph_dist'
zrc_path = r'/home/c2tao/ZRC/'
zrc_data_path = r'/home/c2tao/ZRC_data/'

#####
gg = '/home/c2tao/ZRC/eng/iter1/MR0/50_3'
def p2n(x):
    #tok path to tok name
    return '_'.join(x.split('/')[4:])
#print p2n(gg)

ff = 'eng_iter1_MR0_50_3'
def n2p(x):
    #tok name to tok path
    return zrc_path+'/'.join(x.split('_')[:-2])\
        +'/'+'_'.join(x.split('_')[-2:])
#print n2p(ff)
assert(p2n(n2p(ff)) == ff)
assert(n2p(p2n(gg)) == gg)
#####

def generate_tokset_list():
    tokset_list = []

    l_set = ['iter1_MR0','iter1_MR1','iter1_MR2','iter2_MR0','iter2_MR1']       
    eng_set = map(lambda x: 'eng'+'_'+x,l_set)
    xit_set = map(lambda x: 'xit'+'_'+x,l_set)

    for i in ['50','100','300','500']: 
        for j in ['3','5','7']:
            for x in eng_set:
                tokset_list.append(x+'_'+i+'_'+j)
        for j in ['3','5','7','9']:
            for x in xit_set:
                tokset_list.append(x+'_'+i+'_'+j) 
    return tokset_list

import cPickle as pickle
def get_dm(tokset_name):
    try:
        dm = pickle.load(open(os.path.join(ph_dist_path, tokset_name+'.dat'),'r'))
        print 'loaded precomputed distance for ' + tokset_name
        return dm
    except:
        print 'computing distance for ' + tokset_name
    dm = {}
    H = hmm.parse_hmm(n2p(tokset_name)+'/hmm/models')
    phones = filter(lambda x: 's' not in x,H.keys())
    for i in phones:
        for j in phones:
            dm[(i,j)] =  hmm.kld_hmm(H[i],H[j])

    ok = set([])
    for k in dm.keys():
        ok.add(k[0])
        ok.add(k[1])
    ok = list(ok)

    for k in ok:
        ambig = np.mean([dm[x] for x in dm.keys() \
                         if (x[0] == k or x[1] == k) and dm[x] != float('Inf')])
        dm[('sil', k)] = ambig
        dm[('sp', k)] = ambig
    ambig = np.mean([dm[x] for x in dm.keys() \
                     if dm[x] != float('Inf')])
    dm[('sil', 'sp')] = ambig
    dm[('sil', 'sil')] = ambig
    dm[('sp', 'sp')] = ambig

    for k in dm.keys():
        dm[(k[1], k[0])] = dm[k]
    pickle.dump(dm,open(os.path.join(ph_dist_path,tokset_name+'.dat'),'w'))
    return dm

tokset = generate_tokset_list()
#print tokset[0]

if '__name__'=='__main__':
    import sys
    for t in tokset:
        if sys.argv[1] not in t: continue
        X = get_dm(t)
        print 'progress', 100.0*tokset.index(t)/len(tokset),'%'



'''
Q = std.STD(root = query_path, label = labels_path, corpus = corpus_path)
Q.add_pattern(A,'40_5034_50_3')
Q.add_pattern(B,'36_5034_50_3')
Q.query_init()
Q.query_build()
'''
