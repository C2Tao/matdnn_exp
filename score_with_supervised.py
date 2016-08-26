from lookup import *

import sys
import cPickle as pickle
import numpy as np 
eng_short = filter(lambda x: x.split('_')[0]=='eng' and x.split('_')[2]=='0',qer_list)[:10]
xit_short = filter(lambda x: x.split('_')[0]=='xit' and x.split('_')[2]=='0',qer_list)[:10]

xqer_list = eng_short + xit_short


it_mr_list=['iter1_MR0','iter1_MR1','iter1_MR2','iter2_MR0','iter2_MR1']



for q in eng_short+xit_short:
    wrd = q.split('_')[1]
    print q,len(filter(lambda x: x.split('_')[1]==wrd,qer_list))

def get_feature_dist(ftp):
    return pickle.load(open('qd_dist/'+ftp+'.dat','r'))

def get_pattern_dist(tok):
    return pickle.load(open('sq_dist/'+tok+'.dat','r'))

def get_phoneme_dist(phn, lan):
    return pickle.load(open('su_dist/'+phn+'_'+lan+'_phn_dtw.dat','r'))
    

eng_list = filter(lambda x: x[:3]=='eng',doc_list) 
xit_list = filter(lambda x: x[:3]=='xit',doc_list)
#doc2idx = {}
#for i in range(len(eng_list)):
#    doc2idx[eng_list[i]] = i
#for i in range(len(xit_list)):
#    doc2idx[xit_list[i]] = i

def get_answ():
    answ = {}
    def qer2wrd(qer):
        return '_'.join(qer.split('_')[:2])
    def doc2wav(doc):
        return doc[4:]
    #same[wrd]=doc_list
    same = {}
    wrd_list = list(set(map(qer2wrd,qer_list)))
    for wrd in wrd_list:
        same[wrd] = []
    for qer in qer_list:
        same[qer2wrd(qer)].append(qer[:3]+'_'+qd_parse.qer_time[qer][0])
    for qer in xqer_list:
        answ[qer] = same[qer2wrd(qer)]
    return answ
answ = get_answ()
def get_lan_list(qer):
    if qer[:3]=='eng':
        lan_list = eng_list
    if qer[:3]=='xit':
        lan_list = xit_list
    return lan_list

def get_answ_list(qer):
    lan_list = get_lan_list(qer)
    answ_list = [1 if doc in answ[qer] else 0 for doc in lan_list]
    return answ_list

def get_dist():
    dist = {}
    for ftp in ftp_list:
        dist[ftp] = get_feature_dist(ftp)
    for tok in tok_list:
        dist[tok] = get_pattern_dist(tok)
    for phn in phn_list:
        dist[phn+'_eng'] = get_phoneme_dist(phn, 'eng')
        dist[phn+'_xit'] = get_phoneme_dist(phn, 'xit')
    return dist

dist = get_dist()
def get_dist_list(qer,ftpok):
    lan_list = get_lan_list(qer)
    dist_list = [- dist[ftpok][qer,doc] for doc in lan_list]
    return dist_list
from zrst.util import average_precision_minus1 as ap
#ap = util.average_precision_minus1

def get_map(method, opt, q_list):
    return np.mean([ap(get_answ_list(q), method(q, opt)) 
            for q in q_list])
        
def avg_mn(q, ln_it_mr):
    if q[:3]=='xit':
        m_list = ['50','100','300','500']
    elif q[:3]=='eng':
        m_list = ['50','100','300']
    score = []
    for m in m_list:
        for n in ['3','5','7']:
            tok = ln_it_mr+'_'+m+'_'+n
            score.append(get_dist_list(q, tok))
    return np.sum(np.array(score),axis = 0)
def avg_it_mr_mn(q,ln):
    score = []
    for it_mr in it_mr_list:
        lnitmr = ln+'_'+it_mr
        score.append(avg_mn(q, lnitmr))
    return np.mean(np.array(score),axis = 0)

def avg_all(q,ln):
    score = []
    score.append(avg_it_mr_mn(q, ln))
    score.append(get_dist_list(q,'mfc'))
    score.append(get_dist_list(q,'mbf'))
    return np.mean(np.array(score),axis = 0)

def avg_super(q, ln):
    score = []
    for phn in phn_list:
        score.append(get_dist_list(q, phn+'_'+ln))
    return np.mean(np.array(score),axis = 0)

def avg_all_super(q,ln):
    score = []
    score.append(avg_it_mr_mn(q, ln))
    score.append(avg_super(q, ln)*4)
    score.append(get_dist_list(q,'mfc'))
    score.append(get_dist_list(q,'mbf'))
    return np.mean(np.array(score),axis = 0)
if __name__=='__main__':
    '''
    for q in xqer_list:
        oo = get_answ_list(q)
        for ftp in ftp_list:
            xx = get_dist_list(q,ftp)
            print q, ftp, ap(oo, xx)
     
        for tok in tok_list:
            if tok[:3]!=q[:3]:continue
            xx = get_dist_list(q,tok)
            print q, tok, ap(oo, xx)
    '''
    eng_tok = filter(lambda x: x[:3]=='eng',tok_list)
    xit_tok = filter(lambda x: x[:3]=='xit',tok_list)
    #eng too low...
    eng_short = eng_short[:5]
    for tok in eng_tok:
        print 'eng',tok, get_map(get_dist_list, tok, eng_short)
    for tok in xit_tok:
        print 'xit',tok, get_map(get_dist_list, tok, xit_short)

    for ftp in ftp_list:
        print 'eng',ftp, get_map(get_dist_list, ftp, eng_short) 
    for ftp in ftp_list:
        print 'xit',ftp, get_map(get_dist_list, ftp, xit_short) 
    
    for phn in phn_list:
        print 'eng',phn, get_map(get_dist_list, phn+'_eng', eng_short) 
    for phn in phn_list:
        print 'xit',phn, get_map(get_dist_list, phn+'_xit', xit_short) 

    for it_mr in it_mr_list:
        print 'eng',it_mr, get_map(avg_mn, 'eng_'+it_mr, eng_short) 
    for it_mr in it_mr_list:
        print 'xit',it_mr, get_map(avg_mn, 'xit_'+it_mr, xit_short) 

    print 'eng', 'avg_itmr', get_map(avg_it_mr_mn, 'eng', eng_short) 
    print 'xit', 'avg_itmr', get_map(avg_it_mr_mn, 'xit', xit_short) 

    print 'eng', 'avg_super', get_map(avg_super, 'eng', eng_short) 
    print 'xit', 'avg_super', get_map(avg_super, 'xit', xit_short) 
    
    print 'eng', 'avg_all', get_map(avg_all, 'eng', eng_short) 
    print 'xit', 'avg_all', get_map(avg_all, 'xit', xit_short) 
    
    print 'eng', 'avg_all_super', get_map(avg_all_super, 'eng', eng_short) 
    print 'xit', 'avg_all_super', get_map(avg_all_super, 'xit', xit_short) 
    '''
    for tok in tok_list:
        if sys.argv[1] not in tok: continue
        S = ph_dist.get_dm(tok)
        dist = {}
        for q in qer_list:
            if q[:3]!=tok[:3]: continue
            print tok, q
            Q = parse_qer_pattern(q,tok)
            for d in doc_list:
                if q[:3]!=d[:3]: continue
                D = parse_doc_pattern(d,tok)
                dist[q,d] = warp_pattern(Q,D,S)
                #print q,d, dist[q,d] 
        pickle.dump(dist, open('sq_dist/'+tok+'.dat','w'))
    '''
