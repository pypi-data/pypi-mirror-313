from configparser import ConfigParser, ExtendedInterpolation
import argparse
import sys
import re
import ast
import assetmodelutilities as amu
from messages import *
import eigeningenuity.settings as settings
import processors.labelmanager as lm
import processors.relationshipmanager as rm
import processors.propertymanager as pm


class ConfigManager:

    def __init__(self):

        self.error_list = []
        parser = argparse.ArgumentParser()

        # Start with input parameters i.e. what files/commands to process, and where to find them
        parser.add_argument('-p', '--path', default='.\\', help='Location of the input and output files. Default is current folder')
        parser.add_argument('-c', '--config', default='config.ini', help='Name of the configuration file, default is config.ini in the folder given by -p')
        parser.add_argument('-cs', '--configsection', default='', help='Section of the config file to use, if not DEFAULT')
        parser.add_argument('-d', '--database', default='0', help='Database ID (as set in config file). Defaults to first entry')
        parser.add_argument('-f', '--file', nargs='+', default='', help='List of input files (space separated, quoted with " where necessary)')
        parser.add_argument('-q', '--query', nargs='+', default='', help='List of queries to run (space separated, quoted with " where necessary)')
        parser.add_argument('-pre', '--preprocess', nargs='+', default='', help='Command(s) to execute before processing input files')
        parser.add_argument('-post', '--postprocess', nargs='+', default='', help='Command(s) to execute after processing input files')
        parser.add_argument('-da', '--deleteall', nargs='*', default='', help='Lists of labels to identify nodes to delete before processing any files')

        # This next set change the behaviour of the processing away from the default
        parser.add_argument('-s', '--separator', default=';', help="The separator used in the csv files. Default is a semi-colon ';'")
        parser.add_argument('-sf', '--startfrom', default=1, type=int, help='The first query to process in a .csv file. No effect on cypher files. Default is 1')
        parser.add_argument('-ea', '--endat', default=-1, type=int, help='The last query to process in a .csv file. No effect on cypher files. Default is last query in the file')
        parser.add_argument('-nov', '--noversions', action='store_true', help='Suppress creation of version nodes')
        parser.add_argument('-nosp', '--nosystemproperties', action='store_true', help='Suppress creation of system properties on nodes and relationships. Implies -nov')
        parser.add_argument('-sof', '--stoponfailure', action='store_true', help='Stop processing if an error occurs')
        parser.add_argument('-in', '--ignorenodes', action='store_true', help='Treat node columns in relationship files as relationship properties')
        parser.add_argument('-sd', '--skipduplicates', action='store_true', help='Don\'t create a version node if there are no changes. Same as -nod')
        parser.add_argument('-nod', '--noduplicates', action='store_true', help='Don\'t create a version node if there are no changes. Same as -sd')
        parser.add_argument('-ab', '--allowblanks', nargs='*', default='', help='Update a node_key even if it is blank')
        parser.add_argument('-rb', '--replaceblanks', default=None, type=str, help='Used in combination with allowblanks. Write a specific value instead of blank e.g "__NULL"')
        parser.add_argument('-b', '--batch', default=0, type=int, help='Number of queries to batch together when processing a node .csv file')
        parser.add_argument('-a', '--auth', action='store_true', help='Enable Azure Authentication')
        default_order = 'qnrc'
        parser.add_argument('-o', '--order', default=default_order, help='Order in which to process the input files. Default is ' + default_order)
        parser.add_argument('-ft', '--filetypes', default=default_order, help='File types to process. Default is all')

        # Overrides... used to override values in the config file
        parser.add_argument('-pp', '--primaryproperty', default='', help='Primary node_key')
        parser.add_argument('-rl', '--requiredlabels', default='', help='Required labels - appended to contents of config; use !Label to remove')
        parser.add_argument('-rp', '--requiredproperties', default='', help='Required properties - appended to contents of config; use !node_key to remove')

        # And finally specify what output is required
        parser.add_argument('-v', '--verify', action='store_true', help='Display the generated queries, but do not process them')
        parser.add_argument('-vs', '--summarise', action='store_true', help='Show a summary of the queries, but do not process them')
        parser.add_argument('-sq', '--showqueries', action='store_true', help='Display the queries as they are processed. No effect if -v present')
        parser.add_argument('-sr', '--showreturns', action='store_true', help='Display data from any RETURN clause')
        parser.add_argument('-wq', '--writequeries', help='Name of a file to record the processed queries. No effect if -v present')
        parser.add_argument('-wr', '--writereturns', help='Name of a file to record the results of the queries. No effect if -v present')
        parser.add_argument('-dr', '--displayrate', default='auto', help='Set the frequency of progress update messages. No effect if -v present')

        # Control of the csv writer
        parser.add_argument('-cn', '--createnodecsvfile', action='store_true', help='Create Node csv file(s) from Asset Model')
        parser.add_argument('-nl', '--nodelabels', default='', help='Lists of labels to identify nodes to write to csv file')
        parser.add_argument('-np', '--nodeproperties', default=None, help='Primary node_key of nodes')
        parser.add_argument('-cfs', '--csvfilesuffix', default='', help='Suffix to use in the output Node .csv file')
        parser.add_argument('-cr', '--createrelationshipcsvfile', action='store_true', help='Create Relationship csv file(s) from Asset Model')

        parser.add_argument('-ctl', '--csvtolabels', default='', help='Lists of labels to identify to nodes to write to csv file')
        parser.add_argument('-ctp', '--csvtoproperties', nargs='+', default=None, help='Primary node_key of To nodes')

        args = parser.parse_args()

        self.path = args.path
        self.config_file = args.config
        self.config_section = args.configsection
        self.input_file_list = args.file
        self.inline_query_list = args.query
        self.preprocess_query_list = args.preprocess
        self.postprocess_query_list = args.postprocess
        labels_to_delete = args.deleteall
        if labels_to_delete != '':
            self.labels_to_delete = lm.validate_labels(labels_to_delete)
        else:
            self.labels_to_delete = ''

        self.separator = args.separator
        self.start_from = args.startfrom
        self.end_at = args.endat
        self.no_version = args.noversions or args.nosystemproperties
        self.no_system_properties = args.nosystemproperties
        self.stop_on_failure = args.stoponfailure
        self.ignore_nodes = args.ignorenodes
        self.no_duplicates = args.skipduplicates or args.noduplicates
        blank_properties_list = args.allowblanks
        if blank_properties_list != '':
            self.blank_properties_list = pm.validate_property_keys(blank_properties_list)
        else:
            self.blank_properties_list = ''
        self.blank_properties_override = args.replaceblanks
        self.batch_rate = args.batch
        self.auth = args.auth

        self.primary_property_override = args.primaryproperty
        self.required_labels_override = args.requiredlabels
        self.required_properties_override = args.requiredproperties

        self.db_name = args.database
        self.validation_mode = args.verify
        self.summarise_mode = args.summarise
        self.show_query = args.showqueries and not self.validation_mode
        self.show_return = args.showreturns and not self.validation_mode
        self.display_rate = args.displayrate

        self.path = self.path.replace('\\', '/')
        if len(self.path) > 0 and not self.path.endswith('/'):
            self.path += '/'

        if args.writequeries is not None and not self.validation_mode:
            out_file = args.writequeries.replace('/', '\\')
            if out_file.find('\\') > -1:
                self.query_output = out_file
            else:
                self.query_output = self.path + out_file
        else:
            self.query_output = None

        if args.writereturns is not None and not self.validation_mode:
            if sys.platform.startswith("win"):
                out_file = args.writereturns.replace('/', '\\')
            else:
                out_file = args.writereturns

            if out_file.find('\\') > -1 or out_file.find('/') > -1:
                self.results_output = out_file
            else:
                self.results_output = self.path + out_file
        else:
            self.results_output = None
        config_file_name = amu.find_file(self.path, self.config_file)
        if config_file_name is None:
            config_file_name = amu.find_file('models/default/', 'config.ini')
            if config_file_name == '':
                self.error_list.append([f'Config file {self.config_file} not found', ''])
                return

        if self.auth:
            settings.disable_azure_auth(False)
##            settings.set_azure_client_id('74efa022-e6d6-42ad-bc15-edc76c525bdd')
##            settings.set_azure_tenant_id('74efa022-e6d6-42ad-bc15-edc76c525bdf')
        else:
            settings.disable_azure_auth(True)

        self.config = ConfigParser(interpolation=ExtendedInterpolation())
        self.config.read(config_file_name)
        self.available_sections = ['DEFAULT'] + self.config.sections()

        # Now look at controlling the order we process the files
        # First remove illegal and duplicate inputs
        order_given = ''.join(list(dict.fromkeys(re.findall("[" + default_order + "x]", args.order))))
        if order_given != args.order:
            warning_message('Erroneous characters in order specification - using ', order_given)
        self.orders = {'pre': 0, 'pre-file': 0, 'post': len(default_order) + 1, 'post-file': len(default_order) + 1}
        len_input = len(order_given)
        as_ordered = order_given.find('x')
        count = 0
        num_found = 0
        for input_type in default_order:
            type_given = order_given.find(input_type)
            if type_given > -1:
                num_found += 1
                order = type_given
            elif as_ordered > -1:
                order = as_ordered
            else:
                order = len_input + count - num_found
            self.orders[input_type] = order + 1
            count += 1

        # Identify which files to process (note: order is unimportant, just presence (or not))
        self.process_file_types = ''.join(list(dict.fromkeys(re.findall("[" + default_order + "]", args.filetypes))))

        # Data for .csv file generation
        self.node_csvfile_requested = args.createnodecsvfile
        self.node_labels = lm.validate_labels([args.nodelabels])
        self.node_property_list = pm.validate_properties(args.nodeproperties)
        self.csv_file_suffix = args.csvfilesuffix
        self.relationship_csvfile_requested = args.createrelationshipcsvfile

        self.csv_to_labels = lm.validate_labels([args.csvtolabels])
        self.csv_to_property_list = pm.validate_properties(args.csvtoproperties)

        self.common_section = 'COMMON'

    def read_query_config(self):
        pass

    def read_db_config(self):
        database_section = self.common_section
        database_index = None
        database_name_list = self.get_config_value_list(database_section, "DatabaseNames")
        if isinstance(self.db_name, int):
            database_num = self.db_name
        else:
            try:
                database_num = int(ast.literal_eval(self.db_name))
            except:
                database_num = None

        if not (database_num is None):
            # Database number provided, so check if it's valid
            if database_num < len(database_name_list):
                database_index = database_num
            else:
                self.error_list += [
                    f'Database {self.db_name} requested, but only {len(database_name_list)} database(s) configured']
        else:
            # Must have been a name, so try to find it in the config
            try:
                database_index = database_name_list.index(self.db_name)
            except:
                self.error_list += [f'Database {self.db_name} not configured']

        if database_index is not None:
            self.db_connection_dict = {}
            self.db_connection_dict['url'] = self.get_config_value_list(database_section, "urls")[database_index]
            self.db_connection_dict['user'] = self.get_config_value_list(database_section, "users")[database_index]
            self.db_connection_dict['password'] = self.get_config_value_list(database_section, "passwords")[database_index]
            print(f'Connecting to {database_name_list[database_index]}')


    def read_version_config(self):
        version_section = self.common_section
        version_mode = self.get_config_value(version_section, "Versions", "on")
        self.version_labels_list = lm.validate_labels(self.get_config_value_list(version_section, "VersionLabels", "!Current,Version"))
        self.frozen_labels_list = lm.validate_labels(self.get_config_value_list(version_section, "FrozenLabels", ""))
        self.version_labels_list = lm.validate_labels(self.get_config_value_list(version_section, "VersionLabels", "!Current,Version"))
        self.version_prefix = self.get_config_value(version_section, "VersionLabelPrefix", "")
        self.version_counter = pm.validate_properties(self.get_config_value(version_section, "VersionCounterProperty", "versionCount"))
        self.version_number = pm.validate_properties(self.get_config_value(version_section, "VersionNumberProperty", "versionNumber"))
        self.first_version_property = pm.validate_properties(self.get_config_value(version_section, "FirstVersionProperty", "firstVersion"))
        self.last_version_property = pm.validate_properties(self.get_config_value(version_section, "LastVersionProperty", "lastVersion"))
        self.version_relationship = rm.validate_relationships(self.get_config_value(version_section, "VersionRelationship", "has_version"))
        self.next_version_relationship = rm.validate_relationships(self.get_config_value(version_section, "NextVersionRelationship", "next_version"))
        self.version_valid_from_property = pm.validate_properties(self.get_config_value(version_section, "VersionValidFromProperty", "validFrom"))
        self.version_valid_to_property = pm.validate_properties(self.get_config_value(version_section, "VersionValidToProperty", "validTo"))

        if version_mode.lower() != 'on':
            self.no_version = True

    def read_csv_config(self):
        self.primary_property = {s: self.primary_property_override or self.get_config_value(s, "PrimaryProperty", "node") for s in self.available_sections}
        self.default_data_type = {s: self.get_config_value(s, "DataType", "") for s in self.available_sections}
        self.required_labels_list = {s: lm.combine_required_labels(self.get_config_value_list(s, "RequiredLabels", ""), self.required_labels_override) for s in self.available_sections}

        self.unique_id_property = {s: self.get_config_value(s, "UniqueIDProperty", "uuid") for s in self.available_sections}
        self.creation_time_property = {s: self.get_config_value(s, "CreationTime", "creationTime") for s in self.available_sections}
        self.update_time_property = {s: self.get_config_value(s, "UpdateTime", "updateTime") for s in self.available_sections}

        self.label_alias_list = {s: lm.validate_labels(self.get_config_value_list(s, "Labels", "label")) for s in self.available_sections}
        self.node_alias_list = {s: self.get_config_value_list(s, "Nodes", "node") + [self.primary_property[s]] for s in self.available_sections}
        self.from_alias_list = {s: self.get_config_value_list(s, "FromNodes", "from,start") for s in self.available_sections}
        self.from_label_alias_list = {s: lm.validate_labels(self.get_config_value_list(s, "FromLabels", "fromLabel")) for s in self.available_sections}
        self.to_alias_list = {s: self.get_config_value_list(s, "ToNodes", "to,end") for s in self.available_sections}
        self.to_label_alias_list = {s: lm.validate_labels(self.get_config_value_list(s, "ToLabels", "toLabel")) for s in self.available_sections}
        self.relationship_alias_list = {s: rm.validate_relationships(self.get_config_value_list(s, "Relationships", "relationship")) for s in self.available_sections}

        self.required_properties_dict = {}
        self.unrequired_properties_list = {}

        self.no_system_properties = self.get_config_value(self.common_section, "SystemProperties", "on").lower() != 'on' or self.no_system_properties
        if self.no_system_properties:
            self.no_version = True

        header_mappings = {s: self.get_config_value_list(s, "Mappings", "") for s in self.available_sections}
        alias_header_mappings = {s: [i + '->' + self.primary_property[s] for i in self.node_alias_list[s] if i != self.primary_property[s]] for s in self.available_sections}
        self.header_mappings_dict = {}
        self.alias_header_mappings_dict = {}

        for s in self.available_sections:
            self.required_properties_dict[s], self.unrequired_properties_list[s] = pm.combine_required_properties(self.get_config_value_list(s, "RequiredProperties", ""), [self.required_properties_override], self.default_data_type[s])

            try:
                self.header_mappings_dict[s] = {i.replace('=', '->').split('->')[0].rstrip(): i.replace('=', '->').split('->')[1].lstrip() for i in header_mappings[s]}
            except:
                self.header_mappings_dict[s] = {}

            try:
                self.alias_header_mappings_dict[s] = {i.replace('=', '->').split('->')[0].rstrip(): i.replace('=', '->').split('->')[1].lstrip() for i in alias_header_mappings[s]}
            except:
                self.alias_header_mappings_dict[s] = {}

    def get_error_list(self):
        return self.error_list

    def get_config_value_list(self, section, option, default=None):
        # Get a node_value from the settings file, reporting an error if it's missing
        try:
            raw_value = self.config[section][option] or default
        except:
            if default is not None:
                raw_value = default
            else:
                self.error_list += [f'No value found for {option} in the configuration file']
                raw_value = ''
        # Reformat from a single string of comma separated values to a List (of strings)
        # removing leading and trailing spaces while we're at it
        if raw_value:
            return [i.strip() for i in raw_value.split(',')]
        else:
            return []

    def get_config_value(self, section, option, default=None):
        # Get a node_value from the settings file, reporting an error if it's missing
        value_list = self.get_config_value_list(section, option, default)
        if value_list:
            value = value_list[0]
            if len(value_list) > 1:
                warning('Warning! ', f'Multiple values for [{section}]{option} found - using {value}')
        else:
            value = default

        return value

    def get_default_path(self):
        return self.path

    def get_config_section(self):
        return self.config_section

    def get_available_sections(self):
        return self.available_sections

    def get_input_file_list(self):
        return self.input_file_list

    def get_inline_query_list(self):
        return self.inline_query_list

    def get_preprocess_query_list(self):
        return self.preprocess_query_list

    def get_postprocess_query_list(self):
        return self.postprocess_query_list

    def get_labels_to_delete_list(self):
        return self.labels_to_delete

    def get_separator(self):
        return self.separator

    def get_start_from(self):
        return self.start_from

    def get_end_at(self):
        return self.end_at

    def get_noversion(self):
        return self.no_version

    def get_no_system_properties(self):
        return self.no_system_properties

    def get_stop_on_failure(self):
        return self.stop_on_failure

    def get_skip_duplicates(self):
        return self.no_duplicates

    def get_ignore_nodes(self):
        return self.ignore_nodes

    def get_blank_property_list(self):
        return self.blank_properties_list
    
    def get_blank_property_override(self):
        return self.blank_properties_override

    def get_batch_rate(self):
        return self.batch_rate

    def get_db_connection_dict(self):
        return self.db_connection_dict

    def in_validation_mode(self):
        return self.validation_mode or self.summarise_mode

    def in_summary_mode(self):
        return self.summarise_mode

    def get_show_query(self):
        return self.show_query

    def get_show_return(self):
        return self.show_return

    def get_query_output(self):
        return self.query_output

    def get_results_output(self):
        return self.results_output

    def get_display_rate(self):
        return self.display_rate

    def get_primary_property(self):
        return self.primary_property

    def get_required_labels(self):
        return self.required_labels_list

    def get_required_properties_dict(self):
        return self.required_properties_dict

    def get_unrequired_properties_list(self):
        return self.unrequired_properties_list

    def get_unique_id_property(self):
        return self.unique_id_property

    def get_creation_time_property(self):
        return self.creation_time_property

    def get_update_time_property(self):
        return self.update_time_property

    def get_header_mappings(self):
        return self.header_mappings_dict, self.alias_header_mappings_dict

    def get_default_data_type(self):
        return self.default_data_type

    def get_label_alias(self):
        return self.label_alias_list

    def get_node_alias(self):
        return self.node_alias_list

    def get_from_alias(self):
        return self.from_alias_list

    def get_from_label_alias(self):
        return self.from_label_alias_list

    def get_to_alias(self):
        return self.to_alias_list

    def get_to_label_alias(self):
        return self.to_label_alias_list

    def get_relationship_alias(self):
        return self.relationship_alias_list

    def reset_errors(self):
        self.error_list = []

    def get_process_order(self):
        return self.orders

    def get_process_file_types(self):
        return self.process_file_types

    def get_frozen_labels_list(self):
        return self.frozen_labels_list

    def get_version_labels_list(self):
        return self.version_labels_list

    def get_version_prefix(self):
        return self.version_prefix

    def get_version_counter(self):
        return self.version_counter

    def get_version_number(self):
        return self.version_number

    def get_first_version_property(self):
        return self.first_version_property

    def get_last_version_property(self):
        return self.last_version_property

    def get_version_relationship(self):
        return self.version_relationship

    def get_next_version_relationship(self):
        return self.next_version_relationship

    def get_version_valid_from_property(self):
        return self.version_valid_from_property

    def get_version_valid_to_property(self):
        return self.version_valid_to_property

    def get_node_csvfile_requested(self):
        return self.node_csvfile_requested

    def get_node_csv_labels(self):
        return self.node_labels

    def get_csv_node_property_list(self):
        return self.node_property_list or self.primary_property

    def get_csv_file_suffix(self):
        return self.csv_file_suffix

    def get_relationship_csvfile_requested(self):
        return self.relationship_csvfile_requested

    def get_to_csv_labels(self):
        return self.csv_to_labels

    def get_csv_to_property_list(self):
        return self.csv_to_property_list or self.primary_property

    def get_error_count(self):
        for error in self.error_list:
            error_message(error)
        return len(self.error_list)
