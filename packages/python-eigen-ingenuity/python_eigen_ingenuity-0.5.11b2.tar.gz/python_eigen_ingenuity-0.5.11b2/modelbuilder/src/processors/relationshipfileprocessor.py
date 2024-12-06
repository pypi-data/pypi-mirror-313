import messages
from queries.cypherbuilder import QueryBuilder
import assetmodelutilities as amu
from queries.query import Neo4jQuery
import processors.labelmanager as lm
import processors.relationshipmanager as rm
import processors.propertymanager as pm
import property
from property import Neo4jProperty


class RelationshipFileProcessor:

    def __init__(self, filename, config, contents, section):
        self.filename = filename
        self.contents = contents

        self.primary_property = config.get_primary_property()[section]
        self.add_system_properties = not config.get_no_system_properties()

        self.required_labels = config.get_required_labels()[section]
        self.creation_time_property = config.get_creation_time_property()[section]
        self.update_time_property = config.get_update_time_property()[section]

        self.from_node_alias = config.get_from_alias()[section]
        self.from_label_alias = config.get_from_label_alias()[section]
        self.to_node_alias = config.get_to_alias()[section]
        self.to_label_alias = config.get_to_label_alias()[section]
        self.relationship_alias = config.get_relationship_alias()[section]

        self.validate_only = config.in_validation_mode()
        self.summarise = config.in_summary_mode()

        self.blank_property_override = config.get_blank_property_override()
        self.blank_property_list = config.get_blank_property_list()
        self.batch_rate = config.get_batch_rate()
        self.start_from = config.get_start_from()
        self.last_row = config.get_end_at()

        self.from_types = amu.from_types
        self.to_types = amu.to_types
        self.relation_types = amu.relation_types
        self.all_types = amu.all_types


    def get_last_row(self, num_rows):
        if self.last_row < 0:
            last_row = num_rows
        else:
            last_row = min(num_rows, self.last_row)
        return last_row


    def process_relationship_file(self):

        # For each line in the file, build a cypher query to MERGE a relationship
        # Each query is added to a list of queries, which are returned to the caller. They are NOT actioned here

        num_data_rows = self.contents.get_row_count()
        from_columns = self.contents.get_column_numbers_list(self.from_node_alias, self.from_types)
        from_label_columns = self.contents.get_column_numbers_list(self.from_label_alias)
        to_columns = self.contents.get_column_numbers_list(self.to_node_alias, self.to_types)
        to_label_columns = self.contents.get_column_numbers_list(self.to_label_alias)
        relation_columns = self.contents.get_column_numbers_list(self.relationship_alias, self.relation_types)
        other_columns = self.from_node_alias + self.from_label_alias + self.to_node_alias + self.to_label_alias + self.relationship_alias
        property_columns = self.contents.get_other_column_numbers_list(other_columns, self.all_types)

        queries = []
        from_ref = 'from'
        relation_ref = 'rel'
        to_ref = 'to'
        relation_ref_dot = relation_ref + '.'

        num_rows = num_data_rows - self.start_from + 1
        this_row = self.start_from-1
        last_row = self.get_last_row(num_data_rows)
        while this_row < last_row:

            relationships = rm.validate_relationships(self.contents.get_column_values_list(this_row, relation_columns))

            properties = self.contents.get_property_values_dict(this_row, property_columns, self.blank_property_list, blank_override=self.blank_property_override)
            # If there are multiple From or To nodes, create a relationship query for each combination
            for from_node in self.contents.get_property_values_list(this_row, from_columns, self.primary_property, self.primary_property):
                validated_csv_from_labels = lm.validate_labels(self.contents.get_column_values_list(this_row, from_label_columns))
                from_labels = lm.sort_relationship_labels(self.required_labels, validated_csv_from_labels)
                for to_node in self.contents.get_property_values_list(this_row, to_columns, self.primary_property, self.primary_property):
                    validated_csv_to_labels = lm.validate_labels(self.contents.get_column_values_list(this_row, to_label_columns))
                    to_labels = lm.sort_relationship_labels(self.required_labels, validated_csv_to_labels)

                    # Build a MERGE query for the relationship(s)
                    for relationship in relationships:
                        for relation in relationship.split(':'):
                            if relation:

                                time_now = amu.get_formatted_time_now()
                                query_text = (QueryBuilder()
                                              .match()
                                              .node(labels=from_labels, ref_name=from_ref, properties=from_node)
                                              .match()
                                              .node(labels=to_labels, ref_name=to_ref, properties=to_node)
                                              .merge()
                                              .node(ref_name=from_ref)
                                              .related_to(label=relation, ref_name=relation_ref)
                                              .node(ref_name=to_ref)
                                              )

                                # Add in System properties
                                if self.add_system_properties:
                                    create_time = relation_ref_dot + self.creation_time_property + '=datetime("' + time_now + '")'
                                    update_time = relation_ref_dot + self.update_time_property + '=datetime("' + time_now + '")'
                                    query_text = query_text.on_create().set_literal(create_time).set_literal(update_time)

                                if len(properties) > 0:
                                    query_text = query_text.set(properties=properties, property_ref=relation_ref_dot)
                                query_text = query_text.toStr()
                                query = Neo4jQuery('relationship', query_text, time_now)

                                if self.validate_only and not self.summarise:
                                    print(query.text)

                                queries.append(query)

            this_row += 1
            messages.message_no_cr(f'Generating queries... {100 * (this_row - self.start_from + 1) / num_rows:.0f}%{chr(13)}')

        messages.message('', False)
        return queries


    def process_relationship_file_batch(self):

        # For each line in the file, build a cypher query to MERGE a relationship
        # Each query is added to a list of queries, which are returned to the caller. They are NOT actioned here

        num_data_rows = self.contents.get_row_count()
        from_columns = self.contents.get_column_numbers_list(self.from_node_alias, self.from_types)
        from_label_columns = self.contents.get_column_numbers_list(self.from_label_alias)
        to_columns = self.contents.get_column_numbers_list(self.to_node_alias, self.to_types)
        to_label_columns = self.contents.get_column_numbers_list(self.to_label_alias)
        relation_columns = self.contents.get_column_numbers_list(self.relationship_alias, self.relation_types)
        other_columns = self.from_node_alias + self.from_label_alias + self.to_node_alias + self.to_label_alias + self.relationship_alias
        property_columns = self.contents.get_other_column_numbers_list(other_columns, self.all_types)

        queries = []
        from_ref = 'from'
        relation_ref = 'rel'
        to_ref = 'to'
        relation_ref_dot = relation_ref + '.'
        payload_ref = 'payload'
        payload_ref_dot = payload_ref + '.'

        time_now = amu.get_formatted_time_now()

        # For best optimisation, we need to create a batch query for all the update with the same labels
        # So we will create a dictionary of queries based on the labels and relationships for each query
        # Since the dictionary key can't be a list, we will create a list (of lists) and use the index in that list as the key
        # When we have worked through all the input and grouped the queries by label and relationship combinations, we will create the queries

        batch_keys = []
        query_dictionary = {}
        dict_size = 0

        num_rows = num_data_rows - self.start_from + 1
        this_row = self.start_from-1
        last_row = self.get_last_row(num_data_rows)
        while this_row < last_row:
            relationships = rm.validate_relationships(self.contents.get_column_values_list(this_row, relation_columns))
            properties = self.contents.get_property_values_dict(this_row, property_columns, self.blank_property_list, blank_override=self.blank_property_override)
            # If there are multiple From or To nodes, create a relationship query for each combination
            for from_node in self.contents.get_property_values_list(this_row, from_columns, self.primary_property, self.primary_property):
                validated_csv_from_labels = lm.validate_labels(self.contents.get_column_values_list(this_row, from_label_columns))
                from_labels = lm.sort_relationship_labels(self.required_labels, validated_csv_from_labels)
                for to_node in self.contents.get_property_values_list(this_row, to_columns, self.primary_property, self.primary_property):
                    validated_csv_to_labels = lm.validate_labels(self.contents.get_column_values_list(this_row, to_label_columns))
                    to_labels = lm.sort_relationship_labels(self.required_labels, validated_csv_to_labels)

                    # Build a MERGE query for the relationship(s)
                    for relationship in relationships:
                        for relation in relationship.split(':'):
                            if relation:

                                explicit_properties, calculated_properties = pm.split_out_functional_properties(properties)
                                new_labels = [from_labels, to_labels, relation, from_node.key, to_node.key, calculated_properties]
                                query_data = [from_node.value, to_node.value, explicit_properties, calculated_properties, time_now]

                                # So now we know all about this particular update. Let's put it in the query dictionary
                                try:
                                    dictionary_index = batch_keys.index(new_labels)
                                    query_dictionary[dictionary_index].append(query_data)
                                except:
                                    dictionary_index = len(batch_keys)
                                    query_dictionary[dictionary_index] = [query_data]
                                    batch_keys.append(new_labels)
                                dict_size += 1

            this_row += 1
            messages.message_no_cr(f'Analysing file... {100 * (this_row - self.start_from + 1) / num_rows:.0f}%{chr(13)}')

        messages.message('', False)

        # Right, so now we have a dictionary of updates grouped by labels. Let's create the queries
        query_count = 0
        for from_to_labels, updates in query_dictionary.items():
            num_updates_for_this_label = len(updates)
            num_batches = int((num_updates_for_this_label - 1) / self.batch_rate) + 1
            from_labels = batch_keys[from_to_labels][0]
            to_labels = batch_keys[from_to_labels][1]
            relationship = batch_keys[from_to_labels][2]
            from_key, from_type = pm.split_node_key(batch_keys[from_to_labels][3])
            to_key, to_type = pm.split_node_key(batch_keys[from_to_labels][4])
            batch_num = 1
            while batch_num <= num_batches:
                if batch_num == num_batches:
                    # Last batch, so
                    batch_size = 1 + (num_updates_for_this_label - 1) % self.batch_rate
                else:
                    batch_size = self.batch_rate

                this_size = 0
                payload = []
                while this_size < batch_size:
                    # Combine all the update data...
                    update = updates[(batch_num - 1) * self.batch_rate + this_size]
                    update_properties = update[2] or {}  # In case update_properties[2] is {}
                    func_properties = update[3] or {}  # In case update_properties[3] is {}
                    update_properties[from_ref] = Neo4jProperty(from_ref, update[0], from_type)
                    update_properties[to_ref] = Neo4jProperty(to_ref, update[1], to_type)
                    if self.add_system_properties:
                        update_properties[self.update_time_property] = Neo4jProperty(self.update_time_property, update[4])
                    payload.append(update_properties)
                    this_size += 1
                    query_count += 1

                formatted_payload = []
                for a_payload in payload:
                    formatted_payload.append(property.format(a_payload))
                # Build a MERGE query using queries
                from_keys = " {" + from_key + ":" + payload_ref_dot + from_ref + "}"
                to_keys = " {" + to_key + ":" + payload_ref_dot + to_ref + "}"
                create_time = relation_ref_dot + self.creation_time_property + '=datetime("' + time_now + '")'
                update_time = relation_ref_dot + self.update_time_property + '=datetime("' + time_now + '")'

                query_text = (QueryBuilder()
                              .unwind_list_as(formatted_payload, payload_ref)
                              .match()
                              .node(labels=from_labels, ref_name=from_ref, properties_literal=from_keys)
                              .match()
                              .node(labels=to_labels, ref_name=to_ref, properties_literal=to_keys)
                              .merge()
                              .node(ref_name=from_ref)
                              .related_to(label=relationship, ref_name=relation_ref)
                              .node(ref_name=to_ref)
                              )

                if self.add_system_properties:
                    query_text = query_text.on_create().set_literal(create_time)

                query_text = query_text.set_literal(relation_ref + ' += ' + payload_ref)
                if func_properties:
                    query_text = query_text.set_functional(func_properties, relation_ref_dot)

                if self.add_system_properties:
                    query_text = query_text.set_literal(update_time)

                query_text = query_text.remove_literal(relation_ref_dot + from_ref + ', ' + relation_ref_dot + to_ref)
                query_text = query_text.toStr()

                query = Neo4jQuery('batch relationship', query_text, time_now, batch_size=this_size)

                if self.validate_only and not self.summarise:
                    print(query.text)

                queries.append(query)
                messages.message_no_cr(f'Generating queries... {100 * query_count / dict_size:.0f}%{chr(13)}')

                batch_num += 1

        messages.message('', False)
        return queries

    def get_filename(self):
        return self.filename

    def is_inline_query(self):
        return False
