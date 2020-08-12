from subprocess import * 
import pandas as pd 
import numpy as np 

def Dockpred_get(pdb,chain):
    perl_command = ["perl","your_script_path.pl"]
    Popen(perl_command)
    # get file of results and turn into dataframe 

