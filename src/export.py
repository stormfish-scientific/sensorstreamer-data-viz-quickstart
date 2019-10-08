from datetime import datetime
from elasticsearch import Elasticsearch
from pprint import pprint
import os
import json

import argparse


es = Elasticsearch(os.environ["DOCKER_HOST"] + ":9200")

query = '''
{
  "version": true,
  "size": 500,
  "sort": [
    {
      "@timestamp": {
        "order": "asc",
        "unmapped_type": "boolean"
      }
    }
  ],
  "_source": {
    "excludes": []
  },
  "aggs": {
    "2": {
      "date_histogram": {
        "field": "@timestamp",
        "interval": "1m",
        "time_zone": "America/New_York",
        "min_doc_count": 1
      }
    }
  },
  "stored_fields": [
    "*"
  ],
  "script_fields": {},
  "docvalue_fields": [
    {
      "field": "@timestamp",
      "format": "date_time"
    }
  ],
  "query": {
    "bool": {
      "must": [
        {
          "range": {
            "@timestamp": {
              "format": "strict_date_optional_time",
              "gte": "2019-07-01T18:46:22.398Z",
              "lte": "2019-07-01T20:25:47.884Z"
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
  },
  "highlight": {
    "pre_tags": [
      "@kibana-highlighted-field@"
    ],
    "post_tags": [
      "@/kibana-highlighted-field@"
    ],
    "fields": {
      "*": {}
    },
    "fragment_size": 2147483647
  }
}
'''

res = es.search(
    index="sensor-stream-*",
    body=query,
    scroll='1m'
)

sid = res['_scroll_id']
#scroll_size = res['hits']['total']['value']
scroll_size = len(res['hits']['hits'])
pprint({'sid': sid,
        'scroll_size': scroll_size})

print("Got %d Hits" % res['hits']['total']['value'])

print("Scroll Size: %d" % scroll_size)



counter = 0

while scroll_size > 0:
    data = []

    for hit in res['hits']['hits']:
        data.append(hit['_source'])

    with open('export-%03d.json' % counter, 'w') as f:
        f.write(json.dumps(data))

    counter += 1


    res = es.scroll(scroll_id=sid, scroll='2m')
    # Update the scroll ID
    sid = res['_scroll_id']
    # Get the number of results that we returned in the last scroll
    scroll_size = len(res['hits']['hits'])

    print("Scroll Size: %d" % scroll_size)

    # for hit in res['hits']['hits']:
    #     pprint({'gravity': hit["_source"]['gravity']['value']})

