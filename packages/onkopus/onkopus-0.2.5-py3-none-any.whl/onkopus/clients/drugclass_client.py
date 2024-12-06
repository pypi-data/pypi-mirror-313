import datetime, traceback, copy
import vcfcli.tools
import vcfcli.tools.module_requests as req
from onkopus.conf import read_config as config
from vcfcli.tools import generate_variant_dictionary


class DrugOnClient:
    def __init__(self, genome_version, error_logfile=None):
        self.genome_version = genome_version
        self.url_pattern = config.drugclass_src
        self.srv_prefix = config.drugclass_srv_prefix
        self.extract_keys = config.drugclass_keys
        self.info_lines = config.drugclass_info_lines
        self.error_logfile = error_logfile

        self.qid_key = "q_id"
        if (self.genome_version == "hg19") or (self.genome_version == "GRCh37"):
            self.qid_key = "q_id_hg19"

    def process_data(self, vcf_lines):

        # for each variant, extract drugs from treatment results and query drug classes
        drug_classfications = {}

        qid_list = copy.deepcopy(list(vcf_lines.keys()))
        while True:
            max_length = int(config.config["DEFAULT"]["MODULE_BATCH_SIZE"])
            if max_length > len(qid_list):
                max_length = len(qid_list)
            qids_partial = qid_list[0:max_length]

            variants = vcfcli.tools.filter_alternate_alleles(qids_partial)

            for qid in variants:

                for i,treatment in enumerate(vcf_lines[qid]["onkopus_aggregator"]["merged_evidence_data"]):
                    drug = treatment["drugs"]

                    try:
                        if drug in drug_classfications:
                            vcf_lines[qid]["onkopus_aggregator"]["merged_evidence_data"][i]["drug_class"] = drug_classfications[drug]
                        else:
                            json_body = req.get_connection(drug, self.url_pattern, self.genome_version)

                            if drug.lower() in json_body:
                                    json_obj = json_body[drug.lower()]

                                    try:
                                        drug_class = json_obj["manual drug class"][0]
                                        drug_classfications[drug] = drug_class
                                        vcf_lines[qid]["onkopus_aggregator"]["merged_evidence_data"][i]["drug_class"] = drug_class
                                    except:
                                        vcf_lines[qid]["onkopus_aggregator"]["merged_evidence_data"][i][
                                            "drug_class"] = ''
                                        if self.error_logfile is not None:
                                            cur_dt = datetime.datetime.now()
                                            date_time = cur_dt.strftime("%m/%d/%Y, %H:%M:%S")
                                            print(cur_dt, ": error processing variant response: ", qid, ';',
                                                  traceback.format_exc(), file=self.error_logfile + str(date_time) + '.log')
                                        else:
                                            traceback.format_exc()
                            else:
                                vcf_lines[qid]["onkopus_aggregator"]["merged_evidence_data"][i][
                                    "drug_class"] = ''
                    except:
                        if self.error_logfile is not None:
                            print("error processing request: ", variants, file=self.error_logfile + str(date_time) + '.log')
                        else:
                            print(": error processing variant response: ;", traceback.format_exc())

            for i in range(0, max_length):
                del qid_list[0] #qid_list.remove(qid)
            if len(qid_list) == 0:
                break
        return vcf_lines
