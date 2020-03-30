import pandas as pd
import numpy as np

wiki = pd.read_html("http://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M")


alldata = []

for column in wiki[0].columns:                           
    tmp = wiki[0][column][ wiki[0][column].str.contains('Not assigned') == False ]    
    for item in tmp.values:
        first_idx = item.find("(")  
        item=item.replace('(','')
        item=item.replace(')','')
        item=item.replace(' /',',')
        if len(item[first_idx:])<=1:
            item = item + item[3:first_idx]
        alldata.append([
            item[0:3], 
            item[3:first_idx], 
            item[first_idx:]
            ])

simplified = pd.DataFrame(alldata, columns=['PostalCode', 'Borough', 'Neighborhood'])
print(simplified)