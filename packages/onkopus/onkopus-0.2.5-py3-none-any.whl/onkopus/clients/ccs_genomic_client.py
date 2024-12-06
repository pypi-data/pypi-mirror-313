import re
import pandas as pd, traceback
import vcfcli.tools.module_requests as req
import vcfcli.tools.parse_genomic_data
from onkopus.conf import read_config as config

class CCSGeneToGenomicClient:

    def __init__(self, genome_version, error_logfile=None):
        self.genome_version = genome_version
        self.error_logfile = error_logfile
        self.srv_prefix = config.uta_adapter_genetogenomic_srv_prefix

    def generate_request_str_of_gene_names(self,
            vcf_lines,input_format='json'):

        #print("extract data: ",vcf_lines)
        variant_list=[]

        if input_format == 'vcf':
            keys = [config.uta_adapter_srv_prefix + config.concat_char + config.uta_genomic_keys[0],
                    config.uta_adapter_srv_prefix + config.concat_char + config.uta_genomic_keys[0]]
            annotations = vcfcli.tools.parse_vcf.extract_annotations_vcf(vcf_lines, keys)
        elif input_format == 'tsv':
            keys = [config.uta_genomic_keys[0], config.uta_genomic_keys[1]]
            annotations = vcfcli.tools.parse_vcf.extract_annotations_json(vcf_lines,
                                                                          config.uta_adapter_genetogenomic_srv_prefix, keys)
        else:
            keys = [config.uta_genomic_keys[0], config.uta_genomic_keys[1]]
            annotations = vcfcli.tools.parse_vcf.extract_annotations_json(vcf_lines, config.uta_adapter_srv_prefix, keys)

        gene_names = annotations[keys[0]]
        variants = annotations[keys[1]]
        for i in range(0,len(gene_names)):
            variant_list.append(gene_names[i]+":"+variants[i])

        #print(variant_list)
        variant_str = ','.join(variant_list)
        return variant_str, variant_list

    def generate_genome_locations_as_keys(self, gene_data):

        annotated_data = {}
        for gene_name, value in gene_data.items():

            # extract genomic locations
            if 'results_string' in value:
                results_string = value['results_string']
                chr, ref_seq, pos, ref, alt = vcfcli.tools.parse_genomic_data.parse_genome_position(results_string)
                genompos = "chr" + chr + ":" + pos + ref + ">" + alt

                annotated_data[genompos] = {}
                annotated_data[genompos][config.uta_adapter_genetogenomic_srv_prefix] = value
                annotated_data[genompos]['variant_data'] = gene_data[gene_name]['variant_data']
            else:
                pass

        return annotated_data

    def process_data(self, gene_data, input_format='json'):
        """
        Looks up genomic data of variant calls from gene names and variant exchange data

        Parameters
        ----------
        vcf
        variant_str

        Returns
        -------

        """

        # generate query string
        variant_str, variant_list = self.generate_request_str_of_gene_names(gene_data,input_format=input_format)

        try:
            json_body = req.get_connection(variant_str,
                config.uta_adapter_genetogenomic_src,
                self.genome_version)
            annotated_data = {}
            for item in json_body:

                if item["data"] is not None:
                    for res in item["data"]:
                            if res != "Error":
                                results_string = res['results_string']
                                chr, ref_seq, pos, ref, alt = vcfcli.tools.parse_genomic_data.parse_genome_position(
                                    results_string)
                                qid = 'chr' + chr + ':' + pos + ref + '>' + alt

                                annotated_data[qid] = {}

                                annotated_data[qid][config.variant_data_key] = {}

                                annotated_data[qid][config.variant_data_key]['CHROM'] = chr
                                annotated_data[qid][config.variant_data_key]['reference_sequence'] = ref_seq
                                annotated_data[qid][config.variant_data_key]['POS'] = pos
                                annotated_data[qid][config.variant_data_key]['REF'] = ref
                                annotated_data[qid][config.variant_data_key]['ALT'] = alt
                                annotated_data[qid][config.variant_data_key]['POS_'+self.genome_version] = pos
                                annotated_data[qid]["q_id"] = "chr" + chr + ":" + str(pos) + ref + ">" + alt
                                annotated_data[qid][config.variant_data_key]['ID'] = ''
                                annotated_data[qid][config.variant_data_key]['QUAL'] = ''
                                annotated_data[qid][config.variant_data_key]['FILTER'] = ''

                                annotated_data[qid][self.srv_prefix] = res
        except:
            print("error: genomic to gene")
            print(traceback.format_exc())

        return annotated_data
