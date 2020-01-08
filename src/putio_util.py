import requests
from setup import INFO, CREDS
import json
import time

class PutIO:
    FETCH_WAIT_SECONDS = 30
    def __init__(pio):
        pio.API = "https://api.put.io/v2"
        pio.token = CREDS["creds"]["put_io_token"]
        INFO("token {}".format(pio.token))

    def link(pio, fileid):
        INFO("Checking mp4 for file: {}".format(fileid))
        url = "{}/files/{}/hls/media.m3u8".format(pio.API, fileid)
        response = requests.get(url, params = {'client_id':3439, 'oauth_token':pio.token})
        if response.status_code !=200:
            INFO("URL: {} Response: {}".format(url, response.json()))
        return [l for l in response.text.split('\n') if 'http' in l][0]

    def check_xfer(pio, xfer_id):
        url = "{}/transfers/{}".format(pio.API, xfer_id)
        resp = requests.get(url, params = {'client_id':3439, 'oauth_token':pio.token})
        return resp.json()

    def list_xfers(pio):
        url = "{}/transfers/list".format(pio.API)
        get = requests.get(url, params={'client_id':3439, 'oauth_token':pio.token})
        xfers = get.json()['transfers']
        return xfers

    def add(pio, magnet):
        INFO("Checking for duplicates")
        xisting_xfers = pio.list_xfers()
        # INFO(xisting_xfers)
        for xisting_xfer in xisting_xfers:
            if xisting_xfer['source'] == magnet:
                INFO("existing found, redirecting")
                return pio.check_xfer(xisting_xfer['id'])

        INFO("No dupes found, adding")
        url = "{}/transfers/add".format(pio.API)
        post = requests.post(url, data = {'url' : magnet, 'save_parent_id':0, 'client_id':3439, 'oauth_token':pio.token})
        INFO("tried to add, got back {}".format(post.json()))
        return post.json()

    def add_and_await(pio, magnet):
        INFO("Adding and awaiting magnet")
        xfer = pio.add(magnet)
        INFO(json.dumps(xfer, indent=2))
        xfer_id = xfer['transfer']['id']
        INFO("awaiting xfer")
        for i in range(pio.FETCH_WAIT_SECONDS*5):               
            speed = xfer['transfer']['down_speed']
            INFO("speed is {}".format(speed))
            xfer = pio.check_xfer(xfer_id)
            if xfer['transfer']['status'] == 'COMPLETED':
                INFO("xfer completed")
                fileid = xfer['transfer']['file_id']
                INFO("returning fileid {}".format(fileid))
                return fileid
            if xfer['transfer']['down_speed'] == 0:
                INFO("speed is abysmal.. {}".format(speed))
                return None
            time.sleep(0.2)

