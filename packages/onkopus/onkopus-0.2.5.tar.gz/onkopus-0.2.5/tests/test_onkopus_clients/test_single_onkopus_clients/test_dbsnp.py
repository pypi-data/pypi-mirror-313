import unittest, copy
import onkopus.onkopus_clients


class DBSNPAnnotationTestCase(unittest.TestCase):

    def test_dbsnp_client(self):
        genome_version = 'hg38'

        data = {"chr7:140753336A>T": {}, "chr1:2556710C>A": {},
                "chr1:2556710C>T":{},"chr1:2556714A>G":{}, "chr1:2556718C>T":{},
                "chr1:2556718C>.": {}, "chr1:2556710C>.":{}
                }

        variant_data = onkopus.onkopus_clients.DBSNPClient(
            genome_version=genome_version).process_data(data)

        print("Response ",variant_data)
        self.assertListEqual(["chr7:140753336A>T", "chr1:2556710C>A",
                "chr1:2556710C>T","chr1:2556714A>G", "chr1:2556718C>T",
                "chr1:2556718C>.", "chr1:2556710C>."], list(variant_data.keys()),
                             "")
        self.assertEqual('0:23038(0.0)', variant_data["chr1:2556710C>T"]["dbsnp"]["freq_total"], "")

