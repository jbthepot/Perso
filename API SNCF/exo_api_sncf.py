# Useful packages
import os
import numpy as np
import pandas as pd
import io
import json
import datetime as pkgdt
import time
import requests 
from requests.adapters import HTTPAdapter
import itertools # list operators


####################################################################################################################################################
####Basic GET request####

r = requests.get(
    "api_url",
    headers = ''
)

if r.status_code != 200: # see HTTP errors
    print("HTTP ERROR")
else:  
    r.text
    df = pd.DataFrame(r.json()) # make pandas dataframe from the JSON obtained through the API -- to adapt if format is not JSON
    df.columns = map(str.lower, df) # Can be used to force lower case for column name (can ease data processing in the long run !


##Other models

##With params -- see details below
r = requests.get(
    "url_api",
    params='') #list of params to filter for instance the set of data fields retrieved
####################################################################################################################################################

####################################################################################################################################################
####GET with credentials####

# API parameters
api_user = 'user_name'
api_pwd  = 'pwd'
api_url  = 'api_url'

# 1. authenticate against API : retrieve key
# 2. check HTTP error code status



# Basic authentication function based on usr name and pwd as input (can be changed to take key as input)
# In this case, the API returns the token in a field named 'token'. 
# Check the API documentation to make sure that this is the case in your scenario.
def f_api_key(usr, pwd, api_url):
    
    login_info = {
    'login':usr,
    'password':pwd
    }
    
    r = requests.post(
    api_url,
    data = login_info
    )
    
    return r#.json()#.get('token')

# Advanced function dealing with server time-out on the number of requests per second.
# This is one among other possible solutions.
# Check the documentation of the requests package for information on how to split time into Session().
def f_api_key_wdelay(p_usr, p_pwd, api_url):
    
    login_info = {
        'login':p_usr,
        'password':p_pwd
    }
        
    session = requests.Session()
    
    retry   = Retry(
        connect        = 50, 
        backoff_factor = 3
    )
    
    adapter = HTTPAdapter(
        max_retries = retry
    )
    
    session.mount(api_url, adapter)
       
    r = session.post(
        api_url,
        data = login_info
    )
    
    if r.json().get('token') is None:
        print("No token retrieved. Relaunching authentication procedure")
        f_api_key_wdelay(p_usr, p_pwd, api_url)
    else:
        print("Authentication successful: processing...")
        return r.json().get('token')

##########################################################################################################################
        

##########################################################################################################################
# API query with key parameters (in headers)

key = f_api_key(api_user, api_pwd, api_url)
#key = f_api_key_wdelay(api_user, api_pwd, api_url)

headers_val = {
    'x-access-token':key
}

r = requests.get(
    api_url,
    headers = headers_val
)

if r.status_code != 200: 
    print("HTTP ERROR")
else:  
    df = pd.DataFrame(r.json()) 
    df.columns = map(str.lower, df) 
##############################################################################################################################


##############################################################################################################################
# Others parameters can be passed in params attribute of requests.get()
# For example, to query travel-times between an origin and a destination, between dates, on an hourly interval, etc.
# Check requests.get(url, params={key: value}, args) for all arguments

# Example: API parameters origin place, destination (place), start time and end time
O = 'Place_1'
D = 'Place_2'
t_start = pkgdt.datetime(YYYY,MM,DD) # use datetime package to have a proper datetime object
t_end   = pkgdt.datetime(YYYY,MM,DD) 

# Parameters
params_val = {
        'origin'     :O,
        'destination' :D,
        'start'       :str(t_start), # turn datetime object into ISO-formatted datetime string
        'end'         :str(t_end)
    }

# Headers
headers_val = {
	'x-access-token':key
}

#API query
r = requests.get(
	api_url, 
	headers = headers_val,
	params = params_val
)
###############################################################################################################################


###############################################################################################################################
# If the server has a max limit of records it can send back, it is recommended to split the timeframe into intervals using the 
# timedelta function

## Begin and end of the timeframe
t_start = pkgdt.datetime(YYYY,MM,DD)
t_end   = pkgdt.datetime(YYYY,MM,DD)

## Define the step dt to split the timeframe
dt = pkgdt.timedelta(hours=1) # here per hour

## Build the date range as a numpy array
rg_dates = np.arange(d0,d1,dt).astype(pkgdt.datetime) # astype converts numpy.dateime64 into dt.datetime objects

## Loop the query through rg_dates
## Keep in mind that when looping for each t in rg_dates, the api will be queried between t and tnext = t_start + pkgdt.timedelta(hours=1)
#################################################################################################################################


####################################################################################################################################
## Tip to query more than one (O,D) pair using itertools:

### List of origins
lstO = ['Place1','Place2']
lstD = ['Place3','Place4']

### Building the list can take time
lst_queriedData = []

for e in itertools.product(lstO, lstD, rg_dates):
    lst_queriedData.append(e)
    
    
