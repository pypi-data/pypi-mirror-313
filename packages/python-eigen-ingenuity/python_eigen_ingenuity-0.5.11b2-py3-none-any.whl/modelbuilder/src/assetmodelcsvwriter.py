import sys
from configmanager import ConfigManager
from connectors.dbconnectors import ConnectionManager
from filemanager import FileManager
from csvwriter import CSVFileWriter

if __name__ == "__main__":

    # Create a configuration manager which will read the command line parameters and the contents of the settings file
    # Any errors are stored in a List, which are then displayed to the user
    config_manager = ConfigManager()
    if config_manager.get_error_count() > 0:
        sys.exit()

    config_manager.read_csv_config()
    if config_manager.get_error_count() > 0:
        sys.exit()

    # Create a connection to the database
    config_manager.reset_errors()
    config_manager.read_version_config()
    config_manager.read_db_config()
    if config_manager.get_error_count() > 0:
        sys.exit()
    connection_manager = ConnectionManager(config_manager)
    db_connector = connection_manager.get_db_connector()

    csv_generator = CSVFileWriter(config_manager, db_connector)
    csv_generator.write_csv_files()

    connection_manager.close()
