import logging
import requests
import sys

from cmpparis.parameters_utils import get_parameter

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class QuableAPI:
    BASE_URL = get_parameter("mit", "quabled_api_v5_base_url")
    API_KEY = get_parameter("mit", "quable_token")

    def __init__(self, base_url=None, api_key=None):
        self.base_url = base_url if base_url else self.BASE_URL
        self.headers = {
            'Authorization': f'Bearer {api_key if api_key else self.API_KEY}',
            'Content-Type': 'application/json'
        }

    def get(self, endpoint, params=None):
        url = f'{self.base_url}/{endpoint}'

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            logger.info(f"Error while making GET request to Quable API : {err}")
        except requests.exceptions.RequestException as err:
            logger.info(f"Error while making GET request to Quable API : {err}")
        except Exception as err:
            logger.info(f"Error while making GET request to Quable API : {err}")

    def post(self, endpoint, data):
        url = f'{self.base_url}/{endpoint}'

        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            logger.info(f"Error while making POST request to Quable API : {err}")
        except requests.exceptions.RequestException as err:
            logger.info(f"Error while making POST request to Quable API : {err}")
        except Exception as err:
            logger.info(f"Error while making POST request to Quable API : {err}")