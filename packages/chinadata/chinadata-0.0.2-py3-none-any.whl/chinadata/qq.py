import requests
import pandas as pd
import time


def get_query_data(token,api_name,fields='',**kwargs):
    """
    Fetch stock data from a given URL with specified parameters.

    Parameters:

    ts_code (str): The stock code to fetch data for.
    start_date (str): The start date for fetching data (in 'YYYY-MM-DD HH:MM:SS' format).
    end_date (str): The end date for fetching data (in 'YYYY-MM-DD HH:MM:SS' format).
    freq (str): The frequency of the data (e.g., '1min', '5min'，'15min', '30min'， '60min').
    token (str): The access token for the data source. Default is provided.
    offset (str, 可选): 数据偏移量，用于分页获取数据，默认为'0'。当需要获取更多数据时，可以增大此值。
    freq (str, 可选): 数据频率，指定返回数据的时间间隔，例如'1min'（1分钟）、'5min'（5分钟）、'15min'（15分钟）、
                      '30min'（30分钟）、'60min'（60分钟，即1小时）等。默认为'60min'。

    Returns:
    pd.DataFrame: A DataFrame containing the fetched stock data.
    """
    # url="http://127.0.0.1:9002/tq"
    url = "http://152.136.171.135:9002/tq"

    params = {
        'token':token,
        'api_name': api_name,
        'params': kwargs,
        'fields': fields,
    }



    response = requests.post(url, json=params)



    if response.status_code == 200:
        try:
            data = response.json()
            # print(data)
            if data == 'token无效或已超期,请重新购买':
                return data
            else:
                df = pd.DataFrame(data)
                return df
        except ValueError as e:
            print("Error parsing JSON response:", e)
            return None
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        print(response.text)
        return None


# 示例调用


