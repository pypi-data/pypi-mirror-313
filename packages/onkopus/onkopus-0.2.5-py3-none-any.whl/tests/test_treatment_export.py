import unittest, os
import adagenes
import onkopus


class TestTreatmentExportClass(unittest.TestCase):

    def test_treatment_export(self):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        infile = __location__ + "/test_files/somaticMutations.vcf"
        outfile = __location__ + "/test_files/output_treatments.csv"
        #bframe = onkopus.read_file(infile)
        bframe = adagenes.BiomarkerFrame()
        bframe.data = {"chr7:140753336A>T":{}}

        bframe.data = onkopus.UTAAdapterClient(genome_version="hg38").process_data(bframe.data)
        bframe.data = onkopus.CIViCClient(genome_version="hg38").process_data(bframe.data)
        bframe.data = onkopus.MetaKBClient(genome_version="hg38").process_data(bframe.data)
        bframe.data = onkopus.AggregatorClient(genome_version="hg38").process_data(bframe.data)

        onkopus.CS_TSV_Writer().write_evidence_data_to_file_all_features(bframe.data, output_file=outfile)
        #onkopus.write_file(outfile, bframe)
        #print(bframe)

