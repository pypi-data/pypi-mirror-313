import unittest,os
import adagenes
import onkopus


class TreatmentExportTestCase(unittest.TestCase):

    def test_export_treatment_data(self):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        oncokb_key = os.getenv("ONCOKB_KEY")

        data = {"chr7:140753336A>T":{}, "chr17:7673776G>A":{}}
        genome_version = "hg38"
        bf = adagenes.BiomarkerFrame(genome_version=genome_version,data=data)
        bf = onkopus.annotate(bf, genome_version="hg38",oncokb_key=oncokb_key)

        #print(bf.data["chr7:140753336A>T"]["oncokb"])

        outfile=__location__ + "/../test_files/test_writer.out.csv"
        onkopus.ClinSigWriter().write_evidence_data_to_file(outfile,bf,sep="\t")

        file = open(outfile)
        contents = file.read()
        contents_expected = """biomarker\tcitation_i"""
        self.assertEqual(contents[0:20], contents_expected, "")
        file.close()



    def test_export_treatment_data_filestream(self):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        oncokb_key = os.getenv("ONCOKB_KEY")

        data = {"chr7:140753336A>T":{}, "chr17:7673776G>A":{}}
        genome_version = "hg38"
        bf = adagenes.BiomarkerFrame(genome_version=genome_version,data=data)
        bf = onkopus.annotate(bf, genome_version="hg38",oncokb_key=oncokb_key)

        #print(bf.data["chr7:140753336A>T"]["oncokb"])

        outfile_str=__location__ + "/../test_files/test_writer.out.stream.csv"
        outfile = open(outfile_str, "w")
        onkopus.ClinSigWriter().write_evidence_data_to_file_all_features(bf,output_file=outfile,sep="\t")
        outfile.close()

        file = open(outfile_str)
        contents = file.read()
        contents_expected = """biomarker\tcitation_i"""
        self.assertEqual(contents[0:20], contents_expected, "")
        file.close()

