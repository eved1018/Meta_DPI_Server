from django import forms




class PDBForm(forms.Form):
    pdb = forms.CharField(label=False,widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'PDBID_CHAIN'
        }
    ))
    

class FileForm(forms.Form):
    file = forms.FileField(label=False,widget=forms.FileInput(
        attrs={
            'type':"file" ,
            'name':"files[]",
            'multiple class':"custom-file-input form-control",
            'id':"customFile"
            
        }
    ))
    


    