import Tkinter as tk
import tkFileDialog
import tkMessageBox
import os
# from tkFileDialog import askopenfilename

import re
from help_dialogs import info_inputs, info_maxdimension, info_formats, info_results, info_threshold
from menus_info import about_homology, about_persistent_homology_interpret, help_run_program, help_report_bugs_comments

## file with kernel similarity functions
from functions_kernel_similarity import *
## file with plots for kernel similarity
from functions_plot_kernel import plots_similarity_matrix, errorfill, plot_similarity_curve
## file with the main function to compute similarity
from function_main_similarity import main_function_similarity, main_test, check_and_prepare_variables_sim




# def donothing():
#    filewin = tk.Toplevel(root)
#    button = tk.Button(filewin, text="Do nothing button")
#    button.pack()

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.initUI()
        self.createMenu()



    def initUI(self):      
        self.master.title("PDs Similarity")
        self.grid(row=0,column=0,columnspan=5,rowspan=9) 
        # self.create_menubar()
        self.createWidgets()
        self.createWidgets_optional()

    def browse_file_folder(self,var,b_type='folder',normalize=False):
        if b_type is 'folder':
            filename = tkFileDialog.askdirectory()
        if b_type is 'file':
            filename = tkFileDialog.askopenfilename()

        if normalize:
            filename = os.path.basename(filename)

        var.set(filename)

    def createMenu(self):
        self.menubar = tk.Menu(self)

        self.aboutmenu = tk.Menu(self.menubar, tearoff=0)
        self.aboutmenu.add_command(label="Homology and Persistent Homology", command=about_homology)
        self.aboutmenu.add_command(label="Persistent Homology interpretation", command=about_persistent_homology_interpret)
        
        self.menubar.add_cascade(label="About", menu=self.aboutmenu)

        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Run PDs Similarity", command=help_run_program)
        self.helpmenu.add_command(label="Report bugs and comments", command=help_report_bugs_comments)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        self.master.config(menu=self.menubar)

    def createWidgets(self):
        ###################################################################
        ## select folder data
        ## info button 
        self.info_input = tk.Button(self,text ="info", relief=tk.RAISED,\
                         bitmap="info",command=info_inputs)
        self.info_input.grid(row=0,column = 0,sticky=tk.W)
        self.folder_path_input = tk.StringVar()
        self.label_folder1 = tk.Label(self,textvariable=self.folder_path_input,width=40,height=2)
        self.label_folder1.grid(row=1, column=1)
        self.button_data_path = tk.Button(self,text="Folder data", 
            command=lambda: self.browse_file_folder(self.folder_path_input),
            font='Verdana 12 bold')
        self.button_data_path.grid(row=0, column=1,sticky=tk.W+tk.E)

        ###################################################################
        ## select format files
        self.lab_format_files = tk.Label(self,text="Input file/s format",
            font = "Verdana 12 bold") #  fg = "blue",bg = "white",
        self.lab_format_files.grid(row=2, column=3,sticky=tk.W)
        self.var_format = tk.StringVar(None,"csv")
        ## info button 
        self.info_format = tk.Button(self,text ="info", relief=tk.RAISED,\
                         bitmap="info",command=info_formats)
        self.info_format.grid(row=2,column = 2,sticky=tk.W)
        self.format1 = tk.Radiobutton(self, text="csv", variable=self.var_format, value='csv')
        self.format1.grid(row=3, column=3,sticky=tk.W)
        self.format2 = tk.Radiobutton(self, text="txt (delimiter: ,)", variable=self.var_format, value='txt-comma')
        self.format2.grid(row=4, column=3,sticky=tk.W)
        self.format3 = tk.Radiobutton(self, text=r"txt (delimiter: \t)", variable=self.var_format, value='txt-tab')
        self.format3.grid(row=5, column=3,sticky=tk.W)
        ## \TODO delimiter button
        ##################################################################
        ## Execute programm button ##
        self.execute_button = tk.Button(self,command=self.safe_launch_computation,font='Verdana 12 bold')
        self.execute_button["text"] = "Run program"
        self.execute_button["fg"]   = "blue"
        self.execute_button.grid(row=0, column=5)
        ## ----------------------------------------------------------

    def createWidgets_optional(self):
        ## label results 
        self.lab_results = tk.Label(self,text="Results",
            font = "Verdana 12 bold") # fg = "blue",bg = "white",
        self.lab_results.grid(row=6, column=5,sticky=tk.W)
        ## info button 
        self.info_results1 = tk.Button(self,text ="info", relief=tk.RAISED,\
                         bitmap="info",command=info_results)
        self.info_results1.grid(row=6,column = 4,sticky=tk.W)
        ## ------------- OPTIONAL ----------------------------------
        ## output data path
        # \todo add output folder as optional and data folder as default
        # \todo add input folder starting path from: on sigui
        self.folder_path_output = tk.StringVar()
        self.label_folder2 = tk.Label(self,textvariable=self.folder_path_output,width=40,height=2)
        self.label_folder2.grid(row=1, column=5)
        self.button_output_path = tk.Button(self,text="Output folder", 
            command=lambda: self.browse_file_folder(self.folder_path_output)
            )
        self.button_output_path.grid(row=0, column=3,sticky=tk.W)
        ## ----------------------------------------------------------
        ## similarity normalized or not
        self.sim_norm = tk.BooleanVar()
        self.sim_norm.set(True)
        self.sim_norm_label = tk.Checkbutton(self,text ='Normalized similarity',variable = self.sim_norm)
        self.sim_norm_label.grid(row=7, column=3,sticky=tk.W)
        ## ----------------------------------------------------------
        ## generate plots
        self.plots_on = tk.BooleanVar()
        self.plots_on.set(True)
        self.plots = tk.Checkbutton(self,text ='Generate Plots',variable = self.plots_on)
        self.plots.grid(row=8, column=3,sticky=tk.W)
        ###################################################################
        # dimension to compute similarities of persistence diagrams 
        # \TODO just pick the number 
        ## info button 
        self.info_dim = tk.Button(self,text ="info", relief=tk.RAISED,\
                         bitmap="info",command=info_maxdimension)
        self.info_dim.grid(row=2,column = 0,sticky=tk.W)
        self.lab_dim_max = tk.Label(self,text="Dimension to compute\n similarity on persistence diagrams",
            font = "Verdana 12 bold") # fg = "blue",bg = "white",
        self.lab_dim_max.grid(row=2, column=1,sticky=tk.W)
        self.var_dim = tk.IntVar(None,1)
        self.dim_max0 = tk.Radiobutton(self, text="0 (connected components)", variable=self.var_dim, value=0)
        self.dim_max0.grid(row=3, column=1,sticky=tk.W)
        self.dim_max1 = tk.Radiobutton(self, text="1 (cycles)", variable=self.var_dim, value=1)
        self.dim_max1.grid(row=4, column=1,sticky=tk.W)
        self.dim_max2 = tk.Radiobutton(self, text="2 (voids)", variable=self.var_dim, value=2)
        self.dim_max2.grid(row=5, column=1,sticky=tk.W)
        ##################################################################
        ## optional features (threshold - focused on inputs coming from unweighted networks where we have added weight to non existent edges to avoid distance 0)
        ## Sigma value: if None it will be 0.5 by default, 
        self.label_opt_features = tk.Label(self, text="Optional Features:")
        self.label_opt_features.grid(row=6, column=1,sticky=tk.W)
        ## info button 
        self.info_opt_feature_th = tk.Button(self,text ="info", relief=tk.RAISED,\
                         bitmap="info",command=info_threshold)
        self.info_opt_feature_th.grid(row=6,column = 0,sticky=tk.W)

        self.sigma_label = tk.Label(self, text="Sigma (int,float or list of numbers like [0.1,0.3,0.4])")
        self.sigma_label.grid(row=7, column=1,sticky=tk.W)
        self.sigma_val = tk.Entry(self)
        self.sigma_val.grid(row=8, column=1,sticky=tk.W)


    def launch_computation(self):
        print 'launching...'

        data_path=self.folder_path_input.get()

        print 'fdf ',data_path
        output_path,sigma_val,var_format,delimiter = check_and_prepare_variables_sim(
            self.folder_path_input.get(),
            self.folder_path_output.get(),
            self.sigma_val.get(),
            self.var_format.get()
            )
        
        plots_on=self.plots_on.get()
        dim=self.var_dim.get()
        format_type = self.var_format.get()
        normalized=self.sim_norm.get()

        print 'Your input variables are the following:'
        main_test(data_path=self.folder_path_input.get(),
            format_type = var_format,
            delimiter = delimiter,
            output_path = output_path,
            plots_on=self.plots_on.get(),
            dim=self.var_dim.get(),
            sigma = sigma_val,
            normalized=self.sim_norm.get()
            )

        print 'launching Easy PH... '
        print 'sigma ', sigma_val
        main_function_similarity(data_path,format_type,output_path=output_path,sim_weighted=False,sigma=sigma_val,plots_on=plots_on,normalized=normalized,dim=dim,vmax=True,delimiter=delimiter)
        if(output_path==None):
            print 'Go to check your results at %s/results_similarities!'%self.folder_path_input.get()
        else:
            print 'Go to check your results at %s/results_similarities!'%output_path


    def safe_launch_computation(self):
        try:
            self.launch_computation()
        except Exception as e:
            s = str(e)
            raise(e)
            tkMessageBox.showerror("Error",s)
        



# main_function(data_path,format_type,file_name=None,lower_matrix = False, upper_matrix = False, output_path=None,plots_on=True,normalized=False,max_dim=1): 


def run_app():
    root = tk.Tk()
    root.grid_columnconfigure(5, minsize=70) 
    app = Application(master=root)
    app.mainloop()

if __name__=='__main__':
    run_app()

