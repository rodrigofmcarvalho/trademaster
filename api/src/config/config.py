class BaseConfig:

    SEND_SALE_PATH = "/sale"
    V_API = "v1"
    TESTING = False
    DEBUG = False


class DevConfig(BaseConfig):

    DEBUG = True