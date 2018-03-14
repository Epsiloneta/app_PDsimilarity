import sys
import os
# computer = os.getlogin()
import pickle as pk
import networkx as nx
import numpy as np
import pylab as plt
import scipy.io
import pandas as pd
# sys.path.append('/home/%s/Dropbox/ISI_Esther/templates_stable/'%computer) #IMPORTANT (path holes)
# from functions_plot_persistence_diagram import * 



##### kernel Reinenghaus
def kernel_reininghaus(sigma,F,G):
    """
    Given two persistence diagrams compute kernel reininghaus
    INPUT:
        F, G: two persistence diagrams (multisets)
        sigma: parameter of the kernel related with units of steps in the filtrations
    OUTPUT:
        return kernel value (high values small distance, low values high distance)
    """
    k = 0
    for p in F:
        for q in G:
            a1 = np.sqrt((p[0]-q[0])**2 + (p[1]-q[1])**2)
            a2 = np.sqrt((p[0]-q[1])**2 + (p[1]-q[0])**2)
            k= k + np.exp(-a1/(8.*sigma)) - np.exp(-a2/(8.*sigma))
    k = k/(8*np.pi*sigma)
    return(k)

def kernel_reininghaus_normalized(sigma,F,G,with_auto_dist=None):
    """
    Given two persistence diagrams compute kernel reininghaus normalized by the sum of autodistance.
    k_norm(F,G) = k(F,G) / k(F,F)+k(G,G) 
    INPUT:
        F, G: two persistence diagrams (multisets)
        sigma: parameter of the kernel related with units of steps in the filtrations
        with_auto_dist (optional): sum to normalize  k(F,F)+k(G,G)
    OUTPUT:
        return kernel value (high values small distance, low values high distance) normalized
    """
    if(with_auto_dist!=None):
        k = kernel_reininghaus(sigma,F,G)
        ## if both are zero <--- trying to correct when PDs = []
        if(with_auto_dist ==0 and k == 0):
            return(1)
        else:
            return(2*k/with_auto_dist) ## added 2* 18-04-2017 to normalize between 0 and 1, otherwise is between 0 and 0.5
    else:
        k = kernel_reininghaus(sigma,F,G)
        d = kernel_reininghaus(sigma,F,F)
        f = kernel_reininghaus(sigma,G,G)
        return(2*k/(d+f)) 
    return()

##### weighted kernel (Kusano, Fukumizu, Hiraoka) ####
def weighted_kernel(sigma,F,G,C,p=5): 
    """
    Given two persistence diagrams compute weighted kernel
    INPUT:
        F, G: two persistence diagrams (multisets)
        sigma: parameter of the kernel related with units of steps in the filtrations
    OUTPUT:
        return kernel value (high values small distance, low values high distance)
    """
    k = 0
    for p in F:
        for q in G:
            kg = np.exp(-np.sqrt((p[0]-q[0])**2 + (p[1]-q[1])**2)/(2.*(sigma**2)))
            k = k + warc(p,C)*warc(q,C)*kg
    return(k)

def weighted_kernel_normalized(sigma,F,G,C,p=5,with_auto_dist=None):
    """
    Given two persistence diagrams compute kernel reininghaus normalized by the sum of autodistance.
    k_norm(F,G) = k(F,G) / k(F,F)+k(G,G) 
    INPUT:
        F, G: two persistence diagrams (multisets)
        sigma: parameter of the kernel related with units of steps in the filtrations
        with_auto_dist (optional): sum to normalize  k(F,F)+k(G,G)
    OUTPUT:
        return kernel value (high values small distance, low values high distance) normalized
    """
    if(with_auto_dist!=None):
        k = weighted_kernel(sigma,F,G,C,p)
        ## if both are zero <--- trying to correct when PDs = []
        if(with_auto_dist ==0 and k == 0):
            return(1)
        else:
            return(2*k/with_auto_dist) ## added 2* 18-04-2017 to normalize between 0 and 1, otherwise is between 0 and 0.5
    else:
        k = weighted_kernel(sigma,F,G,C,p)
        d = weighted_kernel(sigma,F,F,C,p)
        f = weighted_kernel(sigma,G,G,C,p)
        return(k/(d+f)) 
    return()


def warc(x,C,p=5):
    """
    x=(x1,x2) point in 2D from a PD
    warc(x) = arctan(C pers(x)^p) where C = [median(pers(D))]^-p, where D is a persistence diagram and pers(D) is the list of persistences in D.
    p is a parameter that we decided (as in the original paper) to fix at 5
    """
    pers = x[1]-x[0]
    warc_value = np.arctan((C*pers)**p)
    return(warc_value)

def C_parameter(PDS,p):
    """
    Given a list of Persistence Diagrams compute: 
    C  =  [median(pers(D))]^-p, where D is a persistence diagram and pers(D) is the list of persistences in D.
    p is a parameter that we decided (as in the original paper) to fix at 5
    """
    C = np.median([np.median([x2-x1 for x1,x2 in PD]) if PD != [] else 0 for PD in PDS])**-p
    return(C)


### \todo: read another kind of formats without dim or just ripser outputs
def read_PDs(file_path,delimiter=','):
    if(file_path.split('.')[-1] =='csv'):
        df = pd.read_csv(file_path,index_col=0)
    if(file_path.split('.')[-1] =='txt'):
        pd.read_csv(file_path,delimiter=delimiter)     
    return(df)


def points_PD(df,dim=None):
    """
    df: DataFrame columns birth and death and may dimH
    """
    if(dim==None):
        b = df.birth.values
        d = df.death.values
    else:
        b = df[df.dimH==dim].birth.values
        d = df[df.dimH==dim].death.values
    return(zip(b,d))

## autodistance 
# \TODO do with weighted kernel too
# sigma_range = np.linspace(0.01,2,30)
def create_auto_dist(auto_dist,data_path,list_files,weighted=False,sigma=.5,delimiter=','):
    """
    list_files = 
    auto_dist (dict)
    dir_results (where are PDs), short_name (name dataset)
    sigma: kernel parameter
    """
    for file_name1 in list_files:
        complete_path = os.path.join(data_path,file_name1)
        df = read_PDs(complete_path,delimiter=delimiter)
        name1 = os.path.splitext(file_name1)[0]
        D = points_PD(df,dim=1)
        auto_dist[(name1,sigma)] = kernel_reininghaus(sigma,D,D)
    return(auto_dist)

