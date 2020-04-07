import redis
import json
import requests
from bs4 import BeautifulSoup, SoupStrainer

redis = redis.Redis(host="localhost", port=6379)
CASES_URL = "our-work/diseases-and-conditions/covid-19-novel-coronavirus/covid-19-current-situation/covid-19-current-cases/covid-19-current-cases-details"


class FindExcelFile(object):

    def __init__(self):
        self._parent_url = "https://www.health.govt.nz/"
        self._cases_url = self._parent_url + CASES_URL

        self._response = requests.get(self._cases_url)
        self._soup = BeautifulSoup(self._response.content, 'html.parser', parse_only=SoupStrainer('a'))

        self._data_file = None

        json.dumps({
            "cached": False,
       })

        redis.setex(self._cases_url, 60, str())

    def _fetch_file(self):
        for link in self._soup:
            if link.has_attr('href'):
                if '.xlsx' in link['href']:
                    self._data_file = self._parent_url + link['href']
                    return self._data_file
        raise FileNotFoundError("Excel file was not found on the MoH website!")

    def fetch(self):
        result = redis.get(self._cases_url)

        if not result:
            return self._fetch_file()
        else:
            return result
