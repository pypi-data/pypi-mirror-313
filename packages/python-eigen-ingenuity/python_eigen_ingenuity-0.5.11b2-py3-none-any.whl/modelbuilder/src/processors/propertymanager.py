import assetmodelutilities as amu
from property import Neo4jProperty

def remove_leading_chars(string, chars):
    if string:
        while string[0] in chars:
            string = string[1:]
    return string


def validate_property(formatted_property):
    # formatted_property might have a data type as a suffix e.g. name:str
    # If it does, we need to only validate the node_key name amd not the whole string
    # Return validated node_key, retaining the data type if provided
    # For example:
    #    name:str -> name:str
    #    full name -> `full name`
    #    full name:str -> `full name`:str
    validated = ''
    property_name = formatted_property.split(':')[0]

    if property_name:
        validated += amu.validate(property_name)
        # try to re-add the type prefix
        try:
            validated += ':' + formatted_property.split(':')[1]
        except:
            # but don't worry if it's missing
            pass
    else:
        # Return what we were given
        validated = formatted_property

    return validated


def validate_properties(properties):
    # We either get a string, or a list of strings.
    # Process as appropriate and return a string or list of strings to match input
    if properties:
        if isinstance(properties, str):
            return validate_property(properties)
        else:
            return [validate_property(i) for i in properties]
    else:
        return properties


def validate_property_keys(key_list):
    validated = []
    for key in key_list:
        validated += [*validate_properties(i.split(':')[0] for i in key.split(','))]
    return validated


def sort_properties(properties, default_type):
    validated = {}
    unwanted = []
    retain = []
    if default_type != '':
        def_type = ':' + default_type
    else:
        def_type = ''
    if properties:
        for property in properties:
            if property:
                for prop in property.strip().split(','):
                    # prop has the format key[[:format]:|=value]
                    split_prop = (prop.replace('=', ':')+':').split(':')
                    num_fields = len(split_prop)-1
                    key = split_prop[0]
                    # Normally, there will 2 fields (property and value) or 3 (property, type and value)
                    # But if it's a datetime there could be another 2 (for minutes and seconds - hours is part of day field)
                    # or, possibly, 4 if there's a timezone as well (again hours are part of the seconds)
                    # So, for now, we can check parity to determine if there's a type field present
                    # May need to revisit this logic if other data types are supported that break the parity rule!
                    if num_fields % 2 == 1:
                        # Odd number ==> there is a type
                        prop_type = split_prop[1]
                        # And recombine all the remaining fields back into the value string
                        if num_fields == 3:
                            prop_value = split_prop[2]
                        else:
                            prop_value = ':'.join(split_prop[2:-1])
                    else:
                        # even number ==> no type, so set it to the default or blank
                        prop_type = def_type
                        # And recombine all the remaining fields back into the value string
                        if num_fields == 2:
                            prop_value = split_prop[1]
                        else:
                            prop_value = ':'.join(split_prop[1:-1])

                    # Remove leading ! as they are not needed in the key
                    valid_key = remove_leading_chars(key.strip(), '!')
                    if key.startswith('!!'):
                        retain.append(valid_key)
                    else:
                        # If we have a format and/or value we have a new property to add
                        # ...unless it starts with ! in which case it belongs in the unwanted list (format/value are ignored)
                        if not key.startswith('!'):
                            if num_fields > 1:
                                validated[valid_key] = Neo4jProperty(valid_key, prop_value, prop_type)
                            else:
                                # We have a property with no value field (as opposed to a blank/empty value) i.e. "key", so we ignore it
                                # If a blank value is needed, the property should end with a ':' to specify so i.e. "key:"
                                pass
                        else:
                            # Add to the unwanted list
                            unwanted.append(valid_key)

    return validated, unwanted, retain


def combine_required_properties(config_properties, override_properties, default_type):
    valid_config_properties, unwanted_config_properties, retain_config_properties = sort_properties(config_properties, default_type)
    valid_override_properties, unwanted_override_properties, retain_override_properties = sort_properties(override_properties, default_type)

    config_properties = {i: valid_config_properties[i] for i in valid_config_properties if i not in unwanted_override_properties}
    override_properties = {i: valid_override_properties[i] for i in valid_override_properties}
    required_properties = {**config_properties, **override_properties}

    unwanted_properties = [i for i in unwanted_override_properties] + [i for i in unwanted_config_properties if i not in valid_override_properties.keys() and i not in retain_override_properties]

    return required_properties, unwanted_properties


def split_node_key(node):
    split_node = node.split(':')
    if len(split_node) == 1:
        name = node
        type = ''
    else:
        name = split_node[0]
        type = ':' + split_node[1]
    return name, type


def combine_properties(default_properties, actual_properties):
    combined_properties = default_properties.copy()
    combined_keys = combined_properties
    for property in actual_properties:
        property_key = actual_properties[property].key
        property_value = actual_properties[property].value

        if property_key not in combined_keys:
            # New property, so add to the list
            # Either value has been specified in csv
            combined_properties[property] = actual_properties[property]
        elif property_value != '':
            # Replace the default property with the actual values from the csv file
            combined_properties[property] = actual_properties[property]

    return combined_properties

def split_out_functional_properties(properties):
    explicit = {k: properties[k] for k in properties if k != '' and not properties[k].is_formula}
    functional = {k: properties[k] for k in properties if k != '' and properties[k].is_formula}

    return explicit, functional
