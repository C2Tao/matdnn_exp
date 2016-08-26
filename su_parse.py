import os
from zrst import util
from qd_parse import qer_list, qer_time, pickle, doc_list
import qd_parse
import sys
ph_dist_path = r'/home/c2tao/asru_2015/ph_dist/'
zrc_path = r'/home/c2tao/ZRC/'
zrc_data_path = r'/home/c2tao/ZRC_data/'
zrc_super_path = r'/home/c2tao/ZRC_supervised/'
import numpy as np

def alt_rep(arr): 
    #compress string of intergers, and return uniq positions
    idx = np.where(arr[1:]!=arr[:-1])[0]+1
    print idx
    idx = np.insert(idx, 0, 0)
    arr[idx]
    return arr[idx], np.insert(idx, len(idx), len(arr))
#print alt_rep(np.array([1,1,1,2,2,2,3,3,3]))
#print alt_rep(np.array([1,2]))
#print alt_rep(np.array([1]))

def check_dur(lan):
    wav_dur = {}
    M = util.MLF(zrc_path+lan+'/iter1/MR0/50_3/result/result.mlf')
    P = util.MLF(zrc_super_path+'EN_'+lan+'.mlf')
    for i, w in enumerate(M.wav_list):
        print w
        j = P.wav_list.index(w)
        wav_dur[lan+'_'+w] = M.int_list[i][-1], P.int_list[j][-1]
        # I thought they were different lengths ...
        # yeah they are different
        assert(abs(P.int_list[j][-1] - M.int_list[i][-1])<=1)
    return wav_dur
#check_dur('eng')
#check_dur('xit')

def build_phn_mlf(lan, phn):
    wav_dur = {}
    M = util.MLF(zrc_path+lan+'/iter1/MR0/50_3/result/result.mlf')
    P = util.MLF(zrc_super_path+phn+'_'+lan+'.mlf')
    selection = [] 
    for i, w in enumerate(M.wav_list):
        j = P.wav_list.index(w)
        selection += (j, P.wav_list[j]),
        dilate = float(P.int_list[j][-1])/float(M.int_list[i][-1])
        P.int_list[j] = map(lambda x: int(x/dilate), P.int_list[j])
        P.int_list[j][-1] = M.int_list[i][-1]
    #print selection
    P.write(zrc_super_path+phn+'_'+lan+'_cut.mlf', selection=selection) 
 
#def qer_type(qer_list):
    
def build_zrc_mlf(lan, dot):
    #try to make mlf for query 
    M = util.MLF(zrc_path+lan+'/iter1/MR0/50_3/result/result.mlf')
    qer_list, qer_time = qd_parse.generate_query(lan, dot)
    #print qer_list[:2]
    #print qer_time.items()[:2]
    qer_type = map(lambda x: '_'.join(x.split('_')[:2]), qer_list)
    qer_type = list(set(qer_type))
    wav_len = map(lambda x: x[-1], M.int_list)
    dur = map(lambda x: np.zeros(x), wav_len)
    #print len(dur), len(M.wav_list)
    for i, (q, t) in enumerate(zip(qer_time.keys(), qer_time.values())):
        lan, qer, cnt = q.split('_')
        wav, beg, end = t
        lan_qer = '_'.join([lan, qer])
        dur[M.wav_list.index(wav)][beg:end] = qer_type.index(lan_qer)+1

    for i, d in enumerate(dur):
        print i, d
        label, interval = alt_rep(dur[i])
        M.int_list[i] = list(interval[1:])
        M.tag_list[i] = map(lambda x: qer_type[int(x)-1] if int(x)>=0 else lan+'_sil', list(label))
        M.log_list[i] = [0.0 for __ in range(len(M.tag_list[i]))]
    M.write(zrc_super_path+dot+'_'+lan+'.mlf')

def parse_phoneme(lan, phn):
    M = util.MLF(zrc_super_path+ '_'.join([phn, lan])+'_cut.mlf')
    for q in qer_list:
        if q[:3]!=lan: continue
        wav,tbeg,tend = qer_time[q]
        ind = M.wav_list.index(wav)
        if tend<=M.int_list[ind][0]:
            seq = [M.tag_list[ind][0]]
        else:
            seq = M.wav_dur(ind,tbeg,tend)
        pickle.dump(seq, open('qer_phoneme/'+q+'.'+phn,'w'))
    for d in doc_list:
        if d[:3]!=lan: continue
        wav = d[4:]
        ind = M.wav_list.index(wav)
        seq = M.tag_list[ind]
        pickle.dump(seq, open('doc_phoneme/'+d+'.'+phn,'w'))

def parse_qer_phoneme(qer,phn):
    return pickle.load(open('qer_phoneme/'+qer+'.'+phn,'r'))

def parse_doc_phoneme(doc,phn):
    return pickle.load(open('doc_phoneme/'+doc+'.'+phn,'r'))

def generate_lan_list():
    return pickle.load(open('list/lan_list.dat','r'))

def generate_phn_list():
    return pickle.load(open('list/phn_list.dat','r'))


if __name__=='__main__':
    lan_list = ['eng', 'xit']
    phn_list = ['EN', 'HU', 'CZ', 'RU']
    if sys.argv[1]=='run':
        pickle.dump(lan_list,open('list/lan_list.dat','w'))
        pickle.dump(phn_list,open('list/phn_list.dat','w'))
        for lan in lan_list:
            for phn in phn_list:
                parse_phoneme(lan, phn)
    elif sys.argv[1]=='mlf':
        for lan in lan_list:
            for phn in phn_list:
                build_phn_mlf(lan, phn)
    elif sys.argv[1]=='zrc':
        for lan in lan_list:
            for dot in ['wrd', 'phn']:
                build_zrc_mlf(lan, dot)
    print parse_qer_phoneme('eng_limited_0', 'RU') 
    print parse_doc_phoneme('eng_s0101a_001', 'RU') 
    #query_list, query_time =  qd_parse.generate_query('eng', 'phn') 
    

