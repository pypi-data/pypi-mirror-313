import onkopus.clients.uta_adapter_client as client
from adagenes.tools import generate_variant_dictionary
import adagenes.tools.parse_args

description = """
========================================================================================================
  %%%%%%   %    %  %   %   %%%%%%   %%%%%%   %     %   %%%%%%  
 %      %  %%   %  %  %   %      %  %     %  %     %   %
 %      %  % %  %  %%%    %      %  %%%%%%   %     %   %%%%%%
 %      %  %  % %  %  %   %      %  %        %     %        %
  %%%%%%   %   %%  %   %   %%%%%%   %         %%%%%    %%%%%%   
========================================================================================================
"""
#from pyfiglet import Figlet
#f = Figlet(font='slant')
#print f.renderText('Onkopus')

def main():
    infile, outfile, genome_version, itype, otype, error_logfile, module = ocseq.tools.parse_args.parse_args()


    # Variant annotation
    # CCS
    obj = client.UTAAdapterClient(genome_version, error_logfile=error_logfile)
    processor = ocseq.process_files.FileProcessor()
    biomarker_data = processor.process_file(infile, None, obj, genome_version=genome_version, input_format=itype,
                                            output_format=otype, output_type='obj', error_logfile=error_logfile)

    # dbSNP
    obj = ocseq.vcf_clients.dbsnp_client.DBSNPClient(genome_version, error_logfile=error_logfile)
    variants = generate_variant_dictionary(biomarker_data)
    biomarker_data = obj.process_vcf_chunk(biomarker_data, variants, None, input_format='json')

    # ClinVar
    obj = ocseq.vcf_clients.clinvar_client.ClinVarClient(genome_version, error_logfile=error_logfile)
    variants = generate_variant_dictionary(biomarker_data)
    biomarker_data = obj.process_vcf_chunk(biomarker_data, variants, None, input_format='json')

    # REVEL
    obj = ocseq.vcf_clients.revel_client.REVELClient(genome_version, error_logfile=error_logfile)
    variants = generate_variant_dictionary(biomarker_data)
    biomarker_data = obj.process_vcf_chunk(biomarker_data, variants, None, input_format='json')

    # LoFTool
    obj = ocseq.vcf_clients.loftool_client.LoFToolClient(genome_version, error_logfile=error_logfile)
    variants = generate_variant_dictionary(biomarker_data)
    biomarker_data = obj.process_vcf_chunk(biomarker_data, variants, None, input_format='json')

    # VUS-Predict
    obj = ocseq.vcf_clients.vuspredict_client.VUSPredictClient(genome_version, error_logfile=error_logfile)
    variants = generate_variant_dictionary(biomarker_data)
    biomarker_data = obj.process_vcf_chunk(biomarker_data, variants, None, input_format='json')

    # MVP
    obj = ocseq.vcf_clients.mvp_client.MVPClient(genome_version, error_logfile=error_logfile)
    variants = generate_variant_dictionary(biomarker_data)
    biomarker_data = obj.process_vcf_chunk(biomarker_data, variants, None, input_format='json')

    # CIViC
    obj = ocseq.vcf_clients.civic_client.CIViCClient(genome_version, error_logfile=error_logfile)
    variants = generate_variant_dictionary(biomarker_data)
    biomarker_data = obj.process_vcf_chunk(biomarker_data, variants, None, input_format='json')

    # OncoKB
    obj = ocseq.vcf_clients.oncokb_client.ModuleClient(genome_version, error_logfile=error_logfile)
    variants = generate_variant_dictionary(biomarker_data)
    biomarker_data = obj.process_vcf_chunk(biomarker_data, variants, None, input_format='json')

    # MetaKB
    obj = ocseq.vcf_clients.metakb_client.MetaKBClient(genome_version, error_logfile=error_logfile)
    variants = generate_variant_dictionary(biomarker_data)
    biomarker_data = obj.process_vcf_chunk(biomarker_data, variants, None, input_format='json')

    #print(biomarker_data)
    # Export biomarker data
    if otype == 'tsv':
        ocseq.export_data(biomarker_data, outfile)
        outfile.close()

if __name__ == "__main__":
    main()
