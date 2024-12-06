import unittest, copy, os
import onkopus.onkopus_clients

class ClinVarAnnotationTestCase(unittest.TestCase):

    def test_clinvar_client(self):
        genome_version = 'hg19'

        data = {"chr17:7681744T>C": {}, "chr10:8115913C>T": {}, "chr10:8115914C>.": {}}

        variant_data = onkopus.onkopus_clients.ClinVarClient(
            genome_version=genome_version).process_data(data)

        print("Response ",variant_data)
        self.assertListEqual(["chr17:7681744T>C", "chr10:8115913C>T", "chr10:8115914C>."], list(variant_data.keys()), "")
        self.assertEqual('0.00001',variant_data["chr10:8115913C>T"]["clinvar"]["AF_EXAC"],"")

    def test_clinvar_client_batch(self):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        input_file = __location__ + "/../../test_files/somaticMutations.vcf"
        genome_version = 'hg38'
        #onkopus.annotate_file(file, file+'.clinvar', 'clinvar', genome_version=genome_version)

        data = onkopus.read_file(input_file)

        data.data = onkopus.onkopus_clients.ClinVarClient(
            genome_version=genome_version).process_data(data.data)

        print(data.data)
