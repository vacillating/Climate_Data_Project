import os
import requests
import pandas as pd
import calendar



def parse_dly(dly_file):
    records = []
    #with open(file_path, 'r') as f:
    for line in dly_file.splitlines():
        station_id = line[0:11]
        year = int(line[11:15])
        month = int(line[15:17])
        element = line[17:21]
        max_day = calendar.monthrange(year, month)[1]  # 动态判断当月最大天数
        for day in range(1, 32):
            if day > max_day:
                continue  # 跳过无效日期
            value_str = line[21 + (day - 1) * 8: 26 + (day - 1) * 8]
            if value_str.strip() == "-9999":
                value = None
            else:
                value = int(value_str) / 10
            date = pd.Timestamp(year=year, month=month, day=day)
            records.append((station_id, date, element, value))
    return pd.DataFrame(records, columns=["station", "date", "element", "value"])


def download_climate_data(station_id, base_url="https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/all/"):
    url = f"{base_url}{station_id}.dly"

    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        raise Exception(f"Failed to download data for station {station_id}. Status code: {response.status_code}")
    
    return parse_dly(response.text)


def fetch_climate_data(station_id, station_name, base_url = "https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/all/", save_file = False):
    
    url = f"{base_url}{station_id}.dly"
    filename = f"./ghcn_data/{station_id}.csv"
    if os.path.exists(filename):
        return pd.read_csv(filename)
    
    df = download_climate_data(station_id, base_url)
    df["city"] = station_name


    # Do the rest of your cleaning here
    df = df[df['element'].isin(['TMAX', 'TMIN','PRCP'])]

    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    
    if save_file:
        df.to_csv(filename, index=False)
    return df


def load_climate_data(station_ids, base_url="https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/all/", save_file=False):
    return pd.concat(
        [fetch_climate_data(station_id, station_name, base_url, save_file) for station_name, station_id in station_ids.items()],
        ignore_index=True
    )
