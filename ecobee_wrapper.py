import requests
import urllib.parse
import logging
import os

class EccobeeWrapper:
    
    def __init__(self, hostname: str, ver: str = '1'):

        self.url = "https://{}/{}/".format(hostname, ver)
        self._fetchAccesToken()

    def _fetchAccesToken(self):
        
        data = {
        'grant_type': 'refresh_token',
        'code': os.environ['REFRESH_TOKEN'],
        'client_id': os.environ['API_KEY'],
        }

        try:
            response = requests.post(url="https://api.ecobee.com/token", data = data)
        except requests.exceptions.RequestException as e:
            logging.error(e)

        self.access_token = response.json().get('access_token')
    
    def _doRequest(self, http_method: str, endpoint: str, ep_params: dict = None, data: str = None):
        
        full_url = self.url + endpoint
        headers = {'Content-Type': 'application/json;charset=UTF-8', 'Authorization': 'Bearer ' + self.access_token}
        # ecobee API asks that JSON data be URL encoded for optimal comptability
        if ep_params and 'body' in ep_params:
            ep_params['body'] = urllib.parse.quote_plus(ep_params['body'])
        if data:
            data = urllib.parse.quote_plus(data)

        try:
            response = requests.request(method=http_method, url=full_url, headers=headers, params=ep_params, data=data)
        except requests.exceptions.RequestException as e:
            logging.error(e)

        if 299 >= response.status_code >= 200:
            return response.json()
        else:
            logging.error(f"Non-200 response code when trying request: {response.status_code}")

    def get(self, endpoint: str, ep_params: dict = None) -> list[dict]:

        return self._doRequest(http_method='GET', endpoint=endpoint, ep_params=ep_params)
    
    def post(self, endpoint: str, ep_params: dict = None, data: str = None):

        return self._doRequest(http_method='POST', endpoint=endpoint, ep_params=ep_params, data=data)