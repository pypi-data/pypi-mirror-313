
tag = "develop"

available_modules = ["dbsnp","clinvar","ccs","ccs_gene","alphamissense","revel","mvp","primateai","gencode","dbnsfp","civic","oncokb",
                     "metakb","loftool","vuspredict","ccs_protein","drug_classification","treatments",""]

module_ids = {
    "dbsnp": "docker.gitlab.gwdg.de/ukeb/mtb/onkopus-modules/snpservice",
    "clinvar": "docker.gitlab.gwdg.de/ukeb/mtb/onkopus-modules/clinvar-service",
    "uta": "docker.gitlab.gwdg.de/ukeb/mtb/onkopus-modules/utaadapter",
    "fathmm": "docker.gitlab.gwdg.de/ukeb/mtb/vus-predict/fathmmadapter",
    "m3d": "docker.gitlab.gwdg.de/ukeb/mtb/vus-predict/m3dadapter",
    "uniprot": "docker.gitlab.gwdg.de/ukeb/mtb/vus-predict/uniprotfetcher",
    "vep": "docker.gitlab.gwdg.de/ukeb/mtb/vus-predict/vepadapter",
    "vus-predict": "docker.gitlab.gwdg.de/ukeb/mtb/vus-predict/vuspredict",
    "revel": "docker.gitlab.gwdg.de/ukeb/mtb/onkopus-modules/variant-scores/revel-adapter",
    "loftool": "docker.gitlab.gwdg.de/ukeb/mtb/onkopus-modules/variant-scores/loftool-service",
    "onkopus-server": "docker.gitlab.gwdg.de/ukeb/mtb/onkopus/onkopus-server",
    "onkopus-web": "docker.gitlab.gwdg.de/ukeb/mtb/onkopus/onkopus-web-frontend",
    "metakb": "docker.gitlab.gwdg.de/ukeb/mtb/onkopus-modules/treatment-databases/metakb-adapter",
    "oncokb": "docker.gitlab.gwdg.de/ukeb/mtb/onkopus-modules/treatment-databases/oncokb-adapter",
    "civic": "docker.gitlab.gwdg.de/ukeb/mtb/onkopus-modules/treatment-databases/civic-adapter",
    "dbnsfp": "docker.gitlab.gwdg.de/ukeb/mtb/onkopus-modules/dbnsfp-adapter",
    "primateai": "docker.gitlab.gwdg.de/ukeb/mtb/onkopus-modules/variant-scores/primateai-adapter",
    "onkopus-database": "docker.gitlab.gwdg.de/ukeb/mtb/onkopus/onkopus-database",
    "onkopus-websocket-server": "docker.gitlab.gwdg.de/ukeb/mtb/onkopus/onkopus-websocket-server",
}


containers = {
    "snpservice": "docker.gitlab.gwdg.de/ukeb/mtb/onkopus-modules/snpservice",
    "clinvar-service": "docker.gitlab.gwdg.de/ukeb/mtb/onkopus-modules/clinvar-service",
    "uta-database": "docker.gitlab.gwdg.de/ukeb/mtb/onkopus-modules/uta-database",
    "uta-adapter": "docker.gitlab.gwdg.de/ukeb/mtb/onkopus-modules/utaadapter",
    "fathmm-adapter": "docker.gitlab.gwdg.de/ukeb/mtb/vus-predict/fathmmadapter",
    "fathmm-db": "docker.gitlab.gwdg.de/ukeb/mtb/vus-predict/fathmm-db",
    "m3d-adapter": "docker.gitlab.gwdg.de/ukeb/mtb/vus-predict/m3dadapter",
    "uniprot-fetcher": "docker.gitlab.gwdg.de/ukeb/mtb/vus-predict/uniprotfetcher",
    "vep-adapter": "docker.gitlab.gwdg.de/ukeb/mtb/vus-predict/vepadapter",
    "vus-predict": "docker.gitlab.gwdg.de/ukeb/mtb/vus-predict/vuspredict",
    "revel-adapter": "docker.gitlab.gwdg.de/ukeb/mtb/onkopus-modules/variant-scores/revel-adapter",
    "loftool-service": "docker.gitlab.gwdg.de/ukeb/mtb/onkopus-modules/variant-scores/loftool-service",
    "onkopus-server": "docker.gitlab.gwdg.de/ukeb/mtb/onkopus/onkopus-server",
    "onkopus-web": "docker.gitlab.gwdg.de/ukeb/mtb/onkopus/onkopus-web-frontend",
    "metakb-adapter": "docker.gitlab.gwdg.de/ukeb/mtb/onkopus-modules/treatment-databases/metakb-adapter",
    "oncokb-adapter": "docker.gitlab.gwdg.de/ukeb/mtb/onkopus-modules/treatment-databases/oncokb-adapter",
    "civic-adapter": "docker.gitlab.gwdg.de/ukeb/mtb/onkopus-modules/treatment-databases/civic-adapter",
    "civic-database": "docker.gitlab.gwdg.de/ukeb/mtb/onkopus-modules/treatment-databases/civic-db",
    "dbnsfp-adapter": "docker.gitlab.gwdg.de/ukeb/mtb/onkopus-modules/dbnsfp-adapter",
    "primateai-adapter": "docker.gitlab.gwdg.de/ukeb/mtb/onkopus-modules/variant-scores/primateai-adapter",
    "onkopus-database": "docker.gitlab.gwdg.de/ukeb/mtb/onkopus/onkopus-database",
    "onkopus-websocket-server": "docker.gitlab.gwdg.de/ukeb/mtb/onkopus/onkopus-websocket-server"
}

