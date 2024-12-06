#!/usr/bin/env python3


class LoadersMixin():

    @staticmethod
    def load_md_table_after_keyword(mdfile, keyword, header_key=0,
                                    ignore_case=True):
        md_table_list = []
        record_line = False

        with open(mdfile, "r") as fh:
            for line in fh:

                if(line.startswith(keyword)):
                    record_line = True

                elif(record_line and line.strip()):
                    if(not line.startswith("|")):
                        record_line = False
                    else:
                        md_table_list.append(line.strip())

        md_table_str = "\n".join(md_table_list)

        return LoadersMixin.load_md_table_to_dict(md_table_str, header_key,
                                                  ignore_case)

    @staticmethod
    def load_md_table_to_dict(md_str, key=0, ignore_case=True):
        """ Input:
                md_str: String containing markdown table
                key: Integer or string. If integer, use the column at that
                     index as keys. If string then the column header matching
                     the string will be used as key.
            Output:
                out_dict: Dictonary containing table information. Keys are as
                specified under 'key' argument. A value is a list containing
                the row information. The key will not be part of the row
                information. Headers of the table will be stored under the
                key 'headers'.

            Loads a markdown formatted string into a dict object, with specified
            column as keys and the remaining row information stored as a list.

        """
        md_str = md_str.strip()
        md_list = md_str.split("\n")

        headers = LoadersMixin.split_and_clean_str(md_list[0], "|")
        header_index = LoadersMixin._get_header_index(key, headers, ignore_case)

        out_dict = {}

        # Skip header and horisontal seperator
        for line in md_list[2:]:

            entries = LoadersMixin.split_and_clean_str(line, "|")

            val_list = []
            for i, entry in enumerate(entries):
                if(i == header_index):
                    entry_key = entry
                else:
                    val_list.append(entry)

            out_dict[entry_key] = val_list

        return out_dict

    @staticmethod
    def _get_header_index(key, headers, ignore_case):
        if(isinstance(key, int)):
            index = key
        else:
            index = 0
            for header in headers:
                if(ignore_case and header.lower() == key.lower()):
                    break
                elif(header == key):
                    break
                else:
                    index = index + 1

        if(index >= len(headers) and isinstance(key, str)):
            raise KeyError("The argument provided as key: {} did not match any"
                           " of the strings in the list of headers: {}"
                           .format(key, headers))
        if(index >= len(headers) and isinstance(key, int)):
            raise IndexError("The argument provided as key: {} was larger or "
                             "equal to the number of headers: {}."
                             .format(key, len(headers)))

        else:
            return index

    @staticmethod
    def split_and_clean_str(string, delimiter):
        """ Input:
                string: String to split and clean.
                delimiter: Delimiter used for split.
            Output:
                tmp_lst: List without empty entries and without leading and
                         trailing whitespaces in entries.

        """
        tmp_lst = [x.strip() for x in string.split(delimiter)]
        return list(filter(None, tmp_lst))
