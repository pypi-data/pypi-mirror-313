import unittest, copy
import onkopus as op

class MolFeatAnnotationTestCase(unittest.TestCase):

    def test_molfeat_client(self):
        #genome_version = 'hg19'
        genome_version = 'hg38'

        #data = {"chr17:7681744T>C": {}, "chr10:8115913C>T": {}}
        data = {"chr7:140753336A>T":{}}

        variant_data = op.UTAAdapterClient(genome_version=genome_version).process_data(data)
        variant_data = op.MolecularFeaturesClient(
            genome_version=genome_version).process_data(variant_data)

        #print("Response ",variant_data)
        self.assertEqual(variant_data["chr7:140753336A>T"]["molecular_features"]["aromaticity_alt"],0,"")

