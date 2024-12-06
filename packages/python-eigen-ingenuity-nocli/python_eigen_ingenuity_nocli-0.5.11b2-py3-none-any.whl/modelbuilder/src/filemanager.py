import ast
from fileanalyser import FileAnalyser
from processors.cypherfileprocessor import CypherFileProcessor
from processors.nodefileprocessor import NodeFileProcessor
from processors.relationshipfileprocessor import RelationshipFileProcessor
import assetmodelutilities as amu
from queries.query import *
from versionmanager import VersionManager
from messages import *
import os

class FileManager:

    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.validation_mode = config_manager.in_validation_mode()
        self.report_queries = config_manager.get_show_query()
        self.show_progress = config_manager.get_display_rate()
        self.show_return = config_manager.get_show_return()
        self.process_order = config_manager.get_process_order()
        self.display_rate = config_manager.get_display_rate()
        self.no_versions = config_manager.get_noversion()
        self.start_from = config_manager.get_start_from()
        self.batch_rate = config_manager.get_batch_rate()
        self.stop_on_failure = config_manager.get_stop_on_failure()
        self.process_file_types = config_manager.get_process_file_types()

        # Create a list of error each type
        self.both_file_list = []
        self.neither_file_list = []
        self.file_not_found_list = []
        self.unrecognised_file_type_list = []
        self.incorrect_file_list = []
        self.incorrect_section_list = []
        self.incomplete_file_list = []
        self.incomplete_file_errors = []

        # And a list of lists for the queries in specified priority order
        self.valid_file_list = [[], [], [], [], [], []]

        self.invalid_file_count = 0

        self.config_section = config_manager.get_config_section()
        self.section = self.config_section

        self.file_analysers = {s: FileAnalyser(config_manager, s) for s in config_manager.get_available_sections()}
        self.version_managers = {s: VersionManager(config_manager, s) for s in config_manager.get_available_sections()}

    def check_section(self, in_file, empty_section_response):
        file = in_file.strip()
        if file.startswith('#'):
            filename = file
            section = None
        else:
            if '[' in file and ']' in file:
                # New section directive found
                section_start = file.index('[')
                section_end = file.index(']')
                section = file[section_start + 1:section_end]
                filename = file[section_end + 1:].strip()
                if filename == '':
                    self.section = section or self.config_section
                elif section == '':
                    section = empty_section_response
            else:
                section = self.section
                filename = in_file

        return filename, section

    def analyse_a_file(self, filename, section):
        a_file = filename.replace('\n', '')
        a_file_split = a_file.split('.')
        if len(a_file_split) > 1:
            file_type = a_file_split[-1]
        else:
            file_type = ''
        match file_type:
            case 'csv':
                if section == None:
                    file, this_section = self.check_section(a_file, '')
                else:
                    file = a_file
                    this_section = section
                self.analyse_csv_file(file, this_section)
            case 'cypher' | 'qry':
                self.analyse_cypher_file(a_file)
            case 'lst':
                self.analyse_lst_file(a_file, section)
            case _:
                self.unrecognised_file_type_list.append(a_file)
                self.invalid_file_count += 1

    def add_file_to_process_list(self, file_processor, file_type):
        if file_type in ['pre', 'pre-file', 'post', 'post-file']:
            file_type_check = 'q'
        else:
            file_type_check = file_type

        if file_type_check in self.process_file_types:
            priority = self.process_order[file_type]
            self.valid_file_list[priority] += [{'processor': file_processor, 'type': file_type}]
        else:
            info_message(file_processor.get_filename(), ' not processed as requested')

    def analyse_lst_file(self, filename, def_section=''):

        f_name = amu.find_file(self.config_manager.get_default_path(), filename)
        current_section = self.section
        self.section = def_section
        if f_name is not None:
            lst_file = open(f_name, 'r')
            for a_file in lst_file:
                if not a_file.startswith('#') and a_file != '\n':
                    file, section = self.check_section(a_file, self.config_section)
                    if file != '':
                        self.analyse_a_file(file, section)
            lst_file.close()
        else:
            warning_message(f'{filename} not found')

        self.section = current_section

    def analyse_files(self):

        message('Checking file types...')
        preprocess_list = self.config_manager.get_preprocess_query_list()
        for a_query in preprocess_list:
            if a_query is not None:
                a_query_split = a_query.split('.')
                if len(a_query_split) > 1:
                    file_type = a_query_split[-1]
                else:
                    file_type = ''
                if file_type == 'cypher' or file_type == 'qry':
                    this_file_processor = CypherFileProcessor(a_query, self.config_manager)
                    self.add_file_to_process_list(this_file_processor, 'pre-file')
                else:
                    query_processor = CypherFileProcessor(a_query, self.config_manager, True)
                    self.add_file_to_process_list(query_processor, 'pre')

        labels_to_delete_list = self.config_manager.get_labels_to_delete_list()
        if labels_to_delete_list == []:
            query = f'MATCH (n) DETACH DELETE n'
            query_processor = CypherFileProcessor(query, self.config_manager, True)
            self.add_file_to_process_list(query_processor, 'pre')
        else:
            for label_list in labels_to_delete_list:
                match_list = ''
                no_match_list = ''
                for label in label_list.split(':'):
                    if label.startswith('!'):
                        no_match_list += ':' + label[1:]
                    else:
                        match_list += ':' + label
                query = f'MATCH (n{match_list}) '
                if no_match_list != '':
                    query += f'WHERE NOT n{no_match_list} '
                query += 'DETACH DELETE n'
                query_processor = CypherFileProcessor(query, self.config_manager, True)
                self.add_file_to_process_list(query_processor, 'pre')

        # Process each file in the list, and determine its content type (ignoring any clues in the filename!)
        # Analyse each of the specified input .csv files to determine if they contain Nodes or Relationships
        # If the file doesn't have a valid combination of columns (or is missing) they are placed in the appropriate list
        file_list = self.config_manager.get_input_file_list()
        for a_file in file_list:
            a_file_split = a_file.split(',')
            for a_split_file in a_file_split:
                if a_split_file != '':
                    self.analyse_a_file(a_split_file.strip(), None)

        query_list = self.config_manager.get_inline_query_list()
        for a_query in query_list:
            if a_query is not None:
                query_processor = CypherFileProcessor(a_query, self.config_manager, True)
                self.add_file_to_process_list(query_processor, 'q')

        postprocess_list = self.config_manager.get_postprocess_query_list()
        for a_query in postprocess_list:
            if a_query is not None:
                a_query_split = a_query.split('.')
                if len(a_query_split) > 1:
                    file_type = a_query_split[-1]
                else:
                    file_type = ''
                if file_type == 'cypher' or file_type == 'qry':
                    this_file_processor = CypherFileProcessor(a_query, self.config_manager)
                    self.add_file_to_process_list(this_file_processor, 'post-file')
                else:
                    query_processor = CypherFileProcessor(a_query, self.config_manager, True)
                    self.add_file_to_process_list(query_processor, 'post')

    def add_file_to_list(self, this_file_processor, this_file_type, file_errors=None):

        match this_file_type:
            case 'nodes':
                self.add_file_to_process_list(this_file_processor, 'n')
            case 'relationships':
                self.add_file_to_process_list(this_file_processor, 'r')
            case 'both':
                self.both_file_list.append(this_file_processor.get_filename())
                self.invalid_file_count += 1
            case 'neither':
                self.neither_file_list.append(this_file_processor.get_filename())
                self.invalid_file_count += 1
            case 'fnf':
                self.file_not_found_list.append(this_file_processor.get_filename())
                self.invalid_file_count += 1
            case 'incorrect file format':
                self.incorrect_file_list.append(this_file_processor.get_filename())
                self.invalid_file_count += 1
            case 'incomplete row(s)':
                self.incomplete_file_list.append([this_file_processor.get_filename(), file_errors])
                self.invalid_file_count += 1
            case 'invalid config section':
                self.incorrect_section_list.append(this_file_processor.get_filename())
                self.invalid_file_count += 1
            case _:
                pass

    def analyse_csv_file(self, csv_file, config_section):
        if not config_section:
            config_section = 'DEFAULT'
        if config_section not in self.config_manager.get_available_sections():
            # Use NodeFileProcessor as placeholder. It won't be used, other than to process the errors
            this_csv_file_processor = NodeFileProcessor(csv_file, self.config_manager, None, 'DEFAULT')
            self.add_file_to_list(this_csv_file_processor, 'invalid config section', [])
        else:
            # Analyse each of the specified input .csv files to determine if they contain Nodes or Relationships
            # If the file doesn't have a valid combination of columns (or is missing) they are placed in the appropriate list
            this_csv_file_type, csv_contents, file_errors = self.file_analysers[config_section].determine_file_type(csv_file, 'csv')
            if this_csv_file_type == 'nodes':
                this_csv_file_processor = NodeFileProcessor(csv_file, self.config_manager, csv_contents, config_section)
            elif this_csv_file_type == 'relationships':
                this_csv_file_processor = RelationshipFileProcessor(csv_file, self.config_manager, csv_contents, config_section)
            else:
                # Use NodeFileProcessor as placeholder. It won't be used, other than to process the errors
                this_csv_file_processor = NodeFileProcessor(csv_file, self.config_manager, csv_contents, config_section)
            self.add_file_to_list(this_csv_file_processor, this_csv_file_type, file_errors)

    def analyse_cypher_file(self, query_file):
        this_file_processor = CypherFileProcessor(query_file, self.config_manager)
        self.add_file_to_process_list(this_file_processor, 'c')

    def process_files(self, db_connector):

        # Report on the missing or faulty files
        self.process_invalid_files()

        if self.invalid_file_count == 0 or not self.stop_on_failure:
            # Finally, process the files that we can
            self.all_results = QueryResult(False)
            self.all_version_results = QueryResult(False)
            queries_processed = self.process_valid_files(db_connector)
            info_message(f'{queries_processed} queries processed in total')
            self.all_results.print_results('Total updates made: ')
            self.all_version_results.print_results('Total version updates made: ', '')

    def process_invalid_files(self):
        self.process_not_found_files()
        self.process_unrecognised_file_type_files()
        self.process_incorrect_files()
        self.process_incomplete_files()
        self.process_incorrect_sections()
        self.process_neither_found_files()
        self.process_both_files()

    def process_not_found_files(self):
        for file in self.file_not_found_list:
            warning_message(f'{file} not found')

    def process_unrecognised_file_type_files(self):
        for file in self.unrecognised_file_type_list:
            error_message(f'{file} has unrecognised file type - file not processed')

    def process_incorrect_files(self):
        for file in self.incorrect_file_list:
            error_message(f'{file} is not a correctly formatted .csv file - file not processed')

    def process_incorrect_sections(self):
        for file in self.incorrect_section_list:
            error_message(f'{file} has an invalid config section - file not processed')

    def process_incomplete_files(self):
        for file in self.incomplete_file_list:
            error_message(f'{file[0]} has incomplete data in rows {file[1]} - file not processed')

    def process_neither_found_files(self):
        for file in self.neither_file_list:
            error_message(f'Insufficient data in {file} to determine content type - file not processed')

    def process_both_files(self):
        for file in self.both_file_list:
            error_message(f'Ambiguous data in {file} - could be multiple content types - file not processed')

    def process_valid_files(self, db_connector):
        num_queries = 0
        for group in self.valid_file_list:
            for file in group:
                processor = file['processor']
                match file['type']:
                    case 'n':
                        if self.batch_rate == 0:
                            queries, file_result, version_result = self.process_file(processor, NodeFileProcessor.process_node_file, db_connector)
                        else:
                            queries, file_result, version_result = self.process_file(processor, NodeFileProcessor.process_node_file_batch, db_connector)
                    case 'r':
                        if self.batch_rate == 0:
                            queries, file_result, version_result = self.process_file(processor, RelationshipFileProcessor.process_relationship_file, db_connector)
                        else:
                            queries, file_result, version_result = self.process_file(processor, RelationshipFileProcessor.process_relationship_file_batch, db_connector)
                    case 'c' | 'pre-file' | 'post-file':
                        queries, file_result, version_result = self.process_file(processor, CypherFileProcessor.process_cypher_file, db_connector)
                    case 'q' | 'pre' | 'post':
                        queries, file_result, version_result = self.process_file(processor, CypherFileProcessor.process_query_list, db_connector)
                    case _:
                        # This should never happen!
                        queries = 0
                        file_result = QueryResult(False)
                        version_result = QueryResult(False)

                num_queries += queries
                self.all_results.combine_results(file_result)
                self.all_version_results.combine_results(version_result)
                if self.stop_on_failure and file_result.status != 200:
                    break

        return num_queries

    def process_file(self, file_to_process, file_processor, db_connector):
        node_queries = 0
        num_errors = 0
        error_list = []
        file_results = QueryResult(False)
        file_results.set_status(200)
        version_results = QueryResult(False)

        query_count = 0
        file_queries = 0
        error_filename = self.config_manager.get_default_path() + 'Failed_queries_' + amu.get_time_for_filename() + '.cypher'
        if error_filename.endswith('.cypher'):
            self.error_file = None
            try:
                self.error_file = open(error_filename, 'w')
            except:
                self.error_file = None
        else:
            self.error_file = None

        if file_to_process.is_inline_query():
            report_message(f'Processing query "{file_to_process.get_filename()}" at {amu.get_formatted_time_now()}')
        else:
            report_message(f'Processing file "{file_to_process.get_filename()}" at {amu.get_formatted_time_now()}')
        # Build all the queries from the file, depending on the content type of the file
        queries = file_processor(file_to_process)
        message(f'{len(queries)} queries generated from {file_to_process.get_filename()}, processing...')

        if not self.validation_mode:

            num_queries = len(queries)
            if self.display_rate == 'auto':
                if num_queries > 10000:
                    display_rate = 1000
                elif num_queries > 1000:
                    display_rate = 100
                elif num_queries > 100:
                    display_rate = 10
                else:
                    display_rate = 1
            else:
                try:
                    display_rate = int(ast.literal_eval(self.display_rate))
                except:
                    display_rate = 0

            if display_rate > 0:
                message(f'0 of {num_queries} queries processed at {amu.get_formatted_time_now()}', False)

            # And action each one in turn
            for query in queries:
                query_count += 1

                if self.report_queries:
                    message(f'{query_count} of {num_queries}: {query.text}')
                update_current_node = True
                version_result = None
                if query.type == 'node':
                    if not self.no_versions:
                        update_current_node, version_result = self.version_managers[query.section].make_new_version_of_node(query, db_connector)
                if update_current_node:
                    version_results.combine_results(version_result)
                    result = db_connector.execute(query, query_count)
                    if result.get_status() == 200:

# Display info on how many of each batch were created
#                        new_nodes = result.get_updates()['nodes created']
#                        new_relationships = result.get_updates()['relationships created']
#                        if (query.type == 'batch node' and new_nodes != query.batch_size) or (query.type == 'batch relationship' and new_relationships != query.batch_size):
#                            info_message(f'Batch {query_count} contained {query.batch_size} updates: only {new_nodes+new_relationships} created')

                        if self.report_queries:
                            result.print_results('Updates made: ')
                            if version_result:
                                version_result.print_results('Version updates made: ', '')
                        if self.show_return:
                            db_connector.print_response(result.get_response())
                        file_results.combine_results(result)
                        file_queries += 1
                    else:
                        if result.get_status() == 414 | 505:
                            error_message(f'Query {query_count} returned ', f'{result.get_status()}')
                        else:
                            error_message(f'{query.text} returned ', f'{result.get_status()}')
                        num_errors += 1
                        error_list.append(query_count)
                        if self.error_file:
                            try:
                                self.error_file.write(query.text+'\n')
                            except:
                                pass
                        if self.stop_on_failure:
                            file_results.set_status(result.get_status())
                            break
                else:
                    info_message(f'No changes made by ', query.text)

                if query.type == 'batch node':
                    batch_info = f'{query.batch_size} nodes, {query.property_count} properties, '
                else:
                    batch_info = ''

                if display_rate > 0 and not self.report_queries:
                    if query_count % display_rate == 0 or query_count == num_queries:
                        message(f'{query_count} of {num_queries} queries processed at {amu.get_formatted_time_now()} ({query_count / num_queries * 100:.2f}%)', False)
                    else:
                        message_no_cr(f'{query_count} of {num_queries} queries processed ({batch_info}{query_count / num_queries * 100:.2f}%)    {chr(13)}')

        report_message(f'{file_queries} queries processed from {file_to_process.get_filename()} at {amu.get_formatted_time_now()}')
        file_results.print_results('Updates made: ')
        version_results.print_results('Version updates made: ', '')
        if self.error_file:
            self.error_file.close()
        if num_errors > 0:
            report_message(f'{num_errors} queries returned errors: {error_list}')
            report_message(f'Failed queries recorded in {error_filename}')
        else:
            try:
                os.remove(error_filename)
            except:
                pass
        node_queries += file_queries

        return node_queries, file_results, version_results
