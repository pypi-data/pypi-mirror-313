import traceback, copy
import vcfcli.tools.module_requests as req
import vcfcli.tools.parse_genomic_data
from onkopus.conf import read_config as config


class LiftOverClient:

    def __init__(self, genome_version, error_logfile=None):
        self.genome_version = genome_version
        self.info_lines = config.uta_adapter_liftover_info_lines
        self.url_pattern = config.uta_adapter_liftover_src
        self.srv_prefix = config.uta_adapter_liftover_srv_prefix
        self.genomic_keys = config.uta_genomic_keys
        self.gene_keys = config.uta_liftover_gene_keys
        self.gene_response_keys = config.uta_liftover_response_keys
        self.extract_keys = config.uta_liftover_gene_keys

        self.qid_key = "q_id"
        if (self.genome_version == "hg19") or (self.genome_version == "GRCh37"):
            self.qid_key = "q_id_hg19"

    def process_data(self, vcf_lines, input_format='json'):

        if input_format == 'vcf':
            keys = ['CHROM', 'POS']
            annotations = vcfcli.tools.parse_vcf.extract_annotations_vcf(vcf_lines, keys,
                                                                         extract_from_info_column=False)
        else:
            keys = ['CHROM', 'POS']
            annotations = vcfcli.tools.parse_vcf.extract_annotations_json(vcf_lines, config.variant_data_key, keys)

        variants = ''
        liftover_qids = []
        qids = []
        chromosomes = annotations[keys[0]]
        positions = annotations[keys[1]]
        qids = annotations['q_id']
        liftover_orig_qids = []

        chromosomes = copy.deepcopy(annotations[keys[0]])
        positions = copy.deepcopy(annotations[keys[1]])
        qid_list = copy.deepcopy(annotations['q_id'])

        #print(len(qid_list),",", len(chromosomes),",", len(positions))

        while True:
            max_length = int(config.config["DEFAULT"]["MODULE_BATCH_SIZE"])
            if max_length > len(qid_list):
                max_length = len(qid_list)
            qids_partial = qid_list[0:max_length]
            #qids_partial = ','.join(vcfcli.tools.filter_alternate_alleles(qids_partial))
            chromosomes_partial = chromosomes[0:max_length]
            positions_partial = positions[0:max_length]
            #chromosomes_partial = vcfcli.tools.parse_vcf.extract_annotations_json_part(vcf_lines, config.variant_data_key, ["CHROM"], qids_partial)["CHROM"]
            #positions_partial = vcfcli.tools.parse_vcf.extract_annotations_json_part(vcf_lines,
            #                                                                           config.variant_data_key, ["POS"],
            #                                                                           qids_partial)["POS"]
            variants = ""
            liftover_qids = []
            liftover_orig_qids = []

            for i, qid in enumerate(qids_partial):
                if config.variant_data_key in vcf_lines[qid]:
                    variants += 'chr' + chromosomes_partial[i] + ':' + positions_partial[i] + ','
                    liftover_qids.append('chr' + chromosomes_partial[i] + ':' + positions_partial[i])
                    liftover_orig_qids.append(qid)
                else:
                    chr, ref_seq, pos, ref, alt = vcfcli.tools.parse_genomic_data.parse_genome_position(qid)
                    liftover_qids.append('chr' + chr + ":" + str(pos))
                    variants += 'chr' + chr + ":" + str(pos) + ','
                    liftover_orig_qids.append(qid)
            variants = variants.rstrip(',')

            try:
                if (self.genome_version == "hg38") or (self.genome_version == "GRCh38"):
                    add_genome = "hg19"
                else:
                    add_genome = "hg38"

                json_body = req.get_connection(variants, self.url_pattern, self.genome_version + ":" + add_genome)

                for result in json_body:
                    qid = result["header"]["qid"]
                    if qid in liftover_qids:
                            index = liftover_qids.index(qid)
                            qid_orig = liftover_orig_qids[index]
                            value = result["data"]
                            if type(value) == type(dict()):
                                vcf_lines[qid_orig][self.srv_prefix] = value

                                if config.variant_data_key not in vcf_lines[qid_orig]:
                                    vcf_lines[qid_orig][config.variant_data_key] = {}
                                    chr, ref_seq, pos, ref, alt = vcfcli.tools.parse_genomic_data.parse_genome_position(qid_orig)
                                    vcf_lines[qid_orig][config.variant_data_key]["CHROM"] = chr
                                    vcf_lines[qid_orig][config.variant_data_key]["REF"] = ref
                                    vcf_lines[qid_orig][config.variant_data_key]["ALT"] = alt

                                pos_orig = qid.split(":")[1]
                                vcf_lines[qid_orig][config.variant_data_key]['POS_' + self.genome_version] = pos_orig

                                try:
                                    if config.variant_data_key in vcf_lines[qid_orig]:
                                        if 'CHROM' in vcf_lines[qid_orig][config.variant_data_key]:

                                            liftover_qid_full = str(value['position'])
                                            vcf_lines[qid_orig][config.variant_data_key][
                                                'POS_' + add_genome] = liftover_qid_full

                                            vcf_lines[qid_orig][config.variant_data_key][
                                                'strand'] = value['strand']

                                            vcf_lines[qid_orig][config.variant_data_key][
                                                'score'] = value['score']
                                except:
                                    print("error: liftover")
                                    print(traceback.format_exc())
            except:
                print("error: liftover")
                print(traceback.format_exc())

            for i in range(0, max_length):
                del chromosomes[0]  # gene_names.remove(qid)
                del positions[0]  # variant_exchange.remove(qid)
                del qid_list[0]  # qid_list.remove(qid)
            if len(qid_list) == 0:
                break

        return vcf_lines
