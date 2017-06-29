lines = open('norm_weight.txt','r').readlines()


for line in lines:
    if 'xit' in line or 'eng' in line:
        ma = line.split()[-1]
        ky = line.split()[1]
        ln = line.split()[0]
        print '{0:05.2f}'.format(float(ma)*100), ln,ky
    else: print line
