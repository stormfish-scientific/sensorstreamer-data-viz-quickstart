from datetime import datetime
from elasticsearch import Elasticsearch
from pprint import pprint
import math

import os

import argparse


es = Elasticsearch(os.environ["DOCKER_HOST"] + ":9200")

res = es.search(
    index="sensor-stream-*",
    body="""
{
  "version": true,
  "size": 500,
  "sort": [
    {
      "@timestamp": {
        "order": "desc",
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
        "interval": "30s",
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
              "gte": "2019-06-25T18:23:57.641Z",
              "lte": "2019-06-25T18:38:57.641Z"
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
"""
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


print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
    vec = hit["_source"]['gravity']['value']
    mag = magnitude(vec)
    norm = normalize(vec, mag)
    pprint({'gravity': vec,
            'magnitude': mag,
            'norm': norm})
