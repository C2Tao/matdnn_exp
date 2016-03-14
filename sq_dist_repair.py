from lookup import *
import os
import sys
import cPickle as pickle
    
eng_short = filter(lambda x: x.split('_')[0]=='eng' and x.split('_')[2]=='0',qer_list)[:10]
xit_short = filter(lambda x: x.split('_')[0]=='xit' and x.split('_')[2]=='0',qer_list)[:10]


for q in eng_short+xit_short:
    wrd = q.split('_')[1]
    print q,len(filter(lambda x: x.split('_')[1]==wrd,qer_list))

if __name__=='__main__':
    qer_list = eng_short + xit_short
    #print qer_list

    for tok in tok_list:
        if os.path.isfile('sq_dist/'+tok+'.dat'): continue
        if hash(tok)%5 != int(sys.argv[1]): continue
        #if sys.argv[1] not in tok: continue
        S = ph_dist.get_dm(tok)
        dist = {}
        for q in qer_list:
            if q[:3]!=tok[:3]: continue
            print 'process', hash(tok)%5,tok, q
            Q = parse_qer_pattern(q,tok)
            for d in doc_list:
                if q[:3]!=d[:3]: continue
                D = parse_doc_pattern(d,tok)
                dist[q,d] = warp_pattern(Q,D,S)
                #print q,d, dist[q,d] 
        pickle.dump(dist, open('sq_dist/'+tok+'.dat','w'))
