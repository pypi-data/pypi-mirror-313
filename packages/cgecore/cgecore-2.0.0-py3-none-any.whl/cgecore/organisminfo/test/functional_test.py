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
from gramstain import Gramstain


class OrganisminfoTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_taxonomy(self):
        # Freja creates an object using the full species name
        info = Species("Salmonella enterica")

        # From the object she pulls the taxonomy information from domain to
        # species
        self.assertEqual(info.tax_tuple[6], "salmonella enterica")
        self.assertEqual(info.tax_tuple[5], "salmonella")
        self.assertEqual(info.tax_tuple[4], "enterobacteriaceae")
        self.assertEqual(info.tax_tuple[3], "enterobacterales")
        self.assertEqual(info.tax_tuple[2], "gammaproteobacteria")
        self.assertEqual(info.tax_tuple[1], "proteobacteria")
        self.assertEqual(info.tax_tuple[0], "bacteria")

        self.assertTrue(info.tax_dict["species"] == "salmonella enterica")
        self.assertTrue(info.tax_dict["genus"] == "salmonella")
        self.assertTrue(info.tax_dict["family"] == "enterobacteriaceae")
        self.assertTrue(info.tax_dict["order"] == "enterobacterales")
        self.assertTrue(info.tax_dict["class"] == "gammaproteobacteria")
        self.assertTrue(info.tax_dict["phylum"] == "proteobacteria")
        self.assertTrue(info.tax_dict["domain"] == "bacteria")

    def test_gram(self):
        gramdb = Gramstain()
        self.assertTrue(gramdb["salmonella enterica"] == "-")


if __name__ == "__main__":
    unittest.main()
