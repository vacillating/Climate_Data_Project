#%%

import os
import requests
import pandas as pd

from climate_data import *


# %%


base_url = "https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/all/"


station_ids = {
    "Harbin": 'CHM00050953',  # Harbin
    "Beijing": 'CHM00054511',  # Beijing
    "Wuhan": 'CHM00057494',  # Wuhan
    "Guangzhou": 'CHM00059287',  # Guangzhou
    "Minneapolis": 'USW00014922',  # Minneapolis
    "Chicago": 'USW00094846',  # Chicago
    "Atlanta": 'USW00013874',  # Atlanta
    "Miami": 'USW00012839',  # Miami
}

df = load_climate_data(station_ids)

# %%
