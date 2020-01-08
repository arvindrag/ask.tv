import requests
from bs4 import BeautifulSoup
from engines import TPB, ENGINES
from putio_util import PutIO
from setup import INFO, CREDS

from multiprocessing import Process


putio = PutIO()

def e(engine, query, type=''):
    # m = engine.get_magnet(query)
    # if m is None:
    #     print "!!! no good magnet yo"
    # else:
    #     putio.add_and_await(m)
    INFO(putio.list_xfers)

for E in ENGINES:
    p = Process(target=e, args=[E, "arrow"])
    p.start()
    

# print r.text
# soup = BeautifulSoup(open(test))