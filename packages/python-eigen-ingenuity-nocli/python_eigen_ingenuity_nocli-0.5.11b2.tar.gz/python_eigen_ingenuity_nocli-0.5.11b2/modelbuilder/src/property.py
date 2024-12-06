import datetime
import messages
import ast
import processors.propertymanager as pm

class Neo4jProperty():

    def __init__(self, key, value = None, format = None, type = None, blank_override = False):

        self.key = pm.validate_property(key)
        # Sanitise the value
        self.value = value.replace('\\', '\\\\').replace('\r', '\\r').replace('\n', '\\n').replace('"', '\\"')

        if self.value == "":
            if blank_override:
                self.value = blank_override

        # format is the data type e.g. int, str, bool
        self.format = format
        # type is the kind of thing this is, such as ID, START_ID etc. See assetmodelutilities.py for the full list
        self.type = type

        # We'll format the value the first time someone wants it, so say it's not formatted yet
        self.formatted_values = {}

        # Now check to see if the value might be a formula
        if '{' in self.value or '}' in self.value:
            self.formula, self.is_formula = parse_value(value, 'n.')
        else:
            self.formula = None
            self.is_formula = False


    def set_format(self, new_format):
        # If the format has changed, update it (otherwise, no need to do anything)
        if new_format != self.format:
            self.format = new_format
            # And say the value hasn't been formatted using the new format
            self.formatted_values = {}

    def set_value(self, new_value):
        # If the value has changed, update it (otherwise, no need to do anything)
        if new_value != self.value:
            self.value = new_value
            # And say the value hasn't been formatted using the new format
            self.formatted_values = {}

    def get_value(self, ref):
        # Check to see if we have a formatted value, and if not do it now
        if not ref in self.formatted_values.keys():
            self.formatted_values[ref] = format_value(self, ref)

        return self.formatted_values[ref]



def format_value(self, ref):

        quote = '"'
        value = self.value
        given_data_format = self.format

        # Redo the formula if ref is not 'n.' (which we did in the init section) and it is a real formula
        if self.is_formula:
            if ref != 'n.':
                formula, is_formula = parse_value(self.value, ref)
            else:
                formula = self.formula
        else:
            formula = ''

        if self.is_formula and formula != '':
            match given_data_format:
                case 'str':
                    result = f'toString({formula})'
                case 'int':
                    result = f'toInteger({formula})'
                case 'float':
                    result = f'toFloat({formula})'
                case 'date':
                    result = f'date({formula})'
                case 'datetime':
                    result = f'datetime({formula})'
                case 'bool':
                    result = f'toBoolean({formula})'
                case '' | _:
                    result = formula
        elif self.is_formula:
            result = ''
        else:
            try:
                match given_data_format:
                    case 'str':
                        result = quote + (formula or value) + quote
                    case 'int':
                        # Remove any leading zeroes because the literal_eval function does not support them
                        while value.startswith('0'):
                            value = value[1:]
                        result = int(ast.literal_eval(value))
                        if result != ast.literal_eval(value):
                            messages.warning_message('Invalid data: ', f'{value} is not a valid Integer, {result} used instead')
                    case 'float':
                        result = float(ast.literal_eval(value))
                    case 'bool' | 'boolean':
                        result = ast.literal_eval(value.capitalize())
                        if str(result) not in ['True', 'False']:
                            messages.error_message('Invalid data: ', f'{value} is not a valid boolean so not set')
                            result = '""'
                    case 'date':
                        formatted_date = try_dates(value)
                        if formatted_date:
                            result = 'date("' + str(formatted_date) + '")'
                        else:
                            messages.error_message(f'Invalid data: {value} is not a valid date so value not set')
                            result = '""'
                    case 'datetime':
                        formatted_datetime = try_datetimes(value)
                        if formatted_datetime:
                            result = 'datetime("' + str(formatted_datetime) + '")'
                        else:
                            messages.error_message(f'Invalid data: {value} is not a valid datetime so value not set')
                            result = '""'
                    case None | '':
                        # No format requested, so we'll try to work it out
                        try:
                            # Use .capitalize() here to catch incorrectly formatted Booleans (e.g. 'true')
                            boolean_check = value.capitalize()
                            if boolean_check in ['True', 'False']:
                                data_type = bool
                                result = boolean_check
                                # Update value for use in Version management in VersionManager.are_there_changes()
                                self.value = boolean_check
                                self.format = 'bool'
                            else:
                                data_type = type(ast.literal_eval(value))
                        except:
                            # Now see if it's a date or datetime
                            formatted_date = try_dates(value)
                            formatted_time = try_times(value)
                            if formatted_date:
                                if formatted_time:
                                    data_type = 'datetime'
                                    # Some legacy data has a space between the date and time, so replace it with 'T'
                                    if value[10] == ' ':
                                        value = value[:10] + 'T' + value[11:]
                                    result = 'datetime("' + str(value) + '")'
                                    self.format = 'datetime'
                                else:
                                    data_type = 'date'
                                    result = 'date("' + str(formatted_date) + '")'
                                    self.format = 'date'
                            else:
                                data_type = 'str'
                                self.format = 'str'

                        match str(data_type):
                            case 'str':
                                result = quote + (formula or value) + quote
                                self.format = 'str'
                            case "<class 'int'>":
                                if value != '0' and value.startswith('0'):
                                    # Has a leading 0, so treat as a string
                                    result = quote + value + quote
                                else:
                                    result = int(ast.literal_eval(value))
                                    if result != ast.literal_eval(value):
                                        messages.warning_message('Invalid data: ', f'{value} is not a valid Integer, {result} used instead')
                                self.format = 'int'
                            case "<class 'float'>":
                                result = ast.literal_eval(value)
                                self.format = 'float'
                            case "<class 'bool'>":
                                # result already set above, so
                                pass
                            case 'date' | 'datetime':
                                # result already set above, so
                                pass
                            case "<class 'list'>":
                                result = value
                            case _:
                                # Shouldn't get here, but just in case use a string
                                result = quote + value + quote
                                self.format = 'str'

                    case _:
                        # Treat unsupported formats as strings
                        result = quote + value + quote
                        self.format = 'str'
            except:
                messages.error_message('Invalid data: ', f"{value} is not valid for type '{given_data_format}' so value not set!")
                result = '""'

        return result


def parse_value(formula, ref):
    num_open = 0
    num_close = 0
    parsed = ''
    index = 0
    open = False
    property_name = ''
    while index < len(formula):
        this_char = formula[index]
        next_char = (formula+' ')[index+1] # Added a space to formula, so we don't run off the end
        if this_char == '{':
            if next_char == '{':
                if open:
                    property_name += this_char
                else:
                    parsed += this_char
                index += 1
            else:
                open = True
                property_name = ''
                num_open += 1
        elif this_char == '}':
            if next_char == '}':
                if open:
                    property_name += this_char
                else:
                    parsed += this_char
                index += 1
            else:
                if open and property_name != '':
                    # Replace {property} with n.property (assuming ref = "n.")
                    parsed += ref + pm.validate_property(property_name)
                else:
                    # We've just found {}, so discount this
                    property_name = property_name[:-1]
                open = False
                num_close += 1
        else:
            if open:
                property_name += this_char
            else:
                parsed += this_char
        index += 1

    is_formula = (num_open == num_close) and (num_open > 0)

    return parsed.strip(), is_formula


def try_date_format(date, date_format):
    try:
        tested_date = datetime.datetime.strptime(date.replace('/', '-'), date_format).date()
    except:
        tested_date = None
    return tested_date


def try_dates(date):
    date1 = try_date_format(date[:10], '%Y-%m-%d')
    date2 = try_date_format(date[:10], '%d-%m-%Y')
    date_found = date1 or date2
    return date_found


def try_datetimes(datetime):
    date = try_dates(datetime)
    time = try_times(datetime) or '00:00:00'
    if date:
        datetime_found = str(date) + 'T' + str(time)
    else:
        datetime_found = None
    return datetime_found


def try_time_format(time, time_format):
    try:
        tested_time = datetime.datetime.strptime(time, time_format).time()
    except:
        tested_time = None
    return tested_time


def try_times(time):
    time1 = try_time_format(time[11:19], '%H:%M:%S')
    if time1:
        time_found = time[11:]
    else:
        time_found = None
    return time_found


def format_property_list(properties, comparison_operator = ':', boolean_operator = ',', property_ref='', key_ref=''):
    if not isinstance(properties, dict):
        prop_list = {properties.key: properties}
    else:
        prop_list = properties
    pairs = [f'{key_ref}{prop_list[property].key}{comparison_operator}{prop_list[property].get_value(property_ref)}' for property in prop_list.keys()]
    res = boolean_operator.join(pairs)
    return res

def format(properties, property_ref=''):
    # Reformat using identified data types
    pairs = []
    for p in properties.keys():
        pairs.append(f'{properties[p].key}:{properties[p].get_value(property_ref)}')
    return '{' + ','.join(pairs) + '}'

def to_str(properties, comparison_operator: str = ':', boolean_operator: str = ',', property_ref='', key_ref='') -> str:
    pairs = [f'{key_ref}{key.split(":")[0]}{comparison_operator}{Neo4jProperty(key, str(value)).get_value(property_ref)}' for key, value in properties.items()]
    res = boolean_operator.join(pairs)
    return res

