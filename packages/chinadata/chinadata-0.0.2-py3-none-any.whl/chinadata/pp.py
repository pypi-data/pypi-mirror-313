
import time
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)#消除告警

import requests
import pandas as pd

def get_bar_data(token,ts_code='', api=None, start_date='', end_date='', freq='D', asset='E',
           exchange='',
           adj = None,
           ma = [],
           factors = None,
           adjfactor = False,
           offset = None,
           limit = None,
           fields = '',
           contract_type = ''):
    """

    """
    # url = "http://127.0.0.1:9002/tp"
    url = "http://152.136.171.135:9002/tp"
    params = {
        'token':token,
        'ts_code':ts_code,
        'api':api,
        'start_date':start_date,
        'end_date':end_date,
        'freq':freq,
        'asset':asset,
        'exchange':exchange,
        'adj' :adj,
        'ma' :ma,
        "factors" : factors,
        "adjfactor" : adjfactor,
        "offset" : offset,
        "limit" :limit,
        "fields" : fields,
        "contract_type" : contract_type
    }

    response = requests.post(url, json=params,)

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





