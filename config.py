class Config:
    PRODUCTION = False
    INDEX = "es_docs"
    DOC_TYPE = "doc"


class TestingConfig(Config):
    DEBUG = True
    ES_ENDPOINT = "http://localhost:9200"


class ProductionConfig(Config):
    PRODUCTION = True
    ES_PASSWORD = "AEwCdtyr8tuBO2452YUdi3hZ"
    ES_USERNAME = "elastic"
    ES_ENDPOINT = "https://ed57da9fe8014345b211254168c3de92.europe-west1.gcp.cloud.es.io:9243/"
