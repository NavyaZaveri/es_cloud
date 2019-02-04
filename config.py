import os
import re

from elasticsearch import Elasticsearch


class Config:
    PRODUCTION = False
    INDEX = "es-testing1-docs"


class TestingConfig(Config):
    DEBUG = True
    ES_ENDPOINT = "http://localhost:9200"
    CLIENT = Elasticsearch(ES_ENDPOINT, ca_serts=False, verify_certs=False)


class ProductionConfig(Config):
    PRODUCTION = True
    ES_ENDPOINT = os.environ["ES_ENDPOINT"]
    INDEX = "events-production-analysis"
    AUTH = re.search('https\:\/\/(.*)\@', ES_ENDPOINT).group(1).split(':')
    HOST = ES_ENDPOINT.replace('https://%s:%s@' % (AUTH[0], AUTH[1]), '')
    ES_HEADERS = [{"host": HOST, "port": 443, "use_ssl": True, "http_auth": (AUTH[0], AUTH[1])}]
    CLIENT = Elasticsearch(ES_HEADERS)
