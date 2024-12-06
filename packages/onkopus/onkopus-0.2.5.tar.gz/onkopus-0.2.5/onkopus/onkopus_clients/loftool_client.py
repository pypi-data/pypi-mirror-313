import datetime, traceback, copy
import adagenes.tools.parse_vcf
import adagenes.tools.module_requests as req
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
            annotations = adagenes.tools.parse_vcf.extract_annotations_vcf(vcf_lines, keys)
        else:
            keys = [config.uta_genomic_keys[0]]
            annotations = adagenes.tools.parse_vcf.extract_annotations_json(vcf_lines, config.uta_adapter_srv_prefix, keys)

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
            qids_partial = adagenes.tools.filter_alternate_alleles(qids_partial)
            genompos_str = ','.join(qids_partial)
            gene_names_partial = \
                adagenes.tools.parse_vcf.extract_annotations_json_part(vcf_lines, config.uta_adapter_srv_prefix,[config.uta_genomic_keys[0]],
                                                                     qids_partial)[config.uta_genomic_keys[0]]
            gene_names_str = ",".join(gene_names_partial)
            q = 'genesymbol=' + gene_names_str + '&genompos=' + genompos_str

            vcf_lines = adagenes.processing.parse_http_responses.parse_module_response(q, vcf_lines, self.url_pattern,
                                                                                     self.genome_version,
                                                                                     self.srv_prefix)

            for i in range(0,max_length):
                #del gene_names[0] #gene_names.remove(qid)
                #del variant_exchange[0]  #variant_exchange.remove(qid)
                del qid_list[0] # qid_list.remove(qid)
            if len(qid_list) == 0:
                break

        return vcf_lines
