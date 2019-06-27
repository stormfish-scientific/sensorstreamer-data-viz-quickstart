from datetime import datetime
from elasticsearch import Elasticsearch
from pprint import pprint
import math
import time
import signal

import os

import argparse


es = Elasticsearch(os.environ["DOCKER_HOST"] + ":9200")

query_template = """
{
    "version": true,
    "size": 500,
    "sort": [
        {
            "@timestamp": "asc"
        }
    ],
    "docvalue_fields": [
        {
            "field": "@timestamp",
            "format": "date_time"
        }
    ],
    "query": {
        ${QUERY}
    }
    ${EXTRA}
}
"""

basic_query = """
"bool": {
    "must": [
        {
            "range": {
                "@timestamp": {
                    "format": "strict_date_optional_time",
                    "gte": "now-1m",
                    "lte": "now"
                }
            }
        }
    ],
    "filter": [
        {
            "match_all": {}
        }
    ],
    "should": [],
    "must_not": []
}
"""


def prepare_query(query=None, extra=None):
    global query_template
    global basic_query

    if query is None:
        query = basic_query

    if extra is None:
        extra = ''

    if extra != '':
        extra = ",\n" + extra

    res = query_template.replace("${QUERY}", query)

    res = res.replace("${EXTRA}", extra)

    return res


q = prepare_query()

res = es.search(
    index="sensor-stream-*",
    body=q
)


def magnitude(vec):
    return math.sqrt(
        math.pow(vec[0], 2.0) +
        math.pow(vec[1], 2.0) +
        math.pow(vec[2], 2.0)
    )


def normalize(vec, mag=None):
    if mag is None:
        mag = magnitude(vec)

    return [vec[0]/mag, vec[1]/mag, vec[2]/mag]


keep_running = True

search_after_val = None

while keep_running:

    try:

        found = False

        # print("Got %d Hits:" % res['hits']['total']['value'])

        # pprint(len(res['hits']['hits']))

        #pprint(res['hits']['hits'])
        for hit in res['hits']['hits']:

            search_after_val = hit['sort'][0]
            found = True

            if 'value' in hit['_source']['gravity']:
                vec = hit["_source"]['gravity']['value']
                mag = magnitude(vec)
                norm = normalize(vec, mag)
                #print(hit['_source']['@timestamp'] + str(vec))

                timestamp = search_after_val / 1000.0
                print("%0.3f - %s" % (timestamp, str(vec)))

                # pprint({'gravity': vec,
                #         'magnitude': mag,
                #         'norm': norm})

        if found:
            print('-')
                

        #pprint({'search_after_val': search_after_val})

        if search_after_val is not None:
            q = prepare_query(
                None,
                '"search_after": [' + str(search_after_val) + "]"
            )

            # print("---")
            # print(q)
            # print("---")

        res = es.search(
            index="sensor-stream-*",
            body=q
        )

        # Do a little sleep
        time.sleep(.25)

    except KeyboardInterrupt:
        keep_running = False

    except Exception as ex:
        keep_running = False
        raise ex
