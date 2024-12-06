import traceback, datetime, json
import adagenes.tools.module_requests as req
from onkopus.conf import read_config as config
import adagenes as ag


class MolecularFeaturesClient:

    def __init__(self, genome_version, error_logfile=None):
        self.genome_version = genome_version
        self.info_lines= config.molecular_features_info_lines
        self.url_pattern = config.molecular_features_src
        self.srv_prefix = config.molecular_features_srv_prefix
        self.response_keys = config.molecular_features_response_keys
        self.extract_keys = config.molecular_features_keys

        self.qid_key = "q_id"
        if (self.genome_version == "hg19") or (self.genome_version == "GRCh37"):
            self.qid_key = "q_id_hg19"
        self.error_logfile = error_logfile

    def process_data(self, biomarker_data, tumor_type=None):
        """

        :param biomarker_data:
        :param tumor_type:
        :return:
        """
        try:
            qid_list = []
            genes = []
            variants = []
            for var in biomarker_data.keys():
                if "UTA_Adapter" in biomarker_data[var]:
                    genes.append(biomarker_data[var]["UTA_Adapter"]["gene_name"])
                    variants.append(biomarker_data[var]["UTA_Adapter"]["variant_exchange"])
                    qid_list.append(var)

            qid_lists_query = ag.tools.split_list(qid_list)
            genes_lists_query = ag.tools.split_list(genes)
            variants_lists_query = ag.tools.split_list(variants)

            for qlist, glist, vlist in zip(qid_lists_query, genes_lists_query, variants_lists_query):
                q_genes = ",".join(glist)
                q_variants = ",".join(vlist)
                q_genompos = ",".join(qlist)
                q = "?genompos=" + q_genompos + "&gene=" + q_genes + "&variant=" + q_variants

                res = req.get_connection(q, self.url_pattern, self.genome_version)

                for var in res.keys():
                    biomarker_data[var]["molecular_features"] = res[var]["molecular_features"]

        except:
            if self.error_logfile is not None:
                cur_dt = datetime.datetime.now()
                date_time = cur_dt.strftime("%m/%d/%Y, %H:%M:%S")
                print("error processing request: ", biomarker_data, file=self.error_logfile+str(date_time)+'.log')
            else:
                print(": error processing variant response: ;", traceback.format_exc())

        return biomarker_data
