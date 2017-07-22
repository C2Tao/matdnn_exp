import sys
import cPickle as pickle
import numpy as np 
from scipy.interpolate import RectBivariateSpline
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib
info_text ='''\
eng iter1_MR0_50_3 0.170633116433
eng iter1_MR1_50_3 0.152116919102
eng iter1_MR2_50_3 0.12000586423
eng iter2_MR0_50_3 0.164116619998
eng iter2_MR1_50_3 0.10503527382
eng iter1_MR0_50_5 0.054312992579
eng iter1_MR1_50_5 0.0829084718971
eng iter1_MR2_50_5 0.133466575616
eng iter2_MR0_50_5 0.0900616122627
eng iter2_MR1_50_5 0.136131220296
eng iter1_MR0_50_7 0.0495592962732
eng iter1_MR1_50_7 0.0938252007345
eng iter1_MR2_50_7 0.0490411688964
eng iter2_MR0_50_7 0.0750231649676
eng iter2_MR1_50_7 0.0609959903765
eng iter1_MR0_100_3 0.0254822706186
eng iter1_MR1_100_3 0.0861607472805
eng iter1_MR2_100_3 0.0622789484868
eng iter2_MR0_100_3 0.0794854491743
eng iter2_MR1_100_3 0.114957801917
eng iter1_MR0_100_5 0.0962664933066
eng iter1_MR1_100_5 0.0776571780541
eng iter1_MR2_100_5 0.0867933052339
eng iter2_MR0_100_5 0.0675394101412
eng iter2_MR1_100_5 0.109441433306
eng iter1_MR0_100_7 0.043678108704
eng iter1_MR1_100_7 0.0249799616706
eng iter1_MR2_100_7 0.0514606720371
eng iter2_MR0_100_7 0.0686727794997
eng iter2_MR1_100_7 0.0739535145325
eng iter1_MR0_300_3 0.0933020744468
eng iter1_MR1_300_3 0.143279846536
eng iter1_MR2_300_3 0.121198042284
eng iter2_MR0_300_3 0.0760960195255
eng iter2_MR1_300_3 0.149551235527
eng iter1_MR0_300_5 0.0681518713905
eng iter1_MR1_300_5 0.0566089299779
eng iter1_MR2_300_5 0.0839699134904
eng iter2_MR0_300_5 0.0735000261997
eng iter2_MR1_300_5 0.0920983204876
eng iter1_MR0_300_7 0.0783425357348
eng iter1_MR1_300_7 0.0525749276056
eng iter1_MR2_300_7 0.083645449631
eng iter2_MR0_300_7 0.0666609551922
eng iter2_MR1_300_7 0.103232950482
eng iter1_MR0_500_3 0.13918117878
eng iter1_MR1_500_3 0.0914791159133
eng iter1_MR2_500_3 0.0674188633807
eng iter2_MR0_500_3 0.133230999127
eng iter2_MR1_500_3 0.121734676981
eng iter1_MR0_500_5 0.067922528364
eng iter1_MR1_500_5 0.0714125623299
eng iter1_MR2_500_5 0.0873610361358
eng iter2_MR0_500_5 0.127571064537
eng iter2_MR1_500_5 0.106004964692
eng iter1_MR0_500_7 0.0468270040387
eng iter1_MR1_500_7 0.0793139413772
eng iter1_MR2_500_7 0.0649214813446
eng iter2_MR0_500_7 0.0698067670884
eng iter2_MR1_500_7 0.102053795034
xit iter1_MR0_50_3 0.269909010724
xit iter1_MR1_50_3 0.268666357159
xit iter1_MR2_50_3 0.327958257586
xit iter2_MR0_50_3 0.207363211337
xit iter2_MR1_50_3 0.223023392139
xit iter1_MR0_50_5 0.221151182804
xit iter1_MR1_50_5 0.0792162582092
xit iter1_MR2_50_5 0.298717130205
xit iter2_MR0_50_5 0.274857814725
xit iter2_MR1_50_5 0.23199176681
xit iter1_MR0_50_7 0.203304853639
xit iter1_MR1_50_7 0.0745003300731
xit iter1_MR2_50_7 0.154908075735
xit iter2_MR0_50_7 0.188027927693
xit iter2_MR1_50_7 0.281020068782
xit iter1_MR0_50_9 0.163147532426
xit iter1_MR1_50_9 0.0416968295548
xit iter1_MR2_50_9 0.0759200096885
xit iter2_MR0_50_9 0.153692501834
xit iter2_MR1_50_9 0.056582990854
xit iter1_MR0_100_3 0.149705806285
xit iter1_MR1_100_3 0.232944172179
xit iter1_MR2_100_3 0.230128014864
xit iter2_MR0_100_3 0.256253204418
xit iter2_MR1_100_3 0.171480563396
xit iter1_MR0_100_5 0.176898828592
xit iter1_MR1_100_5 0.14987472754
xit iter1_MR2_100_5 0.178236085378
xit iter2_MR0_100_5 0.211810733543
xit iter2_MR1_100_5 0.251976185918
xit iter1_MR0_100_7 0.126322733848
xit iter1_MR1_100_7 0.141445951712
xit iter1_MR2_100_7 0.147603920582
xit iter2_MR0_100_7 0.221175118826
xit iter2_MR1_100_7 0.219496082451
xit iter1_MR0_100_9 0.0494478019187
xit iter1_MR1_100_9 0.159145885235
xit iter1_MR2_100_9 0.0998523387163
xit iter2_MR0_100_9 0.247039498071
xit iter2_MR1_100_9 0.114114478397
xit iter1_MR0_300_3 0.208314910695
xit iter1_MR1_300_3 0.13491716772
xit iter1_MR2_300_3 0.219550493119
xit iter2_MR0_300_3 0.271758402366
xit iter2_MR1_300_3 0.255184779896
xit iter1_MR0_300_5 0.126951716098
xit iter1_MR1_300_5 0.251529940595
xit iter1_MR2_300_5 0.186652419256
xit iter2_MR0_300_5 0.154893536819
xit iter2_MR1_300_5 0.235453932807
xit iter1_MR0_300_7 0.162470086328
xit iter1_MR1_300_7 0.14303355673
xit iter1_MR2_300_7 0.144679258941
xit iter2_MR0_300_7 0.32645085534
xit iter2_MR1_300_7 0.221082181974
xit iter1_MR0_300_9 0.100955829275
xit iter1_MR1_300_9 0.0942386181608
xit iter1_MR2_300_9 0.2142396903
xit iter2_MR0_300_9 0.223305268088
xit iter2_MR1_300_9 0.134300155487
xit iter1_MR0_500_3 0.227659252084
xit iter1_MR1_500_3 0.17692623741
xit iter1_MR2_500_3 0.181100683008
xit iter2_MR0_500_3 0.211606041157
xit iter2_MR1_500_3 0.211482028662
xit iter1_MR0_500_5 0.140840441316
xit iter1_MR1_500_5 0.166469950045
xit iter1_MR2_500_5 0.212952473982
xit iter2_MR0_500_5 0.231451709361
xit iter2_MR1_500_5 0.152080315496
xit iter1_MR0_500_7 0.111824506443
xit iter1_MR1_500_7 0.125499177106
xit iter1_MR2_500_7 0.172832967736
xit iter2_MR0_500_7 0.245161494544
xit iter2_MR1_500_7 0.178349881931
xit iter1_MR0_500_9 0.146695873937
xit iter1_MR1_500_9 0.0557546955664
xit iter1_MR2_500_9 0.131737559267
xit iter2_MR0_500_9 0.0820275916252
xit iter2_MR1_500_9 0.0659872700123
eng mfc 0.11087828881
eng mbf 0.133914986108
xit mfc 0.0896568778182
xit mbf 0.287111280203
eng iter1_MR0 0.124996685276
eng iter1_MR1 0.139851927412
eng iter1_MR2 0.134255748975
eng iter2_MR0 0.103793277746
eng iter2_MR1 0.145180469421
xit iter1_MR0 0.190067516728
xit iter1_MR1 0.212798102375
xit iter1_MR2 0.241793539842
xit iter2_MR0 0.258187869961
xit iter2_MR1 0.254435285465
eng avg_itmr 0.152883329818
xit avg_itmr 0.261781453266
eng avg_all 0.180143987086
xit avg_all 0.263335590608'''

def get_info():
    info = {}
    for line in info_text.split('\n'):
        key = line.split()[0]+'_'+line.split()[1]
        val = float(line.split()[2])
        info[key] = val
    return info
info = get_info()

t_list = ['iter1_MR0', 'iter1_MR1', 'iter1_MR2', 'iter2_MR0', 'iter2_MR1']
l_list = ['eng', 'xit'] 
n_list =  [50, 100, 300, 500]


full = {'iter1_MR0':'TOK-1st, MR-0', 'iter1_MR1':'TOK-1st, MR-1', 'iter1_MR2':'TOK-1st, MR-2', 'iter2_MR0': 'TOK-2nd, MR-0', 'iter2_MR1':'TOK-2nd, MR-1'}
    

def get_m_list(l):
    if l=='eng':    
        m_list = [3,5,7]
    else: 
        m_list = [3,5,7,9]
    return m_list

def get_map(l, t, m, n):
    key = '_'.join([l, t, str(n), str(m)])
    return info[key]

def get_xyz(l, t):
    x, y, z = [], [], []
    for m in get_m_list(l):
        for n in n_list:
            x.append(m)
            y.append(n)
            z.append(get_map(l,t,m,n))
    x, y, z = map(lambda f: np.array(f, dtype=np.float32), [x,y,z])
    return x, y, z
def get_zlim(l):
    z = []
    for m in get_m_list(l):
        for n in n_list:
            for t in t_list:
                z.append(get_map(l,t,m,n))
    return min(z), max(z)
if __name__=='__main__':
    #l = l_list[0]
    #t = t_list[0]
    

    m_min, m_max = 0, 11
    n_min, n_max = 0, 600 
    plot_density = 100
    cont_density = 100
    
    def plot_cont(l, t, ax, zlim):
        x_list = np.array(get_m_list(l))
        y_list = np.array(n_list)
        x, y, z = get_xyz(l, t)
        
        #zmin, zmax = min(z), max(z)
        zmin, zmax = zlim
        
        z_list = z.reshape(x_list.shape[0],y_list.shape[0])
        
        xi = np.linspace(m_min, m_max, plot_density)
        yi = np.linspace(n_min, n_max, plot_density)
        xv, yv = np.meshgrid(xi, yi)
        
        #print x,y,z
        #print xv.shape, yv.shape
        #print xi, yi

        rbs = RectBivariateSpline(x_list,y_list,z_list,kx=2,ky=2)#,bbox = [m_min, m_max, n_min, n_max])
        zv = rbs(xi,yi)
     
        CS = ax.contourf(xv, yv, zv, cont_density, vmin=zmin, vmax=zmax, cmap='Greys_r')
        #plt.colorbar(CS)
        ax.scatter(x, y, facecolor='w')
        ax.set_title(full[t])
        ax.set_xlim([m_min, m_max])
        ax.set_ylim([n_min, n_max])
        return CS 
        #plt.clabel(CS, inline=1, fontsize=10)
        #plt.xticks(x_list, map(str,x_list), rotation='vertical')
        #plt.yticks(y_list, map(str,y_list))
        #plt.imshow(grid_0.T)
        #plt.gcf().set_size_inches(6, 6)
    
    l ='eng'
    fig, axarr = plt.subplots(2, 3)
    zlim = get_zlim(l)
    #zlim = [0,.5]
    #f, ((ax1, ax2, ax3),(ax4, ax5, ax6)) = plt.subplots(2, 3, sharex=True, sharey=True)
    for i in range(5):
        CS = plot_cont(l, t_list[i], axarr[i/3,i%3], zlim)
    for p in [(0,0),(0,1),(1,2)]:
        plt.setp(axarr[p].get_xticklabels(), visible=False)
    for p in [(0,1),(0,2),(1,1),(1,2)]:
        plt.setp(axarr[p].get_yticklabels(), visible=False)
    for p in [(1,2)]:
        plt.setp(axarr[p].get_axes(), visible=False)
        #fig.colorbar(CS ,axarr[p].get_axes())
    cbar_ax = fig.add_axes([0.75, 0.12, 0.05, 0.3])
    #CS.set_clim(zlim)
    #plt.colorbar(CS, cax=cbar_ax)
    zmin, zmax = zlim
    norm = matplotlib.colors.Normalize(vmin=zmin, vmax=zmax)
    cb1 = matplotlib.colorbar.ColorbarBase(cbar_ax, cmap='Greys_r', norm=norm)
    cb1.set_label('MAP')

    #plt.setp([a.get_xticklabels() for a in axarr[0,:]],visible=False)
    #plt.setp([a.get_yticklabels() for a in axarr[:,1]],visible=False)
    #plt.setp([a.get_yticklabels() for a in axarr[:,2]],visible=False)
    
    #fig.subplots_adjust(right=0.8)
    #cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    #fig.colorbar(CS, cax=cbar_ax)
    
    plt.show()
    ''' 
    def func(x, y):
        return x*(1-x)*np.cos(4*np.pi*x) * np.sin(4*np.pi*y**2)**2
    grid_x, grid_y = np.mgrid[0:1:100j, 0:1:200j]

    points = np.random.rand(1000, 2)
    values = func(points[:,0], points[:,1])

    from scipy.interpolate import griddata
    grid_z0 = griddata(points, values, (grid_x, grid_y), method='nearest')
    grid_z1 = griddata(points, values, (grid_x, grid_y), method='linear')
    grid_z2 = griddata(points, values, (grid_x, grid_y), method='cubic')
    import matplotlib.pyplot as plt
    plt.subplot(221)
    plt.imshow(func(grid_x, grid_y).T, extent=(0,1,0,1), origin='lower')
    plt.plot(points[:,0], points[:,1], 'k.', ms=1)
    plt.title('Original')
    plt.subplot(222)
    plt.imshow(grid_z0.T, extent=(0,1,0,1), origin='lower')
    plt.title('Nearest')
    plt.subplot(223)
    plt.imshow(grid_z1.T, extent=(0,1,0,1), origin='lower')
    plt.title('Linear')
    plt.subplot(224)
    plt.imshow(grid_z2.T, extent=(0,1,0,1), origin='lower')
    plt.title('Cubic')
    plt.gcf().set_size_inches(6, 6)
    plt.show()
    '''
