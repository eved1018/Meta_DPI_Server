from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .forms import PDBForm,FileForm
import os
from django.conf import settings
from prody import *
import tempfile
import Bio
from Bio.PDB import PDBList
import shutil
import mechanize
import requests
import time
from .Ispred_get import Ispred_get

def handle_uploaded_file(datafile):
    pdbs= []
    with datafile.open('r') as f:
        lines = f.readlines()
        for line in lines:
            pdb = line.decode('utf8')
            pdbs.append(pdb)
        f.close()
    for pdb in pdbs:
        pdb = pdb.rstrip("\n")
        context = Parser(pdb)
    return context 
    

def predition_score_get():
    # this is where we will get the three prediction scores and combine them into a dataframe with residue as index  
    pass

def Meta_DPI():
    # this will take in the dataframe of the three predictiors and perform the Logreg and RF 
    # I (evan) will do this 
    pass
   

def Parser(pdb):
    # gets one pdb at a time 
    # parses pdb input will display error if _ or . isnt used or pdb is too big/ to short need to add lookup from RCBS 
    error_message= ""

    if len(pdb) == 4:
        
        chain = None
        results,tree, error = Meta_DPI_Setup(pdb,chain)
        context = {'pdb':pdb,'results' : results,'tree': tree,'error_message':error}
        return context
    elif len(pdb) == 6:
        
        if "_" in pdb:
            
            pdb_chain = pdb.split("_")
            pdb = pdb_chain[0]
            chain = pdb_chain[1]
            results,tree, error = Meta_DPI_Setup(pdb,chain)
            context = {'pdb':pdb,'results' : results,'tree': tree,'error_message':error}
            return context
            
        if "." in pdb:
            
            pdb_chain = pdb.split(".")
            pdb = pdb_chain[0]
            chain = pdb_chain[1]
            results,tree, error = Meta_DPI_Setup(pdb,chain)
            context = {'pdb':pdb,'results' : results,'tree': tree,'error_message':error ,}
            return context
    else: 
        error_message = "Invalid PDB_ID Input"
        results = ""
        context = {'results': results ,'error_message': error_message}
        return context

def Meta_DPI_Setup(pdb,chain):
    pathPDBFolder=('./Temp/PDBs')
    try:
        pdb_file = parsePDB(fetchPDB(f'{pdb}', compressed=False), chain=chain)
        writePDB('{}.pdb'.format(pdb), pdb_file)
        shutil.move('{}.pdb'.format(pdb), 'Temp/PDBs/{}_{}.pdb'.format(pdb,chain))
        for filename in os.listdir('Temp/PDBs'):
            if filename.endswith('gz'):
                os.remove('Temp/PDBs/{}'.format(filename))
    except:
        error = 'pdb cannot be found'
       
    
    ispred_frame = Ispred_get(pdb,chain)
    
    # do something with pdb file...
    # predition_score_get()
    # this is where we call the functions to perfrom data collection and RF/Logreg
    # Meta_DPI()
    # this is where we will prepare the results for output. 
    if ispred_frame is None:
        error = 'data not handled '
    else:
        results = ispred_frame
        results = results.to_html(index=False)
        error = ""

    tree = '/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/CrossVal_logreg_RF/5foldCV/Crossvaltest47/Tree/Rftree_CV1.svg'

    # delete all files in temp when done:
    # for filename in os.listdir('Temp'):
    # os.remove('Temp/{}'.format(filename))

    return results, tree, error 