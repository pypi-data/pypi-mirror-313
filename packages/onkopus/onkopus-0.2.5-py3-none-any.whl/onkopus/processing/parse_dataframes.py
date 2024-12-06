import traceback
import pandas as pd
import adagenes.conf.read_config as config
from adagenes.tools import parse_genome_position
import onkopus


def parse_dataframe_biomarkers(df: pd.DataFrame, dragen_file:bool = False):
    """

    :param variant_data:
    :param df:
    :param dragen_file:
    :return:
    """
    variant_data = {}
    columns = df.columns
    columns = [x.lower() for x in columns]
    df.columns = columns
    print("columns: ", columns)

    for i in range(0, df.shape[0]):
        key = ''

        if dragen_file:
            chr = df.iloc[i, :].loc["chromosome"]
            pos = df.iloc[i, :].loc["region"]
            ref = df.iloc[i, :].loc["reference"]
            alt = df.iloc[i, :].loc["allele"]
            key = 'chr' + str(chr) + ':' + str(pos) + str(ref) + '>' + str(alt)
            variant_data[key] = {}
            variant_data[key][config.variant_data_key] = {}
            variant_data[key][config.variant_data_key]["CHROM"] = chr
            variant_data[key][config.variant_data_key]["POS"] = pos
            variant_data[key][config.variant_data_key]["REF"] = ref
            variant_data[key][config.variant_data_key]["ALT"] = alt
            variant_data[key]["additional_columns"] = {}
            for j in range(0, (df.shape[1])):
                variant_data[key]["additional_columns"][columns[j]] = df.iloc[i, j]
        elif 'qid' in columns:
            # id_index = columns.index('QID')
            key = df.iloc[i, :].loc["qid"]
            chr, ref_seq, pos, ref, alt = parse_genome_position(key)
            data = {}
            data[config.variant_data_key] = {}
            data[config.variant_data_key]["CHROM"] = chr
            data[config.variant_data_key]["POS"] = pos
            data[config.variant_data_key]["REF"] = ref
            data[config.variant_data_key]["ALT"] = alt
            variant_data[key] = data
        elif ('chrom' in columns) and ('pos' in columns) and ('ref' in columns) and ('alt' in columns):
            chr = df.iloc[i, :].loc["chrom"]
            pos = df.iloc[i, :].loc["pos"]
            ref = df.iloc[i, :].loc["ref"]
            alt = df.iloc[i, :].loc["alt"]
            key = 'chr' + chr + ':' + pos + ref + '>' + alt
            data = {}
            data[config.variant_data_key] = {}
            data[config.variant_data_key]["CHROM"] = chr
            data[config.variant_data_key]["POS"] = pos
            data[config.variant_data_key]["REF"] = ref
            data[config.variant_data_key]["ALT"] = alt
            variant_data[key] = data
        elif ('gene' in columns) and ('variant' in columns):
            print("read data by gene name and amino acid exchange")
            genome_version = "hg38"
            data = {}
            # data[config.variant_data_key] = {}
            gene = df.iloc[i, :].loc["gene"]
            variant = df.iloc[i, :].loc["variant"]
            data[gene + ":" + variant] = {}
            data[gene + ":" + variant][
                config.uta_adapter_genetogenomic_srv_prefix] = {}
            data[gene + ":" + variant][
                config.uta_adapter_genetogenomic_srv_prefix][config.uta_genomic_keys[0]] = gene
            data[gene + ":" + variant][
                config.uta_adapter_genetogenomic_srv_prefix][config.uta_genomic_keys[1]] = variant

            client = onkopus.CCSGeneToGenomicClient(genome_version)
            data = client.process_data(data, input_format='tsv')

            genomic_locations = list(data.keys())
            for genomepos in genomic_locations:
                variant_data[genomepos] = data[genomepos]

                # Add gene and variant data
                variant_data[genomepos]["UTA_Adapter"] = {}
                variant_data[genomepos]["UTA_Adapter"]["gene_name"] = gene
                variant_data[genomepos]["UTA_Adapter"]["variant_exchange"] = variant
        else:
            print("unidentifiable columns: ", columns)
            continue

        # Read existing feature data
        for j, feature in enumerate(columns):
            if key != '':
                if feature not in variant_data[key]:
                    variant_data[key][feature] = {}
                try:
                    if feature in config.tsv_mappings.keys():
                        # if len(elements) > j:
                        #    if elements[j]:
                        # print("assign ",elements,", feature ",feature,",",i,": ",elements[i])

                        #variant_data[key][feature][config.tsv_mappings[feature]] = df.iloc[i, j]
                        pass
                    else:
                        variant_data[key][feature] = df.iloc[i, j]
                except:
                    variant_data[key][feature] = ''
                    print("error adding feature (TSV)")
                    print(traceback.format_exc())

    return variant_data


def is_dragen_file(columns):
    """
    Detects whether an Excel file is in DRAGEN format

    :param columns:
    :return:
    """
    dragen_columns = ['Chromosome', 'Region', 'Type', 'Reference', 'Allele', 'Coverage', 'Frequency', 'Exact match', 'AF',
                          'EUR_AF 1000GENOMES-phase_3_ensembl_v91_o', 'AF_EXAC clinvar_20171029_o', 'CLNSIG clinvar_20171029_o',
                          'RS clinvar_20171029_o', 'Homo_sapiens_refseq_GRCh38_p9_o_Genes', 'Coding region change',
                          'Amino acid change', 'Splice effect', 'mRNA Accession', 'Exon Number', 'dbSNP']
    if len(columns) > 6:
        #print([x for x in columns[0:5] if x in dragen_columns[0:5]])
        if len([x for x in columns[0:5] if x in dragen_columns[0:5]]) == 5:
            print("DRAGEN file detected")
            return True
    print("Could not detect DRAGEN file ",columns)
    return False

