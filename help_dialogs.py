import Tkinter as tk

class CustomText(tk.Text):
    '''A text widget with a new method, highlight_pattern()

    example:

    text = CustomText()
    text.tag_configure("red", foreground="#ff0000")
    text.highlight_pattern("this should be red", "red")

    The highlight_pattern method is a simplified python
    version of the tcl code at http://wiki.tcl.tk/3246
    '''
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

    def HighlightPattern(self, pattern, tag, start="1.0", end="end",
                          regexp=False, background=None,foreground=None):
        '''Apply the given tag to all text that matches the given pattern

        If 'regexp' is set to True, pattern will be treated as a regular
        expression according to Tcl's regular expression syntax.
        '''

        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchLimit", end)

        count = tk.IntVar()
        while True:
            index = self.search(pattern, "matchEnd","searchLimit",
                                count=count, regexp=regexp)
            if index == "": break
            if count.get() == 0: break # degenerate pattern which matches zero-length strings
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")
            # \TODO add features to underline, change color... 
            # self.tag_config(tag, background="black", foreground="green")
            # # Creates a bold font
            # self.bold_font = Font(family="Helvetica", size=14, weight="bold")


def info_inputs():
    win = tk.Toplevel()
    win.title("About Input / Output path")
    about = '''
    'Folder data' (compulsory): select folder where your data is saved. Compulsory field to run the program. Program analyse all files inside this folder with the given format file ('txt','csv','npy','gpickle').

    'File to analyse' (optional, empty by default): If you only want to analyse a file please select 'Folder data' as the folder where your file is and then select the file in the possible formats ('txt','csv','npy','gpickle'). Your file extension must be the same than the selected 'Format input file/s'

    'Output folder' (optional, if empty, it will be by default 'Folder data'): Folder path where you want to save output results from the program. 
    '''

    # about = re.sub("\n\s*", "\n", about) # remove leading whitespace from each line
    t=CustomText(win, wrap="word", width=100, height=15, borderwidth=0)
    t.tag_configure("blue", foreground="blue")
    t.pack(sid="top",fill="both",expand=True)
    t.insert("1.0", about)
    t.HighlightPattern("Folder data", "blue")
    t.HighlightPattern("File to analyse", "blue")
    t.HighlightPattern("Output folder", "blue")
    t.HighlightPattern("optional", "blue")
    t.HighlightPattern("compulsory", "blue")
    tk.Button(win, text='OK', command=win.destroy).pack()


def info_maxdimension():
    win = tk.Toplevel()
    win.title("About Maximum dimension to compute Persistent Homology")
    about = '''
          Homology counts the n-dimensional holes in a given space. The number of holes (how many) given a dimension is called: betti numbers. 
          Persistent Homology (PH) counts the evolution of n-dimensional holes in a given space.
          'n' refers to the dimension of the hole:

          0-dimensional holes: represent connected components
          1-dimensional holes: represent cycles
          2-dimensional holes: represent voids
          n-dimensional holes: represent cavities of n-dimension

          For example a torus (also well known as a empty donut) has:

          number of 0-dimensional holes: 1
          number of 1-dimensional holes: 2
          number of 2-dimensional holes: 1
          number of n-dimensional holes with n>2: 0 (for all n>2)

          Options to choose (with interpretability):

          dim 0, dim 1 (default) and dim 2.

          If you choose dimension 0, holes will be computed only for dimension 0. 
          If you choose dimension 1, holes will be computed for dimension 0 and 1. 
          If you choose dimension 2, holes will be computed for dimension 0,1 and until 2. 
        '''
    # about = re.sub("\n\s*", "\n", about) # remove leading whitespace from each line
    t=CustomText(win, wrap="word", width=100, height=25, borderwidth=0)
    t.tag_configure("blue", foreground="blue")
    t.pack(sid="top",fill="both",expand=True)
    t.insert("1.0", about)
    t.HighlightPattern("Homology", "blue")
    t.HighlightPattern("Persistent Homology", "blue")
    t.HighlightPattern("0-dimensional holes", "blue")
    t.HighlightPattern("1-dimensional holes", "blue")
    t.HighlightPattern("2-dimensional holes", "blue")
    t.HighlightPattern("connected components", "blue")
    t.HighlightPattern("cycles", "blue")
    tk.Button(win, text='OK', command=win.destroy).pack()

def info_results():
    win = tk.Toplevel()
    win.title("About Results outputs and options")
    about = '''

    Results from the computation of Persistent Homology are saved in 'Output Folder' (or 'Data Path' by default) and are the following:

          A folder called 'results' will be created in the output folder selection or as default inside the data folder. There you can find: 

          - summary.txt: contain a summary of the number of holes for each dimension and how many have persisted across a certain percentage of the total possible life.
          - outputs_PDS.csv: recap all holes for each dimension with its birth and death point.
          

          If you have actived the option Generate plots (True by default) another folder plots inside results will be created. There you will find persistent diagram plot and barcode plot (both plots shows the same results in different ways). Moreover if your input files are not lower/upper distance matrix (usually used if you are working with more than 10^4 shape size) also will be generated a representation of your input data.
          - barcodes.png
          - PDs.png
          - input_data.png


          Normalized plots (False by default): if active (True) all output plots will be normalized according the maximum value found in the input data.
            Example: "M" input distance matrix, max_M = max(M) then all values (v_i) in the plots will be converted to (v_i / max_M)
        '''

    # about = re.sub("\n\s*", "\n", about) # remove leading whitespace from each line
    t=CustomText(win, wrap="word", width=100, height=25, borderwidth=0)
    t.tag_configure("blue", foreground="blue")
    t.pack(sid="top",fill="both",expand=True)
    t.insert("1.0", about)
    t.HighlightPattern("persistent diagram", "blue")
    t.HighlightPattern("barcode", "blue")
    t.HighlightPattern("Generate plots", "blue")
    t.HighlightPattern("Normalized plots", "blue")
    t.HighlightPattern("Output Folder", "blue")
    tk.Button(win, text='OK', command=win.destroy).pack()


def info_formats():
    win = tk.Toplevel()
    win.title("About Format files")
    about = '''

    Files have to codify, as a matrix (or upper / lower matrix), the pairwaise 'distance / lenght' between objects. 

    Input files are like distance matrices (obviously distance matrix are welcome):
      That is, higher value implies higer distance and viceversa. 
      Algorith will group first nearer points than farther.

    - If you are using correlations you can convert your data using 1-correlation. Be carefull: All values have to be positive!!!

    Attention!!! Adjacency matrix from a not fully-connected network (weighted or unweighted) are not inputs!!! 
                 Any zero in the input means 0 distance between pair of points! (They are only correct if are on the diagonal)

    Format files can have the following extensions:

          - 'txt': (by default) columns delimited by ',' and rows by newline
          - 'npy': commonly python array / matrix 
          - 'gpickle': commonly from networkx library in python

          Recommended format for big matrices (that greater then 10^4 points, matrix shape 10^4 x 10^4)
          - 'txt' (lower-dist matrix): lower matrix (without diagonal), columns delimited by ',' and rows by newline.
            Example:
             1,             or  1
             1,5,               1,5
             3,5,1,             3,5,1
             1,5,1,2,           1,5,1,2
        - 'txt' (upper-dist matrix): upper matrix (without diagonal), columns delimited by ',' and rows by newline.
            Example:
             1,5,1,2,           1,5,1,2
             3,5,1,             3,5,1
             1,5,               1,5
             1,             or  1

    If you select only a file to analyse format must coincide with the file extension.
    If you just select a Folder data, all your files in that folder with the selected extension will be analysed.

    Attention!!! Be careful, an adjacency matrix from a network is not an input!!!!! Because 0 entries mean zero distance between a couple of nodes!
    Network with edges (0,1),(1,2) -> adjacency matrix = array([[0,1,0],[1,0,1],[0,1,0]]) but zeros indicating not edge between (0,2) does not mean distance zero between these points! 
    Possible solution: input matrix = array([[0,1,2],[1,0,1],[2,1,0]]), where 2 is bigger than other entry and it represents an "infinit" distance between 0 and 2. Many other solutions or values are possible.
    Then you can use parameter threshold = 1  (in the example explained above) to finish your computation faster. 

    Attention!!! Obviously, as a distance matrix not negative values in any kind of input format are accepted!

    '''

    # about = re.sub("\n\s*", "\n", about) # remove leading whitespace from each line
    t=CustomText(win, wrap="word", width=120, height=35, borderwidth=0)
    t.tag_configure("blue", foreground="blue")
    t.pack(sid="top",fill="both",expand=True)
    t.insert("1.0", about)
    t.HighlightPattern("Generate plots", "blue")
    t.HighlightPattern("txt", "blue")
    t.HighlightPattern("npy", "blue")
    t.HighlightPattern("gpickle", "blue")
    t.HighlightPattern("lower-", "blue")
    t.HighlightPattern("upper-", "blue")
    t.HighlightPattern("big matrices", "blue")
    t.HighlightPattern("Attention!!!","blue")
    t.HighlightPattern('distance matrix not negative values', 'blue')
    t.HighlightPattern('adjacency matrix from a network is not an input', 'blue')
    t.HighlightPattern('threshold','blue')
    t.HighlightPattern('Any zero in the input means 0 distance between pair of points!','blue')
    tk.Button(win, text='OK', command=win.destroy).pack()


def info_threshold():
    win = tk.Toplevel()
    win.title("About threshold parameter")
    about = '''

    threshold = None (by default). It accepts integers or floats (Ex. 3 or 3.0 or 0.56)

    If you want to finish PH computation before go through all possible thresholds (all possible values in your input data) you need to provide the point (the threshold) where you want to stop computations.

    Possible application (Homology without persistence):
      If you provide an input data coming from, for example, an unweighted network, you can NOT provide an adjacency matrix as input because it does not give any kind of distance between points (nodes). Hence, you need to provide an input file where 0's entries will be converted as an "infinite" distance. 

        Example:

          Adj_matrix = ([0,1,1,0],[1,0,0,0],[1,0,0,1],[0,0,1,0]]) - correspond a path node1 -> node0 -> node2 -> node3
          Possible input_matrix = ([0,1,1,100],[1,0,100,100],[1,100,0,1],[100,100,1,0]]) -> 0's except diagonal have been converted in 100 (like distance between nodes are very high compared to the real links).
        
          threshold = 1 (all values greater mean infinity. You do not need to compute more)

      Moreover, if you have a non-connected network as input, in order to generate an input file and not see how 
        
        Example:

          Adj_matrix = ([0,1,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0]]) - correspond a path node1 -> node0 -> node2 -> node3
          Possible input_matrix = ([0,1,100,100],[1,0,100,100],[100,100,0,1],[100,100,1,0]]) -> 0's except diagonal have been converted in 100 (like distance between nodes are very high compared to the real links).

          threshold = 1 (all values greater mean infinity. You do not need to compute more, otherwise you will see a connected component at the end of the filtration, that is when we consider threshold > 1 we see that all points are connected)


    '''

    # about = re.sub("\n\s*", "\n", about) # remove leading whitespace from each line
    t=CustomText(win, wrap="word", width=100, height=40, borderwidth=0)
    t.tag_configure("blue", foreground="blue")
    t.pack(sid="top",fill="both",expand=True)
    t.insert("1.0", about)
    t.HighlightPattern("can NOT provide an adjacency matrix as input", "blue")
    t.HighlightPattern("input file where 0's entries will be converted as an infinite distance", "blue")
    t.HighlightPattern("Homology without persistence", "blue")
    t.HighlightPattern("finish PH computation before", "blue")
    # t.HighlightPattern("compulsory", "blue")
    tk.Button(win, text='OK', command=win.destroy).pack()
