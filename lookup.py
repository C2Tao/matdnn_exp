import dtw
import ph_dist 
import qd_parse
import su_parse

def generate_doc_list():
    '''
    format: lan_wav 
    example: eng_s0101a_001
    '''
    doc_list = qd_parse.generate_doc_list()
    return doc_list

def generate_qer_list():
    '''
    format: lan_word_count
    example: eng_limited_0
    '''
    qer_list = qd_parse.generate_qer_list()
    return qer_list

def generate_ftp_list():
    '''
    format: featuretype
    example: mfc
    '''
    ftp_list = qd_parse.generate_ftp_list()
    return ftp_list

def generate_tok_list():
    '''
    format: lan_iter_MRiter_mhyper_nhyper
    example: eng_iter1_MR0_50_3
    '''
    tok_list = qd_parse.generate_tok_list()
    return tok_list

def generate_lan_list():
    '''
    format: languagetype:[eng,xit]
    example: eng
    '''
    lan_list = su_parse.generate_lan_list()
    return lan_list

def generate_phn_list():
    '''
    format: phonemetype:[EN,HU,CZ,RU]
    example: EN
    '''
    phn_list = su_parse.generate_phn_list()
    return phn_list

#def parse_tok_distance(tok):
#    distanc = ph_dist.get_dm(tok)
#    return distanc

def parse_doc_feature(doc, ftp):
    doc_feature = qd_parse.parse_doc_feature(doc, ftp)
    return doc_feature

def parse_qer_feature(qer, ftp):
    qer_feature = qd_parse.parse_qer_feature(qer, ftp)
    return qer_feature

def parse_doc_pattern(doc, tok):
    doc_pattern = qd_parse.parse_doc_pattern(doc, tok)
    return doc_pattern

def parse_qer_pattern(qer, tok):
    qer_pattern = qd_parse.parse_qer_pattern(qer, tok)
    return qer_pattern

def parse_doc_phoneme(doc, phn):
    doc_phoneme = su_parse.parse_doc_phoneme(doc, phn)
    return doc_phoneme

def parse_qer_phoneme(qer, phn):
    qer_phoneme = su_parse.parse_qer_phoneme(qer, phn)
    return qer_phoneme

def warp_feature(qer_feature, doc_feature):
    distance = dtw.feature_dtw(qer_feature, doc_feature)
    return distance

def warp_pattern(qer_pattern, doc_pattern, tok_distance):
    distance = dtw.pattern_dtw(qer_pattern, doc_pattern, tok_distance)
    return distance
    

doc_list = generate_doc_list()
qer_list = generate_qer_list()
tok_list = generate_tok_list()
ftp_list = generate_ftp_list()
lan_list = generate_lan_list()
phn_list = generate_phn_list()
'''
print doc_list[0]
print qer_list[0]
print tok_list[0]
print ftp_list[0]

print parse_doc_feature(doc_list[0],'mfc').shape
print parse_qer_feature(qer_list[0],'mfc').shape
print parse_doc_pattern(doc_list[0],tok_list[0])
print parse_qer_pattern(qer_list[0],tok_list[0])
'''
'''
QF = []
for q in qer_list:
    QF.append(parse_qer_feature(q,'mfc'))

DF = []
for d in doc_list:
    DF.append(parse_doc_feature(d,'mfc'))
'''
