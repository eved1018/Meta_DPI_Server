


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