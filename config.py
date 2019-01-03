import re

from elasticsearch import Elasticsearch


class Config:
    PRODUCTION = False
    INDEX = "es-english-docs"
    DOC_TYPE = "doc"


class TestingConfig(Config):
    DEBUG = True
    ES_ENDPOINT = "http://localhost:9200"
    CLIENT = Elasticsearch(ES_ENDPOINT, ca_serts=False, verify_certs=False)


class ProductionConfig(Config):
    PRODUCTION = True
    ES_ENDPOINT = "https://ih1t24sgu0:knjk6hjbqp@sentiment-analysis-2068917443.ap-southeast-2.bonsaisearch.net"
    INDEX = "events-documents"
    AUTH = re.search('https\:\/\/(.*)\@', ES_ENDPOINT).group(1).split(':')
    HOST = ES_ENDPOINT.replace('https://%s:%s@' % (AUTH[0], AUTH[1]), '')
    ES_HEADERS = [{"host": HOST, "port": 443, "use_ssl": True, "http_auth": (AUTH[0], AUTH[1])}]
    CLIENT = Elasticsearch(ES_HEADERS)


"""
Elastic search sanity checks
to see all records: http://localhost:9200/es_docs/_search?pretty=true&q=*:*
https://ed57da9fe8014345b211254168c3de92.europe-west1.gcp.cloud.es.io:9243/_search?pretty=true&q=*:*
"""
