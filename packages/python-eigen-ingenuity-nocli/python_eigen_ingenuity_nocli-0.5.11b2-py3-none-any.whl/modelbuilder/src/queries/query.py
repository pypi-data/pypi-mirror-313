from messages import *

class QueryResult():
    def __init__(self, updates_made):
        self.status = None
        self.response = None
        self.updates_made = updates_made
        self.updates = {}

    def get_status(self):
        return self.status

    def set_status(self, value):
        self.status = value

    def get_updates(self):
        return self.updates

    def set_updates(self, value):
        self.updates = value

    def get_response(self):
        return self.response

    def set_response(self, value):
        self.response = value

    def get_updates_made(self):
        return self.updates_made

    def set_updates_made(self, value):
        self.updates_made = value

    def combine_results(self, new_result):
        if new_result:
            self.updates_made = self.updates_made | new_result.get_updates_made()
            for key, value in new_result.get_updates().items():
                try:
                    self.updates[key] += value
                except:
                    self.updates[key] = value

    def print_results(self, message, message2='No changes'):
        if self.updates_made:
            changes = ''
            for change, count in self.updates.items():
                if count > 0:
                    changes += f'{count} {change}, '
            changes += '\u0008\u0008'
            info_message(message + changes, '  ')
        else:
            if message2 != '':
                info_message(message2)

class Neo4jQuery():

    def __init__(self, type, text, time=None, labels=[], new_labels=[], primary_property=[], properties={}, batch_size=1, property_count=0, section='DEFAULT'):
        self.type = type
        self.text = text
        self.time_now = time
        self.labels = labels
        self.new_labels = new_labels
        self.primary_property = primary_property
        self.properties = properties
        self.batch_size = batch_size
        self.property_count = property_count
        self.section = section

#    def set_query(self, text):
#        self.text = text

#    def get_batch_size(self, value):
#        return self.batch_size

    def print(self):
        print(f'type: {self.type}')
        print(f'text: {self.text}')
        print(f'time: {self.time_now}')
        print(f'labels: {self.labels}')
        print(f'primary_property: {self.primary_property}')
        print(f'properties: {self.properties}')
        print(f'batch_size: {self.batch_size}')
        print(f'property_count: {self.property_count}')
        print(f'section: {self.section}')
