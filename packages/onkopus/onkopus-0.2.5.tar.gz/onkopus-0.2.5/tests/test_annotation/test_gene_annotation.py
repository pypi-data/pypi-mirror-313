import unittest
import onkopus as op


class TestGeneAnnotation(unittest.TestCase):

    def test_gene_annotation(self):
        data = {"TP53":{ "mutation_type": "gene" }}
        data = op.annotate_genes(data)
        print(data)

