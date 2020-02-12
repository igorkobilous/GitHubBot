from .core import Controller
from .crawlers import SearchCrawler
from .serializers import SearchSerializer


class SearchController(Controller):

    def run(self):
        input_ = SearchSerializer.load(self.input_data)
        crawler = SearchCrawler(input_)
        return [
            x for x in crawler.process()
        ]
