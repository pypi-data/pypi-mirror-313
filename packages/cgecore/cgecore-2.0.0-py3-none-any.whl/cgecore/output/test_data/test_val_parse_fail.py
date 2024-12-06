#!/usr/bin/env python3


class CustomValueParsers():

    @staticmethod
    def char64(val):
        """
        Test val is exactely 64 characters. Can be anything that can be handled
        by str()
        """
        val = str(val)
        if(len(val) != 64):
            return ("This field expects a string of lenght 64 but the lenght "
                    "of the string is {}. The string is: {}"
                    .format(len(val), val))
