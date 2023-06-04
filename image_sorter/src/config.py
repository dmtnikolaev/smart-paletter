import os


class BaseConfig:
    TESTING = False


class DevelopmentConfig(BaseConfig):
    TESTING = True


class ProductionConfig(BaseConfig):
    pass
