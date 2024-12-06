import sys, os, json, time, requests, csv, logging, warnings
from datetime import datetime
from dateparser import parse
import pandas as pd
from collections import ChainMap
from urllib.parse import urlsplit, quote as urlquote

from requests.exceptions import ConnectionError

from eigeningenuity.auth import _authenticate_azure_user
import eigeningenuity.settings as settings

from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single InsecureRequestWarning from urllib3
warnings.simplefilter('ignore', InsecureRequestWarning)
# Suppress only the single InsecureRequestWarning from urllib3
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def _do_eigen_json_request(requesturl,auth,**params):

    headers = {}

    if settings._azure_tenant_id_ and settings._azure_client_id_ and settings._azure_auth_enabled_ and auth:
        headers = _authenticate_azure_user('/'.join(requesturl.split("/")[0:3]))

    if settings._api_token_value_:
        headers['X-Api-Key'] = settings._api_token_value_

    if params:
        if "?" in requesturl:
            sep = "&"
        else:
            sep = "?"

        for k,v in params.items():
            if v is None:
               pass
            else:
                for e in force_list(v):
                    if not isinstance(e, str):
                        if isinstance(e, str):
                            e = e.encode("utf8")
                        else:
                            e = str(e)
                    requesturl += sep + urlquote(k) + "=" + urlquote(e.encode("UTF8"))

                    sep = "&"

    try:
        data = requests.get(requesturl, headers=headers, verify=False)
    except ConnectionError as e:
        # sys.tracebacklimit = 0
        raise EigenException("No Response from ingenuity instance at https://" + requesturl.split("/")[2] + ". Please check this is correct url and that the instance is currently running") from None


    if data.text.startswith("ERROR:"):
        if "UNKNOWN TAG" in data.text:
            raise RemoteServerException(data.text)
        raise RemoteServerException(data.text.split("\n")[1], requesturl)
    elif data.text.startswith("EXCEPT:") and data.status_code != 200:
        raise RemoteServerException( data.text.split("\n")[0], "API could not parse request, check query syntax is correct",)
    else:
        try:
            ret = data.json()
        except ValueError:
            ret = data.text
    try:
        if "Sign in to your account" in ret:
            if not settings._azure_auth_enabled_ or not (settings._azure_tenant_id_ and settings._azure_client_id_):
                msg = "This resource requires authentication with an Azure account. Use set_azure_tenant_id and set_azure_client_id to set the server parameters."
            else:
                msg = "Authentication failed, check the resource you are querying matches the azure parameters set"
            raise EigenException(f"{msg}")
    except:
        pass
    return ret

def _do_eigen_post_request(requesturl,payload,auth):
    headers = {}
    if settings._azure_tenant_id_ and settings._azure_client_id_ and settings._azure_auth_enabled_ and auth:
        headers = _authenticate_azure_user('/'.join(requesturl.split("/")[0:3]))

    if settings._api_token_value_:
        headers['X-Api-Key'] = settings._api_token_value_

    if not str(requests.post(requesturl,json=payload, headers=headers, verify=False)).startswith("2"):
        logging.warning("Failed to push")
        return False
    return True
    

def _do_chunked_eigen_post_request(requesturl,data,label,auth):
    headers = {}
    if settings._azure_tenant_id_ and settings._azure_client_id_ and settings._azure_auth_enabled_ and auth:
        headers = _authenticate_azure_user('/'.join(requesturl.split("/")[0:3]))

    if settings._api_token_value_:
        headers['X-Api-Key'] = settings._api_token_value_

    chunks = list(divide_chunks(data, 500))
    failures = []
    for chunk in chunks:
        payload = {label: chunk}
        resp = requests.post(requesturl, json=payload, verify=False, headers=headers)
        if not str(resp.status_code).startswith("2"):
            failures.append(payload)
    if failures:
        logging.warning("Some events failed to push")
        return failures
    return False

def is_list(x):
    return type(x) in (list, tuple, set)

def force_list(x):
    if is_list(x):
        return x
    else:
        return [x]

def number_to_string(n):
    if type(n) == float:
        return format(n, '^12.5f')
    else:
        return n

def time_to_epoch_millis(t):
    if type(t) == datetime:
        epochmillis = t.timestamp()
    elif (type(t) == int or type(t) == float):
        if t > 100000000000:
            epochmillis = int(t)
        else:
            epochmillis = int(t*1000)
    elif type(t) == str:
        if "ago" in t or "now" in t:
            return t
        else:
            epochmillis = parse(t).timestamp()
    else:
        raise EigenException("Unknown time format " + str(type(t)))
    return int(round(epochmillis))

def get_time_tuple(floatingpointepochsecs):
    time_tuple = time.gmtime(floatingpointepochsecs)
    return time_tuple

def get_timestamp_string(t):
    pattern = '%Y-%m-%d %H:%M:%S UTC'
    s = datetime.fromtimestamp(t).strftime(pattern)
    return s

def get_timestamp(t):
    if type(t) == str:
        try:
            epochmillis = parse(t).timestamp()
        except ValueError:
            try:
                pattern = '%Y-%m-%d %H:%M:%S.%f'
                epochmillis = int(time.mktime(time.strptime(t, pattern)))
            except ValueError:
                try:
                    pattern = '%Y-%m-%dT%H:%M:%S.%f%z'
                    epochmillis = int(time.mktime(time.strptime(t, pattern)))
                except ValueError:
                    try:
                        pattern = '%Y-%m-%d %H:%M:%S'
                        epochmillis = int(time.mktime(time.strptime(t, pattern)))
                    except ValueError:
                        try:
                            pattern = '%Y-%m-%d'
                            epochmillis = int(time.mktime(time.strptime(t, pattern)))
                        except ValueError:
                            try:
                                epochmillis = int(t)
                            except ValueError:
                                raise EigenException("Unknown time format " + str(type(t)))

    else:
        return(time_to_epoch_millis(t))
    return int(round(epochmillis))



def get_datetime(t):
    timestamp = get_timestamp(t)
    return datetime.fromtimestamp(timestamp)

def pythonTimeToServerTime(ts):
# where ts may be supplied as time tuple, datetime or floating point seconds, and server time is (obviously) millis.
    if type(ts) == datetime:
        epochmillis = time.mktime(ts.timetuple()) * 1000
    elif type(ts) == tuple:
        epochmillis = time.mktime(ts) * 1000
    elif type(ts) == float:
        epochmillis = int(ts * 1000)
    else:
        raise EigenException("Unknown python time format " + str(type(ts)))
    return int(round(epochmillis))


def serverTimeToPythonTime(ts):
# where ts is millis and the returned value is consistently whatever we're using internally in the python library (i.e. floating secs)
    return ts / 1000.0

def pythonTimeToFloatingSecs(ts):
# where ts may be supplied as time tuple, datetime or floating point seconds
    if type(ts) == datetime:
        return time.mktime(ts.timetuple())
    elif type(ts) == tuple:
        return time.mktime(ts)
    elif type(ts) == float or type(ts) == int:
        return ts
    else:
        raise EigenException("Unknown python time format " + str(type(ts)))

def pythonTimeToTuple(ts):
# where ts may be supplied as time tuple, datetime or floating point seconds
    if type(ts) == datetime:
        return ts.timetuple()
    elif type(ts) == tuple:
        return ts
    elif type(ts) == float:
        return ts
    else:
        raise EigenException("Unknown python time format " + str(type(ts)))

def pythonTimeToDateTime(ts):
# where ts may be supplied as time tuple, datetime or floating point seconds
    if type(ts) == datetime:
        return ts
    elif type(ts) == tuple:
        epochmillis = time.mktime(ts) * 1000
        return datetime.fromtimestamp(epochmillis)
    elif type(ts) == float:
        return time.gmtime(ts)
    else:
        raise EigenException("Unknown python time format " + str(type(ts)))

def map_java_exception(myExceptionName, params):
    if myExceptionName == "urllib2.HTTPError":
         return RemoteServerException(params)
#    elif: ...
    else:
        return EigenException(myExceptionName)

def parse_duration(timeWindow):
    unit = timeWindow[-1:]
    value = timeWindow[:-1]

    def seconds():
        int(value)

    def minutes():
        return int(value) * 60

    def hours():
        return int(value) * 3600

    def days():
        return int(value) * 3600 * 24

    def months():
        return int(value) * 3600 * 24 * 30

    def years(): int(value) * 3600 * 24 * 365

    options = {"s" : seconds,
               "m" : minutes,
               "h" : hours,
               "d" : days,
               "M" : months,
               "y" : years,
    }

    duration = options[unit]()*1000

    return duration


def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def cypherRespMap(resp):
    return resp["m"]


def jsonToDf(json,transpose:bool=False):
    p = {}
    keys = json.keys()
    if "unknown" in keys: keys.remove("unknown")
    for key in keys:
        if type(json[key]) == list:
            m = list(map(dataMap,json[key]))
            n = dict(ChainMap(*m))
        else:
            n = dataMap(json[key])
        p[key] = n
    try:
        df = pd.DataFrame(p)
        if transpose:
            df = df.T
        return(df[::-1])
    except ValueError:
        return(pd.Series(p))

def dataMap(j):
    try:
        h = {datetime.fromtimestamp(j["timestamp"] / 1000): j["value"]}
    except:
        h = j
    return h

def flattenList(list):
    return [item for sublist in list for item in sublist]

def flattenDict(nestedDict):
    points = []
    keys = nestedDict.keys()
    for key in keys:
        values = nestedDict[key]
        for value in force_list(values):
            tag = {"tag": key}
            tag.update(value)
            points.append(tag)
    return points

def aggMap(x):
    for k in x[1]:
        k["tag"] = x[0]
    return x[1]

def aggToDf(x,cols):
    y = flattenList(list(map(aggMap,x.items())))
    if cols is None:
        cols = ["tag", "start", "end", "min", "max", "avg", "var", "stddev", "numgood", "numbad"]
    else:
        cols = ["tag", "start", "end"] + cols
    df = pd.DataFrame(y)
    df = df[cols]
    try:
        df["start"] = pd.to_datetime(df["start"], unit="ms")
        df["end"] = pd.to_datetime(df["end"], unit="ms")
    except ValueError:
        df["start"] = pd.to_datetime(df["start"], format="ISO8601")
        df["end"] = pd.to_datetime(df["end"], format="ISO8601")
    df.sort_values(by='start', inplace=True)
    return(df)

def get_eigenserver(url):
    split_url = urlsplit(url)
    return split_url.scheme + "://" + split_url.netloc

def constructURL(y,x):
    if "//" not in x["url"]:
        x["url"] = y + x["url"]
    k = {"fileName": x["fileName"], "description": x["description"], "url": x["url"]}
    return k

def parseEvents(events):
    if type(events) == dict or type(events) == list:
        events = events
    elif type(events) == str:
        try:
            with open(events,"r") as f:
                events = json.loads(f.read())
        except FileNotFoundError:
            try:
                events = json.loads(events)
            except json.decoder.JSONDecodeError:
                raise EigenException("Could not parse input, enter the path to a file, or a json/dict object")
    try:
        events = events["events"]
    except:
        pass
    events = force_list(events)
    return events

def parse_properties(x):
    return x["graphapi"]["properties"]

def csvWriter(data,historian,filepath,multi_csv,functionName,order=None,headers=False):
    if "Agg" in functionName:
        timeField = 'start'
    else:
        timeField = 'timestamp'
    if multi_csv:
        for item in data:
            sortedDicts=[]
            for entry in force_list(data[item]):
                if order is not None:
                    entry = (dict(sorted(entry.items(), key=lambda item: order.index(item[0]))))
                sortedDicts.append(dict(entry.items()))
            sortedList = sorted(sortedDicts, key=lambda d: (d[timeField])) 
            keys = sortedList[0].keys()
            if filepath is None:
                filepath = item + "-" + functionName + "-" + str(round(datetime.now().timestamp())) + ".csv"
            elif filepath[-1] == "/":
                filepath += item +  "-" + functionName + "-" + str(round(datetime.now().timestamp())) + ".csv"
            else:
                filepath = item +  "-" + functionName + "-" + str(round(datetime.now().timestamp())) + ".csv"

            with open(filepath, 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                if headers:
                    dict_writer.writeheader()
                dict_writer.writerows(sortedList)
        return True       
    else:
        sortedDicts = []
        points = flattenDict(data)
        for entry in points:
            if order is not None:
                entry = dict(sorted(entry.items(), key=lambda item: order.index(item[0])))
            sortedDicts.append(entry)
        sortedList = sorted(sortedDicts, key=lambda d: (d['tag'], d[timeField])) 
        keys = sortedList[0].keys()
        if filepath is None:
            filepath = historian +  "-" + functionName + "-" + str(round(datetime.now().timestamp())) + ".csv"
        elif filepath[-1] == "/":
            filepath += historian +  "-" + functionName + "-" + str(round(datetime.now().timestamp())) + ".csv"

        with open(filepath, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            if headers:
                dict_writer.writeheader()
            dict_writer.writerows(sortedList)
            return True
        
def process_datapoint(data_dict,key,datapoint):
    tag_name = key
    timestamp = datapoint['timestamp']
    value_data = datapoint['value']

    # Check if timestamp is already a key in the dictionary
    if timestamp not in data_dict:
        data_dict[timestamp] = {}

    # Add data to the dictionary
    data_dict[timestamp][tag_name] = value_data

    return data_dict
        
# Function to convert timestamp to a consistent format
def convert_df_timestamp_header(timestamp):
    # Convert to datetime object and then format as string
    dt = datetime.fromisoformat(timestamp)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def multi_response_to_df(api_response):
    data_dict = {}

    # Iterate through the response
    for key, value in api_response.items():
        if "dataPoints" in value.keys():
            for datapoint in value["dataPoints"]:
                data_dict = process_datapoint(data_dict,key,datapoint)

        elif "dataPoint" in value.keys():
            datapoint = value["dataPoint"]
            data_dict = process_datapoint(data_dict,key,datapoint)

    # Create DataFrame
    df = pd.DataFrame(data_dict)
    df.columns = [convert_df_timestamp_header(col) for col in df.columns]
    df = df.T # Transpose the DataFrame

    # Convert timestamp index to datetime format
    df.index = pd.to_datetime(df.index)

    return df

def merge_tags_from_response(response):
    merged_response = {}

    for key, value in response.items():
        # Extract the header by removing the suffix (e.g., '-0' or '-1')
        header = key.rsplit('-', 1)[0]

        # If the header is not already in the merged_response, initialize it
        if header not in merged_response:
            merged_response[header] = {'dataPoints': []}

        # Append the dataPoint to the list of dataPoints under the header
        merged_response[header]['dataPoints'].append(value['dataPoint'])

    return merged_response

def update_keys(my_dict, historian):
    # Use dictionary comprehension to update keys
    return {
        (historian + key if "/" not in key else key): value
        for key, value in my_dict.items()
    }

def _do_historian_multi_request(url,body,auth,write_request=False,get_request=False):

    headers = {}

    if settings._azure_tenant_id_ and settings._azure_client_id_ and settings._azure_auth_enabled_ and auth:
        headers = _authenticate_azure_user('/'.join(url.split("/")[0:3]))

    if settings._api_token_value_:
        headers['X-Api-Key'] = settings._api_token_value_

    
    if get_request:
        resp = requests.get(url, verify=False, headers=headers).json()

    else:
        resp = requests.post(url, json=body, verify=False, headers=headers).json()

        if write_request:
            return resp['message']

    return resp

def _reformat_multi_response(original_dict):
    reformatted_dict = {}
    
    for key, value in original_dict.items():
        if type(value) == list:
            reformatted_dict = value
        elif key == "dataPoint" or key == "dataPoints":
            reformatted_dict = value
        else:
            # Extract the list of data points from either 'dataPoints' or 'dataPoint' key
            data_points = value.get('dataPoints') or value.get('dataPoint') or value
            # Assign the data points list directly to the top-level key
            reformatted_dict[key] = data_points
        
    return reformatted_dict

def format_output(output,response,tags,timestamps=False):
    if not timestamps:
        items = response['results']
    else:
        items = response

    if output == "raw":
        return response
    elif output == "json":
        if len(tags) == 1 and (not timestamps or len(timestamps) == 1):
            return _reformat_multi_response(items[tags[0]])
        else:
            return _reformat_multi_response(items)
    elif output == "string":
        return json.dumps(items,indent=4)
    elif output == "df":
        return multi_response_to_df(items)
    
    raise EigenException("Unrecognised Output Type. Must be one of ['raw','json','string','df']")


class EigenException (Exception): pass
class RemoteServerException (EigenException): pass
