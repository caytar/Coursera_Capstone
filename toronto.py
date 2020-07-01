import pandas as pd
import json, requests, matplotlib

# DATA - 1
# Falefel venues in Toronto from Foursquare
params1 = dict(    v='20200606',
    near='toronto',
    query='felafel',
    limit=50
)

resp = requests.get(url='https://api.foursquare.com/v2/venues/search', params=params1)
data_1 = json.loads(resp.text)
data_1 = pd.json_normalize(data_1['response']['venues'])
data_1 = data_1[["location.lat","location.lng"]]
print(data_1)

# DATA - 2
# Postal Codes and Longitude-Latitude coordinates from Wikipedia

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

simplified.insert(loc=3,column="Latitude",value=0.0)
simplified.insert(loc=4,column="Longitude",value=0.0)


import geocoder

for index,row in simplified.iterrows():
    g = geocoder.arcgis(row["Borough"] + ", " + row["PostalCode"] + ", Canada" )
    simplified.at[index,'Latitude'] = g.latlng[0]
    simplified.at[index,'Longitude'] = g.latlng[1]

data_2 = simplified.drop('Neighborhood', axis=1)
data_2['close2felafel'] = 0

#%matplotlib tk
#simplified.plot()


# DATA - 3
# Listing of attractions in Toronto, as determined by Visitor Services from Toronto Open Data Portal
aa = pd.read_csv("https://ckan0.cf.opendata.inter.prod-toronto.ca/download_resource/17a6b17e-159f-4f42-9f03-7418388674ea?format=csv&projection=4326")
aa = aa[['NAME', 'CATEGORY','ADDRESS_FULL','POSTAL_CODE']]
aa['PostalCode'] = aa['POSTAL_CODE'].str.slice(0,3)
data_3 = aa
print(data_3)


# DATA joining, cleaning, transformation with raw data
# Determine the postal codes which have Falefal restaurants near to them according to lat, long values

closeness_treshold = 0.1

for myiter in data_1.iterrows():
    query_string = f'Latitude > {myiter[1]["location.lat"] - closeness_treshold} & Latitude < {myiter[1]["location.lat"] + closeness_treshold} & Longitude > {myiter[1]["location.lng"] - closeness_treshold} & Longitude < {myiter[1]["location.lng"] + closeness_treshold}'
    temp_df = data_2.query(query_string)
    temp_df["close2felafel"] = 1
    data_2.update(temp_df)

with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'max_colwidth', 10):
    print (data_2)



'''

params2 = dict(client_id='ZMIFBYADUNN35RUQHQFY32PKLS2F14KUTAC4J2CMU35FVLSJ', client_secret='KOAYUEJ5BV2ORNJKFVYPUKMAZPTOUY5FPOKKZ3E5TCL4ULHA',
    v='20200606',
    limit=50
)

#resp = requests.get(url='https://api.foursquare.com/v2/venues/categories', params=params2)

'''
