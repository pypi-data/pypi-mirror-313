# Query Builder based on Cymple's OpenSource code
import property


class Query():

    def __init__(self, query):
        self.query = query

    def __str__(self) -> str:
        return self.query.strip()

    def __add__(self, other):
        return Query(self.query.strip() + ' ' + other.query.strip())

    def __iadd__(self, other):
        self.query = self.query.strip() + ' ' + other.query.strip()
        return self

    def toStr(self):
        return str(self)

class QueryStart(Query):
    """ """

class Call(Query):

    def call(self):
        return ValidAfterCall(self.query + ' CALL')

class CaseWhen(Query):

    def case_when(self, filters, on_true: str, on_false: str, ref_name: str, comparison_operator: str = "=", boolean_operator: str = "AND"):
        filt = ' CASE WHEN ' + property.to_str(filters, comparison_operator, boolean_operator)
        filt += f' THEN {on_true} ELSE {on_false} END as {ref_name}'
        return ValidAfterCaseWhen(self.query + filt)

class Delete(Query):

    def delete(self, ref_name: str):
        ret = f' DELETE {ref_name}'
        return Query(self.query + ret)

    def detach_delete(self, ref_name: str):
        ret = f' DETACH DELETE {ref_name}'
        return Query(self.query + ret)

class Where(Query):

    def where_literal(self, literal: str):
        if literal:
            return ValidAfterWhere(self.query + f' WHERE {literal}')
        else:
            return ValidAfterWhere(self.query)

    def where(self, name: str, comparison_operator: str, value: str):
        return self.where_multiple({name: value}, comparison_operator)

    def where_multiple(self, filters, comparison_operator: str = "=", boolean_operator: str = ' AND '):
        filt = ' WHERE ' + property.to_str(filters, comparison_operator, boolean_operator)
        return ValidAfterWhere(self.query + filt)

    def where_additional(self, filters, comparison_operator: str = "=", boolean_operator: str = ' AND '):
        filt = boolean_operator + property.to_str(filters, comparison_operator, boolean_operator)
        return ValidAfterWhere(self.query + filt)

class Match(Query):

    def match(self):
        return ValidAfterMatch(self.query + ' MATCH')

    def match_optional(self):
        return ValidAfterMatch(self.query + ' OPTIONAL MATCH')

class Merge(Query):

    def merge(self):
        return ValidAfterMerge(self.query + ' MERGE')

class Node(Query):

    def node(self, labels=None, ref_name: str = None, properties=None, properties_literal: str = ''):
        if not labels:
            labels_string = ''
        elif isinstance(labels, str):
            labels_string = labels
        else:
            labels_string = f':{":".join(labels).strip()}'

        if properties_literal:
            property_string = properties_literal
        else:
            if not properties:
                property_string = ''
            else:
                property_string = f' {{{property.format_property_list(properties, property_ref=ref_name)}}}'

        ref_name = ref_name or ''

        if not (self.query.endswith('-') or self.query.endswith('>') or self.query.endswith('<')):
            self.query += ' '

        return ValidAfterNode(self.query + f'({ref_name}{labels_string}{property_string})')

    def node_batch(self, labels=None, ref_name: str = None, properties: str = None):
        if not labels:
            labels_string = ''
        elif isinstance(labels, str):
            labels_string = labels
        else:
            labels_string = f':{":".join(labels).strip()}'.replace('::', ':')

        ref_name = ref_name or ''

        if not (self.query.endswith('-') or self.query.endswith('>') or self.query.endswith('<')):
            self.query += ' '

        return ValidAfterNode(self.query + f'({ref_name}{labels_string} {{{properties}}})')

class OnCreate(Query):

    def on_create(self):
        return ValidAfterOnCreate(self.query + ' ON CREATE')

class OnMatch(Query):

    def on_match(self):
        return ValidAfterOnMatch(self.query + ' ON MATCH')

class OperatorEnd(Query):

    def operator_end(self):
        return ValidAfterOperatorEnd(self.query + ' )')

class OperatorStart(Query):

    def operator_start(self, operator: str, ref_name: str = None, args=None):
        result_name = '' if ref_name is None else f'{ref_name} = '
        arguments = '' if args is None else f' {args}'

        return ValidAfterOperatorStartValidAs(self.query + f' {result_name}{operator}({arguments}')

class Relation(Query):

    def related(self, label: str = None, ref_name: str = None, properties=None):
        return ValidAfterRelation(self.query + self._directed_relation('none', label, ref_name, properties))

    def related_to(self, label: str = None, ref_name: str = None, properties=None):
        return ValidAfterRelation(self.query + self._directed_relation('forward', label, ref_name, properties))

    def related_from(self, label: str = None, ref_name: str = None, properties=None):
        return ValidAfterRelation(self.query + self._directed_relation('backward', label, ref_name, properties))

    def related_variable_len(self, min_hops: int = -1, max_hops: int = -1):
        min_hops_str = '' if min_hops == -1 else str(min_hops)
        max_hops_str = '' if max_hops == -1 else str(max_hops)

        relation_length = '*' if min_hops == -1 and max_hops == - \
            1 else (f'*{min_hops_str}'if min_hops == max_hops else f'*{min_hops_str}..{max_hops_str}')

        if relation_length:
            relation_str = f'[{relation_length}]'
        else:
            relation_str = ''

        return ValidAfterRelation(self.query + f'-{relation_str}-')

    def _directed_relation(self, direction: str, label: str, ref_name: str = None, properties=None):
        relation_type = '' if label is None else f':{label}'
        relation_ref_name = '' if ref_name is None else f'{ref_name}'
        relation_properties = f' {{{property.to_str(properties)}}}' if properties else ''

        if relation_ref_name or relation_type:
            relation_str = f'[{relation_ref_name}{relation_type}{relation_properties}]'
        else:
            relation_str = ''

        if direction == 'forward':
            return f'-{relation_str}->'
        if direction == 'backward':
            return f'<-{relation_str}-'

        return f'-{relation_str}-'

class Remove(Query):

    def remove_literal(self, set_literal):
        return ValidAfterRemove(self.query + ' REMOVE ' + set_literal)

class Return(Query):

    def return_literal(self, literal: str):
        ret = f' RETURN {literal}'
        return Query(self.query + ret)

    def return_mapping(self, mappings):

        if not isinstance(mappings, list):
           mappings = [mappings]

        ret = ' RETURN ' + \
            ', '.join(
                f'{mapping[0]} as {mapping[1]}' if mapping[1] else mapping[0].replace(".", "_")
                for mapping in mappings)

        return Query(self.query + ret)

class Set(Query):

    def set(self, properties, property_ref=''):
        return ValidAfterSet(self.query + ' SET ' + property.format_property_list(properties, "=", ",", property_ref, property_ref))

    def set_functional(self, properties, property_ref=''):
        return ValidAfterSet(self.query + ' SET ' + property.format_property_list(properties, "=", ",", property_ref, property_ref))

    def set_labels(self, ref_name: str = '', labels=None):
        if not labels:
            labels_string = ''
        elif isinstance(labels, str):
            labels_string = f'{labels}'
        else:
            labels_string = f':{":".join(labels).strip()}'

        return ValidAfterSet(self.query + ' SET ' + ref_name + labels_string)

    def set_literal(self, set_literal):
        return ValidAfterSet(self.query + ' SET ' + set_literal)

class Unwind(Query):

    def unwind(self, variables: str):
        return ValidAfterUnwind(self.query + f' UNWIND {variables}')

    def unwind_list_as(self, variables: list, ref):
        unwind = variables[0]
        next = 1
        while next < len(variables):
            unwind += ','+variables[next]
            next += 1

        return ValidAfterUnwind(self.query + f' UNWIND [{unwind}] AS {ref}')

class With(Query):

    def with_(self, variables: str):
        return ValidAfterWith(self.query + f' WITH {variables}')

class Yield(Query):

    def yield_(self, mappings):
        if not isinstance(mappings, list):
            mappings = [mappings]

        query = ' YIELD ' + \
            ', '.join(f'{mapping[0]} as '
                      f'{mapping[1] if mapping[1] else mapping[0].replace(".", "_")}'
                      for mapping in mappings)
        return ValidAfterYield(self.query + query)

class ValidAsQueryStart(Match, Merge, Call, Unwind):
    """ """

class ValidAfterCall(Node, Return, OperatorStart):
    """ """

class ValidAfterCaseWhen(ValidAsQueryStart, With, Unwind, Where, CaseWhen, Return):
    """ """

class ValidAfterDelete(Query):
    """ """

class ValidAfterWhere(Return, Delete, With, Where, OperatorStart, ValidAsQueryStart, Set, Remove):
    """ """

class ValidAfterMatch(Node, Return, OperatorStart):
    """ """

class ValidAfterMerge(Node, Return, OperatorStart):
    """ """

class ValidAfterNode(Relation, Return, Delete, With, Where, OperatorStart, OperatorEnd, Remove, Set, OnCreate, OnMatch, ValidAsQueryStart):
    """ """

class ValidAfterOnCreate(Set, OperatorStart):
    """ """

class ValidAfterOnMatch(Set, OperatorStart):
    """ """

class ValidAfterOperatorEnd(ValidAsQueryStart, Yield, With, Return):
    """ """

class ValidAfterOperatorStartValidAs(ValidAsQueryStart, Node, With, OperatorEnd):
    """ """

class ValidAfterRelation(Node):
    """ """

class ValidAfterReturn(ValidAsQueryStart, With, Unwind, Return):
    """ """

class ValidAfterSet(ValidAsQueryStart, OnMatch, OnCreate, Set, With, Unwind, Remove, Return):
    """ """

class ValidAfterRemove(Set, With, Unwind, Remove, Return):
    """ """

class ValidAfterUnwind(ValidAsQueryStart, With, Unwind, Return):
    """ """

class ValidAfterWith(ValidAsQueryStart, With, Unwind, Where, CaseWhen, Return):
    """ """

class ValidAfterYield(ValidAsQueryStart, Node, With):
    """ """

class QueryBuilder(ValidAsQueryStart):
    def __init__(self) -> None:
        super().__init__('')

    def reset(self):
        self.query = ''
        return self
