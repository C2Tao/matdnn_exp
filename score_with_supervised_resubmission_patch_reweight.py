from lookup import *

import sys
import cPickle as pickle
import numpy as np 
eng_short = filter(lambda x: x.split('_')[0]=='eng' and x.split('_')[2]=='0',qer_list)[:10]
xit_short = filter(lambda x: x.split('_')[0]=='xit' and x.split('_')[2]=='0',qer_list)[:10]

xqer_list = eng_short + xit_short


it_mr_list=['iter1_MR0','iter1_MR1','iter1_MR2','iter2_MR0','iter2_MR1']


    

def boost_fun(x):
    x = np.array(x)
    x  = (x - np.mean(x))/np.std(x)
    x = x.clip(min=0)
    x  = (x - np.mean(x))/np.std(x)
    return x

def boost_mean(x_array):
    score = []
    for x in x_array:
        score.append(boost_fun(x))
    return np.sum(np.array(score), axis=0)

def norm_fun(x):
    x  = (x - np.mean(x))/np.std(x)
    return x

def norm_weight(x_array, w_array=None):
    if w_array is None:
        w_array = [1.0 for x in x_array]
    score = []
    for i, x in enumerate(x_array):
        score.append(norm_fun(x)*w_array[i])
    return np.sum(np.array(score), axis=0)


def filter_with(x_array):
    score = []
    for i,x in enumerate(x_array):
        if i==0:
            x = np.array(x)
            x  = (x - np.mean(x))/np.std(x)
            filt = 1*(x>1)
        else:
            score.append(boost_fun(x)*filt)
    return boost_mean(score)

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

def get_map_w(method, opt, q_list, w):
    return np.mean([ap(get_answ_list(q), method(q, opt, w)) 
            for q in q_list])
        
def avg_mn(q, ln_it_mr, w=None):# (1)~(5)
    if q[:3]=='xit':
        m_list = ['50','100','300','500']
    elif q[:3]=='eng':
        m_list = ['50','100','300']
    score = []
    for m in m_list:
        for n in ['3','5','7']:
            tok = ln_it_mr+'_'+m+'_'+n
            score.append(get_dist_list(q, tok))
    #return np.mean(np.array(score),axis = 0)
    return norm_weight(score,w)

def boost_super(q, phn_ln,w=None):# (10)~(13)
    score = []
    score.append(get_dist_list(q, 'mfc'))
    score.append(get_dist_list(q, phn_ln))
    return boost_mean(score)
    #return norm_weight(score,w)

def avg_it_mr_mn(q,ln,w=None):# (8)
    score = []
    for it_mr in it_mr_list:
        score.append(avg_mn(q, ln+'_'+it_mr))
    return norm_weight(score,w)

def avg_all(q,ln,w=None):# (9)
    score = []
    for it_mr in it_mr_list:
        score.append(avg_mn(q, ln+'_'+it_mr))
    score.append(get_dist_list(q,'mfc'))
    score.append(get_dist_list(q,'mbf'))
    return norm_weight(score,w)

def avg_super(q, ln, w=None):# (14)
    score = []
    for phn in phn_list:
        score.append(boost_super(q, phn+'_'+ln))
    return norm_weight(score,w)


def avg_all_super_EN(q,ln,w=None):# (16)
    score = []
    score.append(boost_super(q, 'EN_'+ln))
    for it_mr in it_mr_list:
        score.append(avg_mn(q, ln+'_'+it_mr))
    score.append(get_dist_list(q,'mfc'))
    score.append(get_dist_list(q,'mbf'))
    return norm_weight(score,w)

def avg_all_super(q,ln,w=None):# (15)
    score = []
    for phn in phn_list:
        score.append(boost_super(q, phn+'_'+ln))
    for it_mr in it_mr_list:
        score.append(avg_mn(q, ln+'_'+it_mr))
    score.append(get_dist_list(q,'mfc'))
    score.append(get_dist_list(q,'mbf'))
    return norm_weight(score,w)


def plot_table_IV():
    eng_short = filter(lambda x: x.split('_')[0]=='eng' and x.split('_')[2]=='0',qer_list)[:10]
    xit_short = filter(lambda x: x.split('_')[0]=='xit' and x.split('_')[2]=='0',qer_list)[:10]
    eng_tok = filter(lambda x: x[:3]=='eng',tok_list)
    xit_tok = filter(lambda x: x[:3]=='xit',tok_list)
    #eng too low...
    eng_short = eng_short[:5]

    for it_mr in it_mr_list:
        print 'eng',it_mr, get_map(avg_mn, 'eng_'+it_mr, eng_short) 
    for ftp in ftp_list:
        print 'eng',ftp, get_map(get_dist_list, ftp, eng_short) 
    print 'eng', 'avg_itmr', get_map(avg_it_mr_mn, 'eng', eng_short) 
    print 'eng', 'avg_all', get_map(avg_all, 'eng', eng_short) 
    for phn in phn_list:
        print 'eng',phn,'boost', get_map(boost_super, phn+'_eng', eng_short) 
    print 'eng', 'avg_super', get_map(avg_super, 'eng', eng_short) 
    print 'eng', 'avg_all_super', get_map(avg_all_super, 'eng', eng_short) 
    print 'eng', 'avg_all_super_eng', get_map(avg_all_super_EN, 'eng', eng_short)


    for it_mr in it_mr_list:
        print 'xit',it_mr, get_map(avg_mn, 'xit_'+it_mr, xit_short) 
    for ftp in ftp_list:
        print 'xit',ftp, get_map(get_dist_list, ftp, xit_short) 
    print 'xit', 'avg_itmr', get_map(avg_it_mr_mn, 'xit', xit_short) 
    print 'xit', 'avg_all', get_map(avg_all, 'xit', xit_short) 
    for phn in phn_list:
        print 'xit',phn,'boost', get_map(boost_super, phn+'_xit', xit_short) 
    print 'xit', 'avg_super', get_map(avg_super, 'xit', xit_short) 
    print 'xit', 'avg_all_super', get_map(avg_all_super, 'xit', xit_short)
    print 'xit', 'avg_all_super_eng', get_map(avg_all_super_EN, 'xit', xit_short)

     
def random_search(function,N,lan='eng'):
    lan_short = filter(lambda x: x.split('_')[0]==lan and x.split('_')[2]=='0',qer_list)[:10]
    lan_short = lan_short[5:]
    max_score = -999
    best_w = None
    for i in range(100):
        w = np.random.uniform(size=(N))
        s = get_map_w(function, lan, lan_short, w)
        #print i,s
        if s>max_score:
            #print 'score:',s, 'updating w:',w
            best_w = w
            max_score = s
    print   '['+','.join(map(str,best_w))+']'+ '# score:'+str(max_score)
    return best_w
def new_table_IV():
    w_lan,w_tok ={},{}
    w_lan['eng'] =  [ 0.39810934,  0.08118065,  0.01308023,  0.08991072]# score: 0.00918763131298
    w_lan['xit'] =  [ 0.8282399,   0.38735204,  0.02218204,  0.00639997]# score: 0.302381532589

    #w_lan_eng = random_search(avg_super,4,'eng')
    #w_lan_xit = random_search(avg_super,4,'xit')
     
    #w_tok_eng = random_search(avg_all,7,'eng')
    #w_tok_xit = random_search(avg_all,7,'xit')

    w_tok['eng'] = [0.63541005292,0.401443722934,0.967366854108,0.690211192093,0.107730722544,0.642887710698,0.726365338497]# score:0.0471835714342
    w_tok['xit'] = [0.0852545200831,0.337910003643,0.99337351665,0.318232107219,0.0427057438104,0.906350180473,0.723937257387]# score:0.35598932273
     
    eng_short = filter(lambda x: x.split('_')[0]=='eng' and x.split('_')[2]=='0',qer_list)[:10]
    xit_short = filter(lambda x: x.split('_')[0]=='xit' and x.split('_')[2]=='0',qer_list)[:10]
    eng_tok = filter(lambda x: x[:3]=='eng',tok_list)
    xit_tok = filter(lambda x: x[:3]=='xit',tok_list)
    #eng too low...
    eng_short = eng_short[:5]
    
    for it_mr in it_mr_list:
        print 'eng',it_mr, get_map(avg_mn, 'eng_'+it_mr, eng_short) 
    for ftp in ftp_list:
        print 'eng',ftp, get_map(get_dist_list, ftp, eng_short) 
    print 'eng', 'avg_itmr', get_map_w(avg_it_mr_mn, 'eng', eng_short,w_tok['eng'][:5]) 
    print 'eng', 'avg_all', get_map_w(avg_all, 'eng', eng_short,w_tok['eng']) 
    for phn in phn_list:
        print 'eng',phn,'boost', get_map(boost_super, phn+'_eng', eng_short) 
    print 'eng', 'avg_super', get_map_w(avg_super, 'eng', eng_short, w_lan['eng']) 
    print 'eng', 'avg_all_super', get_map_w(avg_all_super, 'eng', eng_short, w_lan['eng']+w_tok['eng'])
    print 'eng', 'avg_all_super_eng', get_map_w(avg_all_super_EN, 'eng', eng_short, w_lan['eng'][:1]+w_tok['eng'])

    for it_mr in it_mr_list:
        print 'xit',it_mr, get_map(avg_mn, 'xit_'+it_mr, xit_short) 
    for ftp in ftp_list:
        print 'xit',ftp, get_map(get_dist_list, ftp, xit_short) 
    print 'xit', 'avg_itmr', get_map_w(avg_it_mr_mn, 'xit', xit_short,w_tok['eng'][:5]) 
    print 'xit', 'avg_all', get_map_w(avg_all, 'xit', xit_short,w_tok['eng']) 
    for phn in phn_list:
        print 'xit',phn,'boost', get_map(boost_super, phn+'_xit', xit_short) 
    print 'xit', 'avg_super', get_map_w(avg_super, 'xit', xit_short, w_lan['eng']) 
    print 'xit', 'avg_all_super', get_map_w(avg_all_super, 'xit', xit_short, w_lan['eng']+w_tok['eng'])
    print 'xit', 'avg_all_super_eng', get_map_w(avg_all_super_EN, 'xit', xit_short, w_lan['eng'][:1]+w_tok['eng'])
if __name__=='__main__':
    plot_table_IV()
