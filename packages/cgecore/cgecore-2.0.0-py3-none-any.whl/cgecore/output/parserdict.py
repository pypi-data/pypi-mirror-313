#!/usr/bin/env python3

from collections import UserDict

from cgecore.output.valueparsers import ValueParsers


class ParserDict(UserDict):

    def __init__(self, input_parser=None):
        super().__init__(self)

        if(input_parser is None):
            parser_class = ValueParsers
        else:
            parser_class = input_parser

        val_parser_list = self.get_method_names(parser_class)

        for parser in val_parser_list:
            if(parser.startswith("parse_")):
                parse_key = parser[6:]
                self[parse_key] = getattr(parser_class, parser)
            else:
                raise SyntaxError(("A function in the {} class did "
                                   "not start with 'parse_'. Function is "
                                   "named: {}"
                                   .format(parser_class.__name__, parser)))

    @staticmethod
    def get_method_names(cls):
        return [func for func in dir(cls) if(not func.startswith("__")
                                             and callable(getattr(cls, func)))]
