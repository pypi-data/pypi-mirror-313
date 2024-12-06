import traceback, copy
import adagenes.tools.module_requests as req
from onkopus.conf import read_config as config
import adagenes.tools.parse_genomic_data
import onkopus as op


class UTAAdapterProteinSequenceClient:

    def __init__(self, genome_version, error_logfile=None):
        self.genome_version = genome_version
        self.info_lines = config.uta_adapter_protein_sequence_info_lines
        self.url_pattern = config.uta_adapter_protein_sequence_src
        self.srv_prefix = config.uta_adapter_protein_sequence_srv_prefix
        self.genomic_keys = config.uta_genomic_keys
        self.gene_keys = config.uta_gene_keys
        self.gene_response_keys = config.uta_gene_response_keys
        self.extract_keys = config.uta_genomic_keys

        self.qid_key = "q_id"
        if (self.genome_version == "hg19") or (self.genome_version == "GRCh37"):
            self.qid_key = "q_id_hg19"

    def process_data(self, data, gene_request=False):
        #keys = [config.uta_genomic_keys[0],
        #            config.uta_genomic_keys[1]]
        #annotations = adagenes.tools.parse_vcf.extract_annotations_json(vcf_lines, config.uta_adapter_srv_prefix, keys)
        #gene_names = copy.deepcopy(annotations[keys[0]])
        #variant_exchange = copy.deepcopy(annotations[keys[1]])
        #qid_list = copy.deepcopy(annotations['q_id'])

        qid_gene_name_dc = {}
        qid_list = []
        for qid in data.keys():
            variant_data = data[qid]
            if ("UTA_Adapter" in variant_data) and (gene_request is False):
                if ("gene_name" in variant_data["UTA_Adapter"]) and ("variant_exchange" in variant_data["UTA_Adapter"]):
                    qid_gene_name_dc[variant_data["UTA_Adapter"]["gene_name"] + ':' + variant_data["UTA_Adapter"][
                        "variant_exchange"]] = [qid]
                    qid_list.append(variant_data["UTA_Adapter"]["gene_name"] + ':' + variant_data["UTA_Adapter"][
                        "variant_exchange"])
            elif ("gene_name" in variant_data) and ("variant_exchange" in variant_data):
                qid_gene_name_dc[variant_data["gene_name"] + ':' + variant_data["variant_exchange"]] = [qid]
                qid_list.append(variant_data["gene_name"] + ':' + variant_data["variant_exchange"])
            elif "gene_name" in variant_data:
                qid_gene_name_dc[variant_data["gene_name"]] = [qid]
                qid_list.append(variant_data["gene_name"])
            elif "gene" in variant_data:
                if variant_data["gene"] in qid_gene_name_dc.keys():
                    qid_gene_name_dc[variant_data["gene"]].append(qid)
                else:
                    qid_gene_name_dc[variant_data["gene"]] = [qid]
                qid_list.append(variant_data["gene"])
            elif gene_request is False:
                print("ProteinFeatures: Could not find UTA adapter section: ", variant_data)
            else:
                qid_list.append(qid)
        q_lists = list(op.tools.divide_list(copy.deepcopy(qid_list), chunk_size=100))

        for q_list in q_lists:
            q = ",".join(q_list)

            #while True:

            max_length = int(config.config["DEFAULT"]["MODULE_BATCH_SIZE"])
            if max_length > len(qid_list):
                max_length = len(qid_list)
            #qids_partial = qid_list[0:max_length]
            #qids_partial = adagenes.tools.filter_alternate_alleles(qids_partial)

            #gene_names_partial = gene_names[0:max_length]
            #variant_exchange_partial = variant_exchange[0:max_length]

            max_length = int(config.config["DEFAULT"]["MODULE_BATCH_SIZE"])
            if max_length > len(qid_list):
                max_length = len(qid_list)
            qids_partial = qid_list[0:max_length]

            #if gene_request:
            #    q = ','.join(qids_partial)
            #else:
            #    variants = []
            #    for gene,variant in zip(gene_names_partial,variant_exchange_partial):
            #        if (gene != '') and (variant != ''):
            #            variants.append(gene + ":" + variant)
            #    q = ','.join(variants)
            a = ','.join(q_list)

            try:
                json_body = req.get_connection(q, self.url_pattern, self.genome_version)

                for key in json_body[0].keys():
                        if gene_request is False:
                            qids = qid_gene_name_dc[str(json_body[0][key]["header"]["qid"])]

                        else:
                            #qid_index = q_list.index(str(json_body[0][key]["header"]["qid"]))
                            #qid = qids_partial[qid_index]
                            qid = str(json_body[0][key]["header"]["qid"])
                            #print("genompos for ",str(json_body[0][key]["header"]["qid"]),": ",qid)

                        if json_body[0][key]["data"] is not None:
                            if type(json_body[0][key]["data"]) is dict:
                                #print("available qids: ",list(vcf_lines.keys()))
                                for qid in qids:
                                    data[qid][self.srv_prefix] = json_body[0][key]["data"]
                            else:
                                for qid in qids:
                                    data[qid][self.srv_prefix] = {}
                                    data[qid][self.srv_prefix]["status"] = 400
                                    data[qid][self.srv_prefix]["msg"] = json_body[0][key]["data"]
            except:
                print("error: genomic to gene")
                print(traceback.format_exc())

            #for i in range(0, max_length):
            #    del qid_list[0]  # qid_list.remove(qid)
            #if len(qid_list) == 0:
            #    break

        return data
