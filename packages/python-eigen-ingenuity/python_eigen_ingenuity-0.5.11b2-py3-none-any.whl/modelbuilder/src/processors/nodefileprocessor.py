import messages
from queries.cypherbuilder import QueryBuilder
import assetmodelutilities as amu
from queries.query import Neo4jQuery
import uuid
import processors.labelmanager as lm
import processors.propertymanager as pm
import property
from property import Neo4jProperty


class NodeFileProcessor:

    def __init__(self, filename, config, contents, section):
        self.filename = filename
        self.contents = contents

        self.primary_property = config.get_primary_property()[section]
        self.add_system_properties = not config.get_no_system_properties()

        self.required_labels = config.get_required_labels()[section]
        self.required_properties = config.get_required_properties_dict()[section]
        self.unrequired_properties = config.get_unrequired_properties_list()[section]
        self.unique_id_property = config.get_unique_id_property()[section]
        self.creation_time_property = config.get_creation_time_property()[section]
        self.update_time_property = config.get_update_time_property()[section]

        self.label_alias = config.get_label_alias()[section]
        self.node_alias = config.get_node_alias()[section]

        self.validate_only = config.in_validation_mode()
        self.summarise = config.in_summary_mode()

        self.blank_property_list = config.get_blank_property_list()
        self.blank_property_override = config.get_blank_property_override()
        self.batch_rate = config.get_batch_rate()
        self.start_from = config.get_start_from()
        self.last_row = config.get_end_at()

        self.node_types = amu.node_types
        self.label_types = amu.label_types
        self.all_types = amu.all_types

        self.section = section

    def get_last_row(self, num_rows):
        if self.last_row < 0:
            last_row = num_rows
        else:
            last_row = min(num_rows, self.last_row)
        return last_row

    def process_node_file(self):

        # For each line in the file, build a cypher query to MERGE a node
        # Each query is added to a list of queries, which are returned to the caller. They are NOT actioned here

        num_data_rows = self.contents.get_row_count()
        node_columns = self.contents.get_column_numbers_list(self.node_alias, self.node_types)
        label_columns = self.contents.get_column_numbers_list(self.label_alias, self.label_types)
        property_columns = self.contents.get_other_column_numbers_list(self.node_alias + self.label_alias, self.all_types)

        queries = []

        num_rows = num_data_rows - self.start_from + 1
        this_row = self.start_from-1
        last_row = self.get_last_row(num_data_rows)
        property_ref = 'n'
        property_ref_dot = property_ref + '.'

        while this_row < last_row:
            validated_csv_labels = lm.validate_labels(self.contents.get_column_values_list(this_row, label_columns))
            merge_labels, new_labels, remove_labels = lm.sort_node_labels(self.required_labels, validated_csv_labels)
            row_properties = self.contents.get_property_values_dict(this_row, property_columns, self.blank_property_list, blank_override=self.blank_property_override, allow_split=False)
            properties = pm.combine_properties(self.required_properties, row_properties)
            # Remove any properties we don't want
            for unwanted in self.unrequired_properties:
                temp = properties.pop(unwanted, None)

            # Split out those properties that are dependent on others, so that we can add them in the right order
            explicit_properties, calculated_properties = pm.split_out_functional_properties(properties)

            for primary_property in self.contents.get_property_values_list(this_row, node_columns, self.primary_property, allow_split=False):
                time_now = amu.get_formatted_time_now()

                # Build a simple MERGE query using queries
                query_text = (QueryBuilder()
                              .merge()
                              .node(labels=merge_labels, ref_name=property_ref, properties=primary_property)
                              )

                # Add in System properties if required
                if self.add_system_properties:
                    new_uuid = str(uuid.uuid4())
                    create_time = property_ref_dot + self.creation_time_property + '=datetime("' + time_now + '")'
                    id_property = property_ref_dot + self.unique_id_property
                    update_id = id_property + '= CASE WHEN ' + id_property + ' IS null THEN "' + new_uuid + '" ELSE ' + id_property + ' END,' +\
                                property_ref_dot + self.update_time_property + '=datetime("' + time_now + '")'
                    query_text = query_text.on_create().set_literal(create_time).set_literal(update_id)

                if len(new_labels) > 0:
                    query_text = query_text.set_labels(ref_name=property_ref, labels=new_labels)
                if len(remove_labels) > 0:
                    query_text = query_text.remove_literal(f'{property_ref}:{":".join(remove_labels)}')
                if len(explicit_properties) > 0:
                    query_text = query_text.set(properties=explicit_properties, property_ref=property_ref_dot)
                if len(calculated_properties) > 0:
                    query_text = query_text.set(properties=calculated_properties, property_ref=property_ref_dot)

                query_text = query_text.toStr()

                query = Neo4jQuery('node', query_text, time_now, merge_labels, new_labels, primary_property, properties, self.section)

                if self.validate_only and not self.summarise:
                    print(query.text)

                queries.append(query)

            this_row += 1
            messages.message_no_cr(f'Generating queries... {100 * (this_row - self.start_from + 1) / num_rows:.0f}%{chr(13)}')

        messages.message('', False)
        return queries

    def process_node_file_batch(self):

        # For each line in the file, build a cypher query to MERGE a node
        # Each query is added to a list of queries, which are returned to the caller. They are NOT actioned here

        num_data_rows = self.contents.get_row_count()
        node_columns = self.contents.get_column_numbers_list(self.node_alias, self.node_types)
        label_columns = self.contents.get_column_numbers_list(self.label_alias, self.label_types)
        property_columns = self.contents.get_other_column_numbers_list(self.node_alias + self.label_alias, self.all_types)

        queries = []

        num_rows = num_data_rows - self.start_from + 1
        this_row = self.start_from-1
        last_row = self.get_last_row(num_data_rows)
        dict_size = 0
        property_ref = 'n'
        property_ref_dot = property_ref + '.'
        payload_ref = 'payload'
        payload_ref_dot = payload_ref + '.'

        time_now = amu.get_formatted_time_now()

        # For best optimisation, we need to create a batch query for all the update with the same labels
        # So we will create a dictionary of queries based on the labels for each query
        # Since the dictionary key can't be a list, we will create a list (of lists) and use the index in that list as the key
        # When we have worked through all the input and grouped the queries by label combination, we will create the queries

        batch_keys = []
        query_dictionary = {}
        id_property = property_ref_dot + self.unique_id_property
        creation_property = property_ref_dot + self.creation_time_property

        while this_row < last_row:
            validated_csv_labels = lm.validate_labels(self.contents.get_column_values_list(this_row, label_columns))
            merge_labels, new_labels, remove_labels = lm.sort_node_labels(self.required_labels, validated_csv_labels)
            row_properties = self.contents.get_property_values_dict(this_row, property_columns, self.blank_property_list, blank_override=self.blank_property_override, allow_split=False)

            for primary_property in self.contents.get_property_values_list(this_row, node_columns, self.primary_property, allow_split=False):
                properties = pm.combine_properties(self.required_properties, row_properties)
                # Remove any properties we don't want
                for unwanted in self.unrequired_properties:
                    temp = properties.pop(unwanted, None)

                primary_property_dict = {primary_property.key: primary_property}
                all_properties = pm.combine_properties(properties, primary_property_dict)

                explicit_properties, calculated_properties = pm.split_out_functional_properties(all_properties)

                query_data = [explicit_properties, calculated_properties, time_now]

                # So now we know all about this particular update. Let's put it in the query dictionary
                # We'll group these by unique combinations of labels and primary key type
                # Have to use a list since a dictionary key can't be a dictionary
                dictionary_key = [new_labels, merge_labels, remove_labels, [primary_property.key], calculated_properties.keys()]
                try:
                    dictionary_index = batch_keys.index(dictionary_key)
                    query_dictionary[dictionary_index].append(query_data)
                except:
                    dictionary_index = len(batch_keys)
                    query_dictionary[dictionary_index] = [query_data]
                    batch_keys.append(dictionary_key)
                dict_size += 1

            this_row += 1
            messages.message_no_cr(f'Analysing file... {100 * (this_row - self.start_from + 1) / num_rows:.0f}%{chr(13)}')

        messages.message('', False)

        # Right, so now we have a dictionary of updates grouped by labels. Let's create the queries
        query_count = 0
        for new_labels, updates in query_dictionary.items():
            num_updates_for_this_label = len(updates)
            num_batches = int((num_updates_for_this_label-1)/self.batch_rate) + 1

            batch_num = 1
            while batch_num <= num_batches:
                if batch_num == num_batches:
                    # Last batch, so
                    batch_size = 1 + (num_updates_for_this_label-1) % self.batch_rate
                else:
                    batch_size = self.batch_rate

                this_size = 0
                payload = []
                while this_size < batch_size:
                    # Combine all the update data...
                    update = updates[(batch_num-1)*self.batch_rate + this_size]
                    update_properties = update[0] or {}
                    func_properties = update[1] or {}
                    if self.add_system_properties:
                        update_properties[self.update_time_property] = Neo4jProperty(self.update_time_property, update[2])
                    payload.append(update_properties)
                    this_size += 1
                    query_count += 1

                formatted_payload = []
                property_count = 0
                for a_payload in payload:
                    formatted_payload.append(property.format(a_payload, property_ref_dot))
                    property_count += len(a_payload)

                # Build a MERGE query using queries
                merge_labels = batch_keys[new_labels][1]
                remove_labels = batch_keys[new_labels][2]
#                if batch_keys[new_labels][0]:
#                    merge_labels += batch_keys[new_labels][0]
                primary_property = batch_keys[new_labels][3][0]
                query_text = (QueryBuilder()
                              .unwind_list_as(formatted_payload, payload_ref)
                              .merge()
                              .node_batch(labels=list(set(merge_labels)), ref_name=property_ref, properties=primary_property+':'+payload_ref_dot+primary_property)
                              .set_literal(property_ref + ' += ' + payload_ref)
                              )

                if batch_keys[new_labels][0]:
                    query_text = query_text.set_labels(ref_name=property_ref, labels=batch_keys[new_labels][0])
                if len(remove_labels) > 0:
                    query_text = query_text.remove_literal(f'{property_ref}:{":".join(remove_labels)}')
                if func_properties:
                    query_text = query_text.set_functional(func_properties, property_ref_dot)
                    property_count += len(func_properties)
                if self.add_system_properties:
                    query_text = query_text.set_literal(id_property + '= CASE WHEN ' + id_property + ' IS null THEN randomUUID() ELSE ' + id_property + ' END')
                    query_text = query_text.set_literal(creation_property + '= CASE WHEN ' + creation_property + ' IS null THEN ' + property_ref_dot + self.update_time_property + ' ELSE ' + creation_property + ' END')

                query_text = query_text.toStr()
                query = Neo4jQuery('batch node', query_text, time_now, batch_size=this_size, property_count=property_count)
                queries.append(query)
                messages.message_no_cr(f'Generating queries... {100 * query_count / dict_size:.0f}%{chr(13)}')

                if self.validate_only and not self.summarise:
                    print(query.text)

                batch_num += 1

        messages.message('', False)
        return queries

    def get_filename(self):
        return self.filename

    def is_inline_query(self):
        return False
