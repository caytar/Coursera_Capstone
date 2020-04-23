import foursquare
import pandas as pd


# Construct the client object
client = foursquare.Foursquare(
    client_id='ZMIFBYADUNN35RUQHQFY32PKLS2F14KUTAC4J2CMU35FVLSJ', 
    client_secret='KOAYUEJ5BV2ORNJKFVYPUKMAZPTOUY5FPOKKZ3E5TCL4ULHA'
    )

# Build the authorization url for your app

liste = client.venues.search(params={'query': 'restaurant', 'll': '40.7233,-74.0030'})


liste2 = pd.json_normalize(liste)
print(liste2)

'''
import pandas as pd
import numpy as np

wiki = pd.read_html("http://en.wikipedia.org/w/index.php?title=List_of_postal_codes_of_Canada:_M&oldid=947772202")


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
#print(simplified)

simplified.insert(loc=3,column="Latitude",value=0.0)
simplified.insert(loc=4,column="Longitude",value=0.0)


#### Get the coordinates
import geocoder 

# ARCGIS provider is used, google is very limited 

for index,row in simplified.iterrows():
    g = geocoder.arcgis(row["Borough"] + ", " + row["PostalCode"] + ", Canada" )
    simplified.at[index,'Latitude'] = g.latlng[0]
    simplified.at[index,'Longitude'] = g.latlng[1]

print(simplified)

'''