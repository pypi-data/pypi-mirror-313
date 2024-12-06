import assetmodelutilities as amu
from queries.query import Neo4jQuery


class CypherFileProcessor:

    def __init__(self, filename, config, inline_query=False):

        self.filename = filename
        self.inline_query = inline_query

        self.def_path = config.get_default_path()
        self.validate_only = config.in_validation_mode()
        self.summarise = config.in_summary_mode()

    def process_cypher_file(self):

        queries = []
        try:
            cypher_file_name = amu.find_file(self.def_path, self.filename)
            cypher_file = open(cypher_file_name, 'r', encoding='UTF8')
            cypher_list = list(cypher_file)
            file_queries = 0
            next_query = ''
            cypher_file_size = len(cypher_list)
            entry_count = 0
            while entry_count < cypher_file_size:
                this_entry = cypher_list[entry_count].strip()
                if not this_entry.startswith('#') and not this_entry == '\n':
                    next_query += this_entry + '\n'
                    if not this_entry.endswith(',') and not this_entry.endswith('\\'):
                        while next_query.endswith('\n'):
                            next_query = next_query[0:-1]
                        query = Neo4jQuery('cypher', next_query.replace('\\', '').strip())
                        next_query = ''
                        if self.validate_only and not self.summarise:
                            print(query.text)
                        queries.append(query)
                        file_queries += 1
                entry_count += 1

            # Process any leftover query at the end of the file
            # This shouldn't normally happen, but will if the last entry ends with a comma or backslash
            # Any trailing backslash is removed, so the query may be OK but will be missing any continuation clause(s)
            # But a trailing comma will be left - result is a query that will generate an error if executed!
            # This is done intentionally as the query in the input file is incomplete
            if next_query != '':
                query = Neo4jQuery('cypher', next_query[0:-1].replace('\\', '').strip())
                if self.validate_only and not self.summarise:
                    print(query.text)
                queries.append(query)
                file_queries += 1

            cypher_file.close()
        except:
            print(f'{self.filename} not found')

        return queries

    def process_query_list(self):

        queries = []
        query = Neo4jQuery('query', self.filename)
        if self.validate_only and not self.summarise:
            print(query.text)
        queries.append(query)
        return queries

    def get_filename(self):
        return self.filename

    def is_inline_query(self):
        return self.inline_query
