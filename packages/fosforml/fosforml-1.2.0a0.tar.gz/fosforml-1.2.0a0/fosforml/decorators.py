# -*- coding: utf-8 -*-
import inspect


class scoring_func(object):
    """decorator for defining user defined scoring function"""

    def __init__(self, user_func):
        # make sure it is a function
        if not inspect.isfunction(user_func):
            raise TypeError("Argument to scoring_func decorator must be a function")
        # make sure it accepts two parameters
        if user_func.__code__.co_argcount != 2:
            raise TypeError("User defined scoring function should accept two arguments")
        self._user_func = user_func

    def __call__(self, *args, **kwargs):
        return self._user_func(*args, **kwargs)