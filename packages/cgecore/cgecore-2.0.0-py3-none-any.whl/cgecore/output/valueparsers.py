#!/usr/bin/env python3

import dateutil.parser
import pandas as pd

class ValueParsers():

    @staticmethod
    def parse_bool(val):
        """
        Test if value is either of the python bool types or if it is one of the
        strings: True or False. The string test is not case sensitive.
        """
        accepted_vals = ("true", "false")
        if(val is True or val is False):
            return
        elif(str(val).lower() in accepted_vals):
            return
        else:
            return ("Value must be a boolean (True/False). Value was: {}"
                    .format(val))

    @staticmethod
    def parse_bool_or_unknown(val):
        """
        Test if value is either of the python bool types or if it is one of the
        strings: True, False, or Unknown. The string test is not case sensitive.
        """
        accepted_vals = ("true", "false", "unknown")
        if(val is True or val is False):
            return
        elif(str(val).lower() in accepted_vals):
            return
        else:
            return ("Value must be a boolean (True/False) or unknown. Value "
                    "was: {}".format(val))

    @staticmethod
    def parse_char64(val):
        """
        Test val is exactely 64 characters. Can be anything that can be handled
        by str()
        """
        val = str(val)
        if(len(val) != 64):
            return ("This field expects a string of lenght 64 but the lenght "
                    "of the string is {}. The string is: {}"
                    .format(len(val), val))

    @staticmethod
    def parse_date(val):
        """
        Test str(val) can be converted using dateutil.parser.isoparse()
        """
        try:
            # If the date is just a year it might be an integer (ex. 2018)
            dateutil.parser.isoparse(str(val))
        except ValueError:
            return ("Date format not recognised. Date format must adhere to "
                    "the ISO 8601 format (YYYY-MM-DD). Provided value was: {}"
                    .format(val))

    @staticmethod
    def parse_integer(val):
        """
        Test that val is an integer
        """
        try:
            val = int(float(val))
        except ValueError:
            return "Value must be an integer. Value was: {}".format(val)

    @staticmethod
    def parse_percentage(val):
        """
        Test that val is between 0 and 100.
        """
        try:
            val = float(val)
        except ValueError:
            return "Value must be a number. Value was: {}".format(val)
        if(val < 0 or val > 100):
            return ("Percentage value must be between 0 and 100. The value "
                    "was: {}".format(val))

    @staticmethod
    def parse_string(val):
        try:
            val = str(val)
        except ValueError:
            return "Value could not be converted to a string."

    @staticmethod
    def parse_float(val):
        try:
            val = float(val)
        except ValueError:
            return "Value must be a float. Value was: {}".format(val)

    @staticmethod
    def parse_dataframe(val):
        if isinstance(val, type(pd.DataFrame)):
            val = val
        else:
            return "Value must be a pandas DataFrame"

    @staticmethod
    def parse_dictionary(val):
        if isinstance(val, dict):
            val = val
        else:
            return "Value must be a dictionary"
