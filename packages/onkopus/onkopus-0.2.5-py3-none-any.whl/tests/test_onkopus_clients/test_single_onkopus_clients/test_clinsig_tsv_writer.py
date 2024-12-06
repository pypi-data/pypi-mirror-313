import unittest
import onkopus

class TestCSTSVWriter(unittest.TestCase):

    def test_clinsig_tsv_export(self):
        genome_version = 'hg38'
        data = {"chr7:140753336A>T": {}, "chr12:25245350C>T": {}}
        outfile="../test_files/cs_tsv_export.tsv"

        data = onkopus.onkopus_clients.uta_adapter_client.UTAAdapterClient(
            genome_version=genome_version).process_data(data)

        variant_data = onkopus.onkopus_clients.ccs_liftover_client.LiftOverClient(
            genome_version=genome_version).process_data(data)

        client = onkopus.onkopus_clients.MetaKBClient(genome_version=genome_version)
        variant_data = client.process_data(variant_data)
        client = onkopus.onkopus_clients.CIViCClient(genome_version=genome_version)
        variant_data = client.process_data(variant_data)
        client = onkopus.onkopus_clients.OncoKBClient(genome_version=genome_version)
        variant_data = client.process_data(variant_data)

        variant_data = onkopus.onkopus_clients.AggregatorClient(
            genome_version=genome_version).process_data(variant_data)

        #onkopus.onkopus_clients.CS_TSV_Writer().write_evidence_data_to_file(variant_data, output_file=outfile)
        onkopus.onkopus_clients.CS_TSV_Writer().write_evidence_data_to_file_all_features(variant_data, output_file=outfile)


