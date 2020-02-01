# python -m IPython
# This script will be used to pull data from Open Sky's REST API
import requests
from azure.storage.blob import BlobServiceClient
import time
import os
import pandas as pd

#Class to hold API functions
class get_flightdata():
    def __init__(self):
        return

    def states_all(self):
        url = "https://opensky-network.org/api/states/all"
        response = requests.get(url).json()
        return response


#JSON Response needs to be parsed and inserted into table
json_data = get_flightdata().states_all()
#print json_data
flights = []
timepulled = json_data['time']
for i in json_data['states']:
    if i[1].startswith('JBU') == True:
        flights.append(i)

#Create pandas data table from the response
headers = ['icao24','callsign','origin_country','time_position','last_contact','longitude','latitude','baro_altitude','on_ground','velocity','true_track','vertical_rate','sensors','geo_altitude','squawk','spi','position_source']
data = pd.DataFrame(flights, columns=headers)

#Connect to azure blob storage account and dump the JSON response into the storage account
credential = "8g2Fqc9sTpHKfwmew7A54I182vyVmBnQM6Z9lHf9V0fvxj5A0oq5WsagpRrR/Dtas8+a/2m7jwMMFoqq8Qk7Qw=="
service = BlobServiceClient(account_url="https://openskystorage.blob.core.windows.net/", credential=credential)
theblob = service.get_blob_client(container="statesall", blob=str(time.time()))
theblob.upload_blob(data.to_csv(index=False))
