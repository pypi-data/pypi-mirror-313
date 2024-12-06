#!/usr/bin/env python3
import unittest
from subprocess import PIPE, run
import os
import shutil
import sys


# This is not best practice but for testing, this is the best I could
# come up with
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from species import Species


class OrganisminfoUnitTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_species_class(self):
        info = Species("Salmonella enterica")

        # Got expected response from ENSEMBL
        self.assertTrue(len(info.ensembl_response) == 6)
        # Convert response to ensembl dict
        self.assertTrue(info.ensembl_dict["salmonella"])
        # Convert ensembl dict to tuple
        dict2tuple_msg = "Uexpected tuple: {}".format(info.tax_tuple)
        self.assertTrue(len(info.tax_tuple) == 7, msg=dict2tuple_msg)
        self.assertTrue(info.tax_tuple[4] == "enterobacteriaceae",
                        msg=dict2tuple_msg)
        self.assertTrue(info.tax_tuple[6] == "salmonella enterica",
                        msg=dict2tuple_msg)
        # Convert tuple to tax dict
        tuple2dict_msg = "Uexpected dict: {}".format(info.tax_dict)
        self.assertTrue(len(info.tax_dict.keys()) == 7, msg=tuple2dict_msg)
        self.assertTrue(info.tax_dict["species"] == "salmonella enterica",
                        msg=tuple2dict_msg)
        self.assertTrue(info.tax_dict["genus"] == "salmonella",
                        msg=tuple2dict_msg)
        self.assertTrue(info.tax_dict["family"] == "enterobacteriaceae",
                        msg=tuple2dict_msg)
        self.assertTrue(info.tax_dict["order"] == "enterobacterales",
                        msg=tuple2dict_msg)
        self.assertTrue(info.tax_dict["class"] == "gammaproteobacteria",
                        msg=tuple2dict_msg)
        self.assertTrue(info.tax_dict["phylum"] == "proteobacteria",
                        msg=tuple2dict_msg)
        self.assertTrue(info.tax_dict["domain"] == "bacteria",
                        msg=tuple2dict_msg)


if __name__ == "__main__":
    unittest.main()
