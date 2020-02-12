import requests
from abc import ABC
from . import constants


class InputSerializer(ABC):

    @staticmethod
    def load(value):
        raise NotImplementedError('this method should be overridden')


class Controller(ABC):

    def __init__(
        self,
        input_data
    ):
        self._input_data = input_data

    def run(self):
        raise NotImplementedError('this method should be overridden')

    @property
    def input_data(self):
        return self._input_data


class SearchParser:

    def __init__(self, query, type_, proxy):
        self.query = query
        self.type_ = type_
        self.proxy = proxy

    @property
    def url(self):
        return constants.BASE_URL \
               + constants.URL_TEMPLATE.format(query=self.query, type=self.type_)

    def process_parser(self, page):
        raise NotImplementedError('this method should be overridden')

    def execute(self):
        html_page = self._get_search_page()
        yield from self.process_parser(html_page)

    def _get_search_page(self):
        proxies = {
            'http': f'http://{self.proxy}'
        }

        resp = requests.get(self.url, proxies=proxies)

        if resp.status_code != 200:
            raise Exception(f'Request response equal to {resp.status_code}')

        return resp.content


class Crawler(ABC):

    def __init__(self, input_):
        self.input_ = input_

    def process(self):
        raise NotImplementedError('this method should be overridden')
