"""Eigen Ingenuity - Asset Model

This package deals with the Eigen Ingenuity Asset Model API, by means
of the Cypher plugin endpoint.

To retrieve an AssetObject use getMatchingNodes, or execute a custom cypher query with executeRawQuery

  from eigeningenuity.assetmodel import getAssetModel
  from eigeningenuity import EigenServer

  eigenserver = EigenServer(ingenuity-base-url)

  model = getAssetModel(eigenserver)

  nodes = model.getMatchingNodes("code","System_")
  
    
"""
import functools

import requests, os
import json
import pandas as pd
from eigeningenuity import EigenServer
from urllib.parse import quote as urlquote
from eigeningenuity.util import force_list, _do_eigen_json_request, parse_properties, get_eigenserver, constructURL, cypherRespMap
from eigeningenuity.core import get_default_server
from requests.exceptions import ConnectionError
from urllib.error import URLError
from typing import Union
import datetime as dt
from datetime import datetime

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

class AssetModel (object):
    """An assetmodel instance which talks the Eigen Neo4j endpoint.
    """
    def __init__(self, baseurl, auth):
        """This is a constructor. It takes in a URL like https://demo.eigen.co/ei-applet/"""
        self.baseurl = baseurl
        self.eigenserver = get_eigenserver(baseurl)
        self.auth = auth

    def _testConnection(self):
        """Preflight Request to verify connection to ingenuity"""
        try:
            status = requests.get(self.baseurl, verify=False).status_code
        except (URLError, ConnectionError):
            raise ConnectionError("Failed to connect to ingenuity instance at " + self.baseurl + ". Please check the url is correct and the instance is up.")

    def _doJsonCypherRequest(self, cmd, params):
        # self._testConnection()
        url = self.baseurl + "jcypher?cmd=" + urlquote(cmd)
        return _do_eigen_json_request(url, self.auth, **params)

    def _doJsonCommonMenuRequest(self, index, params):
        # self._testConnection()
        url = self.baseurl + "commonmenu2/asset/" + index + "?"
        return _do_eigen_json_request(url, self.auth, **params)

    def executeRawQuery(self,query:str,output:str="json"):
        """
        Executes a raw cypher query against AssetModel via the AssetModel API.

        Args: 
            query: A string containing a query in cypher, for information on cypher queries see https://neo4j.com/developer/cypher/

        Returns:
            A Json containing the cypher response to the query.

        Raises:
            KeyError: Raises an exception
            
        """
        args = {'q': query}
        response = self._doJsonCypherRequest("execute", args)

        if output == "raw":
            return response
        if output == "json":
            if type(response) == list and len(response) == 1:
                return response[0]
            else:
                return response
        if output == "df":
            return pd.json_normalize(response)



    def getRelatedAssetsCommonMenu(self, node: str, output="json", filepath = None):
        """
        Return all measurement tags directly related to a given asset via the Common Menu API.

        Args:
            node:
            output (Optional): The format in which to return the data. Accepts one of: "raw" - The raw json returned by the API, "json" - A processed version of the json response, "df" - A formatted pandas dataframe object. Defaults to "json".

        Returns:
            A Json containing all nodes with a relation to any node that meets the criteria, and their relationship type.

        Raises:
            KeyError: Raises an exception

        """
        args = {"asset": node}

        response = self._doJsonCommonMenuRequest("relatedAssets", args)
        relatedassets = response["relatedAssets"]["graphapi"]

        newAssets=[]

        for item in relatedassets:
            relations = item["relations"]
            for relation in relations:
                newItem = {"asset": item["asset"]}
                newItem["relationName"] = relation["relationName"]
                newItem["direction"] = relation["direction"]
                newAssets.append(newItem)



        if output == "raw":
            return response
        if output == "json":
            return newAssets
        if output == "df":
            return pd.json_normalize(newAssets).drop(columns=["asset.externalId"])
        if output == "file":
            if filepath is None:
                filepath = node + "-RelatedAssets-" + str(dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
            with open(filepath + ".json", "w") as f:
                f.write(json.dumps(newAssets, indent=4))

    def getRelatedMeasurementsCypher(self, query:str, prop:str="code", measurement:str="", output="json"):
        """
        Return all measurement tags directly related to a given asset via the AssetModel API.

        Args: 
            nodes: The value of the property to match
            prop (Optional): The property on to query nodes on. Defaults to code.
            measurement (Optional): Return only tags for a specified measurement type. Defaults to return all tags.

        Returns:
            A Json containing all nodes with a relation to any node that meets the criteria, and their relationship type.

        Raises:
            KeyError: Raises an exception
            
        """
        result = []
        exact = True
        for item in force_list(query):
            x = []
            y = []
            args = {}
            # if exact:
            matchStatement = "n.%s = '%s' and r.measurementName contains '%s'" % (prop, item, measurement)
            # else:
            #     matchStatement = "n.%s contains '%s' and r.measurementName contains '%s'" % (prop, node, measurement)
            args['q'] = 'MATCH (n)-[r:hashistoriantag]->(m) WHERE %s RETURN r.measurementName as measurementName, m.code as measurementCode' % matchStatement

            response = self._doJsonCypherRequest("execute", args)


            for meas in response:
                x.append(meas["measurementName"])
                y.append(meas["measurementCode"])

            result.append(pd.Series(y,index=x,name=item))
        k = pd.merge(result[0],result[1],on="index")
        if output == "raw":
            return response
        if output == "json":
            return response
        if output == "df":
            return pd.DataFrame(response)

    def getRelatedMeasurementsCommonMenu(self, node:str, output="json"):
        """
        Return all measurement tags directly related to a given asset via the Common Menu API.

        Args: 
            node: The code (ID) of the node to get related measurements from
            output (Optional): The format in which to return the data. Accepts one of: "raw" - The raw json returned by the API, "json" - A processed version of the json response, "df" - A formatted pandas dataframe object. Defaults to "json".

        Returns:
            A Json containing all nodes with a relation to any node that meets the criteria, and their relationship type.

        Raises:
            KeyError: Raises an exception
            
        """
        args = {}
        args["asset"] = node

        response = self._doJsonCommonMenuRequest("timeseries", args)
        timeseries = response["timeseries"]

        if output == "raw":
            return response
        if output == "json":
            return timeseries
        if output == "df":
            return pd.DataFrame(timeseries)["tag"]

    def getRelatedDocuments(self, node:Union[str,list], match=None, output="json", directory:str=None):
        """
        Return all Documents related to nodes via the Common Menu API.

        Args:
            node: The name of the node to query documents for
            match (Optional): Filter returned Documents to those with filenames matching a string
            output (Optional): The format in which to return the data. Accepts one of: "raw" - The raw json returned by the API; "json" - A processed version of the json response; "df" - A formatted pandas dataframe object; "download" - Downloads the files to a local directory"
            directory (Optional): Name and path to the directory created/used for downloaded documents. If omitted, will download files to current directory. Has no effect unless output is "download".

        Returns:
            The set of all documents related to the nodes, the format is dependent on the output parameter. If output is "download", it returns instead the files themselves

        Raises:
            KeyError: Raises an exception

        """
        nodes = force_list(node)
        results = []
        documents = []
        for node in nodes:
            args = {}
            args["asset"] = node
            response = self._doJsonCommonMenuRequest("documents", args)
            results.append(response)
            documents.append(response["documents"])

        if documents == [[]]:
            return []
        documents = documents[0][0]["documents"]

        documents = list(map(functools.partial(constructURL, self.eigenserver), documents))

        matches = []
        if match is not None:
            for document in documents:
                if match in document['fileName'] or match in document['description']:
                    matches.append(document)
            documents = matches

        if output == "raw":
            return results
        if output == "json":
            return documents
        if output == "df":
            return pd.json_normalize(documents)
        if output == "download":
            if directory is None:
                directory = "."
            os.makedirs(directory, exist_ok=True)
            for doc in documents:
                with requests.get(doc["url"], stream=True,timeout=1000,verify=False) as r:
                    r.raise_for_status()
                    with open(directory + "/" + doc["fileName"], 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                        f.close()


    def getLabels(self,code:str=None):
        """
        List all labels used in an assetmodel instance, or the list of all labels of a given node

        Args:
           code (Optional): The value of the code property for the node to get labels for
        Returns:
            A list of all node labels/types present in the model, or, if specified, for a node
        """
        if code is None:
            args = {"q": "call db.labels()"}
        else: 
            args = {"q": "match (n:EI_CURRENT {code: '" + code + "'}) return labels(n)"}
        response = self._doJsonCypherRequest("EXECUTE",args)

        labels = []
        if code is None:
            for label in response:
                labels.append(label["label"])
        else:
            labels = response[0]['labels(n)']

        return labels

    def getRelatedEvents(self, node:Union[str,list], start:Union[str,int,float,datetime]="24 hours ago", end:Union[str,int,float,datetime]="now", limit:int=1000, output:str="json", directory:str=None):
        """
        Return all Events related to nodes via the Common Menu API.

        Args:
            node: The name of the node to query documents for
            start: Timestamp of beginning of time window to search for events, also accepts strings like "30 mins ago"
            end: Timestamp of end of time window to search for events
            output (Optional): The format in which to return the data. Accepts one of: "raw" - The raw json returned by the API; "json" - A processed version of the json response; "df" - A formatted pandas dataframe object; "download" - Downloads the files to a local directory"
            directory (Optional): Name and path to the directory created/used for downloaded documents. If omitted, will download files to current directory. Has no effect unless output is "download".

        Returns:
            The set of all documents related to the nodes, the format is dependent on the output parameter. If output is "download", it returns instead the files themselves

        Raises:
            KeyError: Raises an exception

        """
        nodes = force_list(node)
        results = []
        events = []
        for node in nodes:
            args = {"asset": node, "start": start, "end": end, "limit": limit}
            response = self._doJsonCommonMenuRequest("events", args)
            results.append(response)
            events.append(response["events"])

        if events == []:
            return 


        if output == "raw":
            return results
        if output == "json":
            return events[0]
        if output == "df":
            return pd.json_normalize(events[0])

    def getProperties(self, nodes:Union[str,list], output="json"):
        """
        Return all properties of a node via the Assetmodel API

        Args:
            node: The name of the node to return properties of
            output:

        Returns:
            A Json containing all nodes with a relation to any node that meets the criteria, and their relationship type.

        Raises:
            KeyError: Raises an exception

        """
        nodes = force_list(nodes)
        results = []
        properties = []
        for node in nodes:
            args = {}
            args["asset"] = node
            response = self._doJsonCommonMenuRequest("properties", args)
            results.append(response)
            properties.append(response["properties"])

        if output == "raw":
            return results
        if output == "json":
            return properties
        if output == "df":
            data = list(map(parse_properties, properties))
            return pd.DataFrame(data,nodes)


    def getMatchingNodes(self,prop:str,node:str,exact:bool=False):
        """
        Return all properties of matching nodes via a cypher query response
    
        Args:
            prop: The property on which to match
            match: A list of nodes to return properties for
            exact (Optional): Whether to only return nodes where the prop is equal to match, or nodes where prop contains match. Defaults to False
    
        Returns:
            A Json containing all nodes that contains the criteria.
    
        Raises:
            KeyError: Raises an exception
        """
    
        args = {}
        if exact:
            matchStatement = "n.%s = '%s'" % (prop,node)
        else:
            matchStatement = "n.%s contains '%s'" % (prop,node)
        args['q'] = 'MATCH (n) WHERE %s RETURN n' % matchStatement
    
        return self._doJsonCypherRequest("execute", args)
    
    def getRelatedAssetsCypher(self, prop, nodes, exact: bool = False, relation=None):
        """
        Return all assets directly related to a given asset.
    
        Args:
            prop: The property on which to match a node
            nodes: The value of the property to match
            exact: Whether or not to only to apply to assets exactly matching value of node (Defaults to False)
            relation: Specify a required relationship type for returned nodes
    
        Returns:
            A Json containing all nodes with a relation to any node that meets the criteria, and their relationship type.
    
        Raises:
            KeyError: Raises an exception
    
        """
        ret = []
        exact = True
        for node in force_list(nodes):
            args = {}
            if relation is not None: relation = ":" + relation
            if exact:
                matchStatement = "n.%s = '%s'" % (prop, node)
            else:
                matchStatement = "n.%s contains '%s'" % (prop, node)
            args['q'] = 'MATCH (n)-[r%s]-(m:AssetObject) WHERE %s RETURN m' % (relation, matchStatement)
    
        return list(map(cypherRespMap, self._doJsonCypherRequest("execute", args)))  # Func was map of k -> k["m"]

def get_assetmodel(eigenserver:EigenServer=None):
    """
    Connect to Assetmodel of eigenserver. If eigenserver is not provided this will default to the EIGENSERVER environmental variable
    
    Args:
        eigenserver: An instance of EigenServer() to query

    Returns:
        An object defining a connection to the AssetModel
    """
    if eigenserver is None:
        eigenserver = get_default_server()
    elif type(eigenserver) == str:
        eigenserver = EigenServer(eigenserver)

    return AssetModel(eigenserver.getEigenServerUrl() + "ei-applet" + "/", eigenserver.auth)
