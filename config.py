class Config:
    PRODUCTION = False
    INDEX = "es_english_docs"
    DOC_TYPE = "doc"


class TestingConfig(Config):
    DEBUG = True
    ES_ENDPOINT = "http://localhost:9200"


class ProductionConfig(Config):
    PRODUCTION = True
    ES_ENDPOINT = "https://cb3651b9fca744f882cd483693bd3ec5.europe-west1.gcp.cloud.es.io:9243/"


"""
Elastic search sanity checks
to see all records: http://localhost:9200/es_docs/_search?pretty=true&q=*:*
https://ed57da9fe8014345b211254168c3de92.europe-west1.gcp.cloud.es.io:9243/_search?pretty=true&q=*:*
"""
