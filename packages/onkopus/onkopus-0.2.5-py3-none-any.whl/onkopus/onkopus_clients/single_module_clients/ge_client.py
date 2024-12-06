import traceback, datetime, json
from onkopus.conf import read_config as conf_reader
import requests
from json import JSONDecodeError
import adagenes as ag


class GeneExpressionClient:

    def __init__(self, error_logfile=None):
        #self.genome_version = genome_version
        self.info_lines= conf_reader.ge_module_info_lines
        self.url_pattern = conf_reader.ge_module_src
        self.srv_prefix = conf_reader.ge_module_srv_prefix
        self.response_keys = conf_reader.ge_module_response_keys
        self.extract_keys = conf_reader.ge_module_keys

        self.qid_key = "q_id"
        self.error_logfile = error_logfile

    def process_data(self, variant_data):
            """
            Generates JSON data for a Plotly variant needleplot with added variant annotations

            :param variant_data:
            :return:
            """
            qid_gene_mapping = {}

            qid_list = []
            for var in variant_data.keys():
                if "UTA_Adapter" in variant_data[var]:
                    if ("gene_name" in variant_data[var]["UTA_Adapter"]):
                        qid_list.append(variant_data[var]["UTA_Adapter"]["gene_name"])
                        if variant_data[var]["UTA_Adapter"]["gene_name"] not in qid_gene_mapping.keys():
                            qid_gene_mapping[variant_data[var]["UTA_Adapter"]["gene_name"]] = []

                        qid_gene_mapping[variant_data[var]["UTA_Adapter"]["gene_name"]].append(var)
                elif "mutation_type" in variant_data[var]:
                    if variant_data[var]["mutation_type"] == "gene":
                        qid_list.append(var)

                        if var not in qid_gene_mapping.keys():
                            qid_gene_mapping[var] = []
                        qid_gene_mapping[var].append(var)

            qid_lists_query = ag.tools.split_list(qid_list)

            for qid_list in qid_lists_query:
                url = conf_reader.ge_module_src + "?gene=" + ",".join(qid_list)
                print(url)
                json_body = requests.get(url, timeout=60).json()
                try:
                    for gene in json_body.keys():
                        for associated_var in qid_gene_mapping[gene]:
                            variant_data[associated_var]["gtex"] = json_body[gene][0]
                except:
                    print(traceback.format_exc())

            return variant_data
