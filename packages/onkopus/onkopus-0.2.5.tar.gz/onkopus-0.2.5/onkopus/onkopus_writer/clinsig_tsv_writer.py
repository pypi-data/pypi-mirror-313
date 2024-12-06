import os, traceback, copy, gzip
import pandas as pd
import adagenes
import adagenes.conf.read_config as conf_reader


class ClinSigWriter():
    """
    Export treatment data on the clinical significance of potential treatments
    """

    def export_feature_results_lv2(self, biomarker_data, record_path=None, meta=None) -> pd.DataFrame:
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
        for var in biomarker_data.keys():
            if "UTA_Adapter" in biomarker_data[var].keys():
                try:
                    df = pd.json_normalize(data=biomarker_data[var], record_path=record_path, meta=meta, errors='ignore')
                    df_sum = pd.concat([df_sum, df], axis=0)
                except:
                    print(traceback.format_exc())
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

    def write_evidence_data_to_file_all_features(self,bframe,
                                                 databases=None,
                                                 output_file=None,
                                                 format='tsv',
                                                 sep='\t'):
        """
        Writes data on clinical significance on treatments on molecular targets in an output file,
        where each row represents a potential treatment.

        :param variant_data:
        :param databases:
        :param output_file:
        :param format:
        :param sep:
        :return:
        """
        variant_data = bframe.data

        for var in variant_data.keys():
            if "onkopus_aggregator" not in variant_data[var]:
                variant_data[var]["onkopus_aggregator"] = {}
            if "merged_evidence_data" not in variant_data[var]["onkopus_aggregator"]:
                variant_data[var]["onkopus_aggregator"]["merged_evidence_data"] = {}
            if "exact_match" not in variant_data[var]["onkopus_aggregator"]["merged_evidence_data"]:
                variant_data[var]["onkopus_aggregator"]["merged_evidence_data"]["exact_match"] = []
            if "any_mutation_in_gene" not in variant_data[var]["onkopus_aggregator"]["merged_evidence_data"]:
                variant_data[var]["onkopus_aggregator"]["merged_evidence_data"]["any_mutation_in_gene"] = []

            if "UTA_Adapter" not in variant_data[var]:
                variant_data[var]["UTA_Adapter"] = {}
            if "gene_name" not in variant_data[var]["UTA_Adapter"]:
                variant_data[var]["UTA_Adapter"]["gene_name"] = ""
            if "variant_exchange" not in variant_data[var]["UTA_Adapter"]:
                variant_data[var]["UTA_Adapter"]["variant_exchange"] = ""

        #record_path = [
        #    ["onkopus_aggregator", "merged_evidence_data",
        #        "exact_match"]]
        record_path = [["onkopus_aggregator", "merged_match_types_data"]]
        meta = [["UTA_Adapter", "gene_name"], ["UTA_Adapter", "variant_exchange"]]

        # exact match
        df = self.export_feature_results_lv2(copy.copy(variant_data), record_path=record_path, meta=meta)

        # any mutation in gene
        #record_path = ["onkopus_aggregator", "merged_evidence_data",
        #        "any_mutation_in_gene"]
        #df2 = self.export_feature_results_lv2(copy.copy(variant_data), record_path=record_path, meta=meta)
        #df = pd.concat([df, df2], axis=0)

        for column in df.columns:
            df[column] = df[column].replace("\"","")
            df[column] = df[column].replace("\n", "")
            df[column] = df[column].replace("'", "")
            df[column] = df[column].replace("\t", " ")
            df[column] = df[column].replace(",", "")

        df = self.normalize_values(df)

        header = sep.join(df.columns)
        output_file.write(header + '\n')

        for _, row in df.iterrows():
            line = sep.join(map(str, row.values))  # Convert each value to string and join with commas
            output_file.write(line + '\n')  # Write data row to file


    def normalize_values(self,df):
        for i in range(0,df.shape[0]):
            drug_str = ""
            if "drugs" in df.columns:
                for drug in df.iloc[i,:].loc["drugs"]:
                    if "drug_name" in drug:
                        drug_name = str(drug["drug_name"])
                        drug_str += drug_name + ", "
                drug_str = drug_str.rstrip(", ")
            df.at[i,"drugs"] = drug_str

        return df

    def write_evidence_data_to_file(self,outfile,variant_data,sep="\t"):
        """

        :param outfile:
        :param variant_data:
        :param sep:
        :return:
        """
        fileopen = False
        if isinstance(outfile, str):
            fileopen = True
            file_name, file_extension = os.path.splitext(outfile)
            input_format_recognized = file_extension.lstrip(".")
            if input_format_recognized == "gz":
                outfile = gzip.open(outfile, 'wt')
            else:
                outfile = open(outfile, 'w')

        if isinstance(variant_data, adagenes.BiomarkerFrame):
            variant_data = variant_data.data
        bframe = adagenes.BiomarkerFrame(data=variant_data)
        self.write_evidence_data_to_file_all_features(bframe,output_file=outfile,sep=sep)

        if fileopen is True:
            outfile.close()

    def write_evidence_data_to_file2(self,variant_data, databases=None,output_file=None,format='tsv', sep='\t'):

        if isinstance(variant_data,adagenes.BiomarkerFrame):
            variant_data = variant_data.data

        if databases is None:
            databases = conf_reader.config["DEFAULT"]["ACTIVE_EVIDENCE_DATABASES"].split()

        if format == 'csv':
            sep=','

        if output_file is None:
            print("not output file given")
            return

        print(output_file)
        outfile = open(output_file, 'w')
        line = 'biomarker' + '\t' + 'disease' + '\t' + 'drugs' + '\t' + 'evidence_level' + '\t' + 'citation_id' + '\t' + 'source'
        print(line, file=outfile)

        for var in variant_data.keys():
            #print(variant_data[var].keys())

            #for db in databases:
            if 'onkopus_aggregator' in variant_data[var]:
                    if 'merged_evidence_data' in variant_data[var]['onkopus_aggregator']:
                        print(len(variant_data[var]['onkopus_aggregator']['merged_evidence_data']))
                        for match_type in variant_data[var]['onkopus_aggregator']['merged_evidence_data']:
                            for result in variant_data[var]['onkopus_aggregator']['merged_evidence_data'][match_type]:
                                #print(result)
                                drugs = result['drugs']
                                drug_name = ""
                                for drug in drugs:
                                    #print(drug)
                                    if isinstance(drug, dict):
                                        if "drug_name" in drug:
                                            drug_name += drug["drug_name"] + ","
                                drug_name = drug_name.rstrip(",")
                                line = str(result['biomarker']) + '\t' + str(result['disease']) \
                                       + '\t' + str(drug_name) + '\t' + str(result['evidence_level']) \
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

    def write_to_file(self, outfile, bframe, databases=None, format="tsv", sep="\t"):
        """

        :param output_file:
        :param bframe:
        :param databases:
        :param format:
        :param sep:
        :return:
        """
        isfile=False
        if isinstance(outfile, str):
            outfile = open(outfile, 'w')
            isffle = True

        self.write_evidence_data_to_file_all_features(bframe, output_file=outfile, format=format,
                                                 sep=sep)

        if isfile is True:
            outfile.close()
