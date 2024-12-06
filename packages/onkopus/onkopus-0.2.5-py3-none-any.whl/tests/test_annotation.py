import unittest, os
import onkopus


class TestCLIAnnotation(unittest.TestCase):


    def test_cli_annotation(self):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        infile = __location__ + "/test_files/somaticMutations.vcf"
        outfile = infile + ".anno.csv"
        bframe = onkopus.read_file(infile)
        bframe.data = onkopus.annotate_variant_data(bframe.data)
        onkopus.write_file(outfile,bframe)

