import json
import re
import urllib

from flask import make_response
from json import JSONEncoder
from app import cache
from contextlib import closing


class EpisodeNotFoundException(Exception):
    pass


class SimpleEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def json_response(data, status=200):
    response = make_response(json.dumps(data, cls=SimpleEncoder), status)
    response.mimetype = 'application/json'
    return response


@cache.memoize(60 * 60 * 24 * 7)
def parse_epguides_data(url):
    with closing(urllib.urlopen("http://epguides.com/" + url)) as x:
        episodes = re.findall("([\d]*)\s*([\d]*)-([\d]*)\s*[\w\-]*"
                              "\s*([0-9][0-9]\/\w*\/[0-9][0-9])[\s"
                              "&\-#<\w='.;:\/]*>([\w\s]*)", x.read())

    return episodes
