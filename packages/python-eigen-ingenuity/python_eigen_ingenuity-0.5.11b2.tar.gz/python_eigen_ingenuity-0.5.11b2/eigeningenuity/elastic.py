"""Eigen Ingenuity - Elasticsearch

This package deals with the Eigen Ingenuity Elasticsearch database.

To retrieve an AssetObject use matchNode, or execute a custom cypher query with 

  from eigeningenuity.assetmodel import matchNode
  from time import gmtime, asctime

  nodes = matchNodes("code","System_")
  
  for node in nodes:
      code = node.code
      print(code)  
"""

from eigeningenuity import EigenServer
from urllib.parse import quote as urlquote
from eigeningenuity.util import is_list,force_list,_do_eigen_json_request,EigenException
from eigeningenuity.core import get_default_server
import pandas as pd
import datetime as dt
import json
import requests
import fnmatch
from requests.exceptions import ConnectionError
from urllib.error import URLError
from typing import Union

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

class ElasticConnection (object):
    """An elasticsearch instance which talks the Eigen elastic endpoint.
    """

    def __init__(self, baseurl, auth):
       """This is a constructor. It takes in a URL like http://infra:8080/ei-applet/search/"""
       self.baseurl = baseurl
       self.auth = auth

    def _doJsonRequest(self,cmd,params):
        url = self.baseurl + "?cmd=" + urlquote(cmd)
        return _do_eigen_json_request(url,self.auth,**params)

    def _testConnection(self,instance,index):
        """Preflight Request to verify connection to ingenuity"""
        try:
            status = requests.get(self.baseurl + "?cmd=DODIRECTSEARCH&clientname=" + instance + "&index=" + index + "&search=%7B%7D", verify=False).status_code
            if status != 200:
                raise ConnectionError(
                    "Invalid API Response from " + self.baseurl + "?cmd=DODIRECTSEARCH&clientname" + instance + ". Please check the base url is correct, the instance is running and has an elasticsearch database.")
        except (URLError, ConnectionError):
            raise ConnectionError ("Failed to connect to ingenuity instance at " + self.baseurl + "?cmd=DODIRECTSEARCH&clientname=" + instance + "&index=" + index + ". Please check the url is correct and the instance is up.")
        
        return status
    
    def listIndices(self,instance:str, wildcard:str=None):
        """Lists all indices in Elastic Database.

        Args:
            instance: The elasticsearch instance to query indices from.
            wildcard: (Optional) Return indices that match the wildcard
            
        Returns:
            List of all indices
        """

        args = {"clientname": instance}

        mappings = self._doJsonRequest("GETMAPPINGS",args)

        if wildcard is not None:
            indices = [item for item in mappings if wildcard in item]
        else:
            indices = mappings

        return indices

        
    def checkIndices(self,instance:str,indices:str):
        """Checks for indices in Elastic Database.

        Args:
            instance: The elasticsearch instance to query instances from.
            indices: The elasticsearch indices to search for
            
        Returns:
            Boolean indicating existence of the index, or dict of form {index: boolean}
        """

        foundIndices = self.listIndices(instance)
        indices = force_list(indices)

        result = {}

        if len(indices) != 1:
            for index in indices:
                if index in foundIndices:
                    result[index] = True
                else:
                    result[index] = False
        else:
            if indices[0] in foundIndices:
                return True
            else:
                return False

        return result


    def executeRawQuery(self,index:str, query:Union[str,dict], instance:str = "elasticsearch-int", output:str = "json", filepath:str = None):
        """Executes a raw cypher query against Elastic.

        Args:
            index: The elasticsearch index to query
            query: The body of the query
            instance: (Optional) The instance of elasticsearch to query. Defaults to elasticsearch-int
            output: (Optional) The format in which to return the data. Accepts one of: "raw" - The raw json returned by the API; "json" - A processed version of the json response; "df" - A formatted pandas dataframe object; "file" - Writes the response to a .json file in the local directory. Defaults to "json"
            filepath: (Optional) Name and path to the .json file that will be created/overwritten. If omitted, will create a file in the current directory with a generated name. Has no effect unless output is "file".
            
        Returns:
            Elasticsearch API response to the query, the format is dependent on the output parameter
        """
        # self._testConnection(instance,index)
        validOutputTypes = ["raw", "json", "df", "file"]
        if output not in validOutputTypes:
            raise ValueError("output must be one of %r." % validOutputTypes)

        if type(query) is dict:
            query = json.dumps(query)

        args = {}
        args["clientname"] = instance
        args["index"] = index
        args["search"] = query

        response = self._doJsonRequest("DODIRECTSEARCH", args)

        if "error" in response.keys():
            raise EigenException("Invalid request", response["error"])

        if output == "raw":
            return response
        elif output == "json":
            return response['results']
        elif output == "df":
            return pd.json_normalize(response['results'])
        elif output == "file":
            if filepath is None:
                filepath = "eigenElasticResponse-" + index + "-" + str(dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
            with open(filepath + ".json", "w") as f:
                f.write(json.dumps(response, indent=4))



def get_elastic(eigenserver:EigenServer = None):
    """Instantiate an elasticsearch connection for the given EigenServer.

    Args:
        eigenserver: (Optional) An EigenServer Object linked to the ingenuity url containing the elasticsearch. Can be omitted if environmental variable "EIGENSERVER" exists and is equal to the Ingenuity base url

    Returns:
        An Object that can be used to query elasticsearch data from the ingenuity.
    """
    if eigenserver is None:
        eigenserver = get_default_server()
    elif type(eigenserver) == str:
        eigenserver = EigenServer(eigenserver)
        
    return ElasticConnection(eigenserver.getEigenServerUrl() + "ei-applet/search", eigenserver.auth)