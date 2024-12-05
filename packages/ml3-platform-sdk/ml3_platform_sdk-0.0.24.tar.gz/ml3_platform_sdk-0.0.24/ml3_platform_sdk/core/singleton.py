import logging

logger = logging.getLogger("ML3_PLATFORM_SDK")
logging.basicConfig(level=logging.INFO)


def client_singleton(cls):
    """
    Allow to declare singleton classes
    """
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        elif len(kwargs) != 0:
            logger.warning("***CLIENT REINIZIALIZATION DETECTED***")
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance
