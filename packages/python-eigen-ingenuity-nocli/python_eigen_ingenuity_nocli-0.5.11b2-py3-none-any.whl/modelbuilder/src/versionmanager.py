from queries.cypherbuilder import QueryBuilder
from queries.query import *
import processors.labelmanager as lm
import processors.relationshipmanager as rm
import uuid
from property import Neo4jProperty

class VersionManager:

    def __init__(self, config_manager, section):
        self.frozen_labels_list = lm.validate_labels(config_manager.get_frozen_labels_list())
        self.version_labels_list = lm.validate_labels(config_manager.get_version_labels_list())
        self.version_prefix = config_manager.get_version_prefix()
        self.version_counter = config_manager.get_version_counter()
        self.version_number = config_manager.get_version_number()
        self.first_version_property = config_manager.get_first_version_property()
        self.last_version_property = config_manager.get_last_version_property()
        self.version_relationship = rm.validate_relationship_string(config_manager.get_version_relationship())
        self.next_version_relationship = rm.validate_relationship_string(config_manager.get_next_version_relationship())

        self.skip_duplicates = config_manager.get_skip_duplicates()

        self.unique_id_property = config_manager.get_unique_id_property()[section]
        self.creation_time_property = config_manager.get_creation_time_property()[section]
        self.update_time_property = config_manager.get_update_time_property()[section]
        self.valid_from_property = config_manager.get_version_valid_from_property()
        self.valid_to_property = config_manager.get_version_valid_to_property()

        self.id_label = 'uuid'
        self.property_label = 'properties'
        self.label_label = 'labels'
        self.data_type_label = 'data_type'
        self.count_label = 'count'

        self.required_labels = config_manager.get_required_labels()[section]

        self.current_node_labels = [i for i in self.required_labels if (not ('!' + i in self.required_labels) and not (i.startswith('!')) and i != '')]
        self.version_node_labels = [i for i in self.version_labels_list if (not ('!' + i in self.version_labels_list) and not (i.startswith('!')) and i != '')]

        self.version_updates = None

    def get_labels_for_version_node(self, current_labels):
        version_labels = []
        for original_label in current_labels:
            # Required labels are Frozen by default
            if original_label in self.frozen_labels_list + self.required_labels:
                version_labels.append(original_label)
            elif '!' + original_label not in self.version_labels_list:
                version_labels.append(lm.validate_label_string(self.version_prefix + original_label))
            else:
                pass

        # Remove any unwanted labels (marked with '!' in the settings file)
        version_labels = [i for i in version_labels + self.version_labels_list if (not ('!' + i in self.version_labels_list) and not (i.startswith('!')) and i != '')]

        return version_labels


    def build_query_to_add_id_property(self, new_id):
        # Build a simple MERGE query using queries
        property_ref = 'o'
        labels = self.query.labels
        primary_property = self.query.primary_property
        properties = self.query.properties
        id_property = property_ref + '.' + self.id_label + '="' + new_id + '"'
        query = (QueryBuilder()
                 .match()
                 .node(labels=labels, ref_name=property_ref, properties=primary_property)
                 .set_literal(id_property)
                 ).toStr()
        add_query = Neo4jQuery('add_id', query, labels, '', properties)

        return add_query

    def build_query_to_get_current_node(self):
        # Build a simple MERGE query using queries
        property_ref = 'o'
        labels = self.query.labels
        primary_property = self.query.primary_property
        properties = self.query.properties
        return_values = [['properties(' + property_ref + ')', self.property_label],
                         ['labels(' + property_ref + ')', self.label_label],
                         ['apoc.meta.cypher.types(' + property_ref + '{.*})', self.data_type_label]]
        query = (QueryBuilder()
                 .match()
                 .node(labels=labels, ref_name=property_ref, properties=primary_property)
                 .return_mapping(return_values)
                 ).toStr()
        original_node_query = Neo4jQuery('version_match', query, labels, '', properties)

        return original_node_query

    def get_property_type(self, key, data_types):
        if key in data_types:
            current_type = data_types[key]
        else:
            current_type = ''

        match current_type:
            case 'STRING': property_type = 'str'
            case 'FLOAT': property_type = 'float'
            case 'DATE_TIME': property_type = 'datetime'
            case 'DATE': property_type = 'date'
            case 'BOOLEAN': property_type = 'bool'
            case 'INTEGER': property_type = 'int'
            case _: property_type = ''

        return property_type

    def build_query_to_get_last_version_node(self):
        property_ref = 'l'
        property_ref_dot = property_ref + '.'
        labels = self.get_labels_for_version_node(self.query.labels)
        properties = {self.query.primary_property.key: self.query.primary_property}
        properties[self.last_version_property] = Neo4jProperty(self.last_version_property, 'True')
        return_values = [[property_ref_dot + self.unique_id_property, self.id_label],
                         [property_ref_dot + self.version_number, 'version_count']]
        query = (QueryBuilder()
                 .match()
                 .node(labels=labels, ref_name=property_ref, properties=properties)
                 .return_mapping(return_values)
                 ).toStr()
        last_version_node_query = Neo4jQuery('last_version_match', query, labels, '', properties)

        return last_version_node_query

    def build_query_to_copy_node(self, original_node):
        property_ref = 'v'
        property_ref_dot = property_ref + '.'
        labels = self.get_labels_for_version_node(original_node[self.label_label])
        properties = {}
        for key, value in original_node[self.property_label].items():
            property_type = self.get_property_type(key, original_node[self.data_type_label])
            properties[key] = Neo4jProperty(key, str(value), property_type)
        properties[self.unique_id_property] = Neo4jProperty(self.unique_id_property, str(uuid.uuid4()))
        # Can't include datetime in the Properties because the driver doesn't support them
        # So take them out (we're going to update them later anyway)
        if self.creation_time_property in properties.keys():
            properties.pop(self.creation_time_property)
        if self.update_time_property in properties.keys():
            properties.pop(self.update_time_property)
        # And also the VersionCount
        if self.version_counter in properties.keys():
            properties.pop(self.version_counter)

        try:
            valid_from = property_ref_dot + self.valid_from_property + '=datetime("' + str(original_node[self.property_label][self.update_time_property]) + '"), '
        except:
            valid_from = property_ref_dot + self.valid_from_property + '=datetime("' + self.time_now + '"), '

        time_properties = property_ref_dot + self.creation_time_property + '=datetime("' + self.time_now + '"), ' + \
            property_ref_dot + self.update_time_property + '=datetime("' + self.time_now + '"), ' + \
            valid_from + \
            property_ref_dot + self.valid_to_property + '=datetime("' + self.time_now + '")'

        try:
            new_count = original_node[self.property_label][self.version_counter] + 1
            first_version = False
        except:
            new_count = 1
            first_version = True

        new_values = {self.version_number: Neo4jProperty(self.version_number, str(new_count)),
                      self.last_version_property: Neo4jProperty(self.last_version_property, 'True'),
                      self.first_version_property: Neo4jProperty(self.first_version_property, str(first_version))}

        # Build a simple MERGE query using queries
        query_text = (QueryBuilder()
                      .merge()
                      .node(labels=labels, ref_name=property_ref, properties=properties)
                      .set_literal(time_properties)
                      .set(new_values, property_ref_dot)
                      .return_literal(property_ref_dot + self.unique_id_property + ' AS ' + self.id_label)
                      ).toStr()
        query = Neo4jQuery('version_node', query_text)
        return query

    def are_there_changes(self, current_node_data):
        current_node_props = current_node_data[self.property_label]
        current_node_types = current_node_data[self.data_type_label]
        new_props = self.query.properties

        change_found = False
        for a_property in new_props:
            if a_property not in [self.creation_time_property, self. update_time_property, self.version_counter]:
                if a_property in current_node_props.keys():
                    # Do the comparison using values formatted as strings
                    # This avoids issues when comparing integers formatted as srtings, for example
                    # Note: if there is a calculated formula, this will always be treated as different
                    if str(new_props[a_property].value) != str(current_node_props[a_property]) or new_props[a_property].format != self.get_property_type(a_property, current_node_types):
                        change_found = True
                else:
                    change_found = True


        current_node_labels = current_node_data[self.label_label]
        new_labels = self.query.new_labels
        for a_label in new_labels:
            if a_label not in current_node_labels:
                change_found = True

        return change_found

    def make_copy_of_node(self):
        current_node_query = self.build_query_to_get_current_node()
        current_node = self.db_connector.execute(current_node_query)
        current_node_response = current_node.get_response()

        current_node_id = None
        last_version_node_id = None
        version_node_id = None

        if current_node_response:
            try:
                current_node_id = current_node_response[0][self.property_label][self.id_label]
            except:
                # Current node doesn't have the required node_key, so let's create and execute a query to add it
                current_node_id = str(uuid.uuid4())
                id_property_query = self.build_query_to_add_id_property(current_node_id)
                self.db_connector.execute(id_property_query)

            # Now check to see if anything will change
            if not self.skip_duplicates:
                node_will_change = True
            else:
                node_will_change = self.are_there_changes(current_node_response[0])

            if node_will_change:
                last_version_node_query = self.build_query_to_get_last_version_node()
                last_version_node = self.db_connector.execute(last_version_node_query)
                self.version_updates.combine_results(last_version_node)
                last_version_response = last_version_node.get_response()
                if last_version_response:
                    last_version_node_id = last_version_response[0][self.id_label]

                version_node = self.build_query_to_copy_node(current_node_response[0])
                version_node_return = self.db_connector.execute(version_node)
                version_node_response = version_node_return.get_response()[0]
                self.version_updates.combine_results(version_node_return)
                version_node_id = version_node_response[self.id_label]

        return current_node_id, last_version_node_id, version_node_id

    def update_version_numbers(self, current_node, last_version_node, version_node):
        # Start by finding the current number of versions, and update the current_node at the same time
        ref_text = 'gvc'
        ref_text_dot = ref_text + '.'
        counter_property = ref_text_dot + self.version_counter
        update_version = counter_property + '= CASE WHEN ' + counter_property + ' IS null THEN 1 ELSE ' + counter_property + '+1 END'
        new_values = ref_text_dot + self.update_time_property + '=datetime("' + self.time_now + '")'
        query_text = (QueryBuilder()
                      .match()
                      .node(ref_name=ref_text, labels=self.current_node_labels)
                      .where(ref_text_dot + self.unique_id_property, '=', str(current_node))
                      .set_literal(new_values)
                      .set_literal(update_version)
                      .return_literal(counter_property + ' AS ' + self.count_label)
                      ).toStr()

        version_query = Neo4jQuery('get version counter', query_text)
        # This should always return a result because the query will add the node_key if it was missing
        # TODO: ...unless the db connection goes down
        count_response = self.db_connector.execute(version_query)
        self.version_updates.combine_results(count_response)

        # If there was a previous Version node, mark to no longer be the Last Version
        if last_version_node:
            ref_text = 'lvn'
            ref_text_dot = ref_text + '.'
            new_values = Neo4jProperty(self.last_version_property, 'False')
            update_time = ref_text_dot + self.update_time_property + '=datetime("' + self.time_now + '")'

            last_version_query_text = (QueryBuilder()
                                       .match()
                                       .node(ref_name=ref_text, labels=self.version_node_labels)
                                       .where(ref_text_dot + self.unique_id_property, '=', str(last_version_node))
                                       .set(new_values, ref_text_dot)
                                       .set_literal(update_time)
                                       ).toStr()

            last_version_query = Neo4jQuery('last_version', last_version_query_text)
            last_version_result = self.db_connector.execute(last_version_query)
            self.version_updates.combine_results(last_version_result)
            # TODO: check result status

    def update_version_relationships(self, current_node, last_version_node, version_node):

        from_ref = 'from'
        from_ref_dot = from_ref + '.'
        to_ref = 'to'
        to_ref_dot = to_ref + '.'
        relation_ref = 'rel'
        relation_ref_dot = relation_ref + '.'

        where_tests = {from_ref_dot + self.unique_id_property: "['" + str(current_node) + "']",
                       to_ref_dot + self.unique_id_property: "['" + str(version_node) + "']"}

        # Add in System properties
        create_time = relation_ref_dot + self.creation_time_property + '=datetime("' + self.time_now + '")'
        update_time = relation_ref_dot + self.update_time_property + '=datetime("' + self.time_now + '")'

        # Build the query. This will create a relationship from the Current node to the new Version node
        query_text = (QueryBuilder()
                      .match()
                      .node(ref_name=from_ref, labels=self.current_node_labels)
                      .match()
                      .node(ref_name=to_ref, labels=self.version_node_labels)
                      .where_multiple(where_tests, ' IN ', ' AND ')
                      .merge()
                      .node(ref_name=from_ref)
                      .related_to(ref_name=relation_ref, label=self.version_relationship)
                      .node(ref_name=to_ref)
                      .on_create().set_literal(create_time)
                      .set_literal(update_time)
                      ).toStr()
        relationship_query = Neo4jQuery('version_relation', query_text)
        relation_result = self.db_connector.execute(relationship_query)
        self.version_updates.combine_results(relation_result)
        # TODO: check result status

        # If there's a previous version node, add a link to it
        if last_version_node:
            where_tests = {from_ref_dot + self.unique_id_property: "['" + str(last_version_node) + "']",
                           to_ref_dot + self.unique_id_property: "['" + str(version_node) + "']"}
            # Build the query. This will create a relationship from the Last Version node to the new Version node
            query_text = (QueryBuilder()
                          .match()
                          .node(ref_name=from_ref, labels=self.version_node_labels)
                          .match()
                          .node(ref_name=to_ref, labels=self.version_node_labels)
                          .where_multiple(where_tests, ' IN ', ' AND ')
                          .merge()
                          .node(ref_name=from_ref)
                          .related_to(ref_name=relation_ref, label=self.next_version_relationship)
                          .node(ref_name=to_ref)
                          .on_create().set_literal(create_time)
                          .set_literal(update_time)
                          ).toStr()
            relationship_query = Neo4jQuery('last_version_relation', query_text)
            relation_result = self.db_connector.execute(relationship_query)
            self.version_updates.combine_results(relation_result)

    def make_new_version_of_node(self, query, db_connector):
        # The input is a node.
        # We will make a copy of this node (which we will call "version_node"), and use this copy as the latest version
        # Set links from the original_node to the version_node, and increment the version count
        # The original_node is otherwise untouched, so that we don't change its element_id in the Neo4j graph

        self.version_updates = QueryResult(False)
        self.db_connector = db_connector
        self.query = query
        self.time_now = query.time_now

        current_node_id, last_version_node_id, new_version_node_id = self.make_copy_of_node()
        if new_version_node_id is not None:
            # We've created a new Version node, so update the version numbers and relationships
            self.update_version_numbers(current_node_id, last_version_node_id, new_version_node_id)
            self.update_version_relationships(current_node_id, last_version_node_id, new_version_node_id)
            update_current_node = True
        else:
            if current_node_id is None:
                # current node doesn't exist yet, so we'll need to create it (which is a sort of update)
                update_current_node = True
            else:
                # current node exists, but hasn't changed
                update_current_node = False

        return update_current_node, self.version_updates
