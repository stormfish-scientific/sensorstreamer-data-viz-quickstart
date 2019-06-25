from datetime import datetime
from elasticsearch import Elasticsearch
from pprint import pprint
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

print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
    pprint({'gravity': hit["_source"]['gravity']['value']})
