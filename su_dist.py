import os
from zrst import util
import numpy as np
from lookup import *
import cPickle as pickle
import sys
ph_dist_path = r'/home/c2tao/asru_2015/ph_dist/'
zrc_path = r'/home/c2tao/ZRC/'
zrc_data_path = r'/home/c2tao/ZRC_data/'
zrc_super_path = r'/home/c2tao/ZRC_supervised/'


def simple_dist(phn, lan):
    super_mlf = util.MLF(zrc_super_path+phn+'_'+lan+'_cut.mlf')
    
    dist_dict = {}
    for i, a in enumerate(super_mlf.tok_list):
        for j, b in enumerate(super_mlf.tok_list):
            dist_dict[(a, b)] = 0.0 if i==j else -99.0
    pickle.dump(dist_dict, open('su_dist/'+phn+'_'+lan+'_sim.dat','w'))
    return dist_dict

def confusion_dist(phn, dot, lan):
    super_mlf = util.MLF(zrc_super_path+phn+'_'+lan+'_cut.mlf')
    truth_mlf = util.MLF(zrc_super_path+dot+'_'+lan+'.mlf')
    
    mat, __ = truth_mlf.overlap(super_mlf)
    #mat, __ = super_mlf.overlap(truth_mlf)
    from sklearn.preprocessing import normalize
    normed_mat = normalize(mat, axis=0, norm='l2') 
    #dist = - np.log( np.dot(normed_mat.T, normed_mat)+0.0001)
    dist = 1.0 - np.dot(normed_mat.T, normed_mat) 
    
    dist_dict = {}
    print dist.shape
    assert(dist.shape[0]==len(super_mlf.tok_list))
    for i, a in enumerate(super_mlf.tok_list):
        for j, b in enumerate(super_mlf.tok_list):
            dist_dict[(a, b)] = dist[i, j]
    pickle.dump(dist_dict, open('su_dist/'+phn+'_'+lan+'_'+dot+'.dat','w'))
    return dist_dict

    
eng_short = filter(lambda x: x.split('_')[0]=='eng' and x.split('_')[2]=='0',qer_list)[:10]
xit_short = filter(lambda x: x.split('_')[0]=='xit' and x.split('_')[2]=='0',qer_list)[:10]

for q in eng_short+xit_short:
    wrd = q.split('_')[1]
    print q,len(filter(lambda x: x.split('_')[1]==wrd,qer_list))

qer_list = eng_short + xit_short
print qer_list



if __name__=='__main__':
    if sys.argv[1]=='build':
        for lan in ['eng', 'xit']:
            for phn in phn_list:
                S = simple_dist(phn, lan)
                for dot in ['phn', 'wrd']:
                    print phn, dot
                    S = confusion_dist(phn, dot, lan)
    if sys.argv[1]=='wrd' or sys.argv[1]=='phn':
        dot = sys.argv[1]
        dist = {}
        for phn in phn_list:
            if phn!=sys.argv[2]: continue
            for lan in lan_list:
                if lan!=sys.argv[3]: continue
                S = pickle.load(open('su_dist/'+phn+'_'+lan+'_'+dot+'.dat','r'))
                for q in qer_list:
                    if q[:3]!=lan: continue
                    Q = parse_qer_phoneme(q, phn)
                    for i, d in enumerate(doc_list):
                        #print q, float(i)/len(doc_list)*100, '%'
                        if q[:3]!=d[:3]: continue
                        D = parse_doc_phoneme(d, phn)
                        dist[q,d] = warp_pattern(Q, D, S)
                    print q, lan, phn
                pickle.dump(dist, open('su_dist/'+phn+'_'+lan+'_'+dot+'_dtw.dat','w'))
