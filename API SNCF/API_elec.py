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
r=requests.get('http://api.sncf.com/v1/coverage/sncf/stop_areas?start_page={}',auth=('16cbfb01-1943-471f-aac9-7a1139abab77', ''))
  

if r.status_code != 200: # see HTTP errors
    print("HTTP ERROR")
else:  
    r.text
    df = pd.DataFrame(r.json()) # make pandas dataframe from the JSON obtained through the API -- to adapt if format is not JSON
    df.columns = map(str.lower, df) # Can be used to force lower case for column name (can ease data processing in the long run !

