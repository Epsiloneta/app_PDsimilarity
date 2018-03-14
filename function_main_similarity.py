import sys
import os
import pickle as pk
import networkx as nx
import numpy as np
import pandas as pd
import scipy.io
import timeit

## file with kernel similarity functions
from functions_kernel_similarity import *
## file with plots for kernel similarity
from functions_plot_kernel import plots_similarity_matrix, errorfill, plot_similarity_curve


def main_test(**kwarg):
    print kwarg


def main_function_similarity(data_path,format_type,output_path=None,sim_weighted=False,sigma=None,plots_on=True,normalized=False,dim=1,vmax=True,delimiter=','):
    """
    Create output folder with or without additional folder for plots. Compute similarity matrix between pairs of files in a folder data. Compute CI at 95% of the mean similarity curve across a range of sigmas (given).
    Create result file with similarities between pairs of files.
    Note: similarity is a symmetric measure.

    data_path: folder path where data is. It will be used as folder where there are all files to compute PH
        Example: '/home/esther/Dropbox/ISI_Esther/Easy_PH/tmp'
    format_type: format of files to analyse: 'txt','csv'
    
    OPTIONAL:
    output_path: path to save results, if None then output_path will be in data_path (by default: None)
    sim_weighted=False 'use weighted similarity' \TODO
    sigma: (default = 0.5) float,int,list,array. It can be just number, or a range of values (sorted).
    plots_on: True or False. Decide if you want to generate also plots of the results. Matrix of similarities
    normalized: use normalized kernel or not
    dim = 1(if your file comes from output Easy PH, you can select from which dimension do you want to compute similarity
    vmax = True (default), then if plots colorbar will have vmax=1. Otherwise vmax = np.max([np.max(m) for m in similarity_matrix_list])
    """
    ## create folder with results
    if(output_path == None): output_path = data_path
    output_path = os.path.join(output_path,'results_similarities')
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    list_files = []  ## contains all desired files to compute PH (without extension)
    for f in os.listdir(data_path):
        if f.endswith('.%s'%format_type):
            list_files.append(f) ## add to summary
    # list_files = list_files[:10]
    print 'list_files to compute similarity measure',list_files
    number_files = len(list_files)
    ## Plots ## 
    if(plots_on):
        ## check or create folder for plots
        plots_folder = os.path.join(output_path,'plots_similarities')
        if not os.path.exists(plots_folder):
            os.makedirs(plots_folder)

    print 'sigma ',sigma
    if sigma == None:
        sigma_range = [0.5]
        sigma_2keep = set(np.array(sigma_range))
        ind = [0]
    elif(type(sigma) == int or type(sigma) == float):
        sigma_range = [sigma]
        sigma_2keep = set(np.array(sigma_range))
        ind = [0]
    else:
        sigma_range = list(sigma) ## range of sigmas
        if(len(sigma_range)<4):
            ind = range(len(sigma_range))
            sigma_2keep = set(np.array(sigma_range))
        else:
            ind = map(int,np.linspace(0,len(sigma_range)-1,4))
            sigma_2keep = set(np.array(sigma_range)[ind])
    print 'sigma range',sigma_range

    ## save results
    df_sim = pd.DataFrame()
    ## save max 4 similarity matrix 
    sim_matrix_list = [0]*len(sigma_range)
    mean_sim = np.zeros(len(sigma_range))
    std_sim = np.zeros(len(sigma_range))
    ii_aux = 0 
    #############################################
    for index_sigma,sigma in enumerate(sigma_range):
        start = timeit.default_timer() 
        print 'sigma ', sigma
        if(normalized):
            print list_files
            ### prepare computation
            auto_dist = dict()
            create_auto_dist(auto_dist,data_path,list_files,weighted=False,sigma=sigma,delimiter=delimiter)

        ### compute similarity by pairs
        names1 = [0]*int(number_files*(number_files-1)/2.)
        names2 = [0]*int(number_files*(number_files-1)/2.)
        sigmas_list = np.zeros(int(number_files*(number_files-1)/2.))
        sim_list = np.zeros(int(number_files*(number_files-1)/2.))

        sim_matrix = np.zeros((number_files,number_files))
        ## file_name devi esssere complete path? if yes:base=os.path.basename('/root/dir/sub/file.ext')

        index = 0
        for i,file_name1 in enumerate(list_files,start=0):
            for j in range(i+1,number_files): 
                print 'ij', i,j
                file_name2 = list_files[j]
                name1 = os.path.splitext(file_name1)[0]
                name2 = os.path.splitext(file_name2)[0]
                names1[index] = name1
                names2[index] = name2

                complete_path1 = os.path.join(data_path,file_name1)
                complete_path2 = os.path.join(data_path,file_name2)

                df1 = read_PDs(complete_path1,delimiter=delimiter)
                df2 = read_PDs(complete_path2,delimiter=delimiter)
                F = points_PD(df1,dim=dim)
                G = points_PD(df2,dim=dim)
                ## Compute similarity
                if(normalized):
                    k = kernel_reininghaus_normalized(sigma,F,G,with_auto_dist=auto_dist[(name1,sigma)]+ auto_dist[(name2,sigma)] )
                else:
                    k = kernel_reininghaus(sigma,F,G)

                ## upgrade similarity matrix 
                sim_matrix[i,j] = k

                sim_list[index] = k
                sigmas_list[index] = sigma
                index = index +1
                stop = timeit.default_timer()
                print 'sigma %.3f similarity execution time '%sigma
                print stop - start 

        aux_data = pd.DataFrame()
        aux_data['id1'] = names1
        aux_data['id2'] = names2
        aux_data['similarity'] = sim_list
        aux_data['sigma'] = sigmas_list
        df_sim = df_sim.append(aux_data,ignore_index=True)

        if(plots_on):
            if(sigma in sigma_2keep):
                sim_matrix_list[ii_aux] = sim_matrix
                ii_aux = ii_aux +1 ##we only save 4 matrix max

            ## to plot similarity curve 
            a = sim_matrix[np.triu_indices_from(sim_matrix,k=1)]
            mean_sim[index_sigma] = np.mean(a)
            std_sim[index_sigma] = np.std(a)
            print 'mean_sim ', mean_sim
            print 'std_sim ', std_sim
            len_sample = len(a)
            print 'len sample ', len_sample
    output_file_path = os.path.join(output_path,'similarity.csv')
    df_sim.to_csv(output_file_path) ## save pandas file with PDs for dim 0,1,2
    ######## Plots ##############################################
    if(plots_on): 
        print 'sigma_range ', sigma_range
        print 'sigma_2keep ', sigma_2keep
        print 'sim_matrix_list ',sim_matrix_list
        print 'ind ', ind
        print 'mean sim ',mean_sim
        print 'std_sim ',std_sim

        print mean_sim[ind],std_sim[ind]
        plots_similarity_matrix(sigma_range,sigma_2keep, sim_matrix_list,mean_sim[ind],std_sim[ind],plots_folder,max_val_one=vmax)
        if(len(sigma_range)>1):
            plot_similarity_curve(sigma_range,mean_sim,std_sim,len_sample,plots_folder)
    ############################################################
    print 'Results will be at %s'%output_path
    return()

def check_and_prepare_variables_sim(data_path,output_path,sigma_val,var_format):

    if(data_path==''):
        raise Exception('You need to select a Data folder')

    if(output_path == ''):
        output_path = None

    print 'sigma ',sigma_val
    print 'type ', type(sigma_val)
    if(sigma_val ==''):
        print 'sigma is not given 0.5 will be assigned'
        sigma_val = None
    elif(',' in sigma_val):
        print 'sigma is a list'
        sigma_val = list(eval(sigma_val))
    else:
        print 'sigma is a number'
        sigma_val = float(sigma_val)
    
    if(var_format=='txt-comma'):
        var_format = 'txt'
        delimiter = ','
    elif(var_format=='txt-tab'):
        var_format = 'txt'
        delimiter = '\t'
    else:
        var_format = 'csv'
        delimiter = ','
    return(output_path,sigma_val,var_format,delimiter)

def main_test(**kwarg):
    print kwarg

#### check coma separing numbers