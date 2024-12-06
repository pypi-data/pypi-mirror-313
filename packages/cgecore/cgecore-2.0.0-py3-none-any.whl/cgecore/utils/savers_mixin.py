import os
import json
import string
import random
import numpy as np
import pandas as pd


class Pd_NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, pd.DataFrame):
            return obj.to_dict()
        return super(Pd_NpEncoder, self).default(obj)


class SaveJson:
    @staticmethod
    def from_dict(object, file_path, overwrite=False):
        '''Save a dict into a json file'''
        # Check if folder exists
        if not os.path.isdir(os.path.dirname(file_path)):
            raise OSError("The folder where the json was going to be saved "
                          "do not exists")
        # Care about overwritting
        if overwrite is False and os.path.file(file_path):
            raise OSError("There is a file already called %s. If you want to"
                          " overwrite that file, set overwrite to True.")

        with open(file_path, 'w') as fp:
            json.dump(object, fp, indent=4, cls=Pd_NpEncoder)

    @staticmethod
    def dump_json(std_result_file, std_result):
        with open(std_result_file, 'w') as fh:
            fh.write(std_result.json_dumps())


class StringCreator:

    @staticmethod
    def random_string(str_len=4):
        """
            Output:
                random string of length 'str_len'

            Return a random string of the provided length. The string will only
            consist of lowercase ascii letters.
        """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(str_len))

    @staticmethod
    def text_table(headers, rows, empty_replace='-'):
        ''' Create text table

        USAGE:
            >>> from tabulate import tabulate
            >>> headers = ['A','B']
            >>> rows = [[1,2],[3,4]]
            >>> print(text_table(headers, rows))
            **********
              A     B
            **********
              1     2
              3     4
            ==========
        '''
        # Replace empty cells with placeholder
        rows = map(lambda row: map(lambda x: x if x else empty_replace, row),
                   rows)
        # Create table
        table = tabulate(rows, headers, tablefmt='simple').split('\n')
        # Prepare title injection
        width = len(table[0])
        # Switch horisontal line
        table[1] = '*' * (width + 2)
        # Update table with title
        table = (("%s\n" * 3)
                 % ('*' * (width + 2), '\n'.join(table), '=' * (width + 2)))
        return table
