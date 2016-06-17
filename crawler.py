#annanikishova@gmail.com

import requests
import base64
import urllib2
import json
import time
from datetime import datetime, timedelta

def encodeBase64(stringToEncode):
    retorno = base64.b64encode(stringToEncode)    
    return retorno

origins = [u'LED', u'MOW']

dayCount = 25

while dayCount < 93:

    endpoint = "https://api.test.sabre.com/v1"
    urlByService = "/auth/token?="
    url = endpoint + urlByService
    password = "v68npJKN"
    encodedUserInfo =  encodeBase64("V1:11dhmnwb72pizl3t:DEVCENTER:EXT")
    encodedPassword =  encodeBase64(password)
    encodedSecurityInfo = encodeBase64(encodedUserInfo + ":" + encodedPassword)
    data = {'grant_type':'client_credentials'}
    headers = {'content-type': 'application/x-www-form-urlencoded ','Authorization': 'Basic ' + encodedSecurityInfo}
    response = requests.post(url, headers=headers,data=data)
    access_token = response.json()
    token = 'Bearer ' + access_token[u'access_token']


    for origin in origins:

        if origin == 'LED':

            destinations = ['AER', 'BCN', 'MOW', 'PRG']

        elif origin == 'MOW':

            destinations = ['AAQ', 'AER', 'AMS', 'AYT', 'BCN', 'BER', 'BOJ', 'DXB', 'DYU', 'EVN', 'FRU', 'IEV', 'IST', 'KGD', 'KRR', 'LED', 'LON', 'MAD', 'MIL', 'MRV', 'MUC', 'NYC', 'ODS', 'OVB', 'PAR', 'PRG', 'PUJ', 'ROM', 'ROV', 'SIP', 'SVX', 'TAS', 'TBS', 'TCI', 'TIV', 'TLV', 'VIE']

        for dist in destinations:

            dd = datetime.now() + timedelta(dayCount)
            departured = str(dd)[:10]
            rd = datetime.now() + timedelta(dayCount + 7)
            returnd = str(rd)[:10]

            url = "https://api.test.sabre.com/v1/shop/flights?origin=" + origin + "&destination=" + dist + "&departuredate=" + departured + "&returndate=" + returnd + "&onlineitinerariesonly=N&limit=300&offset=1&eticketsonly=N&sortby=totalfare&order=asc&sortby2=departuretime&order2=asc&pointofsalecountry=US"

            try:

                req = urllib2.Request(url, headers={'Authorization': token})

                response = urllib2.urlopen(req)

                data = json.load(response)

                date_string = time.strftime("%Y-%m-%d")

                filename = 'DataForThreeMonths/From= '+ origin + ' To= '+ dist + " Departure= " + departured + ' Collected= ' + date_string + '.json'

                with open(filename,'w') as outfile:
                    json.dump(data, outfile)

            except urllib2.HTTPError, err:
                print(err)
                pass

            time.sleep(2)

    dayCount += 1



