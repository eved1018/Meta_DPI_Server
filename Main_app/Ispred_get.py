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
from .HTTPParser import Ispred_to_Frame

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
                Ispred_to_Frame(target_url)

                # r = requests.get('https://ispred4.biocomp.unibo.it/ispred/default/downloadjob?jobid={}'.format(jobid), stream=True,headers={'User-agent': 'Mozilla/5.0'})
                # if r.status_code == 200:
                #     with open("{}/{}_{}.txt".format(output_directory,pdb,chain), 'wb') as f:
                #         r.raw.decode_content = True
                #         shutil.copyfileobj(r.raw, f)
                #         result = 1

                        # ispredfile  = pd.read_csv("{}/{}_{}.txt".format(output_directory,pdb,chain))
                        # print(ispredfile.head())
                # else:
                #     result = 1
                #     print(r.status_code)
            except:
                pass