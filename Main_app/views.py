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

def Ispred_get(pdb,chain):
    proteinname = pdb+'.'+chain
    print(proteinname)
    protein_ids = {}
    br = mechanize.Browser()
    br.set_handle_redirect(mechanize.HTTPRedirectHandler)
    br.open("https://ispred4.biocomp.unibo.it/welcome/default/index")
    # print(br.forms)
    br.select_form(action="#")
    FILENAME='./Temp/PDBs/{}_{}.pdb'.format(pdb, chain)
    br.form.add_file(open(FILENAME), 'text/plain', FILENAME)
    br.form.set_all_readonly(False)
    br['ispred_chain'] = chain
    req = br.submit()
    html = str(br.response().readlines())
    jobid = html.find('jobid')
    jobid= html[jobid+6:jobid+42]
    protein_ids[proteinname] = jobid
    print(protein_ids)
    for key in protein_ids:
        url = "https://ispred4.biocomp.unibo.it/welcome/default/index"
        br.open("https://ispred4.biocomp.unibo.it/ispred/default/searchjob")
        br.select_form(action="#")
        br['jobuuid'] = protein_ids[key]
        br.submit(type='submit')
        target_url = 'https://ispred4.biocomp.unibo.it/ispred/default/display_results.html?jobid={}'.format(jobid)
        output_directory = './Temp/Ispred' 
        # print(target_url)
        result = None
        while result is None:
            try:
                br.open(target_url)
                r = requests.get('https://ispred4.biocomp.unibo.it/ispred/default/downloadjob?jobid={}'.format(jobid), stream=True,headers={'User-agent': 'Mozilla/5.0'})
                if r.status_code == 200:
                    with open("{}/{}_{}.txt".format(output_directory,pdb,chain), 'wb') as f:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, f)
                        result = 1
                else:
                    result = 1
                    print(r.status_code)
            except:
                pass
                
       

def Meta_DPI_Setup(pdb,chain):
    
    pathPDBFolder('./Temp/PDBs')
    pdb_file = parsePDB(fetchPDB(f'{pdb}', compressed=False), chain=chain)
    writePDB('{}.pdb'.format(pdb), pdb_file)
    shutil.move('{}.pdb'.format(pdb), 'Temp/PDBs/{}_{}.pdb'.format(pdb,chain))
    for filename in os.listdir('Temp/PDBs'):
        if filename.endswith('gz'):
            os.remove('Temp/PDBs/{}'.format(filename))
    Ispred_get(pdb,chain)
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

def Parser(pdb):
    # parses pdb input will display error if _ or . isnt used or pdb is too big/ to short need to add lookup from RCBS 
    error_message= ""

    if len(pdb) == 4:
        
        chain = None
        results,tree = Meta_DPI_Setup(pdb,chain)
        context = {'pdb':pdb,'results' : results,'tree' : tree ,}
        return context
    elif len(pdb) == 6:
        
        if "_" in pdb:
            
            pdb_chain = pdb.split("_")
            pdb = pdb_chain[0]
            chain = pdb_chain[1]
            results,tree = Meta_DPI_Setup(pdb,chain)
            context = {'pdb':pdb,'results' : results,'tree' : tree}
            return context
            
        if "." in pdb:
            
            pdb_chain = pdb.split(".")
            pdb = pdb_chain[0]
            chain = pdb_chain[1]
            results,tree = Meta_DPI_Setup(pdb,chain)
            context = {'pdb':pdb,'results' : results,'tree' : tree}
            return context
    else: 
        error_message = "PDb id is not known "
        results = ""
        context = {'results': results ,'error_message': error_message}
        return context



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
    return render(request,'Main_app/home.html',{'title':home ,'form': form ,'form2':file_form ,'error_message': error_message  } )


    
def Results(request): 
    return render(request,'Main_app/Results.html')
    
    

def About(request):

    return render(request,'Main_app/about.html')
    
def Refrences(request):
    
    return render(request,'Main_app/Refrences.html')
    


