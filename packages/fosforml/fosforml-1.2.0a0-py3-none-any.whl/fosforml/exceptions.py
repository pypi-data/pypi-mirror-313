# -*- coding: utf-8 -*-


class ConfigError(Exception):
    pass


class MosaicException(Exception):
    """Mosaic ai common exception"""

    code = 500
    message = "Something went wrong"


class InvalidModelIDException(MosaicException):
    """Mosaic ai authentication error"""

    code = 500
    message = "The Model ID provided is invalid. Kindly provide a valid Model ID !"
