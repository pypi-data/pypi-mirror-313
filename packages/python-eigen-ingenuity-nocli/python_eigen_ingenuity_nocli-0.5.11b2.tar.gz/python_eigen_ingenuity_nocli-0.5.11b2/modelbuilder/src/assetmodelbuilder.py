import sys, os, functools, inspect

# Add current dir to python path to allow relative imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from configmanager import ConfigManager
from connectors.dbconnectors import ConnectionManager
from filemanager import FileManager

import sys
import inspect
import functools

# Take Arguments passed to build function and convert them to sys args to use the cli tool from script
def _convert_sys_argv_(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get the function signature
        sig = inspect.signature(func)
        
        # Create an empty list to hold the sys.argv entries
        argv_entries = []
        
        # Get the arguments passed by position
        args_dict = dict(zip(sig.parameters, args))

        # Loop through the parameters in the function signature
        for param_name, param in sig.parameters.items():
            param_name_cleaned = param_name.replace('_', '')

            # Check if the parameter is provided as a keyword argument
            if param_name in kwargs:
                arg_value = kwargs[param_name]
            # Check if the parameter is provided as a positional argument
            elif param_name in args_dict:
                arg_value = args_dict[param_name]
            else:
                continue  # Skip if not provided

            # If parameter is a boolean, handle it as store_true action
            if param.annotation == bool:
                if arg_value:  # If True, add only the flag
                    argv_entries.append(f"--{param_name_cleaned}")
                else:  # If False, skip adding this argument
                    continue
            elif param.annotation == list:
                argv_entries.extend([f"--{param_name_cleaned}"])
                argv_entries.extend(arg_value)
            else:
                # For non-boolean parameters, add the value
                argv_entries.extend([f"--{param_name_cleaned}", str(arg_value)])

        # Extend sys.argv with the generated entries
        sys.argv.extend(argv_entries)
        
        # Call the original function
        return func(*args, **kwargs)

    return wrapper


@_convert_sys_argv_
def build(path:str='.', config:str='config.ini', configsection:str='', file:str='', query:list=[], preprocess:list=[], postprocess:list=[], delete_all:list=[], separator:str=';',
            start_from:int=1, end_at:int=1, no_versions:bool=False, no_system_properties:bool=False, ignore_nodes:bool=False, skip_duplicates:bool=False,
            no_duplicates:bool=False, allow_blanks:list=[], replace_blanks:str='', batch:int=0, auth:bool=False, order:str='qnrc', filetypes:str='qnrc', primary_property:str='',
            required_labels:list=[], required_properties:list=[], database:str='0', verify:bool=False, summarise:bool=False, show_queries:bool=False, show_returns:bool=False,
            write_queries:str='', write_returns:str='', display_rate='auto', create_node_csv_file:bool=False, node_labels:list=[], node_properties:list=[],
            csv_file_suffix:str='', create_relationship_csv_file:bool=False, csv_to_labels:list=[], csv_to_properties:str=''):
    """The main model builder tools, features a suite of options that allow for importing, exporting, building and updating neo4j data models

        Args:
            ## Input Parameters
            path: Location of the input and output files. Default is current folder
            config: Name of the configuration file, default is config.ini in the folder from path parameter
            configsection: Section of the config to use, if not DEFAULT
            database: Database ID (as set in config file). Defaults to first entry
            file: Space separated string list of input files
            query: Space separated string list of queries to run
            preprocess: Command(s) to execute before processing input files
            postprocess: Command(s) to execute after processing input files
            delete_all: Lists of labels to identify nodes to delete before processing any files

            ## Change the behaviour of the processing away from the default
            separator: The separator used in the csv files. Default is a semi-colon ';'
            start_from: The first query to process in a .csv file. No effect on cypher files. Default is 1
            end_at: The last query to process in a .csv file. No effect on cypher files. Default is last query in the file
            no_versions: Suppress creation of version nodes
            no_system_properties: Suppress creation of system properties on nodes and relationships. Implies -nov
            ignore_nodes: Treat node columns in relationship files as relationship properties
            skip_duplicates: Don't create a version node if there are no changes. Same as -nod
            allow_blanks: List of properties to create even if blank
            replace_blanks: Used in combination with allowblanks. Write a specific value instead of blank e.g "__NULL"
            batch: Number of queries to batch together when processing a node .csv file, significantly improves performance
            auth: Enable Azure Authentication
            order: Order in which to process the input files. Default is qnrc
            filetypes: File types to process. Default is all

            # Override values in the config file
            primary_property: Primary property
            required_labels: Required labels - appended to contents of config; use !Label to remove
            required_properties: Required properties - appended to contents of config; use !property to remove

            # What output is required
            verify: Display the generated queries, but do not process them
            summarise: Show a summary of the queries, but do not process them
            show_queries: Display the queries as they are processed. No effect if -v present
            show_returns: Display data from any RETURN clause
            write_queries: Name of a file to record the processed queries. No effect if -v present
            write_returns: Name of a file to record the results of the queries. No effect if -v present
            display_rate: Set the frequency of progress update messages. No effect if -v present

            # Control of the CSV writer
            create_node_csv_file: Create Node csv file(s) from Asset Model'
            node_labels: Lists of labels to identify nodes to write to csv file'
            node_properties: Primary property of nodes'
            csv_file_suffix: Suffix to use in the output Node .csv file'
            create_relationship_csv_file: Create Relationship csv file(s) from Asset Model'
            csv_to_labels: Lists of labels to identify to nodes to write to csv file'
            csv_to_properties: Primary property of To nodes'

        Returns:
            Boolean for Sucess/Failure. If any queries failed gives False. Logs are printed to terminal during running. TBE
    """
    _asset_model_builder_()


def _asset_model_builder_():
    # Create a configuration manager which will read the command line parameters and the contents of the settings file
    # Any errors are stored in a List, which are then displayed to the user
    config_manager = ConfigManager()
    if config_manager.get_error_count() > 0:
        sys.exit()

    config_manager.read_csv_config()
    if config_manager.get_error_count() > 0:
        sys.exit()

    output_file = config_manager.get_query_output()

    # Read the data needed to create version nodes and relationships
    config_manager.reset_errors()
    config_manager.read_version_config()
    if config_manager.get_error_count() > 0:
        sys.exit()

    # Create a csv file Manager to process all the input files
    file_manager = FileManager(config_manager)
    file_manager.analyse_files()

    # Create a connection to the database
    config_manager.reset_errors()
    config_manager.read_db_config()
    if config_manager.get_error_count() > 0:
        sys.exit()
    connection_manager = ConnectionManager(config_manager)
    db_connector = connection_manager.get_db_connector()

    # And process the generated queries
    file_manager.process_files(db_connector)

    connection_manager.close()


if __name__ == "__main__":
    _asset_model_builder_()