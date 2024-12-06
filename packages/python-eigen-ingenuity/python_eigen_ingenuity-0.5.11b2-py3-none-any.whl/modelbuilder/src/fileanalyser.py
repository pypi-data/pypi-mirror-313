import csv

import messages
from csvcontentsmanager import CSVContentsManager
import assetmodelutilities as amu

class FileAnalyser():

    def __init__(self, config, section):
        self.separator = config.get_separator()
        self.def_path = config.get_default_path()

        header_mappings, alias_mappings = config.get_header_mappings()
        self.header_mappings = header_mappings[section]
        self.alias_mappings = alias_mappings[section]
        self.default_data_type = config.get_default_data_type()[section]

        self.node_alias = config.get_node_alias()[section]
        self.from_node_alias = config.get_from_alias()[section]
        self.to_node_alias = config.get_to_alias()[section]
        self.relationship_alias = config.get_relationship_alias()[section]
        self.ignore_nodes = config.get_ignore_nodes()

        self.node_types = amu.node_types
        self.from_types = amu.from_types
        self.to_types = amu.to_types
        self.relation_types = amu.relation_types
        self.label_types = amu.label_types
        self.all_types = amu.all_types


    def determine_file_type(self, filename, file_format):

        contents = None
        file_name = amu.find_file(self.def_path, filename)
        if file_name is None:
            return 'fnf', contents, []

        match file_format:
            case 'csv':
                try:
                    with open(file_name, encoding='utf8') as csv_file:
                        csv_data = csv.reader(csv_file, delimiter=self.separator)
                        contents = CSVContentsManager(csv_data, self.header_mappings, self.alias_mappings, self.default_data_type)
                except:
                    try:
                        with open(file_name) as csv_file:
                            csv_data = csv.reader(csv_file, delimiter=self.separator)
                            contents = CSVContentsManager(csv_data, self.header_mappings, self.alias_mappings, self.default_data_type)
                    except:
                        return 'incorrect file format', contents, []
            case _:
                pass

        num_node_columns = contents.get_column_count(self.node_alias, self.node_types)
        num_from_columns = contents.get_column_count(self.from_node_alias, self.from_types)
        num_to_columns = contents.get_column_count(self.to_node_alias, self.to_types)
        num_relation_columns = contents.get_column_count(self.relationship_alias, self.relation_types)

        incomplete_rows = contents.get_incomplete_rows()
        if len(incomplete_rows) > 0:
            return 'incomplete row(s)', contents, incomplete_rows

        # If there is a least one Node (including aliases) column, this could be a Node file
        if num_node_columns > 0:
            could_be_node = True
            if num_node_columns > 1:
                messages.warning_message(f'Multiple node columns found in ', f'{filename}')
        else:
            could_be_node = False

        # Check if there are at least one each of From, To and Relationship (including aliases) columns
        # If so, this could be a Relationship file
        if num_from_columns > 0 and num_to_columns > 0 and num_relation_columns > 0:
            could_be_relations = True
        else:
            could_be_relations = False

        if could_be_node:
            if could_be_relations:
                if self.ignore_nodes:
                    file_type = 'relationships'
                else:
                    file_type = 'both'
            else:
                file_type = 'nodes'
        else:
            if could_be_relations:
                file_type = 'relationships'
            else:
                file_type = 'neither'

        return file_type, contents, []
