import urllib.request
from pprint import pprint
from html_table_parser import HTMLTableParser
import pandas as pd


def url_get_contents(url):
    """ Opens a website and read its binary contents (HTTP Response Body) """
    req = urllib.request.Request(url=url)
    f = urllib.request.urlopen(req)
    return f.read()


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

    


# if __name__ == '__main__':
#     main()
