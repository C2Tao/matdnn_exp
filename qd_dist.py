from lookup import *

    
eng_short = filter(lambda x: x.split('_')[0]=='eng' and x.split('_')[2]=='0',qer_list)[:10]

xit_short = filter(lambda x: x.split('_')[0]=='xit' and x.split('_')[2]=='0',qer_list)[:10]

if __name__=='__main__':
    qer_list = eng_short + xit_short
    print qer_list
    import sys
    import cPickle as pickle
    ftp = sys.argv[1]
    dist = {}
    for q in qer_list:
        print ftp, q
        Q = parse_qer_feature(q,ftp)
        for d in doc_list:
            if q[:3]!=d[:3]: continue
            #print q,d
            D = parse_doc_feature(d,ftp)
            dist[q,d] = warp_feature(Q,D)
            #print  dist[q,d] 
    pickle.dump(dist, open('qd_dist/'+ftp+'.dat','w'))
