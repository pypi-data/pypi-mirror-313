import argparse
import os, time, datetime
import onkopus.conf.docker_config as docker_config
import onkopus.conf.read_config as conf_reader
import adagenes as ag
import onkopus.import_data
import onkopus.mtb_requests
import onkopus as op


class OnkopusMain():

    def __init__(self):
        self.__location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.__data_dir__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__))) + "/data"

        self.title = "Onkopus"

        version = op.conf_reader.config["DEFAULT"]["VERSION"]
        self.version = version
        self.__available_modules__ = self._load_available_modules()
        self.module_labels = docker_config.available_modules

        # Load installed modules
        self.installed_modules = self._load_installed_modules()
        self.__docker_compose_file = self.__data_dir__ + "/docker-compose.yml"

        self.formats=["VCF","MAF","CSV","TSV","XLSX","TXT"]

    def _load_available_modules(self):
        return list(docker_config.module_ids.keys())

    def _load_installed_modules(self):
        installed_modules = []

        # Create data directory if it does not exist
        isExist = os.path.exists(self.__data_dir__)
        if not isExist:
            # Create a new directory because it does not exist
            os.makedirs(self.__data_dir__)
            print("Created data directory: ",self.__data_dir__)

        # Create modules file if it does not exist
        if not os.path.exists(self.__data_dir__ + "/" + conf_reader.config["DEFAULT"]["INSTALLED_MODULES_FILE"]):
            file = open(self.__data_dir__ + "/" + conf_reader.config["DEFAULT"]["INSTALLED_MODULES_FILE"], 'w+')
            file.close()
        if not os.path.exists(self.__data_dir__ +
                              "/docker-compose.yml"):
            os.system("cp -v " + self.__location__ + "/conf/docker_compose/docker-compose.yml " + self.__data_dir__ + "/docker-compose.yml")

        file = open(self.__data_dir__ + "/" + conf_reader.config["DEFAULT"]["INSTALLED_MODULES_FILE"], 'r')
        for line in file:
            installed_modules.append(line.strip())
        file.close()

        print("Installed modules: ", installed_modules)

        return installed_modules

    def _add_new_module(self, module):
        with open(self.__data_dir__ + "/" + conf_reader.config["DEFAULT"]["INSTALLED_MODULES_FILE"], "a") as file:
            file.write(module+'\n')

        self.installed_modules.append(module)

    def _db_request(self, pid, module=None, genome_version=None):
        """

        :param pid:
        :param module:
        :param genome_version:
        :return:
        """
        print("Annotate biomarkers of ID: ",pid,", genome version: ", genome_version, ", module: ",module)

        onkopus_server_url = conf_reader.__MODULE_PROTOCOL__ + "://" + conf_reader.__MODULE_SERVER__ + conf_reader.__PORT_ONKOPUS_SERVER__
        onkopus_server_url = onkopus_server_url + "/onkopus-server/v1/analyze_variants"

        onkopus.import_data.annotate_variant_data(pid, onkopus_server_url=onkopus_server_url,
                                        genome_version=genome_version,module=module)

    def _module_request(self, input_file, output_file, module, genome_version=None,
                        input_format=None,output_format=None):
        """
        Annotates a variant file with the defined module and writes the annotated variant file in the file system.
        Directly employs the Onkopus clients, without writing the results in the Onkopus database

        :param input_file:
        :param output_file:
        :param module:
        :param genome_version:
        :return:
        """
        # Get Onkopus client
        #print("Query ", module)
        modules = module.split(",")

        #print("Run Onkopus annotation")
        print("Input file ", input_file)
        #print("Output file ", output_file)

        # Read in input file
        #bframe = onkopus.read_file(input_file, input_format=input_format)

        # Employ CCS GeneToGenomic service if data is in protein format
        #if bframe.data_type == "p":
        #    print("Proteomic data detected: Retrieving genomic locations")
        #    genome_version = "hg38"
        #    client = CCSGeneToGenomicClient(genome_version)
        #    bframe.data = client.process_data(bframe.data, input_format='tsv')

        if (genome_version == "hg19") or (genome_version == "t2t"):
            print("Converting variant data to GRCh38...",genome_version)
            output_file_liftover = input_file + ".GRCh38.avf "
            obj = op.LiftOverClient(genome_version=genome_version,target_genome="hg38")
            ag.process_file(input_file, output_file_liftover, obj, genome_version=genome_version, input_format=input_format,
                            output_format=output_format, error_logfile=None)
            input_file = output_file_liftover
            genome_version = "hg38"
            print("Liftover successful.")

        # Annotate
        for m in modules:
            obj = onkopus.get_onkopus_client(m, genome_version)
            #print("client ", type(client))
            if obj is None:
                print("Error: Onkopus module not found: ", m)
                exit(1)
            if m == "ccs_gene":
                bframe.data = client.process_data(bframe.data,data_type="g")
            else:
                #bframe.data = client.process_data(bframe.data)

                ag.process_file(input_file, output_file, obj, genome_version=genome_version, input_format=input_format,
                                       output_format=output_format, error_logfile=None)

        # Write output file
        #adagenes.write_file(output_file, bframe)
        #adagenes.process_file(input_file, output_file, client,input_format=input_format,output_format=output_format)


    def run_interpretation(self,
                           input_file,
                           output_file,
                           module=None,
                           genome_version=None,
                           pid=None,
                           input_format=None,
                           output_format=None,
                           mode=None
                           ):
        """
        Annotates an input file with the defined module. The annotated file is saved in the given output path

        :param input_file:
        :param output_file:
        :param module:
        :param genome_version:
        :return:
        """
        if mode == "test":
            __location__ = os.path.realpath(
                os.path.join(os.getcwd(), os.path.dirname(__file__)))
            #file = __location__ + '/tests/test_files'
            input_file = __location__ + '/../tests/test_files' + '/' + input_file

        #print("Starting interpretation")
        time_start = time.time()

        # Check input file parameter
        if input_file == '':
            if pid is None:
                print("Error: No input file passed. Please define an input file with the -i option, e.g. onkopus run -i /path/to/file/mutations.vcf.gz")
                exit(1)
            else:
                print("Annotate patient biomarkers: ",pid)
                self._db_request(pid, module=module, genome_version=genome_version)
                exit(0)

        file_name, file_extension = os.path.splitext(input_file)
        input_format_recognized = file_extension.lstrip(".")
        if input_format_recognized == "gz":
            #print("Found .gz file")
            file_name, file_extension = os.path.splitext(file_name)
            input_format_recognized = file_extension.lstrip(".")

        # get output format
        if output_format == "":
            output_format = input_format_recognized
            print("No output format given. Detected input file format: ",file_extension)

        if input_format == "":
            input_format = input_format_recognized
            print("Recognized input format: ",input_format)

        if output_file == '':
            datetime_str = str(datetime.datetime.now())
            output_file = input_file + datetime_str + "_" + ".ann." + output_format
            print("No output file defined. Generated output file path: ", output_file)

        if conf_reader.config["DEFAULT"]["MODE"] == "LOC":
            print("local mode")

            # Check if Onkopus modules are running

        elif conf_reader.config["DEFAULT"]["MODE"] == "PUB":
            print("public mode")

            module_server = conf_reader.__MODULE_PROTOCOL__ + '//' + conf_reader.__MODULE_SERVER__
            print("Module server: ", module_server)


        # Get active modules
        active_modules = []
        try:
            active_modules = conf_reader.config["DEFAULT"]["ACTIVE_MODULES"].split(",")
            print("Active modules: ",active_modules)

        except:
            print("Error: Could not read active modules")
            exit(1)

        # Query all modules if module is set to 'all'
        #if module == 'all':
        #    for module in active_modules:
        #        self.module_request(input_file, output_file, module, genome_version=genome_version)
        #else:
        self._module_request(input_file, output_file, module, genome_version=genome_version,
                             input_format=input_format,output_format=output_format)

        print("File annotated: ",module,", annotations written in: ",output_file)

        time_stop = time.time()
        time_total = (time_stop - time_start)
        print("Annotation time: ",str(time_total))

    def import_data(self,input_file, genome_version=None,data_dir=None):
        """
        Imports an input file or all files within a directory as patient biomarker data in the Onkopus database

        :param input_file:
        :param genome_version:
        :param data_dir:
        :return:
        """
        if (data_dir is not None) and (data_dir != ''):
            # import all files in directory
            pass
        elif input_file != '':
            # import file
            print("Import file: ",input_file)

            onkopus_server_url = conf_reader.__MODULE_PROTOCOL__ + "://" + conf_reader.__MODULE_SERVER__ + conf_reader.__PORT_ONKOPUS_SERVER__
            onkopus_server_url = onkopus_server_url + "/onkopus-server/v1/upload_variant_data"

            pid = onkopus.import_data.import_file(input_file, onkopus_server_url=onkopus_server_url, genome_version=genome_version)
            return pid
        else:
            print("Error: No input file defined. Define an input file or a data directory")

    def install(self, module):
        """
        Installs an Onkopus module

        :param module:
        :return:
        """
        print("Install Onkopus module: ",module)

        # Check if module is already installed
        if module in self.installed_modules:
            print("Module " + module + " is already installed")
            return

        # Download databases
        print(self.__available_modules__)
        if module in self.__available_modules__:
            # get installation directory
            self.__location__ = os.path.realpath(
                os.path.join(os.getcwd(), os.path.dirname(__file__)))

            # Run preprocessing shell script
            print("Running preprocessing script for ",module, end='')
            preprocessing_script = self.__location__ + "/preprocess/preprocess_"+module+".sh"
            if os.path.exists(preprocessing_script):
                print("Running preprocessing script...")
                os.system(preprocessing_script + self.__data_dir__)

            # add Docker compose entry
            print("Adding Docker compose entry for " + module + "...", end='')
            template_files = [self.__location__ + "/conf/docker_compose/" + module + ".yml"]
            if module == "uta-adapter":
                template_files.append(self.__location__ + "/conf/docker_compose/uta-database.yml")

            for tfile in template_files:
                template_file = open(tfile)
                lines = []
                for line in template_file:
                    lines.append(line)

                with open(self.__docker_compose_file, "a") as dc_file:
                    for line in lines:
                        dc_file.write(line)
                template_file.close()

            # pull Onkopus module Docker container
            print("Pull Docker container for " + module, end='')
            os.system("docker-compose -f " + self.__data_dir__ + "/docker-compose.yml pull")

            self._add_new_module(module)

            print("Onkopus module successfully installed: " + module)
        else:
            print("[Error] No Onkopus module found: " + module + ". Get a list of all available modules with 'onkopus list-modules'")

    def start_modules(self):
        """
        Starts all installed Onkopus modules as Docker containers

        :return:
        """
        print("Starting locally installed Onkopus modules")

        print("Installed modules: " + ",".join(self.installed_modules))

        # Start Docker containers
        dc_cmd = "docker-compose -f " + self.__data_dir__ + "/docker-compose.yml up -d"
        #print(dc_cmd)
        os.system(dc_cmd)

        print("Onkopus started")

    def stop_modules(self):
        """
        Stops all running Onkopus containers

        :return:
        """
        print("Stopping Onkopus modules")

        os.system("docker-compose -f " + self.__data_dir__ + "/docker-compose.yml down")

        print("Onkopus stopped")

    def restart_modules(self):
        """
        Restarts all installed Onkopus modules

        :return:
        """
        os.system('docker-compose down')
        os.system('docker-compose pull')
        os.system('docker-compose up -d')

    def list_modules(self):
        """
        Prints a list of all available Onkopus modules

        :return:
        """
        print("Available Onkopus modules: ")
        #print(self.__available_modules__)
        print(self.module_labels)

        print("Install an Onkopus module locally by running 'onkopus install -m [module-name]'")

    def list_formats(self):
        """

        :return:
        """
        print("Available data formats for input format (-if) and output format (-of): ")
        for format in self.formats:
            print(format)

    def add_patient_to_mtb(self,pid,mtb):
        onkopus_server_url = conf_reader.__MODULE_PROTOCOL__ + "://" + conf_reader.__MODULE_SERVER__ + conf_reader.__PORT_ONKOPUS_SERVER__
        onkopus_server_url = onkopus_server_url + "/onkopus-server/v1/updateMTB"
        onkopus.mtb_requests.add_patient_to_mtb(pid,mtb, onkopus_server_url)

    def add_patient_and_perform_annotation(self, input_file, mtb, genome_version=None, data_dir=None):
        pid = self.import_data(input_file, genome_version=genome_version, data_dir=data_dir)
        module = 'all'
        data_dir = "loc"
        self._db_request(pid, module=module, genome_version=genome_version)
        self.add_patient_to_mtb(pid, mtb)

    def show_title(self):
        pass

    def run(self):
        """
        Main Onkopus command-line function

        :return:
        """
        self.show_title()

        parser = argparse.ArgumentParser()
        parser.add_argument('action', choices=['run', 'install', 'list-modules', 'start', 'stop', 'import', 'mtb-add', 'mtb-add-analyze'])
        parser.add_argument('-m', '--module', default='all')
        parser.add_argument('-i', '--input_file', default='')
        parser.add_argument('-o', '--output_file', default='')
        parser.add_argument('-g', '--genome_version', default='')
        parser.add_argument('-d', '--data_dir', default='')
        parser.add_argument('-pid', '--patient_id', default='')
        parser.add_argument('-mtb', '--mtb_id', default='')
        parser.add_argument('-if', '--input_format', default='')
        parser.add_argument('-of', '--output_format', default='')
        parser.add_argument('-md', '--mode', default='')

        args = parser.parse_args()
        action = args.action
        module = args.module
        input_file = args.input_file
        output_file = args.output_file
        genome_version = args.genome_version
        data_dir = args.data_dir
        pid = args.patient_id
        mtb = args.mtb_id
        input_format = args.input_format
        output_format = args.output_format
        mode = args.mode

        if action == 'run':
            self.run_interpretation(input_file, output_file, module=module, genome_version=genome_version, pid=pid,
                                    input_format=input_format,output_format=output_format,mode=mode)
        elif action == 'install':
            self.install(module)
        elif action == 'start':
            self.start_modules()
        elif action == 'stop':
            self.stop_modules()
        elif action == 'import':
            self.import_data(input_file, genome_version=genome_version,data_dir=data_dir)
        elif action == 'list-modules':
            self.list_modules()
        elif action == 'list-formats':
            self.list_formats()
        elif action == 'mtb-add':
            self.add_patient_to_mtb(pid,mtb)
        elif action == 'mtb-add-analyze':
            self.add_patient_and_perform_annotation(input_file, mtb, genome_version=genome_version, data_dir=data_dir)

