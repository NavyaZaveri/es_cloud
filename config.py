class Config:
    pass


class TestingConfig(Config):
    DEBUG = True
    ENDPOINT = "https://localhost:9200"


class ProductionConfig(Config):
    ES_PASSWORD = "AEwCdtyr8tuBO2452YUdi3hZ"
    ES_USERNAME = "elastic"
    ENDPOINT = "https://ed57da9fe8014345b211254168c3de92.europe-west1.gcp.cloud.es.io:9243/"
