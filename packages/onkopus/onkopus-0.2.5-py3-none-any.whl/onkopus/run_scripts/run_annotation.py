import adagenes.tools.parse_args

def main():
    infile, outfile, genome_version, itype, otype, error_logfile, module = adagenes.tools.parse_args.parse_args()

    if module == 'ccs':
        obj = adagenes.onkopus_clients.uta_adapter_client.UTAAdapterClient(genome_version, error_logfile=error_logfile)
    elif module=='dbsnp':
        obj = adagenes.onkopus_clients.dbsnp_client.DBSNPClient(genome_version, error_logfile=error_logfile)
    elif module == 'clinvar':
        obj = adagenes.onkopus_clients.clinvar_client.ClinVarClient(genome_version, error_logfile=error_logfile)
    elif module == 'revel':
        obj = adagenes.onkopus_clients.revel_client.REVELClient(genome_version, error_logfile=error_logfile)
    elif module == 'loftool':
        obj = adagenes.onkopus_clients.loftool_client.LoFToolClient(genome_version, error_logfile=error_logfile)
    elif module == 'vuspredict':
        obj = adagenes.onkopus_clients.vuspredict_client.VUSPredictClient(genome_version, error_logfile=error_logfile)
    elif module=='oncokb':
        obj = adagenes.onkopus_clients.oncokb_client.ModuleClient(genome_version, error_logfile=error_logfile)
    elif module=='civic':
        obj = adagenes.onkopus_clients.civic_client.CIViCClient(genome_version, error_logfile=error_logfile)
    elif module=='metakb':
        obj = adagenes.onkopus_clients.metakb_client.MetaKBClient(genome_version, error_logfile=error_logfile)
    else:
        # Full workflow
        obj = adagenes.onkopus_clients.all_modules_client.ModuleClient(genome_version, error_logfile=error_logfile)

    processor = adagenes.process_files.FileProcessor()
    processor.process_file(infile, outfile, obj, genome_version=genome_version, input_format=itype, output_format=otype, error_logfile=error_logfile)

if __name__ == "__main__":
    main()
