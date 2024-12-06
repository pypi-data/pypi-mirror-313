import unittest
import os
import onkopus as op
import adagenes as ag


class TestFullAnnotation(unittest.TestCase):

    def test_full_annotation(self):
        #data = {"TP53":{ }, "chr7:140753336A>T": {}, "NRAS:Q61L": {} }
        #bframe = adagenes.BiomarkerFrame()
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        #bframe = op.read_file(__location__ + "/../test_files/variants_grch38_20240206_Pathogenic_80.tsv")
        bframe = ag.BiomarkerFrame(["BRAF:V600E","TP53:R282W"])
        bframe.genome_version="hg38"
        #bframe.data = data

        bframe = op.annotate(bframe)

        #self.assertListEqual(list(bframe.data.keys()),["","chr7:140753336A>T",""],"IDs do not match")
        #print(bframe.data.keys())


        outfile_variants = __location__ + "/../test_files/clinvar_80.annotated.csv"
        outfile_treatments = __location__ + "/../test_files/clinvar_80.treatments.csv"

        op.save_variants(outfile_variants, bframe)
        op.save_treatments(outfile_treatments, bframe)

