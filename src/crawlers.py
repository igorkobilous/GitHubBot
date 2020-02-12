import random
import time
from bs4 import BeautifulSoup

from .core import SearchParser, Crawler
from . import constants


class RepositoriesParser(SearchParser):

    def process_parser(self, page):
        soup = BeautifulSoup(page, 'html.parser')

        search_result = soup.find('ul', {'class': 'repo-list'})
        for item in search_result.find_all('li', {'class': 'repo-list-item'}):
            link = item.find('a', {'class': 'v-align-middle'})
            link_href = link['href']
            repo_owner = link_href.split('/')[1]
            language = [x for x in item.find_all('span') if x.has_attr('itemprop')]

            yield {
                'url': f'{constants.BASE_URL}{link_href}',
                'extra': {
                    'owner': repo_owner,
                    'language': language[0].text if language else ''
                }
            }


class WikisParser(SearchParser):

    def process_parser(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        search_result = soup.find('div', {'id': 'wiki_search_results'})
        for item in search_result.find_all('a'):
            if item.has_attr('data-hydro-click'):
                yield {
                    'url': f'{constants.BASE_URL}{item["href"]}'
                }


class IssuesParser(SearchParser):

    def process_parser(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        search_result = soup.find('div', {'id': 'issue_search_results'})
        for item in search_result.find_all('a'):
            if item.has_attr('data-hydro-click'):
                yield {
                    'url': f'{constants.BASE_URL}{item["href"]}'
                }


PARSER_MAP = {
    'Repositories': RepositoriesParser,
    'Wikis': WikisParser,
    'Issues': IssuesParser,
}


def get_parser_cls(input_type):
    return PARSER_MAP.get(input_type, RepositoriesParser)


class SearchCrawler(Crawler):

    def process(self):
        for word in self.input_.keywords:
            time.sleep(constants.SECS_TO_SLEEP)
            proxy = random.choice(self.input_.proxies)
            parser = get_parser_cls(self.input_.type)(word, self.input_.type, proxy)
            yield from parser.execute()
