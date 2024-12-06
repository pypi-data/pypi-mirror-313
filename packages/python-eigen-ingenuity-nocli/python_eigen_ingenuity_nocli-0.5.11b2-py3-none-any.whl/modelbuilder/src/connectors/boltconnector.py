from connectors.genericconnector import GenericConnector
from neo4j import GraphDatabase
from queries.query import QueryResult
from messages import *
from time import sleep
import assetmodelutilities

class BoltConnector(GenericConnector):

    # Fairly standard connector to Neo4j, using the Bolt protocol

    def __init__(self, db_connection_details, config_manager, output_file, results_file):
        super().__init__(db_connection_details, output_file, results_file)
        url = db_connection_details['url']
        user = db_connection_details['user']
        password = db_connection_details['password']
        self.driver = GraphDatabase.driver(url, auth=(user, password))

    def close(self):
        super().close()
        self.driver.close()

    def convert_result(self, this_result):
        converted_result = QueryResult(False)
        update_dict = {}

        if this_result is not None:
            converted_result.set_status(200)
#            converted_result.set_response(this_result.values())
            converted_result.set_response(this_result.data())
            result = this_result.consume().counters
            converted_result.set_updates_made(result.contains_updates)
            update_dict['nodes created'] = result.nodes_created
            update_dict['nodes deleted'] = result.nodes_deleted
            update_dict['properties set'] = result.properties_set
            update_dict['relationships created'] = result.relationships_created
            update_dict['relationships deleted'] = result.relationships_deleted
            update_dict['labels added'] = result.labels_added
            update_dict['labels removed'] = result.labels_removed
            update_dict['indexes added'] = result.indexes_added
            update_dict['indexes removed'] = result.indexes_removed
            update_dict['constraints added'] = result.constraints_added
            update_dict['constraints removed'] = result.constraints_removed
            update_dict['system updates'] = result.system_updates
            converted_result.set_updates(update_dict)
        else:
            converted_result.set_status(-1)
            converted_result.set_response(None)
            converted_result.set_updates_made(False)

        return converted_result

    def execute(self, query, query_num=-1):
        super().execute(query, query_num)
#        session = self.driver.session(database="neo4j")
        session = self.driver.session()
        query_text = query.text

        if self.output_file is not None:
            self.output_file.write(query_text + '\n')

        cypher_error = False
        try_count = 0
        all_good = False
        while not all_good and try_count < 3 and not cypher_error:
#        with session.begin_transaction() as tx:
            try:
                result = session.run(query_text)
#                result = tx.run(query_text)
                converted_result = self.convert_result(result)
                all_good = True
            except Exception as e:
##                print(f'Query failed: {e}')
                if str(type(e)) == "<class 'neo4j.exceptions.ServiceUnavailable'>" or str(type(e)) == "<class 'neo4j.exceptions.SessionExpired'>":
                    info_message(f'Query {self.query_id} failed at {assetmodelutilities.get_formatted_time_now_noms()}: Service unavailable, retrying...')
                    try_count += 1
                    sleep(60)
                elif str(type(e)) == "<class 'neo4j.exceptions.CypherSyntaxError'>":
                    cypher_error = True
                else:
                    info_message(f'Query {self.query_id} failed at {assetmodelutilities.get_formatted_time_now_noms()} with error type {type(e)}, retrying...')
                    try_count += 1
                    sleep(1)
#            finally:
#                if not tx.closed():
#                    tx.rollback()

        if not all_good:
            if cypher_error:
                error_message('Invalid query: ' + query_text)
            else:
                warning_message(f'Query {self.query_id} not processed!')
            converted_result = self.convert_result(None)
        elif try_count > 0:
            info_message(f'Query {self.query_id} processed successfully on attempt {try_count + 1}')

        if self.results_file is not None:
            self.write_response(converted_result.get_response())

        session.close()

        return converted_result

    def print_response(self, response):
        if response is not None:
            for r in response:
                print(r)
#                for t in r:
#                    print(t)

    def write_response(self, response):
        if response is not None:
            for r in response:
                self.results_file.write(str(r) + '\n')
