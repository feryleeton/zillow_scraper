import urllib.parse
import json
import requests
from zillow_scraper import config


class ZillowScraper:
    def __init__(self):
        pass

    @staticmethod
    def get_pages_count(params):
        with requests.Session() as s:
            s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) ' \
                                      'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                                      'Chrome/88.0.4324.150 Safari/537.36'
            data = json.loads(s.get(f"{config.LINK}{urllib.parse.urlencode(params)}").content)

        pages_count = data["cat1"]["searchList"]["totalPages"]
        return pages_count

    @staticmethod
    def parse_page(page_num, params):
        print('Page: ', page_num, '\n\n')
        params['searchQueryState']['pagination']['currentPage'] = page_num

        with requests.Session() as s:
            s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) ' \
                                      'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                                      'Chrome/88.0.4324.150 Safari/537.36'
            data = json.loads(s.get(f"{config.LINK}{urllib.parse.urlencode(config.PARAMS)}").content)
        search_results = data["cat1"]["searchResults"]["listResults"]
        for result in search_results:
            print('detailUrl: ', result['detailUrl'])
            print('Address: ', result['address'])
            print('Price: ', result['price'])
            print('ImgSrc: ', result['imgSrc'])
            print('\n\n')

    def parse_search(self, params):
        pages_count = self.get_pages_count(params)

        for page in range(pages_count + 1)[1:]:
            self.parse_page(page, params)

    @staticmethod
    def parse_search_link(link):
        res = urllib.parse.parse_qs(link)
        parsed_params = json.loads(list(res.values())[0][0])

        print(parsed_params)

        west = parsed_params['mapBounds']['west']
        east = parsed_params['mapBounds']['east']
        south = parsed_params['mapBounds']['south']
        north = parsed_params['mapBounds']['north']

        return west, east, south, north

    def proceed_search_link(self, link):

        west, east, south, north = self.parse_search_link(link)

        params = config.PARAMS

        params['searchQueryState']['mapBounds']['west'] = west
        params['searchQueryState']['mapBounds']['east'] = east
        params['searchQueryState']['mapBounds']['south'] = south
        params['searchQueryState']['mapBounds']['north'] = north

        self.parse_search(params)

