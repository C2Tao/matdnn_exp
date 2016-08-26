from zrst import asr
from zrst import std
from zrst import hmm
from zrst import util


import cPickle as pickle
import os
import numpy as np
import ph_dist

ph_dist_path = r'/home/c2tao/asru_2015/ph_dist/'
zrc_path = r'/home/c2tao/ZRC/'
zrc_data_path = r'/home/c2tao/ZRC_data/'

def get_doc_list():
    def find_white(lan):
        M = util.MLF(zrc_path+lan+'/iter1/MR0/50_3/result/result.mlf')
        return  M.wav_list
    white = find_white('eng') + find_white('xit')

    doc_list = []
    doc_list += map(lambda x: 'eng_'+x,find_white('eng'))
    doc_list += map(lambda x: 'xit_'+x,find_white('xit'))
    return doc_list, white

def get_all_query(w_file):
    doc_list, white = get_doc_list()
    query = {}
    for line in open(w_file,'r'):
        temp = line.strip().split()
        if len(temp)==1 and temp[0]!='.':
            word = temp[0]
            query[word] = []
        if len(temp)==3 and temp[0] in white:
            query[word].append((temp[0],int(temp[1]),int(temp[2])))
    query.pop('SIL',None)
    return query

def generate_query(lan, dot = 'wrd'):
    w_file = os.path.join(zrc_data_path,lan,'classes',lan+'.'+dot)
    query_lan = get_all_query(w_file)
    ret_list = []
    dur_list = {}
    for q in query_lan:
        if len(query_lan[q])>1:
            #print q, len(query_lan[q])  
            #print query_lan[q]
            for d in range(len(query_lan[q])):
                ret_list.append(lan+'_'+q+'_'+str(d))
                dur_list[ret_list[-1]] = query_lan[q][d]
    #qer_list += ret_list
    return ret_list, dur_list 

def get_qer_list():
    qer_list, qer_time= generate_query('eng')
    tmp_list, tmp_time= generate_query('xit')
    qer_list.extend(tmp_list)
    qer_time.update(tmp_time)
    return qer_list, qer_time



#doc_feat = {}
def parse_feature(lan, ftype):
    doc_list, white = get_doc_list()
    wav_list = []
    feat = []
    #wav2feat = {}
    for line in open(zrc_data_path+'/'+lan+'/'+lan+'.'+ftype ,'r'):
            
        if '.wav' in line and line.split('.')[0]:
            wav = lan+'_'+line.split('.')[0]
            wav_list.append(wav)
        if '#' in line:
            feat.append(map(float,line.strip().split('#')[-1].split()))
        if not line.strip():
            #wav2feat[wav] = np.array(feat,dtype='float32')
            if wav in doc_list:
                pickle.dump(np.array(feat, dtype='float32'),open('doc_feature/'+wav+'.'+ftype,'w'))
            feat = []
    #doc_list += wav_list
    #doc_feat[ftype] = wav2feat
    #return wav_list


def parse_doc_feature(doc, ftype):
    return pickle.load(open('doc_feature/'+doc+'.'+ftype,'r'))
def parse_qer_feature(qer, ftype):
    try: 
        return pickle.load(open('qer_feature/'+qer+'.'+ftype,'r'))
    except:
        info = qer.split('_')
        lan = info[0]
        wrd = info[1]
        cnt = info[2]
        wav = qer_time[qer][0]
        beg = qer_time[qer][1]
        end = qer_time[qer][2]
        feat =  parse_doc_feature(lan+'_'+wav,ftype)[beg:end+1,:]
        
        pickle.dump(np.array(feat, dtype='float32'),open('qer_feature/'+wav+'.'+ftype,'w'))
        return feat
#print parse_qer_feature(qer_list[0],'mfc')
    
#qer_feat = {}
#def parse_pattern(lan,ttype) 
def parse_pattern(tok):
    #if os.path.isfile('qer_sequence.dat'):
    #    return pickle.load('qer_sequence.dat','r')
    #if os.path.isfile('doc_sequence.dat'):
    #    return pickle.load('doc_sequence.dat','r')
    #qer_pattern = {}
    #doc_pattern = {}
    #qer_pattern[tok] = {}
    #doc_pattern[tok] = {}
    qer_list, qer_time =  get_qer_list()
    M = util.MLF(ph_dist.n2p(tok)+'/result/result.mlf')
    lan = tok[:3]
    for q in qer_list:
        if q[:3]!=lan: continue
        wav,tbeg,tend = qer_time[q]
        ind = M.wav_list.index(wav)
        if tend<=M.int_list[ind][0]:
            seq = [M.tag_list[ind][0]]
        else:
            seq = M.wav_dur(ind,tbeg,tend)
        #qer_pattern[tok][q] = seq
        pickle.dump(seq, open('qer_pattern/'+q+'.'+tok,'w'))
        '''
        try:
            if tend<=M.int_list[ind][0]:
                qer_pattern[tok][q] = [M.tag_list[ind][0]]
            else:
                qer_pattern[tok][q] = M.wav_dur(ind,tbeg,tend)
        except:
            print wav,tbeg,tend
            print M.int_list[ind]
            print M.tag_list[ind]
            xxxxxx
        '''
    for d in doc_list:
        if d[:3]!=lan: continue
        wav = d[4:]
        ind = M.wav_list.index(wav)
        #doc_pattern[tok][d] = M.tag_list[ind]
        seq = M.tag_list[ind]
        pickle.dump(seq, open('doc_pattern/'+d+'.'+tok,'w'))
    #pickle.dump(qer_pattern,open('qer_sequence.dat','w'))
    #pickle.dump(doc_pattern,open('doc_sequence.dat','w'))
    #return qer_pattern,doc_pattern

def parse_qer_pattern(qer,tok):
    return pickle.load(open('qer_pattern/'+qer+'.'+tok,'r'))
def parse_doc_pattern(doc,tok):
    return pickle.load(open('doc_pattern/'+doc+'.'+tok,'r'))
#qer_pattern, doc_pattern = parse_pattern()
#print doc_pattern[doc_list[0]]
#print qer_pattern[qer_list[0]]
#parse_pattern(tok_list[1])
#for t in tok_list[:1]:
#parse_pattern(t)

def execute(): 
    ftp_list = ['mfc','mbf']
    tok_list = ph_dist.tokset
    doc_list, __ = get_doc_list()
    qer_list, qer_time = get_qer_list()
    pickle.dump(ftp_list,open('list/ftp_list.dat','w'))
    pickle.dump(tok_list,open('list/tok_list.dat','w'))
    pickle.dump(doc_list,open('list/doc_list.dat','w'))
    pickle.dump(qer_list,open('list/qer_list.dat','w'))
    pickle.dump(qer_time,open('list/qer_time.dat','w'))


ftp_list = pickle.load(open('list/ftp_list.dat','r'))
tok_list = pickle.load(open('list/tok_list.dat','r'))
doc_list = pickle.load(open('list/doc_list.dat','r'))
qer_list = pickle.load(open('list/qer_list.dat','r'))
qer_time = pickle.load(open('list/qer_time.dat','r'))

def generate_ftp_list():
    return pickle.load(open('list/ftp_list.dat','r'))
def generate_tok_list():
    return pickle.load(open('list/tok_list.dat','r'))
def generate_doc_list():
    return pickle.load(open('list/doc_list.dat','r'))
def generate_qer_list():
    return pickle.load(open('list/qer_list.dat','r'))

if __name__=='__main__':
    if sys.argv[1] =='run':
        parse_feature('eng','mfc')
        parse_feature('eng','mbf')
        parse_feature('xit','mfc')
        parse_feature('xit','mbf')
        for q in qer_list:
            parse_qer_feature(q,'mfc')
            parse_qer_feature(q,'mbf')
        for t in tok_list:
            parse_pattern(t)
    if sys.argv[2] == 'execute':
        execute()
