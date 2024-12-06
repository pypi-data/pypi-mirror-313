import datetime, traceback, copy
import vcfcli.tools.parse_vcf
import vcfcli.tools.module_requests as req
from onkopus.conf import read_config as config

qid_key = "q_id"
error_logfile=None

class LoFToolClient:
    def __init__(self, genome_version, error_logfile=None):
        self.genome_version = genome_version
        self.info_lines = config.loftool_info_lines
        self.url_pattern = config.loftool_src
        self.srv_prefix = config.loftool_srv_prefix
        self.extract_keys = config.loftool_keys

        self.qid_key = "q_id"
        self.error_logfile = None
        #if (self.genome_version == "hg19") or (self.genome_version == "GRCh37"):
        #    self.qid_key = "q_id_hg19"

    def process_data(self, vcf_lines, input_format='json'):
        if input_format == 'vcf':
            keys = [config.uta_adapter_srv_prefix + config.concat_char + config.uta_genomic_keys[0]]
            annotations = vcfcli.tools.parse_vcf.extract_annotations_vcf(vcf_lines, keys)
        else:
            keys = [config.uta_genomic_keys[0]]
            annotations = vcfcli.tools.parse_vcf.extract_annotations_json(vcf_lines, config.uta_adapter_srv_prefix, keys)

        #gene_names = annotations[ keys[0] ]
        #genompos_str = ",".join(annotations['q_id'])
        #query = ",".join(gene_names) + '&genompos=' + genompos_str
        #q_ids = annotations['q_id']
        #gene_names = copy.deepcopy(annotations[keys[0]])
        #variant_exchange = copy.deepcopy(annotations[keys[1]])
        #qid_list = copy.deepcopy(annotations['q_id'])
        qid_list = list(vcf_lines.keys())

        while True:
            max_length = int(config.config["DEFAULT"]["MODULE_BATCH_SIZE"])
            if max_length > len(qid_list):
                max_length = len(qid_list)
            qids_partial = qid_list[0:max_length]
            qids_partial = vcfcli.tools.filter_alternate_alleles(qids_partial)
            genompos_str = ','.join(qids_partial)
            gene_names_partial = \
                vcfcli.tools.parse_vcf.extract_annotations_json_part(vcf_lines, config.uta_adapter_srv_prefix,[config.uta_genomic_keys[0]],
                                                                     qids_partial)[config.uta_genomic_keys[0]]
            gene_names_str = ",".join(gene_names_partial)
            query = 'genesymbol=' + gene_names_str + '&genompos=' + genompos_str

            try:
                json_body = req.get_connection(query, self.url_pattern, self.genome_version)

                for json_obj in json_body:
                    if json_obj:
                        #annotations = []

                        if self.qid_key not in json_obj:
                            continue
                        qid = json_obj[self.qid_key]

                        # calculate percentage
                        if json_obj['Score'] != '':
                            json_obj['score_percent'] = int(float(json_obj['Score']) * 100)
                        else:
                            json_obj['score_percent'] = 0
                        #colour = "#00b0d2"
                        colour = "#ce8585"
                        #if float(json_obj["Score"]) < 0.5:
                        #    colour = "#ce8585"
                        json_obj['score_color'] = colour

                        for k in self.extract_keys:
                            if k in json_obj:
                                pass
                                #annotations.append('{}_{}={}'.format(self.srv_prefix, k, json_body[i][k]))

                        try:
                            json_obj.pop('q_id')
                            vcf_lines[qid][self.srv_prefix] = json_obj
                        except:
                            if self.error_logfile is not None:
                                cur_dt = datetime.datetime.now()
                                date_time = cur_dt.strftime("%m/%d/%Y, %H:%M:%S")
                                print(cur_dt, ": error processing variant response: ", qid, ';', traceback.format_exc(), file=self.error_logfile+str(date_time)+'.log')
                            else:
                                print(cur_dt, ": error processing variant response: ", qid, ';', traceback.format_exc())
            except:
                print(": error processing variant response: ;", traceback.format_exc())
                if error_logfile is not None:
                    print("error processing request: ", annotations, file=error_logfile+str(date_time)+'.log')

            for i in range(0,max_length):
                #del gene_names[0] #gene_names.remove(qid)
                #del variant_exchange[0]  #variant_exchange.remove(qid)
                del qid_list[0] # qid_list.remove(qid)
            if len(qid_list) == 0:
                break

        return vcf_lines
