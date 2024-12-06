import assetmodelutilities as amu


def validate_label_string(label_string):
    # The input string can both comma and colon separated.
    # We will return a string of colon separated labels, but without a leading colon
    # Labels that do not conform to Neo4j naming rules will be back-ticked (`)
    # For example:
    #    fruit --> fruit
    #    apple,tree --> apple:tree
    #    birds&bees --> `birds&bees`
    #    one,two:!three --> one:two:!three

    result = ''
    for a_label in label_string.replace(',', ':').split(':'):
        # Labels may be prefixed with '!' or '!!'. Check for these before validating
        if a_label.startswith('!!'):
            result += ':!!' + amu.validate(a_label[2:])
        elif a_label.startswith('!'):
            result += ':!' + amu.validate(a_label[1:])
        elif a_label:
            result += ':' + amu.validate(a_label)

    # Remove the leading ':' from the result because we don't want it
    if result.startswith(':'):
        result = result[1:]

    return result


def validate_labels(labels):
    # We either get a string, or a list of strings.
    # Process as appropriate and return a string or list of strings to match input
    if isinstance(labels, str):
        return validate_label_string(labels)
    else:
        return [validate_label_string(i) for i in labels]


def validate_label_string_to_list(labels):
    # Validate a single input string as normal
    # But return the result as a list of the individual labels (without colons) instead of the combined string
    validated_string = validate_label_string(labels)
    validated_list = [i for i in validated_string.split(':') if i != '']
    return list(set(validated_list))


def sort_labels(required_labels, labels):
    # So this is where the real magic happens
    # Combine the various sets of input labels into 4 output lists
    # merge_labels - labels used in the MERGE clause
    # new_labels - labels added to SET clause
    # remove labels - labels that are removed from a node via a REMOVE clause
    # relationship labels - used in the MATCH clause to find the start/end nodes of a relationship (not used for node updates)

    # First off, make a list of all the unique labels given to us
    # Note the string(s) in the input may contain more than one label, hence the split by colon
    unique_labels = []
    for label in labels:
        for split_label in label.replace(',', ':').split(':'):
            if split_label and split_label not in unique_labels:
                unique_labels.append(split_label)

    # Now the first sort
    wanted_label_list = []    # Labels that are required
    unwanted_label_list = []  # Labels that are not wanted (i.e. prefixed with ! in the required label list)
    remove_label_list = []    # Labels that are to be removed (i.e. prefixed with ! in the .csv file)
    for label in unique_labels:
        if label.startswith('!!'):
            wanted_label_list.append(label[2:])
        elif not ('!'+label in required_labels or label.startswith('!')):
            wanted_label_list.append(label)
        elif label.startswith('!'):
            remove_label_list.append(label[1:])
        else:
            unwanted_label_list.append('!' + label)

    return wanted_label_list, unwanted_label_list, remove_label_list


def sort_node_labels(required_labels, input_labels):
    wanted_label_list, unwanted_label_list, remove_label_list = sort_labels(required_labels, input_labels)
    # MERGE clause: required labels without !
    merge_labels = [i for i in required_labels if (not ('!' + i in unwanted_label_list) and not (i.startswith('!')))]
    # Labels to add via the SET clause: specified in the csv file
    new_labels = [i for i in wanted_label_list if i not in merge_labels]

    return merge_labels, new_labels, remove_label_list


def sort_relationship_labels(required_labels, input_labels):
    wanted_label_list, unwanted_label_list, remove_label_list = sort_labels(required_labels, input_labels)
    # Labels used in the relationship MATCH queries
    relationship_labels = [i for i in required_labels + wanted_label_list if (not ('!' + i in unwanted_label_list) and not (i in remove_label_list) and not (i.startswith('!')))]

    return list(set(relationship_labels))

def sort_output_labels(node_labels, version_labels):
    # We need the specifed node labels, but not any version labels
    # This means that any version nodes will not be processed
    input_labels = node_labels + ['!' + label for label in version_labels if not label.startswith('!')]
    # Use the same sort algorithm, but we don't use any required labels
    wanted_label_list, unwanted_label_list, remove_label_list = sort_labels('', input_labels)

    return wanted_label_list, remove_label_list


def strip_quotes(quote_list):
    stripped_list = [i[1:-1].replace('``', '`') if i.startswith('`') and i.endswith('`') else i for i in quote_list]
    return stripped_list


def merge_labels(self, required_labels, unrequired_labels, remove_labels):
    merged_labels = [i for i in self.required_labels + required_labels if (not ('!' + i in unrequired_labels) and not (i in remove_labels) and not (i.startswith('!')))]
    return merged_labels


def combine_required_labels(config_labels, override_labels):
    valid_config_labels = validate_labels(config_labels)
    valid_override_labels = validate_label_string_to_list(override_labels)
    required_labels = [i for i in valid_config_labels if (not(i.startswith('!') and ('!'+i not in valid_config_labels)) and ('!'+i not in valid_override_labels))] + [i for i in valid_override_labels if (not(i.startswith('!')) and ('!'+i not in valid_override_labels))]
    unwanted_labels = [i for i in valid_config_labels if (i.startswith('!') and (i[1:] not in valid_override_labels) and ('!' + i not in valid_override_labels))] + [i for i in valid_override_labels if i.startswith('!') and not i.startswith('!!')]

    combined_list = list(set(required_labels + unwanted_labels))
    if '' in combined_list:
        combined_list.remove('')

    return combined_list

def validate_output_labels(label_list):
    output_list = ['`'+label+'`' if label.startswith('!') else label for label in label_list]
    return ':'.join(output_list)

