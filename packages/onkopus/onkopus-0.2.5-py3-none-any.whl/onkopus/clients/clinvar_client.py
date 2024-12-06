import traceback, copy
import datetime
import vcfcli.tools.module_requests as req
from onkopus.conf import read_config as config
import vcfcli.tools


class ClinVarClient:

    def __init__(self, genome_version, error_logfile=None):
        self.genome_version = genome_version
        self.url_pattern = config.clinvar_src
        self.srv_prefix = config.clinvar_srv_prefix
        self.extract_keys = config.clinvar_keys
        self.info_lines = config.clinvar_info_lines
        self.error_logfile = error_logfile

        self.qid_key = "q_id"
        #if (self.genome_version == "hg19") or (self.genome_version == "GRCh37"):
        #    self.qid_key = "q_id_hg19"

    def process_data(self, vcf_lines):

        qid_list = copy.deepcopy(list(vcf_lines.keys()))
        while True:
            max_length = int(config.config["DEFAULT"]["MODULE_BATCH_SIZE"])
            if max_length > len(qid_list):
                max_length = len(qid_list)
            qids_partial = qid_list[0:max_length]
            variants = ','.join(vcfcli.tools.filter_alternate_alleles(qids_partial))

            try:
                json_body = req.get_connection(variants, self.url_pattern, self.genome_version)

                for json_obj in json_body:
                    if json_obj:
                        #annotations = []

                        if self.qid_key not in json_obj:
                            continue
                        qid = json_obj[self.qid_key]
                        json_obj["clinical_significance"] = json_obj["clinical_significance"].replace("_"," ")

                        # compute clinvar score
                        if "review_status" in json_obj:
                            if json_obj["review_status"] == "no_assertion_provided":
                                json_obj["score"] = 0
                            elif json_obj["review_status"] == "no_assertion_criteria_provided":
                                json_obj["score"] = 0
                            elif json_obj["review_status"] == "no_assertion_for_the_individual_variant":
                                json_obj["score"] = 0
                            elif json_obj["review_status"] == "criteria_provided,_single_submitter":
                                json_obj["score"] = 1
                            elif json_obj["review_status"] == "criteria_provided,_conflicting_interpretations":
                                json_obj["score"] = 1
                            elif json_obj["review_status"] == "criteria_provided,_multiple_submitters,_no_conflicts":
                                json_obj["score"] = 2
                            elif json_obj["review_status"] == "reviewed_by_expert_panel":
                                json_obj["score"] = 3
                            elif json_obj["review_status"] == "practice_guideline":
                                json_obj["score"] = 4
                            else:
                                json_obj["score"] = 0
                        else:
                            json_obj["score"] = 0

                        for k in self.extract_keys:
                            if k in json_obj:
                                pass
                                #annotations.append('{}_{}={}'.format(self.srv_prefix, k, json_body[i][k]))

                        try:
                            json_obj.pop('q_id')
                            vcf_lines[qid][self.srv_prefix] = json_obj
                        except:
                            print("error")
                            if self.error_logfile is not None:
                                cur_dt = datetime.datetime.now()
                                date_time = cur_dt.strftime("%m/%d/%Y, %H:%M:%S")
                                print(cur_dt, ": error processing variant response: ", qid, ';', traceback.format_exc(), file=self.error_logfile+str(date_time)+'.log')

            except:
                if self.error_logfile is not None:
                    print("error processing request: ", variants, file=self.error_logfile)

            for i in range(0, max_length):
                del qid_list[0] #qid_list.remove(qid)
            if len(qid_list) == 0:
                break

        return vcf_lines
