import datetime, requests, traceback, copy
import vcfcli.tools.module_requests as req
from onkopus.conf import read_config as config
import vcfcli.tools

qid_key = "q_id"
error_logfile=None

class PrimateAIClient:
    def __init__(self, genome_version, error_logfile=None):
        self.genome_version = genome_version
        self.info_lines = config.primateai_info_lines
        self.url_pattern = config.primateai_src
        self.srv_prefix = config.primateai_srv_prefix
        self.extract_keys = config.primateai_keys

        self.qid_key = "q_id"
        self.error_logfile = error_logfile
        #if (self.genome_version == "hg19") or (self.genome_version == "GRCh37"):
        #    self.qid_key = "q_id_hg19"

    def get_connection(self, variants, url_pattern, genome_version):
        url = url_pattern.format(genome_version) + variants
        print(url)
        r = requests.get(url)
        return r.json()

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

                for qid, json_obj in json_body.items():
                    if json_obj:

                        # calculate percentage
                        json_obj['score_percent'] = int(float(json_obj['Score']) * 100)

                        #colour = "#00b0d2"
                        colour = "#ce8585"
                        json_obj['score_color'] = colour

                        for k in self.extract_keys:
                            if k in json_obj:
                                pass
                                #annotations.append('{}_{}={}'.format(self.srv_prefix, k, json_body[i][k]))
                        try:
                            #json_obj.pop('q_id')
                            vcf_lines[qid][self.srv_prefix] = json_obj
                        except:
                            print("error")
                            if self.error_logfile is not None:
                                cur_dt = datetime.datetime.now()
                                date_time = cur_dt.strftime("%m/%d/%Y, %H:%M:%S")
                                print(cur_dt, ": error processing variant response: ", qid, ';', traceback.format_exc(), file=self.error_logfile+str(date_time)+'.log')

            except:
                if error_logfile is not None:
                    print("error processing request: ", variants, file=error_logfile+str(date_time)+'.log')

            for i in range(0, max_length):
                del qid_list[0] 
            if len(qid_list) == 0:
                break

        return vcf_lines
