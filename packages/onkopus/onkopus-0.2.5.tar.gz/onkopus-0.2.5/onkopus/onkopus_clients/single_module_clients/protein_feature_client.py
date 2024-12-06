import copy
import traceback, datetime, json
import adagenes.tools.module_requests as req
from onkopus.conf import read_config as conf_reader
import requests
from json import JSONDecodeError
import onkopus as op


class ProteinFeatureClient:

    def __init__(self, genome_version, error_logfile=None):
        self.genome_version = genome_version
        self.info_lines= conf_reader.onkopus_plots_info_lines
        self.url_pattern = conf_reader.onkopus_plots_src
        self.srv_prefix = conf_reader.onkopus_plots_srv_prefix
        self.response_keys = conf_reader.onkopus_plots_response_keys
        self.extract_keys = conf_reader.onkopus_plots_keys

        self.qid_key = "q_id"
        if (self.genome_version == "hg19") or (self.genome_version == "GRCh37"):
            self.qid_key = "q_id_hg19"
        self.error_logfile = error_logfile

    def process_data(self, data, plot=None):
            """
            Generates JSON data for a Plotly variant needleplot with added variant annotations

            :param variant_data:
            :return:
            """
            qid_gene_name_dc = {}
            qid_list=[]
            for qid in data.keys():
                variant_data = data[qid]
                if "UTA_Adapter" in variant_data:
                    if ("gene_name" in variant_data["UTA_Adapter"]) and ("variant_exchange" in variant_data["UTA_Adapter"]):
                        qid_gene_name_dc[variant_data["UTA_Adapter"]["gene_name"] + ':' + variant_data["UTA_Adapter"]["variant_exchange"]] = qid
                        qid_list.append(variant_data["UTA_Adapter"]["gene_name"] + ':' + variant_data["UTA_Adapter"]["variant_exchange"])
                else:
                    #qid_list.append(qid)
                    #print("ProteinFeatures: Could not find UTA adapter section: ", variant_data)
                    pass
            q_lists = list(op.tools.divide_list(copy.deepcopy(qid_list), chunk_size=100))

            for q_list in q_lists:
                q = ",".join(q_list)
                url = conf_reader.protein_module_features_src + "/" + q
                print(url)
                try:
                    json_obj = requests.get(url, timeout=60).json()
                    for result in json_obj:
                        if result["data"] is not None:
                            qid = qid_gene_name_dc[result["header"]["qid"]]
                            data[qid]["protein_features"] = result["data"]
                except JSONDecodeError:
                    print("Could not decode JSON: ",traceback.format_exc())
                except KeyError:
                    print("Could not parse variant: ",traceback.format_exc())

            return data
