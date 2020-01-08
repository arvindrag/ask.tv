import requests
from setup import INFO
import re
from bs4 import BeautifulSoup as Soup


class Engine:
    def __init__(e, name, create_query):
        e.name = name
        e.create_query = create_query 

    def get_search_url(e, query):
        INFO("original query: {}".format(query))
        # lower case the query
        query = query.lower()
        # replace spaces
        query = '%20'.join(query.split(' '))
        # join together
        search_url = e.create_query(query)
        INFO("parsed search_url is {}".format(search_url))
        return search_url

    def get_magnet(e, query):
        search_url = e.get_search_url(query)
        INFO("requesting from {}".format(e.name))
        response = requests.get(search_url)
        if response.status_code != 200:
            INFO("an error {} occured with {} request".format(response.status_code, search_url))
            return None
        else:
            INFO("request {} succeeded".format(search_url))
            soup = Soup(response.text, features="html.parser")
            magnet = soup.find(href = re.compile('magnet'))
            if magnet is None:
                INFO("No result found in {}".format(e.name))
            magnet_link = ['href']
            INFO("returning magnet {}".format(magnet_link))
            return magnet_link

TPB = Engine(
    "TPB",
    lambda q: "https://thepiratebay.org/search/{}/0/7/0".format(q)
    )
KICKASS = Engine(
    "KICKASS",
    lambda q: "https://katcr.co/usearch/torrents-search.php?q={}".format(q)
    )
EZTV = Engine(
    "EZTV",
    lambda q: "https://eztv.ag/search/{}".format(q)
    )
L337 = Engine(
    "L337",
    lambda q: "https://1337x.to/search/{}/1/".format('+'.join(q.split('%20')))
    ) 

ENGINES = [
    TPB,
    EZTV,
    L337
]