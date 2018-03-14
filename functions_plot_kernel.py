import sys
import os
import pickle as pk
import networkx as nx
import numpy as np
import pandas as pd
import scipy.io
import pylab as plt

def errorfill(x, y, yerr, color=None, alpha_fill=0.3, ax=None,label=[]):
    """
    use:
        errorfill(x, y_sin, yerr)
    """
    ax = ax if ax is not None else plt.gca()
    # if color is None:
    #     # color = ax._get_lines.color_cycle.next() # old
    #     color = ax._get_lines.prop_cycler.next()
    if np.isscalar(yerr) or len(yerr) == len(y):
        ymin = y - yerr
        ymax = y + yerr
    elif len(yerr) == 2:
        ymin, ymax = yerr
    ## scaled
    ax.plot(x, y ,'o-',color=color,label=label)
    ax.fill_between(x, ymax, ymin, color=color, alpha=alpha_fill)
    ### unscaled
    # ax.plot(range(len(x)),y ,'o-',color=color,label=label)
    # ax.fill_between(range(len(x)),ymax, ymin, color=color, alpha=alpha_fill)
    # plt.xticks(range(len(x)), sigma_range)
    return()

def plots_similarity_matrix(sigma_range,sigma_2keep, sim_matrix_list,mean_sim,std_sim,plots_folder,max_val_one=True):
    """
    sigma_range:  (number or list of them) sigma (used to compute similarity between PDs)
    sigma_2keep: at max we plot 4 similarity matrix for 4 different sigma values. This contain the 4 sigmas (at max) that we will use.
    sim_matrix_list: list of similarity matrix (full upper triangular matrix)
    mean_sim: selected mean from similarity matrix (mean on full upper triangular matrix without diagonal) 
    std_sim: selected mean from similarity matrix (mean on full upper triangular matrix without diagonal) 
    plots_folder: path to save plots
    max_val_one (True by default): colorbar() max val = 1, otherwise will be the max of selected similarity matrices
    """
    if(max_val_one):
        vmax=1
    else: 
        vmax = np.max([np.max(m) for m in sim_matrix_list])
    plt.figure(figsize=(12,17))
    if(len(sigma_range)==1):
        size = sim_matrix_list[0].shape[0]
        plt.imshow(sim_matrix_list[0],interpolation='None',vmin=0,vmax=vmax)
        plt.colorbar()
        plt.title('Similarity matrix: sigma %.3f \n mean similarity: %.3f, std similarity: %.3f'%(sigma_range[0],mean_sim[0],std_sim[0]))
    else:
        num_plots = len(sigma_2keep)
        size = sim_matrix_list[0].shape[0]
        for i,sigmai in zip(range(1,num_plots+1),sigma_2keep):
            plt.subplot(2,2,i)
            plt.imshow(sim_matrix_list[i-1],interpolation='None',vmin=0,vmax=vmax)
            plt.title('sigma %.3f, mean sim: %.3f, std sim: %.3f'%(sigmai,mean_sim[i-1],std_sim[i-1]))
        plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
        cax = plt.axes([0.85, 0.1, 0.075, 0.8])
        plt.colorbar(cax=cax)
        plt.suptitle('Similarity matrices')

    plot_file_name = os.path.join(plots_folder,'similarity_matrix.png')
    plt.savefig(plot_file_name)  
    print 'Saved similarity matrix plot at %s' %plot_file_name
    return()

def plot_similarity_curve(sigma_range,mean_sim,std_sim,len_sample,plots_folder):
    """
    Plot mean curve of similarity across the given range of sigmas. Ploted confidence interval of the mean at 95%
    sigma_range:  (number or list of them) sigma (used to compute similarity between PDs)
    mean_sim: mean from similarity matrix (mean on full upper triangular matrix without diagonal) 
    std_sim: mean from similarity matrix (mean on full upper triangular matrix without diagonal) 
    len_sample: len of full upper triangular matrix without diagonal flatted. Useful to compute CI
    plots_folder: path to save plot
    """

    plt.figure(figsize=(8,6))
    plt.xlabel('sigma',fontsize=20)
    plt.ylabel('Similarity', fontsize=25)
    plt.title('Group Similarity of Persistence Diagrams \nConfidence interval of mean similarity', fontsize=20)
    er = 1.96*std_sim/np.sqrt(len_sample)
    errorfill(np.array(sigma_range), mean_sim, er,color='b')
    plot_file_name = os.path.join(plots_folder,'similarity_curve.png')
    plt.savefig(plot_file_name)  
    print 'Saved similarity mean CI curve plot at %s' %plot_file_name
    return()
