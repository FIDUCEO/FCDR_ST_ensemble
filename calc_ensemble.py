#!/usr/bin/env python

# ipdb> import os; os._exit(1)

# call as: python calc_ensemble.py

# =======================================
# Version 0.3
# 26 March, 2019
# michael.taylor AT reading DOT ac DOT uk
# =======================================

import os  
import os.path  
import glob  
import optparse 
from  optparse import OptionParser  
import sys   
import numpy as np
import numpy.ma as ma  
import xarray
from sklearn.preprocessing import StandardScaler
#import arpack
import scipy
from scipy.linalg import eigh
from scipy.sparse.linalg import eigsh
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns


# =======================================    

def load_data(file_in):
    '''
    Load harmonisation parameters and covariance matrix
    '''
    # matchup_dataset = "AVHRR_REAL_4_RSA_____"
    # job = "job_avh11_v6_ODR_101_11.nml"
    # matchup_dataset_begin = "19911004"
    # matchup_dataset_end = "20151231"

    ds = xarray.open_dataset(file_in)

    return ds

def calc_eigen(ds):
    '''
    Calculate eigenvalues and eigenvectors from the harmonisation parameter covariance matrix
    '''
    # Harmonisation parameter covariance matrix: (27, 27)
    parameter_covariance_matrix = ds['parameter_covariance_matrix'] 
    X = parameter_covariance_matrix

    eigenval, eigenvec = np.linalg.eig(X)
    print('Eigenvalues \n%s' %eigenval)   
    print('Eigenvectors \n%s' %eigenvec)

    return eigenval, eigenvec

def plot_eigenval(eigenval):
    '''
    Plot eigenvalues as a scree plot
    '''
    X = eigenval

    fig = plt.figure()
    plt.plot(X, drawstyle='steps')
    plt.tick_params(labelsize=12)
    plt.ylabel("Eigenvalue", fontsize=12)
    title_str = 'Max=' + "{0:.5f}".format(X.max())
#    print(title_str)
#    plt.legend(loc='best')
    plt.savefig('eigenvalues.png')    

def plot_eigenvec(eigenvec):
    '''
    Plot eigenvector matrix as a heatmap
    '''
    X = eigenvec

    fig = plt.figure()
    df = pd.DataFrame({'MutProb': [0.1, 0.05, 0.01, 0.005, 0.001, 0.1, 0.05, 0.01, 0.005, 0.001, 0.1, 0.0, 0.01, 0.005, 0.001, 0.1, 0.05, 0.01, 0.005, 0.001, 0.1, 0.05, 0.01, 0.005, 0.001], 'SymmetricDivision': [1.0, 1.0, 1.0, 1.0, 1.0, 0.8, 0.8, 0.8, 0.8, 0.8, 0.6, 0.6, 0.6, 0.6, 0.6, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2, 0.2, 0.2, 0.2, 0.2], 'test': ['sackin_yule', 'sackin_yule', 'sackin_yule', 'sackin_yule', 'sackin_yule', 'sackin_yule', 'sackin_yule', 'sackin_yule', 'sackin_yule', 'sackin_yule', 'sackin_yule', 'sackin_yule', 'sackin_yule', 'sackin_yule', 'sackin_yule', 'sackin_yule', 'sackin_yule', 'sackin_yule', 'sackin_yule', 'sackin_yule', 'sackin_yule', 'sackin_yule', 'sackin_yule', 'sackin_yule', 'sackin_yule'], 'value': [-4.1808639999999997, -9.1753490000000006, -11.408113999999999, -10.50245, -8.0274750000000008, -0.72260200000000008, -6.9963940000000004, -10.536339999999999, -9.5440649999999998, -7.1964070000000007, -0.39225599999999999, -6.6216390000000001, -9.5518009999999993, -9.2924690000000005, -6.7605589999999998, -0.65214700000000003, -6.8852289999999989, -9.4557760000000002, -8.9364629999999998, -6.4736289999999999, -0.96481800000000006, -6.051482, -9.7846860000000007, -8.5710630000000005, -6.1461209999999999]})
    result = df.pivot(index='SymmetricDivision', columns='MutProb', values='value')
    sns.heatmap(result, annot=True, fmt="g", cmap='viridis')
    plt.savefig('eigenvectors.png')    

def plot_covariance(ds):
    '''
    Plot harmonisation parameter covariance matrix as a heatmap
    '''
    # Harmonisation parameter covariance matrix: (27, 27)
    parameter_covariance_matrix = ds['parameter_covariance_matrix'] 
    X = parameter_covariance_matrix

    fig = plt.figure()
    df = X
    result = df.pivot(index='SymmetricDivision', columns='MutProb', values='value')
    sns.heatmap(result, annot=True, fmt="g", cmap='viridis')
    plt.savefig('covariance_matrix.png')    

def calc_ensemble(ds):
    '''
    Sample from the N-normal distribution using the harmonisation parameters as the mean values (best case) and the covariance matrix as the N-variance
    '''
    # Harmonisation parameters: (27,)
    parameter = ds['parameter'] 
    # Harmonisation parameter uncertainties: (27,)
    parameter_uncertainty = ds['parameter_uncertainty'] 
    # Harmonisation parameter covariance matrix: (27, 27)
    parameter_covariance_matrix = ds['parameter_covariance_matrix'] 
    # Harmonisation parameter correlation matrix: (27, 27)
    parameter_correlation_matrix = ds['parameter_correlation_matrix'] 
    # Harmonisation parameter Hessian matrix (internal): (27, 27)
    parameter_hessian_matrix = ds['parameter_hessian_matrix'] 
    # Harmonisation parameter add offsets (internal): (27,)
    parameter_add_offset = ds['parameter_add_offset'] 
    # Harmonisation parameter scale factors (internal): (27,)
    parameter_scale_factor = ds['parameter_scale_factor'] 
    # Sensors associated with harmonisation parameters: (27,)
    parameter_sensors = ds['parameter_sensors'] 
    # the number of residual data: (24,)
    k_res_count = ds['k_res_count'] 
    # the costs associated with the residual data: (24,)
    k_res_cost = ds['k_res_cost'] 
    # the reduced costs associated with the residual data: (24,)
    k_res_cost_reduced = ds['k_res_cost_reduced'] 
    # The mean harmonisation residual: (24,)
    k_res_mean = ds['k_res_mean'] 
    # The standard deviation of the mean harmonisation residual: (24,)
    k_res_mean_stdev = ds['k_res_mean_stdev'] 
    # The standard deviation of the harmonisation residual: (24,)
    k_res_stdev = ds['k_res_stdev'] 
    # The sensors associated with the harmonisation residual: (24,)
    k_res_sensors = ds['k_res_sensors'] 

    #
    # Sample from multivariate Gaussian distribution
    #

    # numpy.random.multivariate_normal(mean, cov[, size, check_valid, tol])

    # The multivariate normal, multinormal or Gaussian distribution is a 
    # generalization of the 1D-normal distribution to higher dimensions. 
    # Such a distribution is specified by its mean and covariance matrix. 
    # These parameters are analogous to the mean (average or “center”) and 
    # variance (standard deviation, or “width,” squared) of the 1D-normal distribution.

    # mean : 1-D array_like, of length N
    # Mean of the N-dimensional distribution.

    # cov : 2-D array_like, of shape (N, N)
    # Covariance matrix of the distribution. It must be symmetric and 
    # positive-semidefinite for proper sampling.

    # size : int or tuple of ints, optional

    # Given a shape of, for example, (m,n,k), m*n*k samples are generated, and 
    # packed in an m-by-n-by-k arrangement. Because each sample is N-dimensional, 
    # the output shape is (m,n,k,N). If no shape is specified, a single (N-D) sample is returned.

    # check_valid : { ‘warn’, ‘raise’, ‘ignore’ }, optional
    # Behavior when the covariance matrix is not positive semidefinite.

    # tol : float, optional
    # Tolerance when checking the singular values in covariance matrix.

    # Returns:

    # out : ndarray

    # The drawn samples, of shape size, if that was provided. If not, the shape is (N,).
    # In other words, each entry out[i,j,...,:] is an N-dimensional value drawn from the distribution.

def calc_pca(ds):
    '''
    Perform PCA using standard eigenvalue decomposition of the harmonisation parameter covariance matrix
    '''
    # Harmonisation parameter covariance matrix: (27, 27)
    parameter_covariance_matrix = ds['parameter_covariance_matrix'] 
    X = parameter_covariance_matrix

    # compute a standard eigenvalue decomposition using eigh:
    evals_all, evecs_all = eigh(X)

    # compute the largest eigenvalues (which = 'LM') of X and compare them to the known results:
    evals_large, evecs_large = eigsh(X, 3, which='LM')
    print(evals_all[-3:])
    print(evals_large)
    print(np.dot(evecs_large.T, evecs_all[:,-3:]))

    # solve for the eigenvalues with smallest magnitude:
    evals_small, evecs_small = eigsh(X, 3, which='SM', tol=1E-2)
    # evals_small, evecs_small = eigsh(X, 3, which='SM', maxiter=5000)
    print(evals_small)
    print(np.dot(evecs_small.T, evecs_all[:,:3]))

    # solve for the eigenvalues of the shift-invert mode analogous problem such that thetransformed eigenvalues will then satisfy the inverse relation where small eigenvalues become large eigenvalues:

    evals_small, evecs_small = eigsh(X, 3, sigma=0, which='LM')
    print(evals_small)
    print(np.dot(evecs_small.T, evecs_all[:,:3]))

    # to find internal eigenvalues and eigenvectors, e.g. those nearest to 1, simply set sigma = 1 and ARPACK takes care of the rest:

    evals_mid, evecs_mid = eigsh(X, 3, sigma=1, which='LM')
    i_sort = np.argsort(abs(1. / (1 - evals_all)))[-3:]
    print(evals_all[i_sort])
    print(evals_mid)
    print(np.dot(evecs_mid.T, evecs_all[:,i_sort]))

if __name__ == "__main__":

#    parser = OptionParser("usage: %prog file_in")
#    (options, args) = parser.parse_args()
#    file_in = args[0]

    file_in = "harm_FO_3.0_27b18eb_ODR_101_11_R____AVHRR_REAL_4_RSA______19911004_20151231.nc"
    ds = load_data(file_in)
    eigenval, eigenvec = calc_eigen(ds)
    plot_eigenval(eigenval)
    plot_eigenvec(eigenvec)
#    plot_covariance(ds)
#    calc_ensemble(ds)
#    calc_pca(ds)


