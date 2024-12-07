import json
import logging
import time

import requests as r
from pandas import json_normalize

from ...utils.utility import MOSException, validate_date
from ...utils.request_utility import get, post


class UserDataPoint:
    """
        Upload and fetch user defined datapoints.
    """

    def __init__(self, base_url, headers, ssl_verify):
        self.logger = logging.getLogger(__name__)
        self.base_url = base_url
        self.headers = headers
        self.ssl_verify = ssl_verify

    def get_available_datapoints(self) -> list:
        """
        List datapoints available to be used within the strategy nodes.
        """
        resp_obj = get(url=self.base_url + "datapoints", headers=self.headers, ssl_verify=self.ssl_verify)
        if resp_obj.status_code == 200:
            resp = resp_obj.json()
        else:
            self.logger.error(f"Error in get available datapoint : {resp_obj.text}")
            raise MOSException(f"Error in get available datapoint : {resp_obj.text}")

        return resp

    def upload_userdata(self, date, dp, dp_type, asset_id_type, data_dict):
        """
        Update/write user data datapoint.

        Args:
            date (str) :  Date for which data is to be uploaded.
            dp (str) : Datapoint to be uploaded. Datapoint must start with 'userdata.' Eg: userdata.my_datapoint_name.
            dp_type (str) : Type of datapoint.
            asset_id_type (str) : Type of asset ID.
            data_dict (dict) : Dictionary of datapoint values.
                        eg: {
                            "x": 1000000,
                            "y": 2000000,
                            "z": 3000000
                            }

        """

        ## Validate if dp already registered

        resp_obj = get(url=self.base_url + "userdata/registration", headers=self.headers, ssl_verify=self.ssl_verify)
        if resp_obj.status_code != 200:
            self.logger.error(f"Error in fetching registered user datapoint : {resp_obj.text}")
            raise MOSException(f"Error in fetching registered user datapoint : {resp_obj.text}")

        if not eval(resp_obj.text):
            self.logger.info(f"No data fetched for existing registered datapoints.")
            self.__register_dp(dp, dp_type)
            self.__upload_dp(dp, asset_id_type, data_dict, date)

        else:
            registered_dp = json_normalize(json.loads(resp_obj.text))

            if dp in registered_dp['datapointName'].to_list():
                if registered_dp[registered_dp['datapointName'] == dp]['dataType'].item() == dp_type:
                    self.logger.info(
                        f"User datapoint {dp} with datatype {dp_type} is already registered. Skipping registration and uploading datapoint.")
                    self.__upload_dp(dp, asset_id_type, data_dict, date)
                else:
                    self.logger.error(
                        f"User datapoint {dp} is already registered with datatype {dp_type}. Cannot upload same datapoint with different datatype.")
                    raise MOSException(
                        f"Error in user datapoint registration. Cannot register datapoint with different datatype. Kindly provide new datapoint name.")

            else:
                self.__register_dp(dp, dp_type)
                self.__upload_dp(dp, asset_id_type, data_dict, date)

    def __register_dp(self, dp, dp_type):
        """
        Register the new datapoint
        """
        data = {
            "datapointName": dp,
            "dataType": dp_type
        }

        resp_obj = post(url=self.base_url + "userdata/registration", headers=self.headers, data=data, ssl_verify=self.ssl_verify)
        if resp_obj.status_code == 200:
            self.logger.info(f"User datapoint {dp} registered successfully.")
        else:
            self.logger.error(f"Error in user datapoint registration : {resp_obj.text}")
            raise MOSException(f"Error in user datapoint registration : {resp_obj.text}")

    def __upload_dp(self, dp, asset_id_type, data_dict, date):
        """
        Uploading new datapoint
        """

        dp_dict = {
            "idType": asset_id_type,
            "data": data_dict
        }
        resource = f"userdata/data/{dp}/date/{date}"

        resp_obj = post(url=self.base_url+resource, headers=self.headers, data=dp_dict, ssl_verify=self.ssl_verify)
        if resp_obj.status_code == 200:
            self.logger.info(f"User datapoint {dp} added successfully for date {date}.")
        else:
            self.logger.error(f"Error in user datapoint addition : {resp_obj.text}")
            raise MOSException(f"Error in user datapoint addition : {resp_obj.text}")

    def get_user_datapoints(self) -> list:
        """
        List datapoints previously uploaded.

        """
        resource = "userdata/data"
        resp_obj = get(self.base_url+resource, headers=self.headers, ssl_verify=self.ssl_verify)
        return resp_obj.json()

    def get_user_datapoint_dates(self, dp) -> list:
        """
        List uploaded dates for given datapoint.

        Args:
             dp (str) : Datapoint to retrieve.

        """
        resource = f"userdata/data/{dp}/date"
        resp_obj = get(self.base_url+resource, headers=self.headers, ssl_verify=self.ssl_verify)
        return resp_obj.json()

    def get_user_datapoint_details(self, dp, date) -> dict:
        """
        Read back the data uploaded for datapoint on the given date.

        Args:
             dp (str) : Datapoint to retrieve.
             date (str) :  Date to retrieve.
        """
        validate_date(date)
        resource = f"userdata/data/{dp}/date/{date}"
        resp_obj = get(self.base_url+resource, headers=self.headers, ssl_verify=self.ssl_verify)
        return resp_obj.json()

