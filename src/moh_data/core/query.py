from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup, SoupStrainer

CASES_URL = "our-work/diseases-and-conditions/covid-19-novel-coronavirus/covid-19-current-situation/covid-19-current-cases/covid-19-current-cases-details"


class FindExcelFile(object):

    def __init__(self):
        self._parent_url = "https://www.health.govt.nz/"
        self._cases_url = self._parent_url + CASES_URL

        url_reader = urlopen(self._cases_url)
        try:
            html = url_reader.read().decode('utf-8')
        finally:
            url_reader.close()

        self._response = requests.get(self._cases_url)
        self._soup = BeautifulSoup(self._response.content, 'html.parser', parse_only=SoupStrainer('a'))

    def fetch_file(self):
        for link in self._soup:
            if link.has_attr('href'):
                if '.xlsx' in link['href']:
                    data_file = self._parent_url + link['href']
                    return data_file
        raise FileNotFoundError("Excel file was not found on the MoH website!")
