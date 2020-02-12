import random
import time
import unittest
from types import GeneratorType
from unittest import mock

from .core import InputSerializer, Controller
from .serializers import SearchSerializer
from .controllers import SearchController
from .crawlers import (
    RepositoriesParser,
    WikisParser,
    IssuesParser,
    SearchCrawler,
    get_parser_cls,
)


class InputSerializerTestCase(unittest.TestCase):

    def test_fail_initialize_serializer(self):

        class TestSerialize(InputSerializer):
            pass

        try:
            TestSerialize().load({})
        except Exception as err:
            self.assertIsInstance(err, NotImplementedError)
        else:
            raise AssertionError('this test should throw an error')


class SearchSerializerTestCase(unittest.TestCase):

    def test_success_initialize_search_serializer(self):
        data = {
            'keywords': ['test', 'test1'],
            'proxies': ['192.168.0.1'],
            'type': 'Repositories'
        }
        search_input = SearchSerializer.load(data)

        self.assertEqual(data['keywords'], search_input.keywords)
        self.assertEqual(data['proxies'], search_input.proxies)
        self.assertEqual(data['type'], search_input.type)

    def test_fail_initialize_search_serializer_missing_field(self):
        data = {
            'keywords': ['test', 'test1'],
            'proxies': ['192.168.0.1']
        }

        try:
            SearchSerializer.load(data)
        except Exception as err:
            self.assertIsInstance(err, TypeError)
        else:
            raise AssertionError('this test must throw an exception')

    def test_fail_initialize_search_serializer_unknown_field(self):
        data = {
            'keywords': ['test', 'test1'],
            'proxies': ['192.168.0.1'],
            'type': 'Repositories',
            'new_field': 'test'
        }

        try:
            SearchSerializer.load(data)
        except Exception as err:
            self.assertIsInstance(err, TypeError)
        else:
            raise AssertionError('this test must throw an exception')


class ControllerTestCase(unittest.TestCase):

    def test_fail_initialize_controller(self):

        class TestController(Controller):
            pass

        data = {
            'keywords': ['test', 'test1'],
            'proxies': ['192.168.0.1'],
            'type': 'Repositories'
        }
        search_input = SearchSerializer.load(data)

        try:
            TestController(search_input).run()
        except Exception as err:
            self.assertIsInstance(err, NotImplementedError)
        else:
            raise AssertionError('this test should throw an error')


class SearchControllerTestCase(unittest.TestCase):

    def test_success_initialize_search_controller(self):
        data = {
            'keywords': ['test', 'test1'],
            'proxies': ['192.168.0.1'],
            'type': 'Repositories'
        }

        controller = SearchController(input_data=data)

        self.assertEqual(controller.input_data['keywords'], data['keywords'])
        self.assertEqual(controller.input_data['proxies'], data['proxies'])
        self.assertEqual(controller.input_data['type'], data['type'])

    def test_fail_initialize_search_controller(self):
        data = {
            'keywords': ['test', 'test1'],
            'proxies': ['192.168.0.1']
        }

        try:
            SearchController(input_data=data).run()
        except Exception as err:
            self.assertIsInstance(err, TypeError)
        else:
            raise AssertionError('this test must throw an exception')

    @mock.patch('src.crawlers.SearchCrawler.process')
    def test_search_controller_process_success(self, urls):
        urls.return_value = (x for x in [{'url': 'test1'}, {'url': 'test1'}])

        data = {
            'keywords': ['test', 'test1'],
            'proxies': ['192.168.0.1'],
            'type': 'Repositories'
        }

        controller = SearchController(input_data=data)
        resp = controller.run()
        self.assertEqual(resp, [{'url': 'test1'}, {'url': 'test1'}])


class SearchParserTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.repo_input = SearchSerializer.load({
            'keywords': ["openstack", "nova", "css"],
            'proxies': ["107.190.148.202:50854", "95.85.36.236:8080"],
            'type': 'Repositories'
        })
        cls.wiki_input = SearchSerializer.load({
            'keywords': ["openstack", "nova", "css"],
            'proxies': ["107.190.148.202:50854", "95.85.36.236:8080"],
            'type': 'Wikis'
        })
        cls.issue_input = SearchSerializer.load({
            'keywords': ["openstack", "nova", "css"],
            'proxies': ["107.190.148.202:50854", "95.85.36.236:8080"],
            'type': 'Issues'
        })

    def test_repositories_parser(self):
        for word in self.repo_input.keywords:
            time.sleep(3)
            proxy = random.choice(self.repo_input.proxies)
            parser = RepositoriesParser(word, self.repo_input.type, proxy)

            result = parser.execute()
            self.assertIsInstance(result, GeneratorType)

            list_result = list(result)
            self.assertIsNot(list_result, [])
            self.assertIn('url', list_result[0])

    def test_wikis_parser(self):
        for word in self.wiki_input.keywords:
            time.sleep(3)
            proxy = random.choice(self.wiki_input.proxies)
            parser = WikisParser(word, self.wiki_input.type, proxy)

            result = parser.execute()
            self.assertIsInstance(result, GeneratorType)

            list_result = list(result)
            self.assertIsNot(list_result, [])
            self.assertIn('url', list_result[0])

    def test_issues_parser(self):
        for word in self.issue_input.keywords:
            time.sleep(3)
            proxy = random.choice(self.issue_input.proxies)
            parser = IssuesParser(word, self.issue_input.type, proxy)

            result = parser.execute()
            self.assertIsInstance(result, GeneratorType)

            list_result = list(result)
            self.assertIsNot(list_result, [])
            self.assertIn('url', list_result[0])

    def test_get_parser_cls(self):
        parser = get_parser_cls('Repositories')
        self.assertEqual(parser, RepositoriesParser)

        parser = get_parser_cls('Wikis')
        self.assertEqual(parser, WikisParser)

        parser = get_parser_cls('Issues')
        self.assertEqual(parser, IssuesParser)

        parser = get_parser_cls('smth')
        self.assertEqual(parser, RepositoriesParser)


class CrawlerTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.repo_input = SearchSerializer.load({
            'keywords': ["openstack", "nova", "css"],
            'proxies': ["107.190.148.202:50854", "95.85.36.236:8080"],
            'type': 'Repositories'
        })
        cls.wiki_input = SearchSerializer.load({
            'keywords': ["openstack", "nova", "css"],
            'proxies': ["107.190.148.202:50854", "95.85.36.236:8080"],
            'type': 'Wikis'
        })
        cls.issue_input = SearchSerializer.load({
            'keywords': ["openstack", "nova", "css"],
            'proxies': ["107.190.148.202:50854", "95.85.36.236:8080"],
            'type': 'Issues'
        })

    @mock.patch('src.core.SearchParser.execute')
    def test_repositories_parser(self, value):
        value.return_value = (x for x in [{'url': 'test'}])

        crawler = SearchCrawler(self.repo_input)
        result = crawler.process()
        self.assertIsInstance(result, GeneratorType)

        list_result = list(result)
        self.assertIsNot(list_result, [])
        self.assertIn('url', list_result[0])

    @mock.patch('src.core.SearchParser.execute')
    def test_wikis_parser(self, value):
        value.return_value = (x for x in [{'url': 'test'}])

        crawler = SearchCrawler(self.wiki_input)
        result = crawler.process()
        self.assertIsInstance(result, GeneratorType)

        list_result = list(result)
        self.assertIsNot(list_result, [])
        self.assertIn('url', list_result[0])

    @mock.patch('src.core.SearchParser.execute')
    def test_issues_parser(self, value):
        value.return_value = (x for x in [{'url': 'test'}])

        crawler = SearchCrawler(self.issue_input)
        result = crawler.process()
        self.assertIsInstance(result, GeneratorType)

        list_result = list(result)
        self.assertIsNot(list_result, [])
        self.assertIn('url', list_result[0])
