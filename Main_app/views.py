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
from .HTTPHandle import handle_uploaded_file,Parser,Meta_DPI_Setup



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
    


