import traceback
import pandas as pd
import onkopus.conf.read_config as conf_reader
import adagenes

class ClinSigWriter(adagenes.writer.Writer):
    """
    File writer to export data on potential treatments on molecular targets.
    Exports the treatment drugs, their target as well as data on clinical significance of the treatment.

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def write_to_file(self, outfile: str, bframe: adagenes.BiomarkerFrame):
        if isinstance(bframe, dict):
            data = bframe
        else:
            data = bframe.data
            self.write_evidence_data_to_file_all_features(data, output_file=outfile)


    def export_feature_results_lv2(self,biomarker_data, record_path=None, meta=None) -> pd.DataFrame:
        """
        Exports biomarker data in full mode with level 2 meta data

        :param biomarker_data:
        :param outfile_src:
        :param feature:
        :param record_path:
        :param meta:
        :param sep:
        :return:
        """
        df_sum = pd.DataFrame()
        for var in biomarker_data:
            df = pd.json_normalize(data=biomarker_data[var], record_path=record_path, meta=meta)
            df_sum = pd.concat([df_sum, df], axis=0)
            print(df_sum)
        return df_sum

    def fill_in_missing_keys_lv2(self,biomarker_data, struc):

        for var in biomarker_data.keys():
            for key in struc:
                if key not in biomarker_data[var]:
                    biomarker_data[var][key] = {}
                for val in struc[key]:
                    if val not in biomarker_data[var][key]:
                        biomarker_data[var][key][val] = {}

        return biomarker_data

    def write_evidence_data_to_file_all_features(self,variant_data, databases=None,output_file=None,format='tsv', sep='\t'):

        record_path = [
            ["onkopus_aggregator", "merged_match_types_data"]]
        meta = [["UTA_Adapter", "gene_name"], ["UTA_Adapter", "variant_exchange"]]
        df = self.export_feature_results_lv2(variant_data, record_path=record_path, meta=meta)

        df.to_csv(output_file, sep=sep)

    def write_evidence_data_to_file(self,variant_data, databases=None,output_file=None,format='tsv', sep='\t'):
        if databases is None:
            databases = conf_reader.config["DEFAULT"]["ACTIVE_EVIDENCE_DATABASES"].split()

        if format == 'csv':
            sep=','

        if output_file is None:
            print("not output file given")
            return

        outfile = open(output_file, 'w')
        line = 'gene' + '\t' + 'variant' + '\t' + 'disease' + '\t' + 'drugs' + '\t' + 'evidence_level' + '\t' + 'citation_id' + '\t' + 'source'
        print(line, file=outfile)

        for var in variant_data.keys():
            #print(variant_data[var].keys())

            #for db in databases:
            if 'onkopus_aggregator' in variant_data[var]:
                    if 'merged_evidence_data' in variant_data[var]['onkopus_aggregator']:
                        print(len(variant_data[var]['onkopus_aggregator']['merged_evidence_data']))
                        for result in variant_data[var]['onkopus_aggregator']['merged_evidence_data']:
                            line = str(result['gene']) + '\t' + str(result['variant']) + '\t' + str(result['disease']) + '\t' + str(result['drugs']) + '\t' + str(result['evidence_level']) \
                                   + '\t' + str(result['citation_id']) + '\t' + str(result['source'])
                            print(line, file=outfile)
            else:
                    print("no data: ")

        outfile.close()

    def to_single_tsv_line(self, variant_data, srv_prefix, extract_keys):
            tsv_line = ''

            chr_prefix = ""
            if not variant_data[conf_reader.variant_data_key]["CHROM"].startswith("chr"):
                chr_prefix = "chr"
            tsv_line += chr_prefix + variant_data[conf_reader.variant_data_key]["CHROM"] + ':' + \
                        variant_data[conf_reader.variant_data_key]["POS"] \
                        + variant_data[conf_reader.variant_data_key]["REF"] + '>' + variant_data[conf_reader.variant_data_key][
                            "ALT"] + '\t'

            # print("write data to tsv file: ",variant_data)
            tsv_features = conf_reader.tsv_columns
            if self.features is not None:
                tsv_features = self.features

            try:
                # if srv_prefix in variant_data:

                for k in tsv_features:
                    if k in variant_data:
                        if k in conf_reader.tsv_mappings:
                            if conf_reader.tsv_mappings[k] in variant_data[k]:
                                tsv_line += str(variant_data[k][conf_reader.tsv_mappings[k]]) + '\t'
                            else:
                                tsv_line += '\t'
                        else:
                            tsv_line += str(variant_data[k]) + '\t'
                    else:
                        tsv_line += '\t'
                # else:
                #    tsv_line += '\t'
                tsv_line = tsv_line.rstrip("\t")
                # print("return ",tsv_line)
                return tsv_line.rstrip("\t")
            except:
                print(traceback.format_exc())
                return ''
