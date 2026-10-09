# -*- coding: utf-8 -*-
"""
 PortWatch Nowcasting functions

---

<br>**Contributors:** [Alessandra Sozzi](asozzi@imf.org) & [Mario Saraiva](msaraiva@imf.org)
<br> **Description:** This notebook contains several functions needed to extract, transform and output data according to the IMF PortWatch Nowcasting of Global Trade methodology. You may access the full methodology through the IMF Working Paper [soon to be released] - *Arslanalp S., S. M. Choi, P. Kamali, R. Koepke, M. McKetty, M. Ruta, M. Saraiva, A. Sozzi, and J. Verschuur (2025), "Nowcasting Global Trade from Space," IMF Working Paper 25/XX.*

<br> **Tags:** #bigdata #ais #portwatch #ports #nowcasting #trade

---

###Import libraries
"""

import numpy as np
import pandas as pd

from datetime import datetime, date, timedelta
import time
import re
import json
import requests
from io import StringIO
from bs4 import BeautifulSoup

import sdmx # Requires installation in Colab


"""### ASSETS"""

# World (WLD)
# Advanced Economies (110)
# Euro Area (163)
# Major Advanced Economies (G7) (119)
# Other Advanced Economies (Advanced Economies excluding G7 and Euro Area) (123)
# European Union (998)
# ASEAN-5 (510)
# Emerging Market and Developing Economies (200)
# Emerging and Developing Asia (505)
# Emerging and Developing Europe (903)
# Latin America and the Caribbean (205)
# Middle East and Central Asia (400)
# Sub-Saharan Africa (603)

# Country Composition of WEO Groups from https://www.imf.org/en/Publications/WEO/weo-database/2023/April/groups-and-aggregates
WEO_COUNTRY_GROUPS = [
    # World
    {
        'code': 'WLD',
        'name': 'World',
    },

    # Advanced Economies
    {
        'code': '110',
        'name': 'Advanced Economies',
        'country_list': ['AND', 'AUS', 'AUT', 'BEL', 'CAN', 'HRV', 'CYP', 'CZE', 'DNK', 'EST', 'FIN', 'FRA', 'DEU',
                         'GRC', 'HKG', 'ISL', 'IRL', 'ISR', 'ITA', 'JPN', 'KOR', 'LVA', 'LTU', 'LUX', 'MAC', 'MLT',
                         'NLD', 'NZL', 'NOR', 'PRT', 'PRI', 'SMR', 'SGP', 'SVK', 'SVN', 'ESP', 'SWE', 'CHE', 'TWN',
                         'GBR', 'USA']
    },

    # Euro Area
    {
        'code': '163',
        'name': 'Euro Area',
        'country_list': ['AUT', 'BEL', 'HRV', 'CYP', 'EST', 'FIN', 'FRA', 'DEU', 'GRC', 'IRL', 'ITA', 'LVA', 'LTU',
                        'LUX', 'MLT', 'NLD',  'PRT', 'SVK', 'SVN', 'ESP']
    },

    # Major Advanced Economies (G7)
    {
        'code': '119',
        'name': 'Major Advanced Economies (G7)',
        'country_list': ['CAN', 'FRA', 'DEU', 'ITA', 'JPN', 'GBR', 'USA']
    },

    # Other Advanced Economies (Advanced Economies excluding G7 and Euro Area)
    {
        'code': '123',
        'name': 'Other Advanced Economies (Advanced Economies excluding G7 and Euro Area)',
        'country_list': ['AND', 'AUS', 'CZE', 'DNK', 'HKG', 'ISL',
                        'ISR',  'KOR', 'MAC', 'NZL', 'NOR', 'PRI',
                        'SMR', 'SGP', 'SWE', 'CHE', 'TWN']
    },

    # European Union
    {
        'code': '998',
        'name': 'European Union',
        'country_list': ['AUT', 'BEL', 'BGR', 'HRV', 'CYP', 'CZE', 'DNK', 'EST', 'FIN', 'FRA', 'DEU', 'GRC', 'HUN', 'IRL',
                        'ITA', 'LVA', 'LTU', 'LUX', 'MLT', 'NLD', 'POL', 'PRT', 'ROU', 'SVK', 'SVN', 'ESP', 'SWE']
    },

    # ASEAN-5
    {
        'code': '510',
        'name': 'ASEAN-5',
        'country_list': ['IDN', 'MYS', 'PHL', 'SGP', 'THA']
    },

    # Emerging Market and Developing Economies
    {
        'code': '200',
        'name': 'Emerging Market and Developing Economies',
        'country_list': ['AFG', 'ALB', 'DZA', 'AGO', 'ATG', 'ARG', 'ARM', 'ABW', 'AZE', 'BHS',
                        'BHR', 'BGD', 'BRB', 'BLR', 'BLZ', 'BEN', 'BTN', 'BOL', 'BIH', 'BWA',
                        'BRA', 'BRN', 'BGR', 'BFA', 'BDI', 'CPV', 'KHM', 'CMR', 'CAF', 'TCD',
                        'CHL', 'CHN', 'COL', 'COM', 'COD', 'COG', 'CRI', 'CIV', 'DJI', 'DMA',
                        'DOM', 'ECU', 'EGY', 'SLV', 'GNQ', 'ERI', 'SWZ', 'ETH', 'FJI', 'GAB',
                        'GMB', 'GEO', 'GHA', 'GRD', 'GTM', 'GIN', 'GNB', 'GUY', 'HTI', 'HND',
                        'HUN', 'IND', 'IDN', 'IRN', 'IRQ', 'JAM', 'JOR', 'KAZ', 'KEN', 'KIR',
                        'KOS', 'KWT', 'KGZ', 'LAO', 'LBN', 'LSO', 'LBR', 'LBY', 'MDG', 'MWI',
                        'MYS', 'MDV', 'MLI', 'MHL', 'MRT', 'MUS', 'MEX', 'FSM', 'MDA', 'MNG',
                        'MNE', 'MAR', 'MOZ', 'MMR', 'NAM', 'NRU', 'NPL', 'NIC', 'NER', 'NGA',
                        'MKD', 'OMN', 'PAK', 'PLW', 'PAN', 'PNG', 'PRY', 'PER', 'PHL', 'POL',
                        'QAT', 'ROU', 'RUS', 'RWA', 'WSM', 'STP', 'SAU', 'SEN', 'SRB', 'SYC',
                        'SLE', 'SLB', 'SOM', 'ZAF', 'SSD', 'LKA', 'KNA', 'LCA', 'VCT', 'SDN',
                        'SUR', 'SYR', 'TJK', 'TZA', 'THA', 'TLS', 'TGO', 'TON', 'TTO', 'TUN',
                        'TUR', 'TKM', 'TUV', 'UGA', 'UKR', 'ARE', 'URY', 'UZB', 'VUT', 'VEN',
                        'VNM', 'WBG', 'YEM', 'ZMB', 'ZWE']
    },

    # Emerging and Developing Asia
    {
        'code': '505',
        'name': 'Emerging and Developing Asia',
        'country_list': ['BGD', 'BTN', 'BRN', 'KHM', 'CHN', 'FJI', 'IND', 'IDN', 'KIR', 'LAO', 'MYS', 'MDV', 'MHL', 'FSM',
                        'MNG', 'MMR', 'NRU', 'NPL', 'PLW', 'PNG', 'PHL', 'WSM', 'SLB', 'LKA', 'THA', 'TLS', 'TON',
                        'TUV', 'VUT', 'VNM']
    },

    # Emerging and Developing Europe
    {
        'code': '903',
        'name': 'Emerging and Developing Europe',
        'country_list': ['ALB', 'BLR', 'BIH', 'BGR', 'HUN', 'KOS', 'MDA', 'MNE', 'MKD', 'POL',
                        'ROU', 'RUS', 'SRB', 'TUR', 'UKR']
    },

    # Latin America and the Caribbean
    {
        'code': '205',
        'name': 'Latin America and the Caribbean',
        'country_list': ['ATG', 'ARG', 'ABW', 'BHS', 'BRB', 'BLZ', 'BOL', 'BRA', 'CHL', 'COL', 'CRI', 'DMA', 'DOM', 'ECU',
                        'SLV', 'GRD', 'GTM', 'GUY', 'HTI', 'HND', 'JAM', 'MEX', 'NIC', 'PAN', 'PRY', 'PER', 'KNA',
                        'LCA', 'VCT', 'SUR', 'TTO', 'URY', 'VEN']
    },

    # Middle East and Central Asia
    {
        'code': '400',
        'name': 'Middle East and Central Asia',
        'country_list': ['AFG', 'DZA', 'ARM', 'AZE', 'DJI', 'BHR', 'EGY', 'GEO', 'IRN', 'IRQ', 'JOR', 'KAZ', 'KWT', 'KGZ',
                        'LBN', 'LBY', 'MRT', 'MAR', 'OMN', 'PAK', 'QAT', 'SAU', 'SOM', 'SDN', 'SYR', 'TJK', 'TUN', 'TKM',
                        'ARE', 'UZB', 'WBG', 'YEM']
    },

    # Sub-Saharan Africa
    {
        'code': '603',
        'name': 'Sub-Saharan Africa',
        'country_list': ['AGO', 'BEN', 'BWA', 'BFA', 'BDI', 'CPV', 'CMR', 'CAF', 'TCD', 'COM', 'COG', 'COD', 'CIV', 'GNQ',
                           'ERI', 'SWZ', 'ETH', 'GAB', 'GMB', 'GHA', 'GIN', 'GNB', 'KEN', 'LSO', 'LBR', 'MDG', 'MLI',
                           'MWI', 'MUS', 'MOZ', 'NAM', 'NER', 'NGA', 'RWA', 'STP', 'SEN', 'SYC', 'SLE', 'ZAF', 'SSD',
                           'TZA', 'TGO', 'UGA', 'ZMB', 'ZWE']
    }
]

"""### Functions Query PortWatch data from PortWatch API"""

"""
This module provides functions to query data from the PortWatch API.
Functions:
    get_api_data(url, params):
        Sends a GET request to the specified URL with the given parameters and returns the JSON response.
    paginate_api(url, params, delay=1):
        Paginates through the API results by incrementing the resultOffset parameter and returns all results.
    query_portwatch(url, where="1=1", maxRecordCountFactor=5, outFields="*", f="json"):
        Queries the PortWatch API with the specified parameters and returns the results as a pandas DataFrame.
"""

# Query PortWatch data from portwatch.imf.org
def get_api_data(url, params):
    """
    Fetch data from the given API endpoint.

    Args:
        url (str): The URL of the API endpoint.
        params (dict): A dictionary of query parameters to include in the request.

    Returns:
        dict: The JSON response from the API.

    Raises:
        requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
    """
    response = requests.get(url, params=params)
    response.raise_for_status()
    response_json = response.json()
    return response_json

# Function to make API requests and increment resultOffset
def paginate_api(url, params, delay=1):
    """
    Fetches and paginates data from an API endpoint.
    This function handles the pagination of API requests by making multiple
    requests to fetch all records in batches. It uses the 'resultOffset' parameter
    to fetch records in chunks and appends them to a list which is returned at the end.
    Args:
        url (str): The API endpoint URL.
        params (dict): A dictionary of parameters to be sent with the API request.
            Required keys are:
                - 'where': The query condition.
                - 'outFields': The fields to be returned.
                - 'f': The format of the response.
                - 'maxRecordCountFactor': A positive integer to determine the batch size.
        delay (int, optional): The delay in seconds between consecutive API requests. Default is 1 second.
    Returns:
        list: A list of all records fetched from the API.
    Raises:
        ValueError: If the response does not contain 'count' key or if 'maxRecordCountFactor' is not a positive integer.
        requests.exceptions.HTTPError: If the API request fails.
    """
    params_initial = {
        "where": params['where'],
        "returnCountOnly": True,
        "outFields": params['outFields'],
        "f": params['f']
    }
    response = requests.get(url, params=params_initial)
    response.raise_for_status()
    response_json = response.json()
    if 'count' not in response_json:
        raise ValueError("The response does not contain 'count' key")

    total_records = response_json['count']
    if params['maxRecordCountFactor'] <= 0:
        raise ValueError("maxRecordCountFactor must be a positive integer")
    batch_size = params['maxRecordCountFactor'] * 1000
    print(f"Begin extraction of {total_records} number of records...")

    batch_size = params['maxRecordCountFactor']*1000

    # Initialize an empty list to store the results
    all_results = []

    # Loop to fetch all records
    for offset in range(0, total_records, batch_size):
        print(f"Extracting batch of {batch_size} starting at record {offset}...")

        # Make the API request
        params["resultOffset"] = offset
        result = get_api_data(url, params)

        # Check if there are any features in the result
        if 'features' in result and len(result['features']) > 0:
            # Append the features to the list
            all_results.extend(result['features'])
        else:
            # No more records, break out of the loop
            break

        time.sleep(delay)

    return all_results

def query_portwatch(dataset, where="1=1", maxRecordCountFactor=5, outFields="*", f="json", index_col=None):
    """
    Queries the PortWatch API and returns the results as a pandas DataFrame.
    Parameters:
    dataset (str): The dataset to query from the PortWatch API.
    where (str, optional): The SQL-like WHERE clause to filter the query. Defaults to "1=1".
    maxRecordCountFactor (int, optional): Factor to determine the maximum record count for pagination. Defaults to 5.
    outFields (str, optional): Comma-separated list of fields to include in the output. Defaults to "*".
    f (str, optional): The format of the response. Defaults to "json".
    index_col (str, optional): Column to set as the index of the DataFrame. Defaults to None.
    Returns:
    pd.DataFrame: A pandas DataFrame containing the query results. If the 'date' field is present, it will be converted to datetime and sorted.
    """
    url = f"https://services9.arcgis.com/weJ1QsnbMYJlCHdG/arcgis/rest/services/{dataset}/FeatureServer/0/query"
    print(f"Querying PortWatch data {dataset}...")
    results = paginate_api(url,
                            {"where": where,
                            "maxRecordCountFactor":maxRecordCountFactor,
                            "outFields":outFields,
                            "f":f},
                            delay=0)
    attributes = [f['attributes'] for f in results]
    df = pd.DataFrame.from_records(attributes)
    if 'date' in df.columns:
        if df['date'].dtype == 'int64':
            df['date'] = pd.to_datetime(df['date'], unit='ms', origin='unix')
        else:
            df['date'] = pd.to_datetime(df['date'])
        df.sort_values(by='date', inplace=True, ignore_index=True)
    if index_col is not None:
        df.set_index(index_col, inplace=True)
    return df

"""### Functions Load PortWatch Local Data """

# Portwatch Local Data
def fetch_portwatch_local(filepath):
    df = pd.read_csv(filepath)
    print("Latest Observation: ", df.date.max())
    return df

def tweak_portwatch_local(df, iso3='WLD', start_date='2019-01-01', end_date=None):
    flows = ['import', 'export']
    vessel_types = ['tanker', 'dry_bulk', 'container', 'general_cargo', 'roro']
    vessel_types_subset = ['tanker', 'dry_bulk', 'cargo']
    cols_to_keep = [f'{flow}_{vtype}' for vtype in vessel_types for flow in flows]

    # Convert date column 
    df['date'] = pd.to_datetime(df['date'])

    # Add Regional Aggregates
    print(f"Processing group {iso3} ...")
    if iso3 == 'WLD':
        regional_df = df.groupby(['date'])[cols_to_keep].sum().resample('MS').sum()
    else:
        if isinstance(iso3, str):
            iso3 = [iso3]
        regional_df = df[df['ISO3'].isin(iso3)].groupby(['date'])[cols_to_keep].sum().resample('MS').sum()

    # Filter based given start_date and end_date
    regional_df = bound_dates(regional_df, start_date, end_date)

    return(regional_df
           # Sum Import/Export Container, General Cargo  and Ro-Ro under a single category Cargo
            .assign(**{'import_cargo':lambda df_: df_.loc[:, ['import_container',
                                                            'import_general_cargo',
                                                            'import_roro']].sum(axis=1).values},
                    **{'export_cargo':lambda df_: df_.loc[:, ['export_container',
                                                            'export_general_cargo',
                                                            'export_roro']].sum(axis=1).values})
            .pipe(lambda df_: pd.DataFrame(
                df_.values,
                index=df_.index,
                columns=pd.MultiIndex.from_tuples(
                    [('_'.join(c.split('_')[1:]), c.split('_')[0]) for c in df_.columns])))
            .loc[:, (vessel_types_subset, flows)]
            .sort_index(axis='columns'))

"""### Functions Utilities and Calculations """

def get_last_month_end():
    """
    Get the last day of the previous month.
    This function calculates the last day of the month preceding the current month.
    It returns the date in the format 'YYYY-MM-DD' and prints a message indicating
    the date up to which the process is running.
    Returns:
      str: The last day of the previous month in 'YYYY-MM-DD' format.
    """
    today = date.today()
    first = today.replace(day=1)
    last_month = first - timedelta(days=1)
    print(f"Running process until {last_month.strftime('%B %d, %Y')} ...")
    return last_month.strftime('%Y-%m-%d')

def bound_dates(df, start_date=None, end_date=None):
    """
    Reindex a dataframe to a specified date range.
    Parameters:
    df (pd.DataFrame): The dataframe to reindex. It should have a DatetimeIndex.
    start_date (str, optional): The start date for the date range in 'YYYY-MM-DD' format. 
                  If None, the minimum date in the dataframe index is used.
    end_date (str, optional): The end date for the date range in 'YYYY-MM-DD' format. 
                  If None, the maximum date in the dataframe index is used.

    Returns:
    pd.DataFrame: The reindexed dataframe with the specified date range.
    """
    if start_date is None:
      start_date = df.index.min().strftime('%Y-%m-%d')
    if end_date is None:
      end_date = df.index.max().strftime('%Y-%m-%d')
    date_range = pd.date_range(start=start_date, end=end_date, freq='MS')
    date_range.name = 'date'
    return df.reindex(date_range)

def to_index(df, base_year=2019):
    """
    Convert a dataframe to an index.
    Parameters:
      df (pd.DataFrame): The dataframe to convert.
      base_year (int, optional): The base year for the index. Default is 2019.
    Returns:
      pd.DataFrame: The index dataframe.
    """
    index = df/df.loc[df.index.year == base_year].mean()*100
    return index

def growth_rate(df, period=12):
    """
    Calculate the growth rate of a dataframe.
    Parameters:
      df (pd.DataFrame): The dataframe to calculate the growth rate for.
      base_year (int, optional): The base year for the growth rate. Default is 2019.
    Returns:
      pd.DataFrame: The growth rate dataframe.
    """
    # Calculate the growth rate
    growth = (df/df.shift(period)-1)*100
    # Set the index name to 'date'
    return growth.iloc[period:]

def moving_avg(df, period=3):
    """
    Calculate the moving average of a dataframe.
    Parameters:
      df (pd.DataFrame): The dataframe to calculate the moving average for.
      period (int, optional): The period for the moving average. Default is 3.
    Returns:
      pd.DataFrame: The moving average dataframe.
    """
    # Calculate the growth rate
    # Set the index name to 'date'
    return df.rolling(period).mean().iloc[period-1:]

def correlate(s1, s2):
  """
  Calculate the correlation between two series.
  Parameters:
    s1 (pd.Series): The first series.
    s2 (pd.Series): The second series.
  Returns:
    float: The correlation coefficient between the two series.
  """
  # Ensure both series have the same date index 
  if s1.index.max() > s2.index.max():
    s1 = bound_dates(s1, end_date=s2.index.max())
  else:
    s2 = bound_dates(s2, end_date=s1.index.max())
  return round(s1.corr(s2), 2)


"""###Functions Fetch, Tweak and Compile"""

def fetch_and_tweak(fetch_func, tweak_func, *args, **kwargs):
    """
    Fetches data using fetch_func and then tweaks it using tweak_func.
    Returns the tweaked data.
    """
    df = fetch_func(*args, **kwargs)
    return tweak_func(df, **kwargs)


# CPB World Trade Monitor (Official Data)
def fetch_cpb(**kwargs):
    """
    Fetches the CPB World Trade Monitor data from the CPB website.
    """
    base_url = requests.get("https://www.cpb.nl/en/worldtrademonitor/latest")
    soup = BeautifulSoup(base_url.content, 'html.parser')
    latest_data_url = 'https://www.cpb.nl'+soup.find('a', {'download':"", 'class':"button-primary"})['href']
    return pd.read_excel(latest_data_url, header=3)

def tweak_cpb(df, start_date='2019-01-01', end_date=None, **kwargs):
    """
    Tweaks the CPB World Trade Monitor data.
    """
    date_cols = [c for c in df.columns if re.match(r'^\d{4}m\d{2}$', c)]
    country_codes = {'w1': 'World', 'i1': 'Advanced Economies', 'e6': 'Euro Area',
                   'us': 'United States', 'gb': 'United Kingdom',
                   'jp': 'Japan', 'a3': 'Advanced Asia excl Japan',
                   'r2': 'Other Advanced Economies', 'd1': 'Emerging Economies',
                   'cn': 'China', 'a5': 'Emerging Asia excl China',
                   't1': 'Eastern Europe / CIS',
                   'l1': 'Latin America', 'f3':'Africa and Middle East'}
    flow_codes = {'tgz': 'trade', 'mgz': 'import', 'xgz': 'export',
                'hfl': 'price index', 'hpr': 'price index excl fuels'}
    series_codes = {'qnmi': 'volume', 'pdmi': 'price'}

    def _tweak_final_data(df):
        return(df
          .stack(future_stack=True)
          .swaplevel()
          .sort_index())

    extracted = (df
              .pipe(lambda df_: df_.rename(columns={df_.columns[2]: 'code'}))
              .dropna(subset=['code'])
              .assign(country=lambda df_: df_.code.str.slice(4,6).map(country_codes),
                      flow=lambda df_: df_.code.str.slice(0,3).map(flow_codes),
                      series=lambda df_: df_.code.str.slice(7,11).map(series_codes))
              .melt(id_vars=['country', 'flow', 'series'], value_vars=date_cols,
                    var_name='date', value_name='value')
              .assign(date=lambda df_: pd.to_datetime(df_.date, format='%Ym%m'))
              .pivot(index='date', columns=['series', 'flow', 'country'], values='value')
              .sort_index(axis='columns')
              .pipe(lambda df_: bound_dates(df_, start_date=start_date, end_date=end_date)))

    year = pd.to_datetime(start_date).year
    price = extracted.loc[:, ('price')].loc[:, ['import', 'export']]
    volume = extracted.loc[:, ('volume')].loc[:, ['import', 'export']]
    value = (price
            .multiply(volume)
            .pipe(lambda df_: to_index(df_, base_year=year))
            .pipe(lambda df_: _tweak_final_data(df_)))
    volume = (volume
                .pipe(lambda df_: to_index(df_, base_year=year))
                .pipe(lambda df_: _tweak_final_data(df_)))

    return (value, volume)

# US CPI 
def fetch_us_cpi(**kwargs):
    """
    Fetches the US CPI data from the BLS website.
    """
    query_url = "https://api.bls.gov/publicAPI/v1/timeseries/data/"
    params = json.dumps({"seriesid": ['CUUR0000SACL1E'],
                        "startyear": "2019",
                        "endyear": datetime.today().strftime('%Y')})
    response = requests.post(query_url,
                            data=params, headers={'Content-type': 'application/json'})
    raw_df = pd.DataFrame(json.loads(response.text)['Results']['series'][0]['data'])
    return raw_df

def tweak_us_cpi(df, start_date='2019-01-01', end_date=None, **kwargs):
    """
    Tweaks the US CPI data.
    """
    clean_df = (df
                .assign(value=lambda df_: df_.value.replace('-', np.nan)) # Format missing values as NaN - eg October 2025 
                .assign(date=lambda df_: pd.to_datetime(df_.year.astype(str)+df_.period, format='%YM%m'),
                        value=lambda df_: df_.value.astype(float))
                .loc[:, ['date', 'value']]
                .sort_values('date')
                .set_index('date')
                .pipe(lambda df_: bound_dates(df_, start_date=start_date, end_date=end_date)))
    # Interpolate missing values (e.g. Oct 2025) using prior and next month values
    clean_df = clean_df.interpolate(method='linear')
    return clean_df

# Cleveland FED US CPI Nowcasts
def fetch_cleveland_cpi(**kwargs):
    """
    Fetches the Cleveland FED US CPI Nowcasts data from the Cleveland FED website.
    These are nowcasts of the US CPI Index calculated by the Cleveland FED.
    """
    base_url = requests.get("https://www.clevelandfed.org/indicators-and-data/inflation-nowcasting")
    soup = BeautifulSoup(base_url.content, 'html.parser')
    inflation_table = soup.find('table', attrs={'class': 'table-default'})
    inflation_table.tfoot.decompose()
    return pd.read_html(StringIO(str(inflation_table)))[0]

def tweak_cleveland_cpi(df, **kwargs):
    """
    Tweaks the Cleveland FED US CPI Nowcasts data. Calculates the change in the nowcasted US CPI Index.
    """
    return(df
            .assign(date=lambda df_: pd.to_datetime(df_.Month, format='%B %Y'),
                    value=lambda df_: df_.PCE.astype(float))
            .loc[:, ['date', 'value']]
            .sort_values('date')
            .set_index('date')
            .divide(100).add(1))

# Extend US CPI using Cleveland FED US CPI Nowcasts
def adjust_cpi(cpi, end_date, start_date='2019-01-01'):
    """
    Use the Cleveland FED US CPI nowcasted values to extend the US CPI data.
    """
    cleveland_cpi_change = fetch_and_tweak(fetch_cleveland_cpi, tweak_cleveland_cpi)
    return(cpi
            .pipe(lambda df_: bound_dates(df_, start_date=start_date, end_date=end_date))
            .fillna((cleveland_cpi_change*cpi.shift(1)).dropna()))

# WTO Import/Export commodities indexes
def fetch_wto(wto_api_key, flow, **kwargs):
    """
    Fetches the WTO Import/Export price indexes of manufactured goods.
    A WTO API key is required to access the data.
    """
    if wto_api_key is None:
        raise ValueError("WTO API key not provided. Specify wto_api_key.")

    if flow == 'import':
        series = 'ITS_MTP_MMPM'
    elif flow == 'export':
        series = 'ITS_MTP_MXPM'
    else:
        raise ValueError("Unknown flow. Specify flow = 'import' or flow = 'export'.")

    query_url = "https://api.wto.org/timeseries/v1/data?"
    params = {"i": series,
                "r": "000",
                "pc": "MA",
                "ps": f"2019-{datetime.today().strftime('%Y')}",
                "subscription-key": wto_api_key}
    response = requests.get(query_url, params=params)
    return pd.DataFrame.from_records(response.json()['Dataset'])

def tweak_wto(df, start_date='2019-01-01', end_date=None, **kwargs):
    """
    Tweaks the WTO Import/Export price indexes data.
    """
    return(df
            .assign(date=lambda df_: pd.to_datetime(df_.Year.astype(str)+df_.PeriodCode, format='%YM%m'),
                    value=lambda df_: df_.Value.astype(float))
            .loc[:, ['date', 'value']]
            .sort_values('date')
            .set_index('date')
            .pipe(lambda df_: bound_dates(df_, start_date=start_date, end_date=end_date)))

# Extend WTO Import/Export Indexes using US CPI
def adjust_wto_with_cpi(wto, cpi, end_date=None):
    if end_date is None:
        end_date = cpi.index.max().strftime('%Y-%m-%d')
    new_wto = wto.pipe(lambda df_: bound_dates(df_, end_date=end_date))
    cpi = cpi.assign(change=lambda df_: df_.value.pct_change()+1)
    for date in new_wto[new_wto.value.isna()].index:
        prev_date = date-pd.tseries.offsets.DateOffset(months=1)
        new_wto.loc[date, 'value'] = new_wto.loc[prev_date, 'value'] * cpi.loc[date, 'change']
    return new_wto

# IMF Dry Bulk/Energy Prices (via SDMX API)
def fetch_imf_prices(price_name, **kwargs):
    """
    Fetches the IMF Dry Bulk/Energy Prices data from the IMF SDMX API.
    """

    if price_name == 'commodity':
        codes_list = 'G001.PNFUEL.INDEX.M'
    elif price_name == 'energy':
        codes_list = 'G001.PNRG.INDEX.M'
    elif price_name == 'coal':
        codes_list = 'G001.PCOAL.INDEX.M'
    elif price_name == 'precious_metals':
        codes_list = 'G001.PPMETA.INDEX.M'
    else:
        raise ValueError("Unknown price name. Specify price_name = 'commodity', 'energy', 'coal' or 'precious_metals'.")

    dataset_id = "PCPS"
    start_date = 2019
    IMF_DATA = sdmx.Client('IMF_DATA')

    response = IMF_DATA.data('PCPS', key=codes_list, params={'startPeriod': start_date})
    return sdmx.to_pandas(response)


def tweak_imf_prices(df, start_date='2019-01-01', end_date=None, **kwargs):
    """

    """
    return(df
            .reset_index()
            .assign(date=lambda d: pd.to_datetime(d.TIME_PERIOD, format='%Y-M%m'))
            .sort_values('date')
            .set_index('date')
            .loc['2019-01-01':, ['value']]
            #.pipe(lambda df_: bound_dates(df_, start_date=start_date, end_date=end_date))
        )

def imf_fuel_wo_coal(fuel_idx, coal_idx):
    """
    Adjust IMF fuel price index to exclude coal.
    """
    assert (fuel_idx.index == coal_idx.index).all(), f"Indexes must have the same DateTimeIndex."
    fuel_const = 0.409
    coal_const = 0.03 
    fuel_excl_coal_idx = (fuel_idx*fuel_const - coal_idx*coal_const)/(fuel_const-coal_const)
    return fuel_excl_coal_idx

def imf_nonfuel_w_coal_wo_pmetals(nonfuel_idx, coal_idx, precious_metals_idx):
    """
    Adjust IMF fuel price index to exclude coal.
    """
    assert (nonfuel_idx.index == coal_idx.index).all(), f"Indexes must have the same DateTimeIndex."
    assert (nonfuel_idx.index == precious_metals_idx.index).all(), f"Indexes must have the same DateTimeIndex."

    nonfuel_const = 0.591
    coal_const = 0.03 
    pmetals_const = 0.116
    nonfuel_w_coal_wo_pmetals_idx = (nonfuel_idx*nonfuel_const + coal_idx*coal_const - precious_metals_idx*pmetals_const)/(nonfuel_const+coal_const-pmetals_const)
    return nonfuel_w_coal_wo_pmetals_idx

# Compile Price Indexes table for all 3 major vessel types
def compile_price_indexes(energy_index=None,
                          commodity_index=None,
                          coal_index=None,
                          precious_metals_index=None,
                          cpi=None,
                          import_wto=None,
                          export_wto=None,
                          wto_api_key=None,
                          start_date='2019-01-01', end_date=None, **kwargs):

    if energy_index is None:
        energy_index = fetch_and_tweak(fetch_imf_prices, tweak_imf_prices, price_name='energy',
                                    start_date=start_date, end_date=end_date)
    if commodity_index is None:
        commodity_index = fetch_and_tweak(fetch_imf_prices, tweak_imf_prices, price_name='commodity',
                                        start_date=start_date, end_date=end_date)
    if coal_index is None:
        coal_index = fetch_and_tweak(fetch_imf_prices, tweak_imf_prices, price_name='coal',
                                     start_date=start_date, end_date=end_date)
    if precious_metals_index is None:
        precious_metals_index = fetch_and_tweak(fetch_imf_prices, tweak_imf_prices, price_name='precious_metals',
                                        start_date=start_date, end_date=end_date)
    if cpi is None:
        cpi = fetch_and_tweak(fetch_us_cpi, tweak_us_cpi,
                            start_date=start_date, end_date=end_date)

    if end_date is None:
        end_date = min(energy_index.index.max(), commodity_index.index.max()).strftime('%Y-%m-%d')

    cpi = adjust_cpi(cpi, end_date=end_date)

    if import_wto is None:
        import_wto = fetch_and_tweak(fetch_wto, tweak_wto, wto_api_key=wto_api_key,
                                     flow='import',
                                     start_date=start_date, end_date=end_date)
    if export_wto is None:
        export_wto = fetch_and_tweak(fetch_wto, tweak_wto, wto_api_key=wto_api_key,
                                     flow='export',
                                     start_date=start_date, end_date=end_date)

    import_wto = adjust_wto_with_cpi(import_wto, cpi, end_date=end_date)
    export_wto = adjust_wto_with_cpi(export_wto, cpi, end_date=end_date)

    # Combine IMF prices 
    fuel_excl_coal = imf_fuel_wo_coal(energy_index, coal_index)
    nonfuel_coal_excl_pmetals = imf_nonfuel_w_coal_wo_pmetals(commodity_index, coal_index, precious_metals_index)

    return(pd.concat([fuel_excl_coal.rename(columns={'value':'import'}).join(fuel_excl_coal.rename(columns={'value':'export'})),
                      nonfuel_coal_excl_pmetals.rename(columns={'value':'import'}).join(nonfuel_coal_excl_pmetals.rename(columns={'value':'export'})),
                      import_wto.rename(columns={'value':'import'}).join(export_wto.rename(columns={'value':'export'}))],
                      axis=1, keys=['tanker', 'dry_bulk', 'cargo'])
            .sort_index(axis='columns'))


# From Price Indexes into prices 
def to_prices(baci_rel_prices, price_indexes, base_year=2019):
    base_year_avg = price_indexes.loc[price_indexes.index <=f'{base_year}-12-01', :].mean()
    return price_indexes.multiply((baci_rel_prices.to_numpy()/base_year_avg.to_numpy()))


# BACI
def fetch_baci_local(filepath, iso3=None):
  df =  pd.read_csv(filepath, index_col=0, header=[0,1])
  if iso3 is not None:
    df = df.loc[[iso3]]
  return df


# Nowcast Import/Export Values 
def to_value_series(portwatch, prices):
    # Value Series
    value = (portwatch
            .multiply(prices))
    value.loc[:, ('total', 'import')] = value.xs('import', axis=1, level=1).sum(axis=1)
    value.loc[:, ('total', 'export')] = value.xs('export', axis=1, level=1).sum(axis=1)
    return value

# Nowcast Import/Export Volumes 
# Nowcast Import/Export Volumes 
def to_laspeyres_price_index(portwatch, prices):
    """
    Fixed-Base Laspeyres Price Index
    Uses base period quantities (Q_0) throughout the entire series

    Parameters:
    - portwatch: DataFrame with quantity data
    - prices: DataFrame with price data
    - base_date: Date to use as base period (default: first date in index)
    """
    base = 100
    base_year = 2019

    # Get base period (2019 avg) quantities (these stay constant throughout)
    base_vol_avg = portwatch.loc[portwatch.index.year == base_year].mean()
    # Get base period (2019 avg) prices (these stay constant throughout)
    base_uv_avg = prices.loc[prices.index.year == base_year].mean()

    base_value = (
            base_uv_avg['tanker'] * base_vol_avg['tanker'] +
            base_uv_avg['dry_bulk'] * base_vol_avg['dry_bulk'] +
            base_uv_avg['cargo'] * base_vol_avg['cargo']
    )

    # Initialize result DataFrame
    chpi = pd.DataFrame(index=prices.index, columns=prices.columns.levels[-1], dtype=float)
    chpi.iloc[0] = base

    # Calculate index for each period
    for current_date in chpi.index[1:]:
        # Current period value using base quantities (P_t * Q_0)
        current_value = (
            prices.loc[current_date, 'tanker'] * base_vol_avg['tanker'] +
            prices.loc[current_date, 'dry_bulk'] * base_vol_avg['dry_bulk'] +
            prices.loc[current_date, 'cargo'] * base_vol_avg['cargo']
        )

        # Fixed-base Laspeyres formula: (P_t * Q_0) / (P_0 * Q_0) * 100
        chpi.loc[current_date, :] = (current_value / base_value) * base

    return chpi

def to_volume_weighted_series(chained_price_index, values):
    # Volumes Series
    total_value = (values
                   .loc[:, 'total'])
    return(total_value/chained_price_index)

def to_volume_unweighted_series(portwatch):
    return(pd.DataFrame({'import': portwatch.xs('import', axis=1, level=1).sum(axis=1),
                        'export': portwatch.xs('export', axis=1, level=1).sum(axis=1)},
                        index=portwatch.index))




