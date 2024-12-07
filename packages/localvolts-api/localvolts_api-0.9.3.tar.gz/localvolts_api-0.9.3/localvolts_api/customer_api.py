import requests
import pickle
import json
from datetime import datetime, timedelta
from dateutil import tz
from pydantic import BaseModel
import pandas as pd


class IntervalData(BaseModel):
    NMI: str  # National Meter Identifier for which data is being provided. All data is that obtained at the NMI location. NMI will be a 10 character id, without checksum.
    battery: str  # ‘A’ or ’U’ A: battery is operational and available U: battery is unavailable
    control: str  # ‘E’ or ‘A’ E: Battery control is enabled but not activated A: Battery is being controlled externally
    intervalDuration: int  # Duration of the interval in minutes. Default is 5 minutes
    intervalDurationUnits: str  # ‘minutes’
    intervalEnd: str  # Time at the end of the NEM interval, in UTC (24-hour format). Note that the NEM always runs off AEST (UTC+10)
    importsMainLoad: float  # energy drawn from the grid on the main circuit
    importsMainLoadUnits: str  # ‘Wh’
    importsControlledLoad: float  # energy drawn from the grid on the controlled load circuit
    exports: float  # energy injected into the grid
    exportsUnits: str  # ‘Wh’
    batteryCharging: float  # power being drawn by the battery
    batteryChargingUnits: str  # ‘kW’
    batteryDischarging: float  # power being discharged by the battery
    batteryDischargingUnits: str  # ‘kW’
    batteryEnergy: float  # useable energy stored in the battery
    batteryEnergyUnits: str  # ‘kWh’
    batterySOC: float  # useable energy stored in the battery as % of total capacity
    batterySOCUnits: str  # ‘%’
    lastUpdate: str  # date/time this data-set was updated, in UTC (YYYY-MM- DDTHH:mm:ssZ)

class CustomerIntervalData:
    def __init__(self, json_data):
        self.data = json_data

    def __getattr__(self, item):
        return self.data.get(item, None)

class CustomerAPI:
    BASE_URL = "https://api.localvolts.com/v1"

    def __init__(self, auth):
        """
        Initialize the CustomerAPI with authentication details.

        :param auth: LocalvoltsAuth - An instance of the LocalvoltsAuth class for API authentication.
        """
        self.auth = auth

    def get_interval_data(self, nmi='*', from_time=None, to_time=None, time_zone='Australia/Brisbane', keep_log=False):
        """
        Fetches interval data for a given NMI and time range.

        :param nmi: str - The NMI to query. Use '*' for all NMIs.
        :param from_time: str - The start time in ISO 8601 UTC format.
        :param to_time: str - The end time in ISO 8601 UTC format.
        :return: CustomerIntervalData - Custom object containing the response data.
        """
        if len(nmi) > 10:
            nmi = nmi[0:10]
        params = {'NMI': nmi}
        if from_time:
            if isinstance(from_time, datetime):
                # Change to UTC
                from_time = from_time.astimezone(tz.UTC)
                params['from'] = from_time.strftime('%Y-%m-%dT%H:%M:00Z')
            else:
                params['from'] = from_time
        else:
            # Max is 3 days ago
            _tz = tz.gettz(time_zone)
            from_time = (datetime.now().astimezone().replace(hour=0, minute=0, second=0, microsecond=0).astimezone(_tz) - timedelta(days=2))
            from_time = from_time.astimezone(tz.UTC)
            days_ago = datetime.now().day - from_time.day
            if days_ago > 2:
                from_time = from_time + timedelta(days=(days_ago-2))
            params['from'] = from_time.strftime('%Y-%m-%dT%H:%M:00Z')

        if to_time:
            if isinstance(to_time, datetime):
                to_time = to_time.astimezone(tz.UTC)
                params['to'] = to_time.strftime('%Y-%m-%dT%H:%M:00Z')
            else:
                params['to'] = to_time

        response = requests.get(f"{self.BASE_URL}/customer/interval", headers=self.auth.get_headers(), params=params)
        if response.status_code != 200:
            reason = response.content.decode('utf-8')
            raise requests.HTTPError(f"{response.status_code} {response.reason}: {reason}")
        response_json = response.json()
        if keep_log:
            time_stamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S.%f')
            with open(f'/tmp/{time_stamp}_localvolts_response.pickle', 'wb') as f:
                f.write(pickle.dumps({'response': response, 'response_json': response_json}))
                print('response saved to /tmp')
        return CustomerIntervalData(response_json)

    def set_interval_data(self, nmi, interval_data: IntervalData):
        """
        Sets interval data for a given NMI.

        :param nmi: str - The NMI to update.
        :param interval_data: dict - The interval data to set.
        :return: dict - The response data.
        """
        url = f"{self.BASE_URL}/customer/interval?NMI={nmi}"
        print('posting to ', url)
        print('body', json.dumps(interval_data.dict()))
        response = requests.post(url, headers=self.auth.get_headers(), json=interval_data.dict())
        if response.status_code != 200:
            reason = response.content.decode('utf-8')
            raise requests.HTTPError(f"{response.status_code} {response.reason}: {reason}")
        return response.json()

    def get_interval_data_df(self, nmi='*', from_time=None, to_time=None, time_zone='Australia/Brisbane', keep_log=False):
        """
        Fetches interval data for a given NMI and time range and returns it as a pandas DataFrame.

        :param nmi: str - The NMI to query. Use '*' for all NMIs.
        :param from_time: str - The start time in ISO 8601 UTC format.
        :param to_time: str - The end time in ISO 8601 UTC format.
        :return: pandas.DataFrame - The response data as a DataFrame.
        """
        data = self.get_interval_data(nmi, from_time, to_time, keep_log=keep_log).data
        df = pd.DataFrame(data)
        if df.empty:
            return df
        df['interval_time'] = pd.to_datetime(df['intervalEnd']).dt.tz_convert(time_zone)
        df.set_index('interval_time', inplace=True)
        return df
