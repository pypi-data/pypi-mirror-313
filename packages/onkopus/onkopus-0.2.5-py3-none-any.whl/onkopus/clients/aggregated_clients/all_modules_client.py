import onkopus.clients.clinvar_client, onkopus.clients.uta_adapter_client


class AllModulesClient:

    def __init__(self, genome_version):
        self.queryid = 'q_id'
        self.genome_version = genome_version

    def process_data(self, biomarker_data):

        # UTA-Adapter
        biomarker_data = vcfcli.onkopus_clients.UTAAdapterClient(self.genome_version).process_data(biomarker_data)

        # Liftover
        biomarker_data = vcfcli.onkopus_clients.LiftOverClient(self.genome_version).process_data(biomarker_data)

        # dbSNP
        biomarker_data = vcfcli.onkopus_clients.DBSNPClient(self.genome_version).process_data(biomarker_data)

        # ClinVar
        biomarker_data = vcfcli.onkopus_clients.ClinVarClient(self.genome_version).process_data(biomarker_data)

        # REVEL
        biomarker_data = vcfcli.onkopus_clients.REVELClient(self.genome_version).process_data(biomarker_data)

        # LoFTool
        biomarker_data = vcfcli.onkopus_clients.LoFToolClient(self.genome_version).process_data(biomarker_data)

        # VUS-Predict
        biomarker_data = vcfcli.onkopus_clients.VUSPredictClient(self.genome_version).process_data(biomarker_data)

        # dbNSFP
        biomarker_data = vcfcli.onkopus_clients.DBNSFPClient(self.genome_version).process_data(biomarker_data)

        # MVP
        biomarker_data = vcfcli.onkopus_clients.MVPClient(self.genome_version).process_data(biomarker_data)

        # OncoKB
        biomarker_data = vcfcli.onkopus_clients.OncoKBClient(self.genome_version).process_data(biomarker_data)

        # CIViC
        biomarker_data = vcfcli.onkopus_clients.CIViCClient(self.genome_version).process_data(biomarker_data)

        # MetaKB
        biomarker_data = vcfcli.onkopus_clients.MetaKBClient(self.genome_version).process_data(biomarker_data)

        # Aggregate evidence data
        biomarker_data = vcfcli.onkopus_clients.AggregatorClient(self.genome_version).process_data(biomarker_data)

        biomarker_data = vcfcli.onkopus_clients.DefaultFeaturesClient(self.genome_version).process_data(biomarker_data)

        return biomarker_data
