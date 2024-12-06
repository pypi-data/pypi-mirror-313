class GenericConnector:

    # Connector template
    # Specific connectors will most probably override the majority of these functions

    def __init__(self, db_connection_details, output_file, results_file):
        self.output_file = output_file
        self.results_file = results_file
        self.last_query = 0
        self.last_version_query = 0
        self.query_id = ''

    def close(self):
        pass

    def convert_result(self, this_result):
        pass

    def execute(self, query, query_num=-1):
        if query_num == -1:
            self.last_version_query += 1
            self.query_id = f'{self.last_query}.{self.last_version_query}'
        else:
            self.last_query = query_num
            self.last_version_query = 0
            self.query_id = f'{self.last_query}'

    def print_response(self, response):
        pass

