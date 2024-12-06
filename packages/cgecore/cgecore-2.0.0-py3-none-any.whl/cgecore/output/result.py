#!/usr/bin/env python3

import logging
import json
import os.path
from datetime import datetime, timezone
from collections import UserDict

from cgecore.utils.pliers_mixin import PliersMixin
from cgecore.utils.transformer_mixin import TransformerMixin
from cgecore.output.parserdict import ParserDict
from cgecore.output.exceptions import (CGECoreOutTypeError, CGECoreOutInputError,
                                      CGECoreOutDuplicateKeyError)


class Result(UserDict):

    BEONE_JSON_FILE = "beone/beone.json"
    TEMPLATE_DIR = "templates_json"
    beone_json_path = os.path.join(os.path.dirname(__file__), TEMPLATE_DIR,
                                   BEONE_JSON_FILE)

    def __init__(self, type, fmt_file=beone_json_path,
                 parsers=None, **kwargs):
        super().__init__()

        self.defs = {}
        # classes in a template translates to Result objects.
        self.classes = set()
        self.errors = {}
        with open(fmt_file, "r") as fh:
            self.defs = json.load(fh)

        if(parsers is None):
            self.val_parsers = ParserDict()
        else:
            self.val_parsers = ParserDict(parsers)

        self._set_type(type)
        self._parser = ResultParser(result_def=self.defs[type])
        for d in self._parser.arrays:
            self[d] = []
        for d in self._parser.dicts:
            self[d] = {}

        self.add(**kwargs)

    @staticmethod
    def init_software_result(name, gitdir, type="git_repo"):
        """
            Input: software_name, path to git directory
            Return: Result object with type: software_result
        """
        if(type == "python_module"):
            version = PliersMixin.get_version_pymodule(name)
            commit = "unknown"
        elif(type == "git_repo"):
            version, commit = PliersMixin.get_version_commit(gitdir)
        else:
            version, commit = ("unknown", "unknown")
        date = datetime.now(timezone.utc).date().isoformat()

        result_dict = {
            "type": "software_result",
            "software_name": name,
            "software_version": version,
            "software_commit": commit,
            "run_date": date,
            "key": "{}-{}".format(name, version)
        }
        return Result(**result_dict)

    def init_database(self, name, db_dir):
        database_metadata = {}
        database_metadata["type"] = "database"
        database_metadata["database_name"] = name

        if hasattr(PliersMixin, 'get_version_database'):
            version = PliersMixin.get_version_database(db_dir)
        else:
            version = 'unknown'
        version_in_git, commit = PliersMixin.get_version_commit(db_dir)

        if version == 'unknown':
            version = version_in_git

        database_metadata["database_version"] = version
        database_metadata["key"] = "{}-{}".format(name, version)
        database_metadata["database_commit"] = commit

        self.add_class(cl="databases", **database_metadata)

    def get_db_key(self, name):
        """
            Input:
                name: database name for which key(s) are desired.
            Ouput:
                list of keys: List of all keys which values match the input.

            Method for retrieving all keys for a specific database name. Often
            you will only expect a list with a single entry.
        """
        key_list = []
        for key, val in self["databases"].items():
            if(val["database_name"] == name):
                key_list.append(key)
        return key_list

    def _set_type(self, type):
        if(type in self.defs):
            self["type"] = type
        else:
            raise CGECoreOutTypeError(
                "Unknown result type given. Type given: {}. Type must be one "
                "of:\n{}".format(type, list(self.defs.keys())))

    def add(self, **kwargs):
        for key, val in kwargs.items():
            if(val is None):
                continue
            self[key] = val

    def add_class(self, cl, type, clobber=True, clobber_warn=True, **kwargs):
        res = Result(type=type, **kwargs)
        self.classes.add(cl)
        if(cl in self._parser.arrays):
            self[cl].append(res)
        elif(cl in self._parser.dicts):
            self._add_class_dict(cl, res, clobber, clobber_warn)
            # self[cl][res["key"]] = res
        # Do not store the result object in neither a dict or a list.
        else:
            self[cl] = res

    def _add_class_dict(self, cl, res, clobber, clobber_warn):
        # val = self[cl][res["key"]]
        val = self[cl].get(res["key"], None)
        if(val):
            if(clobber):
                if(clobber_warn):
                    logging.warn("In {}. Clobbered entry with the key: {}."
                                 .format(cl, res["key"]))
            else:
                raise CGECoreOutDuplicateKeyError(
                    "The add_class would have clobbered an existing non-empty "
                    "entry. If this was intended you need to call the method "
                    "with the clobber argument set to True. Duplicate key: {}"
                    .format(res["key"])
                )
        self[cl][res["key"]] = res

    def check_results(self, strict=False, errors=None):
        """ Populates self.errors if any errors are encountered """

        for key, val in self.items():
            if(key == "type"):
                continue
            # The key is not defined
            elif(key not in self.defs[self["type"]]):
                if(strict):
                    self.errors[key] = ("Key not defined in template: {}"
                                        .format(key))
                    continue
                else:
                    continue
            self._check_result(key, val, self.errors)

        # errors is not None if called recursively
        if(errors is not None):
            errors[self["key"]] = self.errors
            return None
        # errors is None if it is the first/root call
        elif(errors is None and self._no_errors(self.errors)):
            return None
        else:
            raise CGECoreOutInputError(
                "Some input data did not pass validation, please consult the "
                "Dictionary of ERRORS:{}".format(self.errors),
                self.errors)

    def _check_result(self, key, val, errors, index=None):
        # Remember Result is a dict object and therefore this test should
        # be before the dict test.
        if(isinstance(val, Result)):
            val.check_results(errors)
        elif(isinstance(val, dict)):
            self._check_result_dict(key, val, errors)
        elif(isinstance(val, list)):
            self._check_result_list(key, val, errors)
        else:
            self._check_result_val(key, val, errors, index)

    def del_entries_by_values(self, values):
        values = tuple(values)
        deleted_keys = []
        for key, entry_val in self.items():
            if(key == "type"):
                continue
            if(entry_val in values):
                deleted_keys.append(key)
        for key in deleted_keys:
            del self[key]
        return deleted_keys

    def json_dumps(self):
        return json.dumps(TransformerMixin.userdict_to_dict(self))

    def _no_errors(self, errors):
        no_errors = True

        for key, val in errors.items():

            if(isinstance(val, dict)):
                no_errors = self._no_errors(val)
                if(no_errors is False):
                    return False

            elif(val is not None):
                return False

        return no_errors

    def _check_result_val(self, key, val, errors, index=None):
        val_type = self._parser[key]

        if(val_type.endswith("*")):
            val_type = val_type[:-1]

        val_error = self.val_parsers[val_type](val)

        if(val_error):
            if(index is not None):
                val_error = "{}:{} ".format(index, val_error)
            errors[key] = val_error

    def _check_result_dict(self, result_key, result_dict, errors):
        errors[result_key] = {}
        for key, val in result_dict.items():
            self._check_result(key, val, errors[result_key])

    def _check_result_list(self, result_key, result_list, errors):
        errors[result_key] = {}
        for i, val in enumerate(result_list):
            self._check_result(result_key, val, errors[result_key], index=i)


class ResultParser(dict):
    """"""
    def __init__(self, result_def):
        # self.classes = set()
        self.arrays = {}
        self.dicts = {}

        for key, val_def_str in result_def.items():
            val_def, *sub_def = val_def_str.split(" ")
            if(sub_def and val_def == "dict"):
                self.dicts[key] = sub_def[0]
                self[key] = sub_def[0]
            elif(sub_def and val_def == "array"):
                self.arrays[key] = sub_def[0]
                self[key] = sub_def[0]
            else:
                self[key] = val_def
