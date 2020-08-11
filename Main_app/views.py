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
from HTTPHandle import handle_uploaded_file,Parser
from HTTPParser import Ispred_to_Frame
from Ispred_get import Ispred_get



def Meta_DPI_Setup(pdb,chain):
    
    pathPDBFolder('./Temp/PDBs')
    pdb_file = parsePDB(fetchPDB(f'{pdb}', compressed=False), chain=chain)
    writePDB('{}.pdb'.format(pdb), pdb_file)
    shutil.move('{}.pdb'.format(pdb), 'Temp/PDBs/{}_{}.pdb'.format(pdb,chain))
    for filename in os.listdir('Temp/PDBs'):
        if filename.endswith('gz'):
            os.remove('Temp/PDBs/{}'.format(filename))
    Ispred_get(pdb,chain)
    Ispred_read(pdb,chain)
    # do something with pdb file...
    # predition_score_get()
    # this is where we call the functions to perfrom data collection and RF/Logreg
    # Meta_DPI()
    # this is where we will prepare the results for output. 

    results = pd.DataFrame()
    results["col1"] = ["1","2",'3']
    results["col2"] = ["1","2",'3']
    results = results.to_html(index=False)

    tree = '/Users/evanedelstein/Desktop/Research_Evan/Raji_Summer2019_atom/Data_Files/CrossVal_logreg_RF/5foldCV/Crossvaltest47/Trees/Rftree_CV1.svg'

    # delete all files in temp when done:
    # for filename in os.listdir('Temp'):
    # os.remove('Temp/{}'.format(filename))

    return results, tree

def home(request):
    form = PDBForm(request.POST)
    file_form = FileForm(request.POST)
    error_message = ""
    if request.method == "POST" and form.is_valid():
        pdb = form.cleaned_data['pdb']
        context = Parser(pdb)
        return render(request,'Main_app/Results.html' ,context)
    elif request.method == 'POST' and request.FILES:
        file_form = FileForm(request.POST, request.FILES)
        datafile = request.FILES['file']
        context  = handle_uploaded_file(datafile)
        return render(request,'Main_app/Results.html' ,context)
    
    form = PDBForm
    file_form = FileForm
    context ={'title':home ,'form': form ,'form2':file_form ,'error_message': error_message  }
    return render(request,'Main_app/home.html',context )


    
def Results(request): 
    return render(request,'Main_app/Results.html')
    
    

def About(request):

    return render(request,'Main_app/about.html')
    
def Refrences(request):
    
    return render(request,'Main_app/Refrences.html')
    


