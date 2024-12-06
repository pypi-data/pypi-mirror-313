import csv
from queries.query import Neo4jQuery
from queries.cypherbuilder import QueryBuilder, ValidAfterWhere
#from queries.typedefs import *
from messages import *
import assetmodelutilities as amu
from processors import labelmanager as lm

class CSVFileWriter:

    def __init__(self, config_manager, db_connector):
        self.db_connector = db_connector
        self.config_manager = config_manager

        self.write_node_file = config_manager.get_node_csvfile_requested()
        self.node_labels = config_manager.get_node_csv_labels()
        self.csv_node_primary_property = config_manager.get_csv_node_property_list()['DEFAULT']

        self.file_suffix = config_manager.get_csv_file_suffix()
        self.write_relationship_file = config_manager.get_relationship_csvfile_requested()
        self.to_labels = config_manager.get_to_csv_labels()
        self.csv_to_primary_property = config_manager.get_csv_to_property_list()['DEFAULT']
        if self.csv_to_primary_property != self.csv_node_primary_property:
            self.to_prefix = self.csv_to_primary_property + '::'
        else:
            self.to_prefix = ''

        self.batch_size = config_manager.get_batch_rate()
        if self.batch_size == 0:
            self.batch_size = 100

        self.required_labels = config_manager.get_required_labels()
        self.primary_property = config_manager.get_primary_property()['DEFAULT'][0]
        self.unique_id_property = config_manager.get_unique_id_property()
        self.version_labels = config_manager.get_version_labels_list()

        self.relationship_alias = config_manager.get_relationship_alias()['DEFAULT'][0]
        self.from_alias = config_manager.get_from_alias()['DEFAULT'][0]
        self.to_alias = config_manager.get_to_alias()['DEFAULT'][0]
        self.node_label = config_manager.get_label_alias()['DEFAULT'][0]
        self.from_label = config_manager.get_from_label_alias()['DEFAULT'][0]
        self.to_label = config_manager.get_to_label_alias()['DEFAULT'][0]

        self.all_keys = [self.node_label]
        self.all_nodes = []
        self.all_relationship_keys = [self.from_alias, self.to_alias, self.from_label, self.to_label, self.relationship_alias]
        self.all_relationships = []

    def pop_property(self, dictionary, property):
        try:
            dictionary.pop(property)
        except:
            pass

    def find_property(self, data, options):
        value = ''
        key = self.primary_property
        all_options = [self.primary_property, *options]
        for option in all_options:
            try:
                value = data[option]
                if option != self.primary_property:
                    value = option + '::' + value
                    key = option
                break
            except:
                pass

        return value, key

    def write_data(self):

        if self.write_node_file:
            def_path = self.config_manager.get_default_path()
            suffix = self.file_suffix
            #        label_suffix = '-'.join(label_set)
            #        output_file = def_path + 'Nodes ' + suffix + '-' + label_suffix.replace(':', '-') + '.csv'
            output_file = def_path + 'Nodes ' + suffix

            try:
                with open(output_file+'.csv', 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=self.all_keys, delimiter=';', quoting=csv.QUOTE_MINIMAL)
                    writer.writeheader()
                    writer.writerows(self.all_nodes)
            except:
                try:
                    with open(output_file+'.csv', 'w', encoding='UTF8', newline='') as f:
                        writer = csv.DictWriter(f, fieldnames=self.all_keys, delimiter=';', quoting=csv.QUOTE_MINIMAL)
                        writer.writeheader()
                        writer.writerows(self.all_nodes)
                except:
                    pass

        if self.write_relationship_file:
            def_path = self.config_manager.get_default_path()
            suffix = self.file_suffix
            output_file = def_path + 'Relationships ' + suffix

            try:
                with open(output_file+'.csv', 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=self.all_relationship_keys, delimiter=';', quoting=csv.QUOTE_MINIMAL)
                    writer.writeheader()
                    writer.writerows(self.all_relationships)
            except:
                try:
                    with open(output_file+'.csv', 'w', encoding='UTF8', newline='') as f:
                        writer = csv.DictWriter(f, fieldnames=self.all_relationship_keys, delimiter=';', quoting=csv.QUOTE_MINIMAL)
                        writer.writeheader()
                        writer.writerows(self.all_relationships)
                except:
                    pass

    def update_node_data(self, data):

        for node in data:

            properties = node['Properties']
            properties[self.node_label] = lm.validate_output_labels(node['FromLabels'])

            self.pop_property(properties, self.config_manager.get_update_time_property())
            self.pop_property(properties, self.config_manager.get_creation_time_property())
            try:
                self.pop_property(properties, self.config_manager.get_version_counter())
            except:
                pass

            primary_property_val, primary_key = self.find_property(properties, self.csv_node_primary_property)
            properties[self.primary_property] = primary_property_val

            if primary_key != self.primary_property:
                properties.pop(primary_key)
                if primary_key in self.all_keys:
                    self.all_keys.remove(primary_key)

            these_keys = properties.keys()
            self.all_keys = list(set([*these_keys, *self.all_keys]))
            self.all_nodes.append(properties)

    def update_relationship_data(self, data):

        for relationship in data:
            if relationship['Relationship']:
                properties = relationship['RelationshipProperties']

                properties[self.from_alias] = relationship['From']
                properties[self.to_alias] = self.to_prefix + relationship['To']
                properties[self.from_label] = lm.validate_output_labels(relationship['FromLabels'])
                properties[self.to_label] = lm.validate_output_labels(relationship['ToLabels'])
                properties[self.relationship_alias] = relationship['Relationship']

                self.pop_property(properties, self.config_manager.get_update_time_property())
                self.pop_property(properties, self.config_manager.get_creation_time_property())

                if properties[self.from_alias] and properties[self.to_alias]:
                    these_keys = properties.keys()
                    self.all_relationship_keys = list(set([*these_keys, *self.all_relationship_keys]))
                    self.all_relationships.append(properties)

    def combine_labels(self, label_set):
        query_labels = []
        if label_set:
            requested_labels = label_set[1:].split(':')

            required_labels = list({i for i in self.required_labels if (not (i.startswith('!') and ('!' + i not in self.required_labels)) and ('!' + i not in requested_labels))} | {i for i in requested_labels if not i.startswith('!')})
            unwanted_labels = list({i[1:] for i in self.required_labels if (i.startswith('!') and (i[1:] not in requested_labels) and ('!' + i) not in requested_labels)} | {i[1:] for i in requested_labels if i.startswith('!') and not i.startswith('!!')})
            query_labels.append([required_labels, unwanted_labels])
        else:
            query_labels = [i for i in self.required_labels if (not ('!' + i in self.required_labels) and not (i.startswith('!')) and i != '')]
            query_labels = [[query_labels, []]]

        return query_labels

    def make_get_nodes_query(self, labels, list_name):

        node_ref = 'gn'
        incl_labels = labels[0]
        excl_labels = labels[1]
        where_literal = f'NOT {node_ref}:' + f' AND NOT {node_ref}:'.join(excl_labels)
        response_text = f'{node_ref}.{self.csv_node_primary_property} AS {list_name}'

        node_query_text = (QueryBuilder()
                           .match()
                           .node(labels=incl_labels, ref_name=node_ref)
                           )
        if excl_labels:
            node_query_text = node_query_text.where_literal(where_literal)

        node_query_text = node_query_text.return_literal(response_text).toStr()
        node_query = Neo4jQuery('get node list', node_query_text)

        return node_query

    def make_base_queries(self, labels, to_labels):

        node_ref = 'cn'
        from_node_ref = 'cfrom'
        to_node_ref = 'cto'
        rel_ref = 'crel'

        incl_labels = labels[0]
        excl_labels = labels[1]
        to_incl_labels = to_labels[0]
        to_excl_labels = to_labels[1]

        where_literal = f'NOT {node_ref}:' + f' AND NOT {node_ref}:'.join(excl_labels)
        to_where_literal = f'NOT {to_node_ref}:' + f' AND NOT {to_node_ref}:'.join(to_excl_labels)

        node_query = (QueryBuilder()
                      .match()
                      .node(labels=incl_labels, ref_name=node_ref)
                      )
        if excl_labels:
            node_query = node_query.where_literal(where_literal)

        node_response_text = f'{node_ref}{{.*}} as Properties, ' \
                             f'labels({node_ref}) AS FromLabels'
#                             f'{node_ref}.{self.csv_node_primary_property} AS From, ' \

        relationship_query = (QueryBuilder()
                              .match_optional()
                              .node(ref_name=node_ref)
                              .related_to(ref_name=rel_ref)
                              .node(labels=to_incl_labels, ref_name=to_node_ref)
                              )
        if to_excl_labels:
            relationship_query = relationship_query.where_literal(to_where_literal)

        relationship_response_text = f'{node_ref}.{self.csv_node_primary_property} AS From, ' \
                                     f'{to_node_ref}.{self.csv_to_primary_property} AS To, ' \
                                     f'labels({node_ref}) AS FromLabels, ' \
                                     f'labels({to_node_ref}) AS ToLabels, ' \
                                     f'type({rel_ref}) AS Relationship, ' \
                                     f'{rel_ref}{{.*}} AS RelationshipProperties'

        return node_query, node_response_text, relationship_query, relationship_response_text

    def process_data(self, node_list, label_set, to_label_set):

        num_nodes = len(node_list)
        node_query, node_response_text, relationship_query, relationship_response_text = self.make_base_queries(label_set, to_label_set)
        num_batches = int((num_nodes - 1) / self.batch_size) + 1
        batch_num = 0
        while batch_num < num_batches:
            num_none = 0
            message_no_cr(f'Processing batch {batch_num+1} of {num_batches} at {amu.get_formatted_time_now_noms()}{chr(13)}')
            this_batch = node_list[batch_num * self.batch_size:(batch_num + 1) * self.batch_size]
            while None in this_batch:
                this_batch.remove(None)
                num_none += 1
            where_tests = {'cn.' + self.csv_node_primary_property: this_batch}

            if 'WHERE' in node_query.toStr():
                this_query = node_query.where_additional(where_tests, ' IN ', ' AND ')
            else:
                this_query = node_query.where_multiple(where_tests, ' IN ', ' AND ')

            if self.write_node_file:
                this_query_text = this_query.return_literal(node_response_text).toStr().replace('\\"', '"')
                this_node_query = Neo4jQuery('get data', this_query_text)
                result = self.db_connector.execute(this_node_query)
                response = result.get_response()
                if response:
                    self.update_node_data(response)

            if self.write_relationship_file:
                this_query_text = this_query.toStr().replace('\\"', '"') + ' ' + relationship_query.return_literal(relationship_response_text).toStr()
                this_relationship_query = Neo4jQuery('get data', this_query_text)
                result = self.db_connector.execute(this_relationship_query)
                response = result.get_response()
                if response:
                    self.update_relationship_data(response)

            batch_num += 1

        message('', False)
        self.write_data()

    def get_node_list(self, label_set):

        list_name = 'NodeList'
        nodes_query = self.make_get_nodes_query(label_set, list_name)
        result = self.db_connector.execute(nodes_query)
        response = result.get_response()
        try:
            nodes_found = [i[list_name] for i in response]
        except:
            nodes_found = []

        return nodes_found

    def write_csv_files(self):
        if self.write_node_file or self.write_relationship_file:
            wanted_labels, unwanted_labels = lm.sort_output_labels(self.node_labels, self.version_labels)
            wanted_to_labels, unwanted_to_labels = lm.sort_output_labels(self.to_labels, self.version_labels)
            node_list = self.get_node_list([wanted_labels, unwanted_labels])
            num_nodes_found = len(node_list)
            if num_nodes_found == 1:
                intro = 'There is 1 node'
            else:
                intro = f'There are {num_nodes_found} nodes'
            print(f'{intro} with :{":".join(lm.strip_quotes(wanted_labels))}', end='')
            if unwanted_labels:
                print(f' but not :{" nor :".join(lm.strip_quotes(unwanted_labels))}')
            else:
                print()
            self.process_data(node_list, [wanted_labels, unwanted_labels], [wanted_to_labels, unwanted_to_labels])
