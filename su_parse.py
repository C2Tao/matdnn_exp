import os
from zrst import util
import ph_dist
ph_dist_path = r'/home/c2tao/asru_2015/ph_dist/'
zrc_path = r'/home/c2tao/ZRC/'
zrc_data_path = r'/home/c2tao/ZRC_data/'
zrc_super_path = '/home/c2tao/ZRC_supervised/'
from qd_parse import qer_list, qer_time, pickle, doc_list
#def parse_phoneme(lan):

phn_list = ['EN', 'HU', 'CZ', 'RU']
'''
def find_white(lan):
    M = util.MLF(zrc_path+lan+'/iter1/MR0/50_3/result/result.mlf')
    return  M.wav_list
white = find_white('eng') + find_white('xit')

doc_list = []
doc_list += map(lambda x: 'eng_'+x,find_white('eng'))
doc_list += map(lambda x: 'xit_'+x,find_white('xit'))

def find_dur(lan):
    wav_dur = {}
    M = util.MLF(zrc_path+lan+'/iter1/MR0/50_3/result/result.mlf')
    P = util.MLF(zrc_super_path+'EN_'+lan+'.mlf')
    for i, w in enumerate(M.wav_list):
        j = P.wav_list.index(w)
        wav_dur[lan+'_'+w] = M.int_list[i][-1], P.int_list[j][-1]
        # I thought they were different lengths ...
        assert(P.int_list[j][-1] - M.int_list[i][-1]<=1)
    return wav_dur
wav_dur = {}
wav_dur.update(find_dur('eng'))
wav_dur.update(find_dur('xit'))
def get_all_query(w_file):
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

qer_list = []
qer_time = {}
def generate_query(lan):
    w_file = os.path.join(zrc_data_path,lan,'classes',lan+'.wrd')
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
    qer_time.update(dur_list)
    return ret_list
qer_list += generate_query('eng')
qer_list += generate_query('xit')
'''

def parse_phoneme(phn, lan):
    M = util.MLF(zrc_super_path+ '_'.join([phn, lan])+'.mlf')
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
if __name__=='__main__':
    lan = 'eng'
    phn = 'EN'
    parse_phoneme(phn, lan)
