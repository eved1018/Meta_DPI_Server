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
import urllib.request
from pprint import pprint
from html_table_parser import HTMLTableParser
import pandas as pd
from background_task import background

@background()
def Ispred_to_Frame(url):
    # for testing 
    # url = 'https://ispred4.biocomp.unibo.it/ispred/default/display_results.html?jobid=05b2b1e1-d9ff-449a-acb2-ff06caad6a1c'
    xhtml = url_get_contents(url).decode('utf-8')
    


    p = HTMLTableParser()
    p.feed(xhtml)
    # pprint(p.tables)
    first= p.tables[0]
    first =first[0]
    
    columns=first[0:10]
    first=first[10:]
    # print(first)
    to_append = p.tables[0]
    to_append= to_append[1:]
    # print(to_append)
    df = pd.DataFrame( columns = columns)
    df_length = len(df)
    df.loc[df_length] = first
    for i in to_append:
        # print(i)
        to_append_2 = i
        a_series = pd.Series(to_append_2, index = df.columns)
        df = df.append(a_series, ignore_index=True)
        Ispred_frame=df.drop(columns=[ 'Residue type',  'ASA' ,'RSA' ,'Predicted RSA', 'Depth' ,'Protrusion' ,'Surface','Interface' ])
        Ispred_frame = Ispred_frame.rename(columns={'Probability': 'Ispred' })
        Ispred_frame=Ispred_frame.replace({'-': 0}) 
    print(Ispred_frame.head())
    return Ispred_frame



@background()
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
                    Ispred_frame = Ispred_to_Frame(target_url)
                    result = 1
                    return Ispred_frame

                    # with open("{}/{}_{}.txt".format(output_directory,pdb,chain), 'wb') as f:
                    #     r.raw.decode_content = True
                    #     shutil.copyfileobj(r.raw, f)
                    #     result = 1

                    #     ispredfile  = pd.read_csv("{}/{}_{}.txt".format(output_directory,pdb,chain))
                    #     print(ispredfile.head())
                else:
                    result = 1
                    print(r.status_code)
            except:
                pass


