from connectors.httpsconnector import HTTPSConnector
from connectors.boltconnector import BoltConnector

class ConnectionManager:

    def __init__(self, config_manager):
        self.query_output_file = None
        query_file_name = config_manager.get_query_output()
        if query_file_name is not None:
            try:
                self.query_output_file = open(query_file_name, 'w', encoding='UTF8')
            except:
                pass

        self.results_output_file = None
        results_file_name = config_manager.get_results_output()
        if results_file_name is not None:
            try:
                self.results_output_file = open(results_file_name, 'w', encoding='UTF8')
            except:
                pass

        db_connection_details = config_manager.get_db_connection_dict()
        url = db_connection_details['url']

        if url.startswith('https:'):
            self.db_connection = HTTPSConnector(db_connection_details, config_manager, self.query_output_file, self.results_output_file)
        else:
            self.db_connection = BoltConnector(db_connection_details, config_manager, self.query_output_file, self.results_output_file)

    def get_db_connector(self):
        return self.db_connection

    def close(self):
        if self.query_output_file is not None:
            self.query_output_file.close()
        if self.results_output_file is not None:
            self.results_output_file.close()

        self.db_connection.close()
