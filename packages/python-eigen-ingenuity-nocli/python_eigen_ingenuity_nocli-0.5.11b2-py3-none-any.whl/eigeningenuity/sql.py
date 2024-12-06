"""Eigen Ingenuity - SQL

This package deals with the Eigen Ingenuity SQL database.

To retrieve data execute a custom query with

  from eigeningenuity.assetmodel import matchNode
  from time import gmtime, asctime

  h = get_historian("Demo-influxdb","demo.eigen.co")

  cmd = "EXECUTE"
  db = "aveva-db",
  query = '''
    SELECT TAG_TISLOCATIONCODE, TAG_TISLOCATIONNAME, TAG_NUMBER, TAG_DESC, TAG_STATUS, TAG_STATUSDESC, TAG_BARRIERCODE, TAG_BARRIERNAME, TAG_BARRIERISACTIVE, TAG_BARRIERPERFORMANCESTD, TAG_BARRIERVERIFICATIONACT
    FROM VT_TAGBARRIER
    WHERE (ROWNUM <= 10)
    '''

  response = h.executeRawQuery(cmd,db,query)
"""

from eigeningenuity import EigenServer
from urllib.parse import quote as urlquote
from eigeningenuity.util import _do_eigen_json_request
from eigeningenuity.core import get_default_server
import requests, json
import pandas as pd
import datetime as dt

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

class sqlConnection (object):
    """An elasticsearch instance which talks the Eigen elastic endpoint.
    """
    def __init__(self, baseurl, auth):
       """This is a constructor. It takes in a URL like http://demo.eigen.co/eigen-webtools-servlet/sqlquery"""
       self.baseurl = baseurl
       self.auth = auth

    def _testConnection(self):
        """Preflight Request to verify connection"""
        try:
            status = requests.get(self.baseurl, verify=False).status_code
        except ConnectionError:
            raise ConnectionError("Failed to connect to ingenuity instance at " + self.baseurl + ". Please check the url is correct and the instance is up.")

    def _doJsonRequest(self,cmd,params):
        url = self.baseurl + "?cmd=" + urlquote(cmd)
        return _do_eigen_json_request(url, self.auth, **params)

    def executeRawQuery(self,cmd:str,db:str,query:str,output:str="json",filepath:str=None):
        """
        Run a user composed raw SQL query against an ingenuity SQL database

        Args:
            cmd: Command to run against the database e.g. EXECUTE
            db: Name of the SQL database to query
            query: The Body of the SQL query
            output: (Optional) The format in which to return the data. Accepts one of: "raw" - The raw json returned by the API; "json" - A processed version of the json response; "df" - A formatted pandas dataframe object; "file" - Writes the response to a .json file in the local directory. Defaults to "json"
            filepath: (Optional) Name and path to the .json file that will be created/overwritten. If omitted, will create a file in the current directory with an auto-generated name. Has no effect unless output is "file".

        Returns:
            The SQL response to the given query, the format is dependent on the output parameter
        """
        args = {}
        args['db'] = db
        args['query'] = query
        response = self._doJsonRequest(cmd,args)["results"]

        if output == "raw" or output == "json":
            return response
        elif output == "string":
            return json.dumps(response)
        elif output == "df":
            return pd.DataFrame(response)
        elif output == "file":
            if filepath is None:
                filepath = "eigenSQLResponse-" + db + "-" + str(dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
            with open(filepath + ".json", "w") as f:
                f.write(json.dumps(response, indent=4))
        return None
    
    def listDatabases(self):
        """
        Get the available SQL Databases on the server

        Args:
            None
        Returns:
            A list of SQL databases that allow this library to access them
        """
        args = {}
        cmd = "LISTDBS"
        response = self._doJsonRequest(cmd,args)["results"]

        return response
    
    def listTables(self,db):
        """
        A list of Tables from within a provided database

        Args:
            db: Name of the SQL database to query
        
        Returns:
            The list of tables available for the user to query within the given database
        """
        args = {}
        cmd = "LIST"
        args["db"] = db
        response = self._doJsonRequest(cmd,args)["results"]

        return response


def get_sql(eigenserver:EigenServer = None):
    """Instantiate an SQL connection for the given EigenServer.

    Args:
        eigenserver: (Optional) An EigenServer Object linked to the ingenuity url containing the elasticsearch. Can be omitted if environmental variable "EIGENSERVER" exists and contains the Ingenuity base url

    Returns:
        An Object that can be used to query SQL databases connected to the ingenuity.
    """
    if eigenserver is None:
        eigenserver = get_default_server()
    elif type(eigenserver) == str:
        eigenserver = EigenServer(eigenserver)
        
    return sqlConnection(eigenserver.getEigenServerUrl() + "eigen-webtools-servlet/sqlquery", eigenserver.auth)