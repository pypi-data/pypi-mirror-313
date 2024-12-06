import os, configparser

# read in config.ini
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '', 'config.ini'))

def get_config(client_config=None):
    if client_config is None:
        return config
    else:
        # Merge client configuration and default configuration
        return config | client_config

if "ONKOPUS_MODULE_SERVER" in os.environ:
    __MODULE_SERVER__ = os.getenv("ONKOPUS_MODULE_SERVER")
    print("Onkopus module server: ",__MODULE_SERVER__)
else:
    __MODULE_SERVER__ = config['DEFAULT']['ONKOPUS_MODULE_SERVER']

if "ONKOPUS_MODULE_PROTOCOL" in os.environ:
    __MODULE_PROTOCOL__ = os.getenv("ONKOPUS_MODULE_PROTOCOL")
    print("Onkopus module protocol: ",__MODULE_PROTOCOL__)
else:
    __MODULE_PROTOCOL__ = config['DEFAULT']['ONKOPUS_MODULE_PROTOCOL']

#if "MODULE_PROTOCOL" in os.environ:
#    __MODULE_PROTOCOL__ = os.getenv("MODULE_PROTOCOL")
#else:
#    __MODULE_PROTOCOL__ = config['DEFAULT']['MODULE_PROTOCOL']

if "ONKOPUS_PORTS_ACTIVE" in os.environ:
    __PORTS_ACTIVE__ = os.getenv("ONKOPUS_PORTS_ACTIVE")
    print("Onkopus module ports active: ",__PORTS_ACTIVE__)
else:
    __PORTS_ACTIVE__ = config['DEFAULT']['ONKOPUS_PORTS_ACTIVE']

if "ONKOPUS_PROXY_PORT" in os.environ:
    __PROXY_PORT__ = os.getenv("ONKOPUS_PROXY_PORT")
else:
    __PROXY_PORT__ = config['DEFAULT']['ONKOPUS_PROXY_PORT']

if "ONKOPUS_SYS_DIR" in os.environ:
    __DATA_DIR_SYS__ = os.getenv('ONKOPUS_SYS_DIR')
else:
    __DATA_DIR_SYS__ = config['DEFAULT']['ONKOPUS_SYS_DIR']

if "ONKOPUS_DATA_DIR" in os.environ:
    __DATA_DIR__ = os.getenv('ONKOPUS_DATA_DIR')
else:
    __DATA_DIR__ = config['DEFAULT']['ONKOPUS_DATA_DIR']

if "ONKOPUS_DATA_DIR_PUB" in os.environ:
    __DATA_DIR_PUB__ = os.getenv('ONKOPUS_DATA_DIR_PUB')
else:
    __DATA_DIR_PUB__ = config['DEFAULT']['ONKOPUS_DATA_DIR_PUB']

__ID_FILE__= __DATA_DIR__ + "/ids.txt"
__ID_FILE_PUB__= __DATA_DIR_PUB__ + "/ids.txt"
__FEATURE_FILE__= "features.csv"
__META_FILE__="meta.csv"
__UPLOAD_FILE__="files.csv"
__HIST_FILE__="history.csv"

__ACTIVE_MODULES__ = config['DEFAULT']['ACTIVE_MODULES'].split(",")

__FEATURE_GENE__ = 'gene_name'
__FEATURE_VARIANT__ = 'variant_exchange'
__FEATURE_QID__ = 'q_id'

__VCF_FILE__ = 'variants.vcf.gz'
__VCF_FILTERED_FILE__ = 'filtered.vcf.gz'
__VCF_ANNOTATED_FILE__ = 'annotated.vcf.gz'

if "LIFTOVER_DATA_DIR" in os.environ:
    __LIFTOVER_DATA_DIR__ = os.getenv('LIFTOVER_DATA_DIR')
else:
    #__LIFTOVER_DATA_DIR__ = config['DEFAULT']['LIFTOVER_DATA_DIR']
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    __LIFTOVER_DATA_DIR__ = __location__ + '/data'

__LIFTOVER_FILE_HG38 = "hg38ToHg19.over.chain.gz"
__LIFTOVER_FILE_HG19 = "hg19ToHg38.over.chain.gz"


__location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
__LOGFILE__ = __location__ + '/error.log'

#if "MODULE_SERVER" in os.environ:
#    __MODULE_SERVER__ = os.getenv("MODULE_SERVER")
#else:
#    __MODULE_SERVER__ = config['DEFAULT']['MODULE_SERVER']

#if "PORTS_ACTIVE" in os.environ:
#    __PORTS_ACTIVE__ = os.getenv("PORTS_ACTIVE")
#else:
#    __PORTS_ACTIVE__ = config['DEFAULT']['PORTS_ACTIVE']

if "SYS_DIR" in os.environ:
    __DATA_DIR_SYS__ = os.getenv('SYS_DIR')
else:
    __DATA_DIR_SYS__ = config['DEFAULT']['SYS_DIR']

# MODULE PORTS
__PORT_DBSNP__ = ':8090'
__PORT_CLINVAR__ = ':8092'
__PORT_METAKB__ = ':8100'
__PORT_UTAADAPTER__ = ':8084'
__PORT_REVEL__ = ':8096'
__PORT_LOFTOOL__ = ':8094'
__PORT_VUSPREDICT__ = ':9000'
__PORT_MVP__ = ':10108'
__PORT_CIVIC__ = ':10106'
__PORT_ONCOKB__ = ':10112'
__PORT_ONKOPUS_AGGREGATOR__ = ':10110'
__PORT_ONKOPUS_INTERPRETER__ = ':10114'
__PORT_ONKOPUS_PLOTS__ = ':10116'
__PORT_PRIMATEAI__ = ':10120'
__PORT_DBNSFP__ = ':10122'
__PORT_DRUGCLASS__ = ':11010'
__PORT_GENCODE__ = ':10132'
__PORT_DGIDB_DB__ = ':10148'
__PORT_DGIDB_ADAPTER__ = ':10150'
__PORT_ALPHAMISSENSE__ = ':10162'
__PORT_PROTEIN_MODULE__ = ':10400'
__PORT_ONKOPUS_WEB__ = ':10102'
__PORT_COSMIC__ = ':10136'
__PORT_SCANNET__ = ':10166'
__PORT_ONKOPUS_SERVER__ = ':10100'
__PORT_MOLECULAR_FEATURES__ = ':10174'
__PORT_GE_MODULE__ = ':10180'

if __PORTS_ACTIVE__ != "1":
    __PORT_DBSNP__ = ''
    __PORT_CLINVAR__ = ''
    __PORT_METAKB__ = ''
    __PORT_UTAADAPTER__ = ''
    __PORT_REVEL__ = ''
    __PORT_LOFTOOL__ = ''
    __PORT_VUSPREDICT__ = ''
    __PORT_MVP__ = ''
    __PORT_CIVIC__ = ''
    __PORT_ONCOKB__ = ''
    __PORT_ONKOPUS_AGGREGATOR__ = ''
    __PORT_ONKOPUS_INTERPRETER__ = ''
    __PORT_PRIMATEAI__ = ''
    __PORT_DBNSFP__ = ''
    __PORT_DRUGCLASS__ = ''
    __PORT_GENCODE__ = ''
    __PORT_ALPHAMISSENSE__ = ''
    __PORT_PROTEIN_MODULE__ = ''
    __PORT_ONKOPUS_WEB__ = ''
    __PORT_ONKOPUS_PLOTS__ = ''
    __PORT_COSMIC__ = ''
    __PORT_SCANNET__ = ''
    __PORT_ONKOPUS_SERVER__ = ''
    __PORT_MOLECULAR_FEATURES__ = ''
    __PORT_GE_MODULE__ = ''
elif __PROXY_PORT__ != "":
    __PORT_DBSNP__ = __PROXY_PORT__
    __PORT_CLINVAR__ = __PROXY_PORT__
    __PORT_METAKB__ = __PROXY_PORT__
    __PORT_UTAADAPTER__ = __PROXY_PORT__
    __PORT_REVEL__ = __PROXY_PORT__
    __PORT_LOFTOOL__ = __PROXY_PORT__
    __PORT_VUSPREDICT__ = __PROXY_PORT__
    __PORT_MVP__ = __PROXY_PORT__
    __PORT_CIVIC__ = __PROXY_PORT__
    __PORT_ONCOKB__ = __PROXY_PORT__
    __PORT_ONKOPUS_AGGREGATOR__ = __PROXY_PORT__
    __PORT_ONKOPUS_INTERPRETER__ = __PROXY_PORT__
    __PORT_PRIMATEAI__ = __PROXY_PORT__
    __PORT_DBNSFP__ = __PROXY_PORT__
    __PORT_DRUGCLASS__ = __PROXY_PORT__
    __PORT_GENCODE__ = __PROXY_PORT__
    __PORT_ALPHAMISSENSE__ = __PROXY_PORT__
    __PORT_PROTEIN_MODULE__ = __PROXY_PORT__
    __PORT_ONKOPUS_WEB__ = __PROXY_PORT__
    __PORT_ONKOPUS_PLOTS__ = __PROXY_PORT__
    __PORT_COSMIC__ = __PROXY_PORT__
    __PORT_SCANNET__ = __PROXY_PORT__
    __PORT_ONKOPUS_SERVER__ = __PROXY_PORT__
    __PORT_MOLECULAR_FEATURES__ = __PROXY_PORT__
    __PORT_GE_MODULE__ = __PROXY_PORT__

__FEATURE_GENE__ = 'gene_name'
__FEATURE_VARIANT__ = 'variant_exchange'
__FEATURE_QID__ = 'q_id'

error_logfile = __DATA_DIR_SYS__ + 'error'
concat_char = "_"
vcf_header_key = 'vcf_header'
variant_data_key = 'variant_data'

# Molecular features
molecular_features_info_lines= [
        '##INFO=<ID=Molecular features,Number=1,Type=String,Description="Molecular features of amino acid exchange">',
    ]
molecular_features_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_MOLECULAR_FEATURES__ + "/molecular-features/v1/MolecularFeatures"
molecular_features_srv_prefix= "Molecular features"
molecular_features_keys = [ 'position' ]
molecular_features_response_keys= []

# Onkopus Interpreter
onkopus_interpreter_info_lines= [
        '##INFO=<ID=Onkopus_Interpreter_Score,Number=1,Type=String,Description="Variant classification score">',
    ]
onkopus_interpreter_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_ONKOPUS_INTERPRETER__ + "/onkopus-interpreter/v1/compute_pathogenicity_prediction"
onkopus_interpreter_srv_prefix= "Onkopus_Interpreter"
onkopus_interpreter_keys = [ 'position' ]
onkopus_interpreter_response_keys= []

# Onkopus Aggregator
onkopus_aggregator_info_lines=[
        '##INFO=<ID=Onkopus_Aggregator,Number=1,Type=String,Description="">',
    ]
onkopus_aggregator_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_ONKOPUS_AGGREGATOR__ + "/onkopus-aggregator/v1/aggregate_treatment_data"
onkopus_aggregator_srv_prefix= "onkopus_aggregator"
onkopus_aggregator_keys = [ 'position' ]
onkopus_aggregator_response_keys= []

# UTA Adapter
uta_adapter_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_UTAADAPTER__ + "/CCS/v1/GenomicToGene/{}/"
uta_genomic_keys = ['gene_name', 'variant_exchange', 'input_data', 'transcript', 'variant', 'variant_exchange_long']
uta_gene_keys = ['results_string']
uta_gene_response_keys = ['chr', 'start', 'ref', 'var', 'input_data']
uta_adapter_genetogenomic_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_UTAADAPTER__ + "/CCS/v1/GeneToGenomic/{}/"
uta_adapter_info_lines = [
        '##INFO=<ID=UTA-Adapter-GeneName,Number=1,Type=String,Description="Gene name of genomic location">',
        '##INFO=<ID=UTA-Adapter-VariantExchange,Number=1,Type=Float,Description="Variant exchange of a genomic location">'
    ]
uta_adapter_srv_prefix = 'UTA_Adapter'
uta_adapter_genetogenomic_srv_prefix = 'UTA_Adapter_gene'
uta_adapter_genetogenomic_gene_prefix = 'Gene'
uta_adapter_genetogenomic_variant_prefix = 'Variant'

uta_adapter_liftover_srv_prefix = "UTA_Adapter_liftover"
uta_adapter_liftover_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_UTAADAPTER__ + "/CCS/v1/liftover/{}/"
uta_adapter_liftover_info_lines = [
        '##INFO=<ID=UTA-Adapter-LiftOver,Number=1,Type=String,Description="Reference Genome LiftOver">'
    ]
uta_liftover_gene_keys = [ 'position' ]
uta_liftover_response_keys = ['position']

uta_adapter_genefusion_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_UTAADAPTER__ + "/CCS/v1/fusionIsInFrame/{}/"
uta_adapter_genefusion_srv_prefix = 'UTA_Adapter_fusion'

# UTA-Adapter Protein Sequence
uta_adapter_protein_sequence_info_lines = [
        '##INFO=<ID=UTA-Adapter-ProteinSequence,Number=1,Type=String,Description="Protein Sequence of a variant">'
    ]
uta_adapter_protein_sequence_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_UTAADAPTER__ + "/CCS/v1/get_protein_sequence/"
uta_adapter_protein_sequence_srv_prefix = "UTA_Adapter_protein_sequence"

# dbSNP
dbsnp_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_DBSNP__ + "/dbsnp/v1/{}/full?genompos="
dbsnp_srv_prefix = 'dbsnp'
dbsnp_keys = ['rsID', 'freq_total']
dbsnp_return_keys = ['dbsnpRSID','']
dbsnp_srv_prefix = 'dbsnp'
dbsnp_info_lines = ['##INFO=<ID=dbSNP-rsID,Number=1,Type=String,Description="dbSNP reference ID  (rs or RefSNP)">',
        '##INFO=<ID=dbSNP-total,Number=1,Type=Float,Description="Percentage of the people with this variant">']

# ClinVar
clinvar_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_CLINVAR__ + "/clinvar/v1/{}/full?genompos="
clinvar_keys = ['CLNSIG']
clinvar_srv_prefix = config['MODULES']['CLINVAR_PREFIX']
clinvar_info_lines = ['##INFO=<ID=ClinVar-ClinicalSignificance,Number=1,Type=String,Description="Estimated pathogenicity of genomic alteration">']

# REVEL
revel_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_REVEL__ + "/revel/v1/{}/full?genompos="
revel_srv_prefix = config['MODULES']['REVEL_PREFIX']
revel_keys = ['Score']
revel_response_keys = ['revelScore']
revel_info_lines = ['##INFO=<ID=REVEL_Score,Number=1,Type=String,Description="REVELScore">']

# LoFTool
loftool_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_LOFTOOL__ + "/loftool/v1/{}/full?"
loftool_srv_prefix = config['MODULES']['LOFTOOL_PREFIX']
loftool_keys = ['Score']
loftool_response_keys = ['loftoolScore']
loftool_info_lines = ['##INFO=<ID=LoFTool-Score,Number=1,Type=String,Description="LoFTool-Score">']

# VUS-Predict
vuspredict_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_VUSPREDICT__ + "/VUS/v1/{}/toPipeline?"
vuspredict_srv_prefix = config['MODULES']['VUSPREDICT_PREFIX']
vuspredict_keys = ['FATHMM', 'Missense3D', 'SIFT', 'Score', 'Pipeline']
vuspredict_response_keys = ['vusFATHMM', 'vusMissense3D', 'vusSIFT', 'vusScore', 'vusPipeline']
vuspredict_info_lines = ['##INFO=<ID=VUS-Predict-Score,Number=1,Type=String,Description="VUS-Predict-Score">']

# PrimateAI
primateai_info_lines = ['##INFO=<ID=PrimateAI-Score,Number=1,Type=String,Description="PrimateAI-Score">']
primateai_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_PRIMATEAI__ + "/primateai-adapter/v1/{}/full?genompos="
primateai_srv_prefix = config['MODULES']['PRIMATEAI_PREFIX']
primateai_keys = ['Score']

# AlphaMissense
alphamissense_info_lines = ['##INFO=<ID=AlphaMissense-Score,Number=1,Type=String,Description="AlphaMissense-Score">']
alphamissense_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_ALPHAMISSENSE__ + "/alphamissense/v1/{}/getScore?q="
alphamissense_srv_prefix = config['MODULES']['ALPHAMISSENSE_PREFIX']
alphamissense_keys = ['score']

# OncoKB
oncokb_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_ONCOKB__ + "/oncokb/v1/{}/full?"
oncokb_srv_prefix = config['MODULES']['ONCOKB_PREFIX']
oncokb_keys = []
oncokb_response_keys = []
oncokb_info_lines = [
]

# MetaKB
metakb_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_METAKB__ + "/METAKB/v1/GenomicClinicalEvidence?"
metakb_srv_prefix = config['MODULES']['METAKB_PREFIX']
metakb_keys = ['DB Variants', 'DB diseases', 'Drugs', 'Evidence Label', 'Origin Database', 'References']
metakb_response_keys = ['DBVariants', 'DBdiseases', 'Drugs', 'EvidenceLabel', 'OriginDatabase', 'References']
metakb_info_lines = [
    '##INFO=<ID=MetaKB-DB-Variants,Number=1,Type=String,Description="">',
    '##INFO=<ID=MetaKB-DB-diseases,Number=1,Type=Float,Description="">',
    '##INFO=<ID=MetaKB-Drugs,Number=1,Type=Float,Description="">',
    '##INFO=<ID=MetaKB-Evidence-Label,Number=1,Type=Float,Description="">',
    '##INFO=<ID=MetaKB-Origin-Database,Number=1,Type=Float,Description="">',
    '##INFO=<ID=MetaKB-References,Number=1,Type=Float,Description="">'
]

# MVP
mvp_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_MVP__ + "/mvp-adapter/v1/{}/full?genompos="
mvp_srv_prefix = config['MODULES']['MVP_PREFIX']
mvp_keys = ['Score']
mvp_response_keys = ['mvpScore']
mvp_info_lines = ['##INFO=<ID=MVP-Score,Number=1,Type=String,Description="MVP-Score">']

# dbNSFP
dbnsfp_info_lines = ['##INFO=<ID=dbNSFP,Number=1,Type=String,Description="dbNSFP">']
dbnsfp_srv_prefix = config['MODULES']['DBNSFP_PREFIX']
dbnsfp_extract_keys = []
dbnsfp_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_DBNSFP__ + "/dbnsfp-adapter/v1/{}/full?genompos="
dbnsfp_keys = ['aaref', 'aapos', 'aapos', 'codonpos', 'refcodon', 'rs_dbSNP', 'Interpro_domain','REVEL_score','AlphaMissense_score','ESM1b_score', 'ALFA_Total_AF',
               'ALFA_Total_AN', 'EVE_score', 'Eigen-PC-phred_coding','Ensembl_geneid', 'Ensembl_proteinid',
               'Ensembl_transcriptid',
               'ExAC_AC', 'Exac_AF', 'FATHMM_score', 'GENCODE_basic', 'GERP++_NR', 'GERP++_RS',
               'GTEx_V8_gene', 'GTEx_V8_tissue', 'LIST-S2_pred', 'M-CAP_pred', 'MPC_score', 'MVP_score',
               'MetaLR_score', 'MetaSVM_pred', 'MutPred_score', 'MutationAssessor_score', 'Mutation_Assessor_pred',
               'PROVEAN_pred', 'PrimateAI_pred', 'PrimateAI_score', 'SIFT_pred', 'SIFT_score',
               'Uniprot_acc', 'Uniprot_entry', 'VARITY_ER_LOO_score', 'VEST4_score', 'gMVP_score',
               'gnomAD_exomes_AC', 'gnomAD_exomes_AF'
               ]

## Clinical Evidence Data

# CIViC
civic_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_CIVIC__ + "/civic-adapter/v1/{}/GenomicClinicalEvidence?q="
civic_gene_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_CIVIC__ + "/civic-adapter/v1/{}/GeneClinicalEvidence?q="
civic_srv_prefix = 'civic'
civic_keys = ['Interpretations']
civic_response_keys = ['civicData']
civic_info_lines = ['##INFO=<ID=CIViC variant interpretations,Number=1,Type=String,Description="CIViC variant interpretations">']

# DrugClass-Adapter
drugclass_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_DRUGCLASS__ + "/drugon2/v1/drugclass/"
drugclass_srv_prefix = 'drugclass'
drugclass_keys = ['DrugClass']
drugclass_response_keys = ['DrugClasses']
drugclass_info_lines = ['##INFO=<ID=Drug Classes,Number=1,Type=String,Description="Generated drug classes from DrugOn">']

# GENCODE-Adapter
gencode_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_GENCODE__ + "/gencode/v1/{}/GeneFunctionalElements"
gencode_genomic_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_GENCODE__ + "/gencode/v1/{}/GenomicFunctionalRegions"
gencode_mane_select_transcript_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_GENCODE__ + "/gencode/v1/{}/getMANESelectTranscript"
gencode_srv_prefix = 'gencode'
gencode_genomic_srv_prefix = 'gencode_genomic'
gencode_mane_select_transcript_srv_prefix = 'gencode_mane_select'
gencode_keys = ['Gencode']
gencode_info_lines = ['##INFO=<ID=Gencode,Number=1,Type=String,Description="Functional element within a gene">']

# DGIdb
dgidb_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_DGIDB_ADAPTER__ + "/dgidb/v1/GeneInteractions"
#dgidb_genomic_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_GENCODE__ + "/dgidb/v1/GenomicFunctionalRegions"
dgidb_srv_prefix = 'dgidb'
#dgidb_genomic_srv_prefix = 'gencode_genomic'
dgidb_keys = ['DGIdb']
dgidb_info_lines = ['##INFO=<ID=DGIdb,Number=1,Type=String,Description="Drug-gene interactions">']

# Protein module
protein_module_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_PROTEIN_MODULE__ + "/protein_module/v1/plot/"
protein_module_annotations_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_PROTEIN_MODULE__ + "/protein_module/v1/plot_with_added_annotation_post"
protein_module_pdb_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_PROTEIN_MODULE__ + "/protein_module/v1/get_PDB_file"
protein_module_features_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_PROTEIN_MODULE__ + "/protein_module/v1/get_features_at_mutation_point"
protein_module_pdb_openfold_wt_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_PROTEIN_MODULE__ + "/protein_module/v1/get_PDB_file_openfold_wt"
protein_module_pdb_openfold_mutated_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_PROTEIN_MODULE__ + "/protein_module/v1/get_PDB_file_openfold_mutated"


# Gene expression
ge_module_info_lines= []
ge_module_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_GE_MODULE__ + "/gtex/v1/MedianExpressionPerTissue"
ge_module_srv_prefix= "gtex"
ge_module_keys = [ 'position' ]
ge_module_response_keys= []
# Gene expression plots
ge_plot_module_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_GE_MODULE__ + "/gtex/v1/MedianExpressionPerTissuePlot"



# COSMIC
cosmic_info_lines = ['##INFO=<ID=COSMIC,Number=1,Type=String,Description="COSMIC">']
cosmic_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_COSMIC__ + "/cosmic/v1/{}/GeneCensus"
cosmic_srv_prefix = 'cosmic'
cosmic_keys = ['cosmic']

# Plots
onkopus_plots_info_lines= []
onkopus_plots_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_ONKOPUS_PLOTS__ + "/onkopus-plots/v1/plot_data/"
onkopus_plots_srv_prefix= "onkopus-plots"
onkopus_plots_keys = [ 'position' ]
onkopus_plots_response_keys= []

# Scannet
scannet_info_lines= []
scannet_src = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_SCANNET__ + "/scannet/v1/{}/getBindingSitePrediction?protein="
scannet_srv_prefix= "scannet"
scannet_keys = [ 'binding-site-predictions' ]
scannet_response_keys= []

# Onkopus Server
onkopus_server_info_lines = []
onkopus_server_src_upload = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_ONKOPUS_SERVER__ + "/onkopus-server/v1/upload_variant_data"
onkopus_server_src_analyze_id = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_ONKOPUS_SERVER__ + "/onkopus-server/v1/analyze_variants"
onkopus_server_src_analyze_variant_request = __MODULE_PROTOCOL__ + "://" + __MODULE_SERVER__ + __PORT_ONKOPUS_SERVER__ + "/onkopus-server/v1/analyze_variant_request"
onkopus_server_srv_prefix = "onkopus-server"
onkopus_server_keys = []

# All modules client
all_modules_keys = [
    uta_genomic_keys,
    clinvar_keys,
    dbsnp_keys,
    dbnsfp_keys
]
all_modules_srv_prefix = [ "UTA_Adapter","clinvar", "dbsnp", "dbnsfp" ]

def generate_vcf_keys():
    vcf_extract_keys = []

    # UTA-Adapter
    for feature_key in uta_genomic_keys:
        vcf_extract_keys.append(uta_adapter_srv_prefix + "_" + feature_key)

    # dbSNP
    for feature_key in dbsnp_keys:
        vcf_extract_keys.append(dbsnp_srv_prefix + "_" + feature_key)

    # ClinVar
    for feature_key in clinvar_keys:
        vcf_extract_keys.append(clinvar_srv_prefix + "_" + feature_key)

    # REVEL
    for feature_key in revel_keys:
        vcf_extract_keys.append(revel_srv_prefix + "_" + feature_key)

    #LoFTool
    for feature_key in loftool_response_keys:
        vcf_extract_keys.append(loftool_srv_prefix + "_" + feature_key)

    # VUS-Predict
    for feature_key in vuspredict_response_keys:
        vcf_extract_keys.append(vuspredict_srv_prefix + "_" + feature_key)

    return vcf_extract_keys

vcf_extract_keys = generate_vcf_keys()

onkopus_modules = { dbsnp_srv_prefix: { "rsID": "", "freq_total": "" },
                    clinvar_srv_prefix: { "clinical_significance": "" },
                    uta_adapter_srv_prefix: { "gene_name": "", "variant_exchange": "" },
                    uta_adapter_genetogenomic_srv_prefix: {},
                    revel_srv_prefix: { "Score": "" },
                    loftool_srv_prefix: { "Score": ""},
                    vuspredict_srv_prefix: { "Score": ""},
                    metakb_srv_prefix: {},
                    mvp_srv_prefix: { "Score": "" },
                    primateai_srv_prefix: { "Score": ""},
                    dbnsfp_srv_prefix: { "aaref": "", "aaalt": "" },
                    civic_srv_prefix: { },
                    oncokb_srv_prefix: { "mutationEffect": { "knownEffect": "" }, "treatments": []},
                    onkopus_aggregator_srv_prefix : { "aggregated_evidence_data":{}
                        ,"meta": { "total_number_of_results":"" } },
                    variant_data_key: { "info_features": { "AF":"" } }
                  }

extract_keys_list = config["VCF"]["EXTRACT_KEYS"].split(" ")
extract_keys = {}
extract_keys[uta_adapter_genetogenomic_srv_prefix] = ["hgnc_symbol","aminoacid_exchange"]
extract_keys[uta_adapter_srv_prefix] = ["gene_name","variant_exchange"]
extract_keys[revel_srv_prefix] = ["Score"]
extract_keys[dbnsfp_srv_prefix] = ["SIFT_pred"]
extract_keys[vuspredict_srv_prefix] = ["FATHMM","Missense3D","SIFT","Score"]
extract_keys[dbsnp_srv_prefix] = ["rsID", "freq_total"]

for assign in extract_keys_list:
    key,vals = assign.split(":")
    extract_keys[key] = vals.split(",")

# TSV writer feature keys
#tsv_columns = [ civic_srv_prefix, oncokb_srv_prefix, metakb_srv_prefix, revel_srv_prefix, loftool_srv_prefix,
#                vuspredict_srv_prefix, dbsnp_srv_prefix, clinvar_srv_prefix, mvp_srv_prefix,
#                dbsnp_srv_prefix, loftool_srv_prefix, uta_adapter_srv_prefix, uta_adapter_genetogenomic_srv_prefix ]

#tsv_columns = [ civic_srv_prefix, oncokb_srv_prefix, metakb_srv_prefix, revel_srv_prefix, loftool_srv_prefix,
#                vuspredict_srv_prefix, dbsnp_srv_prefix, clinvar_srv_prefix, mvp_srv_prefix,
#                dbsnp_srv_prefix, loftool_srv_prefix, uta_adapter_srv_prefix, uta_adapter_genetogenomic_srv_prefix ]
tsv_mappings = {
                 "variant_data": ["CHROM","POS_hg38","POS_hg19","REF","ALT","type","blosum62"],
                 uta_adapter_srv_prefix: ["gene_name", "variant_exchange", "transcript", "variant_exchange_long"],
                 uta_adapter_genetogenomic_srv_prefix: ["c_dna_string","cds_start","cds_end","strand","prot_location"],
                 uta_adapter_protein_sequence_srv_prefix: ["protein_id", "protein_sequence"],
                 dbnsfp_srv_prefix: ["gnomAD_exomes_AC","gnomAD_exomes_AF","1000Gp3_AF","1000Gp3_AC","ALFA_Total_AF","ALFA_Total_AC",
                                     "ExAC_AC", "ExAC_AF",
                                     "CADD_raw_aggregated_value", "Polyphen2_HDIV_score_aggregated_value", "Polyphen2_HDIV_pred_formatted",
                                     "Polyphen2_HVAR_score_aggregated_value", "Polyphen2_HVAR_pred_formatted",
                                     "SIFT_score_aggregated_value", "SIFT_pred_formatted",
                                     "GERP++_RS", "MetaLR_score", "MetaSVM_score",
                                     "phastCons17way_primate", "phyloP17way_primate",
                                     "MutationAssessor_score_aggregated_value",
                                     "MutationTaster_score_aggregated_value",
                                     "fathmm-MKL_coding_score", "fathmm-XF_coding_score",
                                     "Interpro_domain"
                                     ],
                 revel_srv_prefix: ["Score"],
                 alphamissense_srv_prefix: ["score", "uniprot_id", "alphamissense_class"],
                 mvp_srv_prefix: ["Score"],
                 clinvar_srv_prefix: ["CLNSIG","CLNREVSTAT","CLNDN","CLINVARID"],
                 dbsnp_srv_prefix: ["freq_total", "rsID"],
                 loftool_srv_prefix: ["Score"],
                 vuspredict_srv_prefix: ["Missense3D"],
                 "protein_features": ["DSSP","RSA"]
                 }
vcf_mappings = {
                 uta_adapter_srv_prefix: ["gene_name", "variant_exchange", "transcript", "variant_exchange_long"],
                 uta_adapter_genetogenomic_srv_prefix: ["c_dna_string","cds_start","cds_end","strand","prot_location"],
                 uta_adapter_protein_sequence_srv_prefix: ["protein_id", "protein_sequence"],
                 dbnsfp_srv_prefix: ["gnomAD_exomes_AC","gnomAD_exomes_AF","1000Gp3_AF","1000Gp3_AC","ALFA_Total_AF","ALFA_Total_AC",
                                     "ExAC_AC", "ExAC_AF",
                                     "CADD_raw_aggregated_value", "Polyphen2_HDIV_score_aggregated_value", "Polyphen2_HDIV_pred_formatted",
                                     "Polyphen2_HVAR_score_aggregated_value", "Polyphen2_HVAR_pred_formatted",
                                     "SIFT_score_aggregated_value", "SIFT_pred_formatted", "GERP++_RS", "MetaLR_score", "MetaSVM_score",
                                     "phastCons17way_primate", "phyloP17way_primate",
                                     "MutationAssessor_score_aggregated_value", "MutationTaster_score_aggregated_value",
                                     "fathmm-MKL_coding_score", "fathmm-XF_coding_score",
                                     "Interpro_domain"
                                     ],
                 revel_srv_prefix: ["Score"],
                 alphamissense_srv_prefix: ["score", "uniprot_id", "alphamissense_class"],
                 mvp_srv_prefix: ["Score"],
                 clinvar_srv_prefix: ["CLNSIG","CLNREVSTAT","CLNDN","CLINVARID"],
                 dbsnp_srv_prefix: ["freq_total", "rsID"],
                 loftool_srv_prefix: ["Score"],
                 vuspredict_srv_prefix: ["Missense3D"],
                 "protein_features": ["DSSP","RSA"],
                 "variant_data": ["blosum62"]
                 }

tsv_feature_ranking = ['genomic_location_hg38', 'chrom', 'pos_hg38', 'pos_hg19', 'ref', 'alt', 'mutation_type', 'hgnc_gene_symbol', 'aa_exchange', 'aa_exchange_long', 'ncbi_transcript_mane_select', 'ncbi_cdna_string', 'ncbi_cds_start', 'ncbi_cds_end', 'ncbi_cds_strand', 'ncbi_prot_location', 'ncbi_protein_id', 'clinvar_clinical_significance', 'clinvar_review_status', 'clinvar_cancer_type', 'clinvar_id', 'dbsnp_population_frequency', 'dbsnp_rsid', 'gnomAD_exomes_ac', 'gnomAD_exomes_af', '1000genomes_af', '1000genomes_ac', 'alfa_total_af', 'alfa_total_ac', 'ExAC_AF', 'ExAC_AC', 'revel_score', 'alphamissense_score', 'mvp_score', 'loftool_score', 'vuspredict_score', 'missense3D_pred', 'CADD_score_raw', 'Polyphen2_HDIV_score', 'Polyphen2_HDIV_pred', 'Polyphen2_HVAR_score', 'Polyphen2_HVAR_pred', 'SIFT_score', 'SIFT_pred', 'GERP++_score', 'MetaLR_score', 'MetaSVM_score', 'phastCons17way_primate_score', 'phyloP17way_primate', 'MutationAssessor_score', 'MutationTaster_score', 'fathmm-MKL_coding_score', 'fathmm-XF_coding_score', 'uniprot_id', 'alphamissense_class', 'Interpro_domain', 'protein_sequence_MANE_Select', 'Secondary_protein_structure', 'RelASA', 'BLOSUM62']

tsv_labels = {
    "mutation_type":"variant_data_type",
    "genomic_location_hg38":"qid",
    "chrom":"variant_data_CHROM",
    "pos_hg38":"variant_data_POS_hg38",
    "pos_hg19":"variant_data_POS_hg19",
    "ref":"variant_data_REF",
    "alt":"variant_data_ALT",
    "hgnc_gene_symbol": "UTA_Adapter_gene_name",
    "aa_exchange": "UTA_Adapter_variant_exchange",
    "aa_exchange_long": "UTA_Adapter_variant_exchange_long",
    "ncbi_transcript_mane_select": "UTA_Adapter_transcript",
    "ncbi_cdna_string": "UTA_Adapter_gene_c_dna_string",
    "ncbi_cds_start": "UTA_Adapter_gene_cds_start",
    "ncbi_cds_end": "UTA_Adapter_gene_cds_end",
    "ncbi_cds_strand": "UTA_Adapter_gene_strand",
    "ncbi_prot_location": "UTA_Adapter_gene_prot_location",
    "ncbi_protein_id": "UTA_Adapter_protein_sequence_protein_id",
    "clinvar_clinical_significance": "clinvar_CLNSIG",
    "clinvar_review_status": "clinvar_CLNREVSTAT",
    "clinvar_cancer_type": "clinvar_CLNDN",
    "clinvar_id": "clinvar_CLINVARID",
    "dbsnp_population_frequency": "dbsnp_freq_total",
    "dbsnp_rsid": "dbsnp_rsID",
    "gnomAD_exomes_ac": "dbnsfp_gnomAD_exomes_AC",
    "gnomAD_exomes_af": "dbnsfp_gnomAD_exomes_AF",
    "1000genomes_af": "dbnsfp_1000Gp3_AF",
    "1000genomes_ac": "dbnsfp_1000Gp3_AC",
    "alfa_total_af": "dbnsfp_ALFA_Total_AF",
    "alfa_total_ac": "dbnsfp_ALFA_Total_AC",
    "ExAC_AF": "dbnsfp_ExAC_AF",
    "ExAC_AC": "dbnsfp_ExAC_AC",
    "revel_score": "revel_Score",
    "alphamissense_score": "alphamissense_score",
    "mvp_score": "mvp_Score",
    "loftool_score": "loftool_Score",
    "vuspredict_score": "vus_predict_Score",
    "missense3D_pred": "vus_predict_Missense3D",
    "CADD_score_raw": "dbnsfp_CADD_raw_aggregated_value",
    "Polyphen2_HDIV_score": "dbnsfp_Polyphen2_HDIV_score_aggregated_value",
    "Polyphen2_HDIV_pred": "dbnsfp_Polyphen2_HDIV_pred_formatted",
    "Polyphen2_HVAR_score": "dbnsfp_Polyphen2_HVAR_score_aggregated_value",
    "Polyphen2_HVAR_pred": "dbnsfp_Polyphen2_HVAR_pred_formatted",
    "SIFT_score": "dbnsfp_SIFT_score_aggregated_value",
    "SIFT_pred": "dbnsfp_SIFT_pred_formatted",
    "GERP++_score": "dbnsfp_GERP++_RS",
    "MetaLR_score": "dbnsfp_MetaLR_score",
    "MetaSVM_score": "dbnsfp_MetaSVM_score",
    "phastCons17way_primate_score": "dbnsfp_phastCons17way_primate",
    "phyloP17way_primate": "dbnsfp_phyloP17way_primate",
    "MutationAssessor_score": "dbnsfp_MutationAssessor_score_aggregated_value",
    "MutationTaster_score": "dbnsfp_MutationTaster_score_aggregated_value",
    "fathmm-MKL_coding_score": "dbnsfp_fathmm-MKL_coding_score",
    "fathmm-XF_coding_score": "dbnsfp_fathmm-XF_coding_score",
    "uniprot_id": "alphamissense_uniprot_id",
    "alphamissense_class": "alphamissense_alphamissense_class",
    "Interpro_domain": "dbnsfp_Interpro_domain",
    "protein_sequence_MANE_Select": "UTA_Adapter_protein_sequence_protein_sequence",
    "Secondary_protein_structure": "protein_features_DSSP",
    "RelASA": "protein_features_RSA",
    "BLOSUM62": "variant_data_blosum62"
}

clinical_evidence_mappings = {
    "variant_data": ["CHROM","POS_hg38","POS_hg19","REF","ALT"],
    "onkopus_aggregator": ["merged_evidence_data"]
}

normalized_treatment_features = [ 'gene', 'variant', 'drugs', 'evidence_level', 'evidence_type', 'citation_id', 'reference', 'source' ]

clinical_evidence_match_types = ["exact_match"]
# Match types of clinical evidence data
match_types = ["exact_match","any_mutation_in_gene","same_position","same_position_any_mutation"]
