import Tkinter as tk

from help_dialogs import CustomText

# \TODO add references 
def about_homology():
    win = tk.Toplevel()
    win.title("Homology and Persistent Homology")
    about = '''

          -------------------------------------------------------------------
          HOMOLOGY
          -------------------------------------------------------------------
          Homology counts the n-dimensional holes in a given space. 

          How to interpret holes?

          0-dimensional holes: represent connected components
          1-dimensional holes: represent cycles
          2-dimensional holes: represent voids
          n-dimensional holes: represent cavities of n-dimension

          The number of holes (how many) given a dimension is called: betti numbers 
          (betti0: how many connected components there are, betti1: how many cycles there are, ...). 

          Obs: if our space or our object is embedded (lives) in dimension 3 we can not have holes of higher dimension than 2.

          Examples:
            * Sphere:           
              number of 0-dimensional holes: 1
              number of 1-dimensional holes: 0
              number of 2-dimensional holes: 1
              number of n-dimensional holes with n>2: 0 (for all n>2)

            * Torus (also well known as a empty donut):
              number of 0-dimensional holes: 1
              number of 1-dimensional holes: 2
              number of 2-dimensional holes: 1
              number of n-dimensional holes with n>2: 0 (for all n>2)

          -------------------------------------------------------------------
          PERSISTENT HOMOLOGY
          -------------------------------------------------------------------
          Persistent Homology (PH) counts the evolution of n-dimensional holes in a given space.
          'n' refers to the dimension of the hole.

          Filtration: a set of datasets (set1 contained in set2, contained in set3, ... ) from our original dataset.
          
          Example (a): 
            Given a weighted network, G, that respresent a distances between pairs, we can consider all possible thresholds, 
            then we will obtain a set of networks.

            Adjacency matrix of G = [[0,1,3,4],[1,0,10,2],[3,10,0,3],[4,2,3,0]]

            step 0: threshold = 0 -> all nodes disconnected -> betti_0 = 4, betti_1 = 0, betti_n = 0 for n>1
            step 1: threshold = 1 -> appears edge (0,1) ->  betti_0 = 3, betti_1 = 0, betti_n = 0 for n>1
            step 2: threshold = 2 -> appears edge (1,3) ->  betti_0 = 2, betti_1 = 0, betti_n = 0 for n>1
            step 3: threshold = 3 -> appears edges (0,2) and (2,3) ->  betti_0 = 1, betti_1 = 1, betti_n = 0 for n>1 
            (here a cycle appears and we already have an unique connected component)
            step 4: threshold = 4 -> appears edge (0,3) ->  betti_0 = 1, betti_1 = 0, betti_n = 0 for n>1 
            (here the cycle disappears (a triangle is considered full, then it is not a cycle) and we continue to have an unique connected component)
            step 5: threshold > 10 -> appears edge (1,2) ->  betti_0 = 1, betti_1 = 0, betti_n = 0 for n>1 

          It is possible define a parametrization of betti numbers (defined above), that how many holes (for each dimension) there are for each step in the filtration.
          But, there are a better and more informative feature obtained from PH: persistence diagrams or equivalently barcodes.

          Persistence diagrams: set of (x,y) points where,
             x: step/threshold where a n-dim hole is born
             y: step/threshold where a n-dim hole is died

          Barcode:
            Bars of lenght (y-x) indicating when a n-dim hols has been born and died.

          Persistence diagram (PD) from example (a) accoring threshold units:
            0-dimensional PD:
                  points = {(0,1),(0,2),(0,3),(0,)} # (0,) or (0,10) indicates that the one connected component persist forever in the filtration.
            1-dimensional PD:
                  points = {(4,10)} ## there is only one cycle that apperas at threshold >= 4 and then dissapear at threshold = 10
          
          Interpretation (go to Persistent Homology Interpretation to know more about):

            Persistence diagram: as farther a point is from the diagonal more persistent is.
            Barcodes: as larger the bar is more persistent is.

          Keywords in PH:
            * Rips-Vietoris complex filtration
            * Cech complex filtration
            * Clique complex
            * Simplicial complex


          How to compute it?

          Go to... 
          * Classical computation of homology: reduction to Smith normal form: https://www.cs.duke.edu/courses/fall06/cps296.1/Lectures/sec-IV-3.pdf
          * Recent (and improved) methods to compute Persistent Homology: http://mrzv.org/publications/dualities-persistence/manuscript/
          * Optimizations by Ripser: http://ulrich-bauer.org/ripser-talk.pdf

          How to understand theory below Persistent Homology?

          Read ...

          Books about Algebraic Topology:
          * J. R. Munkres. Elements of algebraic topology, volume 2. Addison-Wesley Menlo Park, 1984.
          * A. Hatcher. Algebraic topology. 2002.

          Papers explaining Persistent Homology and its outputs:
          * H. Edelsbrunner and J. Harer. Persistent homology-a survey. Contemporary mathematics, 453:257, 2008.
          * A. Zomorodian and G. Carlsson. Computing persistent homology. Discrete & Computational Geometry, 33(2):249, 2005.
          * R. Ghrist. Barcodes: the persistent topology of data. Bulletin of the American Mathematical Society, 45(1):61, 2008.

        '''
    # about = re.sub("\n\s*", "\n", about) # remove leading whitespace from each line
    t=CustomText(win, wrap="word", width=100, height=25, borderwidth=0)
    t.tag_configure("blue", foreground="blue")
    t.pack(sid="top",fill="both",expand=True)
    t.insert("1.0", about)
    # t.HighlightPattern("Homology", "blue")
    # t.HighlightPattern("Persistent Homology", "blue")
    # tk.Button(win, text='OK', command=win.destroy).pack()

def about_persistent_homology_interpret():
    win = tk.Toplevel()
    win.title("About Persistent Homology interpretation and comparison")
    about = '''

          Persistent Homology can give an idea of the shape of the data.
          
          How? Knowing when connected components, cycles and voids appear and disappear and how many we have.

          Main shapes are that live longer across the filtration.

          For example: Persistence diagrams can help in shape classification.

          Some applications in:

          - Neursocience 
          - Shape classification
          -

          Go to... 


          Measures to compare persistence diagrams:
            * qth Wasserstein distance
            * Bottleneck distance
            * Persistence landscape (Bubenik 2012 and 2015).
            * Vineyards
            * Similarity Kernel (Reininhaus et al 2015)


        '''
    # about = re.sub("\n\s*", "\n", about) # remove leading whitespace from each line
    t=CustomText(win, wrap="word", width=100, height=25, borderwidth=0)
    t.tag_configure("blue", foreground="blue")
    t.pack(sid="top",fill="both",expand=True)
    t.insert("1.0", about)
    # t.HighlightPattern("Homology", "blue")
    # t.HighlightPattern("Persistent Homology", "blue")
    # tk.Button(win, text='OK', command=win.destroy).pack()


def help_run_program():
    win = tk.Toplevel()
    win.title("How to run Easy Persistent Homology?")
    about = '''
    -----------------------------------------------------------------------------------------------------
        Easy run:
        1) Select your folder data in 'Folder data' browser button.
        2) Select file extension / format contained in 'Folder data' that you want to analyse.
        3) Run program!! Trust default parameters ;) 
        4) Your results will be saved in 'Folder data' inside a folder called 'results'
    -----------------------------------------------------------------------------------------------------
        More detailed run:

        1) Select your folder data in 'Folder data' browser button.
        2) Do you want to compute persistent homology in only one file? or in some?
              1.1) If your answer is in only one file, browse your file in 'File to analyse' browser button.
              1.2) If you have many files to analyse, just put these files in your 'Folder data' and not select any in 'File to analyse'. 
                   All files in the 'Folder data' with the given extension (and format) will be analysed.
        3) Do you want to save results in a specific folder?
            3.1) Just select your predilect folder in 'Output folder' browser. Results will be saved there in a new folder:'results'

            3.2) Doubts: Where results have been saved if I have not select any 'Output folder'?
              If you have not select any folder in 'Output folder' your results by default will be in a 'results' folder in the selected 'Data Folder'
        4) Select file extension between possibilites showed in 'Input file/s format'. 
            You only can select one. Then all files in that format/extension containded in the 'Folder data' will be analysed automatically.
            In the case that you have selected just a file, name extension of 'File to analyse' have to coincide with the extension and format of 'Input file/s extension'
        5) What about 'Results'?
          ## PLOTS
          5.1) Default option will generate 2 (if your format is lower/upper txt) or 3 plots (otherwise) saved in 'Output folder' or 'Data folder'(by default). You can turn off this option.
            5.1.1) You can activate option 'Normalized plots' (False by default) then all output plots will be normalized according the maximum value found in the input data.
              Example: "M" input distance matrix, max_M = max(M) then all values (v_i) in the plots will be converted to (v_i / max_M)
        

          ## FILES will be always generated automatically.
          5.2) 'output_PDs.csv': recap all holes for each dimension with its birth and death point. This information serves to plot barcodes and persistence diagrams and analyse a posteriori results or use them as input for another algorithms.
               'summary.txt': contain a summary of the number of holes for each dimension and how many have persisted across a certain percentage of the total possible life.

        6) Max dimension to compute persistent homology:
          * Are you interested in compute how evolve connected components?
            6.1) Compute until dimension 0 if you do not wnat to know about cycles or higher cavities. 

          * Are you interested in know how many cycles, and when they are born and death, you have? (by default 1 is selected)
            6.2) Select 1, automatically 0-dimensional holes (connected components) and 1-dimensional holes (cycles) will be computed.

          * Are you interested in higher dimensional holes like voids?
            6.3) Select 2, automatically 0-dimensional holes (connected components), 1-dimensional holes (cycles) and also 2-dimensional holes (voids) will be computed.
          I am sorry I do not think that you will want to compute higher dimensions... because how are you going to interpret them?? Let me know if you have the answer and I will upgrade the app Easy PH to be able to compute until hihger dimensions ;)
          
        7) Very optional feature (but it can be useful!): Threshold
            In the case that you only are interested in compute persistent homology until a certain baseline (because after that you know that nothing interesting can appear) you just need to put this value here and computations will be also faster if you stop there.
            Possible examples:
              * You know that threshold from a certain distance all will be "connected" then you know a priori the result and you do not need to spend computational time in that. 
              * You are interested in compute just Homology (it can happen), that is, compute the number of n-dimensional holes for only one step/time or let's said frozen dataset. You have to pass as input a fully matrix with values different than zero, then for the connections or distances that you consider infinit you put a greater value than the maximum in the dataset. Then add threshold equal or greater than the maximum value and computation will be faster and after the threshold all will be consider as the same distance.

      -----------------------------------------------------------------------------------------------------

        '''
    # about = re.sub("\n\s*", "\n", about) # remove leading whitespace from each line
    t=CustomText(win, wrap="word", width=100, height=25, borderwidth=0)
    t.tag_configure("blue", foreground="blue")
    t.pack(sid="top",fill="both",expand=True)
    t.insert("1.0", about)
    # t.HighlightPattern("2-dimensional holes", "blue")
    # tk.Button(win, text='OK', command=win.destroy).pack()

def help_report_bugs_comments():
    win = tk.Toplevel()
    win.title("Report bugs and comments")
    about = '''
      If you detect any bug or you have problems to run the program please, contact me and I will try to solve.

      If you have any comment or propose any improvement it will be welcome, just contact me and I will do my best.

      Email: esther.ibanez@isi.it      

        '''
    # about = re.sub("\n\s*", "\n", about) # remove leading whitespace from each line
    t=CustomText(win, wrap="word", width=100, height=25, borderwidth=0)
    t.tag_configure("blue", foreground="blue")
    t.pack(sid="top",fill="both",expand=True)
    t.insert("1.0", about)