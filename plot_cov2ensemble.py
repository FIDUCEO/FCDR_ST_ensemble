# !/usr/bin/env python

# Code include segment in: cov2ensemble.py
# ========================================
# Version 0.1
# 11 July, 2019
# michael.taylor AT reading DOT ac DOT uk
# ========================================

def plot_BT_deltas(dBT,BT_MMD):
    
    fig,ax = plt.subplots()
    for i in range(2*n):
        labelstr = 'ens(' + str(i+1) + ')'
        gd = dBT[:,i] > 0
        plt.plot(BT_MMD[gd],dBT[gd,i], '.', markersize=2, alpha=0.2, label=labelstr)
    plt.plot([220,310],[220,310], '--', color='black', label=None)
    plt.xlim(220,310)
    plt.ylim(220,310)
    plt.legend(loc=2, fontsize=8, ncol=5)
    plt.xlabel(r'brightness temperature, BT / $K$')
    plt.ylabel(r'ensemble brightness temperature, ens(BT) / $K$')
    plotstr = 'bt_deltas' + plotstem
    plt.tight_layout()
    plt.savefig(plotstr)
    plt.close('all')

    BTvec = np.arange(230,310,10)
    for k in range(len(BTvec)-1):
        fig,ax = plt.subplots()
        for i in range(2*n):
            labelstr = 'ens(' + str(i+1) + ')'
            domain = (BT_MMD >= BTvec[k]) & (BT_MMD < BTvec[k+1])  
            gd = (dBT[:,i] > 0) & domain 
            plt.plot(BT_MMD[gd],dBT[gd,i], '.', markersize=2, alpha=0.2, label=labelstr)
        plt.plot([BTvec[k],BTvec[k+1]],[BTvec[k],BTvec[k+1]], '--', color='black', label=None)
        plt.xlim(BTvec[k],BTvec[k+1])
        plt.ylim(BTvec[k],BTvec[k+1])
        plt.legend(loc=2, fontsize=8, ncol=5)
        plt.xlabel(r'brightness temperature, BT / $K$')
        plt.ylabel(r'ensemble brightness temperature, ens(BT) / $K$')
        plotstr = 'bt_deltas' + '_' + str(BTvec[k]) + '_' + str(BTvec[k+1]) + plotstem
        plt.tight_layout()
        plt.savefig(plotstr)
        plt.close('all')

def plot_eigenspectrum(ev):

    nPC = ev['nPC']
    fig,ax = plt.subplots()
    plt.plot(ev['eigenvalues_rank'], ev['eigenvalues_norm'], linestyle='-', marker='.', color='b', label=r'$\lambda/sum(lambda)$')
    plt.plot(ev['eigenvalues_rank'][nPC], ev['eigenvalues_norm'][nPC], marker='o', color='k', mfc='none',label=None)
    plt.plot(ev['eigenvalues_rank'], ev['eigenvalues_cumsum'], linestyle='-', marker='.', color='r',label='cumulative')
    labelstr = 'n(PC)='+str(nPC+1)+' var='+"{0:.5f}".format(ev['nPC_variance'])
    plt.plot(ev['eigenvalues_rank'][nPC], ev['eigenvalues_cumsum'][nPC], marker='o', color='k', mfc='none',label=labelstr)
    plt.legend(loc='right', fontsize=10)
    plt.xlabel('rank')
    plt.ylabel('relative variance')
    plotstr = 'eigenspectrum' + plotstem
    plt.tight_layout()
    plt.savefig(plotstr)
    plt.close('all')

def plot_ensemble_an(dA,Xu):

    nensemble = dA.shape[0]
    nparameters = dA.shape[1]
    if nparameters > 27:
        for i in range(4):
            fig,ax = plt.subplots()
            idx = np.arange(i,nparameters-1,4) # -1 --> MTA:N12 (excl N11)
            for k in range(len(idx)-1):
                for l in range(nensemble):
                    labelstr = 'ens('+str(l+1)+')'
                    if k == 0:
                        plt.plot(k,dA[l,idx[k]]/Xu[idx[k]],'.',label=labelstr)
                    else:
                        plt.plot(k,dA[l,idx[k]]/Xu[idx[k]],'.',label=None)
            plt.legend(loc=2, fontsize=8, ncol=5)
            plt.ylabel(r'$\delta a(n)/u(n)$')
            plt.xlabel('sensor')
            plotstr = 'ensemble_a' + str(i) + plotstem
            plt.tight_layout()
            plt.savefig(plotstr)
            plt.close('all')
    else:
        for i in range(3):
            fig,ax = plt.subplots()
            idx = np.arange(i,nparameters-1,3) # -1 --> MTA:N12 (excl N11)
            for k in range(len(idx)-1):
                for l in range(nensemble):
                    labelstr = 'ens('+str(l+1)+')'
                    if k == 0:
                        plt.plot(k,dA[l,idx[k]]/Xu[idx[k]],'.',label=labelstr)
                    else:
                        plt.plot(k,dA[l,idx[k]]/Xu[idx[k]],'.',label=None)
            plt.legend(loc=2, fontsize=8, ncol=5)
            plt.ylabel(r'$\delta a(n)/u(n)$')
            plt.xlabel('sensor')
            plotstr = 'ensemble_a' + str(i) + plotstem
            plt.tight_layout()
            plt.savefig(plotstr)
            plt.close('all')

def plot_ensemble_deltas_normalised(dX,Xu):

    fig,ax = plt.subplots()
    for i in range(2*n):
        labelstr_c = 'ens(' + str(i+1) + ')'
        plt.plot(dX[i,:]/Xu, lw=2, label=labelstr_c)
#    plt.ylim(-2,2)
    plt.legend(loc=2, fontsize=8, ncol=5)
    plt.xlabel('parameter, a(n)')
    plt.ylabel(r'$\delta a(n)/u(n)$')
    plotstr = 'npc_deltas_over_Xu' + plotstem
    plt.tight_layout()
    plt.savefig(plotstr)
    plt.close('all')

def plot_ensemble_deltas(dX):

    fig,ax = plt.subplots()
    for i in range(2*n):
        labelstr_c = 'ens(' + str(i+1) + ')'
        plt.plot(dX[i,:], lw=2, label=labelstr_c)
#    plt.ylim(-2,2)
    plt.legend(loc=2, fontsize=8, ncol=5)
    plt.xlabel('parameter, a(n)')
    plt.ylabel(r'$\delta a(n)$')
    plotstr = 'npc_deltas' + plotstem
    plt.tight_layout()
    plt.savefig(plotstr)
    plt.close('all')

def plot_pc_deltas(dX2,Xu):

    fig,ax = plt.subplots()
    for i in range(2*n):
        labelstr_c = '(constrained) ens(' + str(i+1) + ')'
        plt.plot(dX2['dX0_constrained'][i,:]/Xu, lw=2, label=labelstr_c)
    for i in range(2*n):
        labelstr_u = '(unconstrained) ens(' + str(i+1) + ')'
        plt.plot(dX2['dX0_unconstrained'][i,:]/Xu, '.', label=labelstr_u)
#    plt.ylim(-2,2)
    plt.legend(loc=2, fontsize=6, ncol=2)
    plt.xlabel('parameter, a(n)')
    plt.ylabel(r'$\delta a(n)/u(n)$')
    plotstr = 'pc1_deltas_over_Xu' + plotstem
    plt.tight_layout()
    plt.savefig(plotstr)
    plt.close('all')

    fig,ax = plt.subplots()
    for i in range(2*n):
        labelstr_c = '(constrained) ens(' + str(i+1) +')'
        plt.plot(dX2['dX1_constrained'][i,:]/Xu, lw=2, label=labelstr_c)
    for i in range(2*n):
        labelstr_u = '(unconstrained) ens(' + str(i+1) + ')'
        plt.plot(dX2['dX1_unconstrained'][i,:]/Xu, '.', label=labelstr_u)
#    plt.ylim(-2,2)
    plt.legend(loc=2, fontsize=6, ncol=2)
    plt.xlabel('parameter, a(n)')
    plt.ylabel(r'$\delta a(n)/u(n)$')
    plotstr = 'pc2_deltas_over_Xu' + plotstem
    plt.tight_layout()
    plt.savefig(plotstr)
    plt.close('all')

def plot_crs():

    for n in np.array([10,50,100,500,1000,5000,10000,50000]):

        random_numbers_unconstrained = crs.generate_10_single(n)
        random_numbers_constrained = crs.generate_10(n)

        fig,ax = plt.subplots(1,2)
        labelstr_constrained = 'n=' + str(n) + ': constrained'
        labelstr_unconstrained = 'n=' + str(n) + ': unconstrained'
        ax[0].plot(np.sort(np.array(random_numbers_unconstrained)), label=labelstr_unconstrained)
        ax[0].plot(np.sort(np.array(random_numbers_constrained)), label=labelstr_constrained)
        ax[0].legend(loc=2, fontsize=8)
        ax[0].set_ylim(-5,5)
        ax[0].set_ylabel('z-score')
        ax[0].set_xlabel('rank')
        ax[0].set_title(r'Sorted random sample from $erf^{-1}(x)$')
        ax[1].hist(random_numbers_unconstrained,bins=100,alpha=0.3,label='unconstrained')
        ax[1].hist(random_numbers_constrained,bins=100,alpha=0.3,label='constrained')
        ax[1].set_xlim(-5,5)
        ax[1].set_xlabel('z-score')
        ax[1].set_ylabel('count')
        plotstr = 'random_numbers_n_' + str(n) + plotstem + '.png' 
        plt.tight_layout()
        plt.savefig(plotstr)
        plt.close('all')

