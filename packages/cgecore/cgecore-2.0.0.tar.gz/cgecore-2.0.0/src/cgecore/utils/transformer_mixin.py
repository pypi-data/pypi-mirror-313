#!/usr/bin/env python3

from collections import UserDict


class TransformerMixin():

    @staticmethod
    def userdict_to_dict(userdict):
        """
            Input: dict or UserDict object.
            Output: same as input, but all UserDict objects (also the ones
                    stored inside other UserDict or dict objects) have been
                    converted to dict objects.
        """
        builtin_dict = dict()
        for key, val in userdict.items():
            if(isinstance(val, UserDict) or isinstance(val, dict)):
                builtin_dict[key] = TransformerMixin.userdict_to_dict(val)
            else:
                builtin_dict[key] = val
        return builtin_dict
