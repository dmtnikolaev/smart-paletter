import os


class BaseConfig:
    TESTING = False

    IMAGE_STORE_URL = 'http://smart-paletter-image-store-1:5000/'
    IMAGE_SORTER_URL = 'http://smart-paletter-image-sorter-1:5000/'


class DevelopmentConfig(BaseConfig):
    TESTING = True


class ProductionConfig(BaseConfig):
    pass
