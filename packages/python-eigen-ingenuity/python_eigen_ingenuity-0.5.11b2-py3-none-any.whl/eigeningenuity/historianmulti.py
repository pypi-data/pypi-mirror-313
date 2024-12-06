"""Eigen Ingenuity - Historian

This package deals with the Eigen Ingenuity Historian API, mostly by means
of the JSON Bridge Historian.

To get a historian object to work with, use get_historian(xxx) with either
an instance name (which will be resolved via the the usual methods in
eigeningenuity.core) or a full URL to a JSON Bridge Historian instance.

  from eigeningenuity.historian import get_historian
  from time import gmtime, asctime

  h = get_historian("pi-opc")
  tags = h.listDataTags()
  for tag in tags:
      dp = h.getCurrentDataPoint(tag)
      print(asctime(time.gmtime(dp['timestamp'])), dp['value'])
"""

import requests, warnings
from urllib.parse import quote as urlquote
from typing import Union
from datetime import datetime

from requests.exceptions import ConnectionError
from urllib.error import URLError
from eigeningenuity.core import get_default_server, EigenServer
from eigeningenuity.util import force_list, time_to_epoch_millis, EigenException, \
        multi_response_to_df, merge_tags_from_response, update_keys, _do_historian_multi_request, format_output

class HistorianMulti (object):
    """A Historian which talks the Eigen Historian Json Bridge protocol.
    """

    def __init__(self, baseurl, auth, historian):
        """This is a constructor. It takes in a URL like http://infra:8080/historian-servlet/jsonbridge/Demo-influxdb"""
        self.baseurl = baseurl
        self.serverurl = baseurl + "multi/"
        self.writeurl = baseurl + "write/points"
        self.listurl = baseurl + "list"
        self.searchurl = baseurl + "search"

        self.auth = auth
        self.historian = ""
        if historian:
            self.historian = historian + "/"
        
        
    def _testConnection(self):
        try:
            status = requests.get(self.serverurl, verify=False).status_code
            if status != 200:
                raise ConnectionError(
                    "Invalid API Response from " + self.serverurl + ". Please check the url is correct and the instance is up.")
        except (URLError, ConnectionError):
            raise ConnectionError ("Failed to connect to ingenuity instance at " + self.serverurl + ". Please check the url is correct and the instance is up.")

    def getCurrentDataPoints(self,tags: Union[str, list], output: str = "json"):
        tags = force_list(tags)
        body = {
            "requests": {}
        }

        for tag in tags:
            fulltag = tag
            if "/" not in tag:
                fulltag = self.historian + tag
            request = {
                "type": "CURRENT_POINT",
                "tag": fulltag,
                "details": {}
            }

            body["requests"][tag] = request

        response = _do_historian_multi_request(self.serverurl,body,self.auth)

        return format_output(output,response,tags)



    def getInterpolatedPoints(self, tags: Union[str, list], timestamps: Union[list, int, float, str, datetime],
                              output: str = "json"):
        """
        Return a specified number of interpolated datapoints between a start and end timestamp for one or more datatags

        Args:
            tags: A datatag (string), or list of datatags
            timestamps: One (string) or more (list) timestamps for which to return a datapoint. Accepts epoch milliseconds, python datetime objects, or strings of format dd-mm-YYYYTHH:MM:DD
            output (Optional): The format in which to return the data. Accepts one of: "raw" - The raw json returned by the API, "json" - A processed version of the json response, "df" - A formatted pandas dataframe object. Defaults to "json".

        Returns:
            Timestamps, values and statuses for each datapoint returned, the format is dependent on the output parameter

        Raises:
            ValueError: When invalid Output Type is given
            URLError: When no Ingenuity instance could be found at given EigenServer, or no internet connection is available
            RemoteServerException: When the provided historian could not be found, or the API response contains an error
            RunTimeError/HTTPError: No response from the API
        """
        body = {
            "requests": {}
        }

        tags = force_list(tags)
        timestamps = force_list(timestamps)
        timestamps = [time_to_epoch_millis(timestamp) for timestamp in timestamps]

        for tag in tags:
            fulltag = tag
            if "/" not in tag:
                fulltag = self.historian + tag
            for index, timestamp in enumerate(timestamps):
                request = {
                    "type": "HISTORICAL_POINT",
                    "tag": fulltag,
                    "details": {
                        "at": timestamp
                    }
                }

                body["requests"][tag + "-" + str(index)] = request


        response = _do_historian_multi_request(self.serverurl,body,self.auth)
        items = merge_tags_from_response(response["results"])

        return format_output(output,items,tags,timestamps)


    def getInterpolatedRange(self, tags: Union[str, list], start: Union[int, float, str, datetime],
                             end: Union[int, float, str, datetime], count: int = 1000, output: str = "json"):
        """Return a specified number of interpolated datapoints between a start and end timestamp for one or more datatags

        Args:
            tags: A datatag, or list of datatags
            start: Start of the time range. Accepts epoch milliseconds, python datetime objects, or strings of format dd-mm-YYYYTHH:MM:DD
            end: End of the time range. Accepts epoch milliseconds, python datetime objects, or strings of format dd-mm-YYYYTHH:MM:DD
            count (Optional): Number of points to return, evenly spaced across the given time range. Defaults to 1000
            output (Optional): The format in which to return the data. Accepts one of: "raw" - The raw json returned by the API, "json" - A processed version of the json response, "df" - A formatted pandas dataframe object. Defaults to "json".

        Returns:
            Timestamps, values and statuses for each datapoint returned, the format is dependent on the output parameter

        Raises:
            ValueError: When invalid Output Type is given
            URLError: When no Ingenuity instance could be found at given EigenServer, or no internet connection is available
            RemoteServerException: When the provided historian could not be found, or the API response contains an error
            RunTimeError/HTTPError: No response from the API
        """

        body = {
            "requests": {}
        }

        tags = force_list(tags)

        for tag in tags:
            fulltag = tag
            if "/" not in tag:
                fulltag = self.historian + tag
            request = {
                "type": "INTERPOLATED_POINTS",
                "tag": fulltag,
                "details": {
                    "from": time_to_epoch_millis(start),
                    "to": time_to_epoch_millis(end),
                    "count": count
                }
            }
            
            body["requests"][tag] = request

        response = _do_historian_multi_request(self.serverurl,body,self.auth)

        return format_output(output,response,tags)
    
    def getRawDatapoints(self, tags: Union[str, list], start: Union[int, float, str, datetime],
                             end: Union[int, float, str, datetime], maxpoints: int = 1000, output: str = "json"):
        """Return up to a specified number of raw datapoints between a start and end timestamp for one or more datatags

        Args:
            tags: A datatag, or list of datatags
            start: Start of the time range. Accepts epoch milliseconds, python datetime objects, or strings of format dd-mm-YYYYTHH:MM:DD
            end: End of the time range. Accepts epoch milliseconds, python datetime objects, or strings of format dd-mm-YYYYTHH:MM:DD
            maxPoints (Optional): Max number of points to return. The query will return raw points in sequence from the first raw point in the timespan, until the end, or the point limit is reached. Defaults to 1000
            output (Optional): The format in which to return the data. Accepts one of: "raw" - The raw json returned by the API, "json" - A processed version of the json response, "df" - A formatted pandas dataframe object. Defaults to "json".

        Returns:
            Timestamps, values and statuses for each datapoint returned, the format is dependent on the output parameter

        Raises:
            ValueError: When invalid Output Type is given
            URLError: When no Ingenuity instance could be found at given EigenServer, or no internet connection is available
            RemoteServerException: When the provided historian could not be found, or the API response contains an error
            RunTimeError/HTTPError: No response from the API
        """

        body = {
            "requests": {}
        }

        tags = force_list(tags)

        for tag in tags:
            fulltag = tag
            if "/" not in tag:
                fulltag = self.historian + tag
            request = {
                "type": "RAW_POINTS",
                "tag": fulltag,
                "details": {
                    "from": time_to_epoch_millis(start),
                    "to": time_to_epoch_millis(end),
                    "maxPoints": maxpoints
                }
            }
            
            body["requests"][tag] = request

        response = _do_historian_multi_request(self.serverurl,body,self.auth)

        return format_output(output,response,tags)
    
    def getClosestRawPoint(self, tags: Union[str, list], timestamps: Union[int, float, str, datetime, list],
                             before_or_after:str="AFTER_OR_AT", output: str = "json"):
        """Return up to a specified number of raw datapoints between a start and end timestamp for one or more datatags

        Args:
            tags: A datatag, or list of datatags
            start: Start of the time range. Accepts epoch milliseconds, python datetime objects, or strings of format dd-mm-YYYYTHH:MM:DD
            end: End of the time range. Accepts epoch milliseconds, python datetime objects, or strings of format dd-mm-YYYYTHH:MM:DD
            maxPoints (Optional): Max number of points to return. The query will return raw points in sequence from the first raw point in the timespan, until the end, or the point limit is reached. Defaults to 1000
            output (Optional): The format in which to return the data. Accepts one of: "raw" - The raw json returned by the API, "json" - A processed version of the json response, "df" - A formatted pandas dataframe object. Defaults to "json".

        Returns:
            Timestamps, values and statuses for each datapoint returned, the format is dependent on the output parameter

        Raises:
            ValueError: When invalid Output Type is given
            URLError: When no Ingenuity instance could be found at given EigenServer, or no internet connection is available
            RemoteServerException: When the provided historian could not be found, or the API response contains an error
            RunTimeError/HTTPError: No response from the API
        """
        before_or_after = before_or_after.upper()

        if before_or_after.upper() not in ["BEFORE", "BEFORE_OR_AT", "AFTER", "AFTER_OR_AT"]:
            raise EigenException('before_or_after must be one of ["BEFORE", "BEFORE_OR_AT", "AFTER", "AFTER_OR_AT"]')

        body = {
            "requests": {}
        }

        tags = force_list(tags)
        timestamps = force_list(timestamps)
        timestamps = [time_to_epoch_millis(timestamp) for timestamp in timestamps]

        for tag in tags:
            fulltag = tag
            if "/" not in tag:
                fulltag = self.historian + tag
            for index, timestamp in enumerate(timestamps):
                request = {
                    "type": f"POINT_{before_or_after.upper()}",
                    "tag": fulltag,
                    "details": {
                        "at": time_to_epoch_millis(timestamp),
                    }
                }
            
                body["requests"][tag + "-" + str(index)] = request


        response = _do_historian_multi_request(self.serverurl,body,self.auth)
        items = merge_tags_from_response(response["results"])

        return format_output(output,items,tags,timestamps)
    
    def listDataTags(self, historian:str=None, limit:int=100, match:str=""):
        """List all tags in a historian, or those matching a wildcard

        Args:
            historian: Name of the historian containing tags of interest
            limit: Max number of records to return
            match: A string that tags must match to be returned (Accepts * as wildcard character)

        Returns:
            A list of tag names

        Raises:
            URLError: When no Ingenuity instance could be found at given EigenServer, or no internet connection is available
            RemoteServerException: When the provided historian could not be found, or the API response contains an error
            RunTimeError/HTTPError: No response from the API
        """
        metadata = self.getMetaData(historian, limit, match)

        tags = [tag["tagName"] for tag in metadata]

        return tags
    
    def getMetaData(self, historian:str=None, limit:int=100, match:str=""):
        """Get Metadata for all tags in a historian, or those matching a wildcard

        Args:
            historian: Name of the historian containing tags of interest
            limit: Max number of records to return
            match: A string that tags must match to be returned (Accepts * as wildcard character)

        Returns:
            A list of dicts with metadata fields for each tag

        Raises:
            URLError: When no Ingenuity instance could be found at given EigenServer, or no internet connection is available
            RemoteServerException: When the provided historian could not be found, or the API response contains an error
            RunTimeError/HTTPError: No response from the API
        """
        if historian is None:
            historian = self.historian

        resp = _do_historian_multi_request(self.searchurl + f'?historian={historian}&limit={limit}&search={match}',{},self.auth,get_request=True)
        metadata = resp["tags"]

        return metadata
    
    def listHistorians(self, historian:str=None, limit:int=100, match:str=""):
        """Get Metadata for all tags in a historian, or those matching a wildcard

        Args:
            historian: Name of the historian containing tags of interest
            limit: Max number of records to return
            match: A string that tags must match to be returned (Accepts * as wildcard character)

        Returns:
            A list of dicts with metadata fields for each tag

        Raises:
            URLError: When no Ingenuity instance could be found at given EigenServer, or no internet connection is available
            RemoteServerException: When the provided historian could not be found, or the API response contains an error
            RunTimeError/HTTPError: No response from the API
        """
        if historian is None:
            historian = self.historian

        resp = _do_historian_multi_request(self.searchurl + f'?historian={historian}&limit={limit}&search={match}',{},self.auth,get_request=True)
        metadata = resp["tags"]

        return metadata
    
    def writePoints(self, tag:str, points: Union[dict, list]):
        """Write one or more points to a single tag

        Args:
            tag: A datatag
            points: A dict, or list of dicts of the form {"value": x, "timestamp": y}. Where x is an int/double and y is a python datetime, iso datetime string, or epoch timestamp

        Returns:
            A dict with keys: success (bool) representing the success of the request. message (str) forwarded from the api.

        Raises:
            URLError: When no Ingenuity instance could be found at given EigenServer, or no internet connection is available
            RemoteServerException: When the provided historian could not be found, or the API response contains an error
            RunTimeError/HTTPError: No response from the API
        """
        points = force_list(points)
        if "/" not in tag:
            tag = self.historian + tag

        for point in points:
            if "status" not in point.keys():
                point['status'] = "OK"
            point['timestamp'] = time_to_epoch_millis(point['timestamp'])
        
        body = {
            "points": {
                tag: points
            },
            "createTags": True
        }

        message = _do_historian_multi_request(self.writeurl,body,self.auth,True)

        if message == 'All points written!':
            ret = {"success": True, "message": message}
        else:
            ret = {"success": False, "message": message}

        return ret


    def writePointsBatch(self, data:Union[dict,list]):
        """Write one or more points to multiple tags

        Args:
            payloads: A dict (or list of dicts) of the form {tag1: [{"value": x, "timestamp": y}, ...], tag2: [...], ...}    
        
        Returns:
            None

        Raises:
            URLError: When no Ingenuity instance could be found at given EigenServer, or no internet connection is available
            RemoteServerException: When the provided historian could not be found, or the API response contains an error
            RunTimeError/HTTPError: No response from the API
        """
        data = force_list(data)

        payload = {}
        tags = []

        for item in data:
            if set(item.keys()).intersection(set(tags)):
                for tag in set(item.keys()).intersection(set(tags)):
                    payload[tag] += item[tag]
                    item.pop(tag)
            payload = payload | item
            tags += item.keys()

        for key in payload.keys():
            for datapoint in payload[key]:
                if "status" not in datapoint.keys():
                    datapoint['status'] = "OK"
                datapoint['timestamp'] = time_to_epoch_millis(datapoint['timestamp'])
        
        payload = update_keys(payload, self.historian)

        body = {
            "points": payload,
            "createTags": True
        }

        message = _do_historian_multi_request(self.writeurl,body,self.auth,True)

        if message == 'All points written!':
            ret = {"success": True, "message": message}
        else:
            ret = {"success": False, "message": message}

        return ret


def createPoint(value:Union[int,float],timestamp:Union[int,str,datetime],status:str="OK"):
    """Quickly Create a dict of the format required to push data to historians

        Args:
            value: The value to be pushed
            timestamp: The timestamp to assign the value to. Accepts formats of epoch milliseconds, python datetimes, and iso format datetime strings
            status: (Optional) Indicates the quality of the data, accepts "OK" or "BAD". Defaults to "OK"

        Returns:
            A structured dict for use in the WriteToTag method
        """
    if status not in ["OK","BAD"]:
        raise EigenException("Bad Status Parameter, must be 'OK' or 'BAD'")
    return {"value": value, "timestamp": timestamp, "status": status}

def get_historian_multi(eigenserver = None, default_historian = None) -> HistorianMulti:
    """Instantiate a historian object for the given instance.

    Args:
        eigenserver (Optional): An EigenServer Object linked to the ingenuity url containing the historian. Can be omitted if environmental variable "EIGENSERVER" exists and is equal to the Ingenuity base url
        default_historian (Optional): The name of the historian to be used if none is passed with a tag. Defaults to None, and will not hanbdle tags without historians.

    Returns:
        An Object that can be used to query historian data.

    """
    if eigenserver is None:
        eigenserver = get_default_server()
    elif type(eigenserver) == str:
        eigenserver = EigenServer(eigenserver)

    return HistorianMulti(eigenserver.getEigenServerUrl() + "historian" + "/", eigenserver.auth, default_historian)


