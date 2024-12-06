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

import json
import math
import logging
import csv
import requests
from urllib.parse import quote as urlquote
from typing import Union
from datetime import datetime

from requests.exceptions import ConnectionError
from urllib.error import URLError
from eigeningenuity.core import get_default_server, EigenServer
from eigeningenuity.util import _do_eigen_json_request, force_list, time_to_epoch_millis, is_list, \
    get_datetime, number_to_string, EigenException, get_timestamp_string, pythonTimeToFloatingSecs, \
    serverTimeToPythonTime, pythonTimeToServerTime, get_time_tuple, parse_duration, jsonToDf, \
    aggToDf, divide_chunks, flattenDict, csvWriter

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class JsonBridgeHistorian (object):
    """A Historian which talks the Eigen Historian Json Bridge protocol.
    """

    def __init__(self, serverurl, auth):
        """This is a constructor. It takes in a URL like http://infra:8080/historian-servlet/jsonbridge/Demo-influxdb"""
        self.serverurl = serverurl
        self.historian = serverurl.split("/")[-1]
        self.baseurl = serverurl.rsplit("/",1)[0]
        self.auth = auth

    def _testConnection(self):
        try:
            status = requests.get(self.serverurl, verify=False).status_code
            if status != 200:
                raise ConnectionError(
                    "Invalid API Response from " + self.serverurl + ". Please check the url is correct and the instance is up.")
        except (URLError, ConnectionError):
            raise ConnectionError ("Failed to connect to ingenuity instance at " + self.serverurl + ". Please check the url is correct and the instance is up.")

    def listDataTags(self, wildcard):
        """Return a list of all tags that match a given wildcard, or all tags in the historian

        Args:
            wildcard (Optional): Return all tags that contain this value in their name. Defaults to All Tags in historian.

        Returns:
            A list of all tags containing wildcard

        Raises:
            ValueError: When invalid Output Type is given
            URLError: When no Ingenuity instance could be found at given EigenServer, or no internet connection is available
            RemoteServerException: When the provided historian could not be found, or the API response contains an error
            RunTimeError/HTTPError: No response from the API
        """
        # self._testConnection()
        args = {}
        if wildcard is not None:
            args['match'] = force_list(wildcard)

        return self._doJsonRequest("list", args)

    def getMetaData(self, tags: Union[str, list], output: str = "json", filepath:str=None, multi_csv:bool=False):
        """
        Return a specified number of interpolated datapoints between a start and end timestamp for one or more datatags

        Args:
            tags: A datatag, or list of datatags
            output (Optional): The format in which to return the data. Accepts one of: "raw" - The raw json returned by the API, "json" - A processed version of the json response, "df" - A formatted pandas dataframe object. Defaults to "json".

        Returns:
            Units, unit multiplier, and description for each datatag, the format is dependent on the output parameter

        Raises:
            ValueError: When invalid Output Type is given
            URLError: When no Ingenuity instance could be found at given EigenServer, or no internet connection is available
            RemoteServerException: When the provided historian could not be found, or the API response contains an error
            RunTimeError/HTTPError: No response from the API
        """
        validOutputTypes = ["raw", "json", "df", "csv", "string"]
        if output not in validOutputTypes:
            raise ValueError("output must be one of %r." % validOutputTypes)
        response = {}

        for tag in force_list(tags):
            args = {}
            args['tag'] = tag
            response[tag] = (self._doJsonRequest("getmeta", args))


        if output == "raw":
            return response
        elif output == "json":
            if len(force_list(tags)) == 1:
                return response[tags]
            else:
                return response
        elif output == "string":
            return json.dumps(response)
        elif output == "df":
            return jsonToDf(response, True)
        elif output == "csv":
            return csvWriter(response,self.historian,filepath,multi_csv,"GetMetaData")
        return None


    def getCurrentDataPoints(self, tags: Union[str, list], output: str = "json", filepath:str=None, multi_csv:bool=False):
        """
        Return most recent raw value for one or more datatags

        Args:
            tags: A datatag, or list of datatags
            output (Optional): The format in which to return the data. Accepts one of: "raw" - The raw json returned by the API, "json" - A processed version of the json response, "df" - A formatted pandas dataframe object. Defaults to "json".

        Returns:
            A timestamps, values and statuses for each tag, the format is dependent on the output parameter

        Raises:
            ValueError: When invalid Output Type is given
            URLError: When no Ingenuity instance could be found at given EigenServer, or no internet connection is available
            RemoteServerException: When the provided historian could not be found, or the API response contains an error
            RunTimeError/HTTPError: No response from the API
        """
        validOutputTypes = ["raw", "json", "df", "csv", "string"]
        if output not in validOutputTypes:
            raise ValueError("output must be one of %r." % validOutputTypes)
        args = {}
        args['tag'] = force_list(tags)
        response = self._doJsonRequest("getmulticurrent", args)
        items = response["items"]

        if response['unknown'] != []:
            if items == {}:
                raise EigenException("None of the provided tags could be found in historian " + self.historian)
            logging.warning("Could not find tags: " + str(response["unknown"]) + " in historian " + self.historian)

        if output == "raw":
            return response
        elif output == "json":
            if len(force_list(tags)) == 1:
                return items[tags]
            else:
                return items
        elif output == "string":
            return json.dumps(items)
        elif output == "df":
            return jsonToDf(items)
        elif output == "csv":
            return csvWriter(items,self.historian,filepath,multi_csv,"GetCurrent")
        return None


    def getInterpolatedPoints(self, tags: Union[str, list], timestamps: Union[list, int, float, str, datetime],
                              output: str = "json", filepath:str=None, multi_csv:bool=False):
        """
        Return a specified number of interpolated datapoints between a start and end timestamp for one or more datatags

        Args:
            tags: A datatag, or list of datatags
            timestamps: One or more timestamps for which to return a datapoint. Accepts epoch milliseconds, python datetime objects, or strings of format dd-mm-YYYYTHH:MM:DD
            output (Optional): The format in which to return the data. Accepts one of: "raw" - The raw json returned by the API, "json" - A processed version of the json response, "df" - A formatted pandas dataframe object. Defaults to "json".

        Returns:
            Timestamps, values and statuses for each datapoint returned, the format is dependent on the output parameter

        Raises:
            ValueError: When invalid Output Type is given
            URLError: When no Ingenuity instance could be found at given EigenServer, or no internet connection is available
            RemoteServerException: When the provided historian could not be found, or the API response contains an error
            RunTimeError/HTTPError: No response from the API
        """
        validOutputTypes = ["raw", "json", "df", "csv", "string"]
        if output not in validOutputTypes:
            raise ValueError("output must be one of %r." % validOutputTypes)
        args = {}
        args['tag'] = force_list(tags)
        args['timestamp'] = force_list(timestamps)
        response = self._doJsonRequest("getmulti", args)
        items = response['items']

        if response['unknown'] != []:
            if items == {}:
                raise EigenException("None of the provided tags could be found in historian " + self.historian)
            logging.warning("Could not find tags: " + str(response["unknown"]) + " in historian " + self.historian)

        if output == "raw":
            return response
        elif output == "json":
            if len(force_list(tags)) == 1:
                return items[tags]
            else:
                return items
        elif output == "string":
            return json.dumps(items)
        elif output == "df":
            return jsonToDf(items)
        elif output == "csv":
            return csvWriter(items,self.historian,filepath,multi_csv,"GetInterpolatedPoints")
        return None


    def getRawDataPoints(self, tags: Union[str, list], start: Union[int, float, str, datetime],
                         end: Union[int, float, str, datetime], maxpoints: int = 1000, output: str = "json", filepath:str=None, multi_csv:bool=False) -> object:
        """Return the first [maxpoints] raw datapoints between a start and end timestamp for one or more datatags, if maxpoints is greater than the total number of raw points, return all raw points within the time window

        Args:
            tags: A datatag, or list of datatags
            start: Start of the time range. Accepts epoch milliseconds, python datetime objects, or strings of format dd-mm-YYYYTHH:MM:DD
            end: End of the time range. Accepts epoch milliseconds, python datetime objects, or strings of format dd-mm-YYYYTHH:MM:DD
            maxpoints (Optional): The maximum number of points to return. Defaults to 1000
            output (Optional): The format in which to return the data. Accepts one of: "raw" - The raw json returned by the API, "json" - A processed version of the json response, "df" - A formatted pandas dataframe object. Defaults to "json".

        Returns:
            Timestamps, values and statuses for each datapoint returned, the format is dependent on the output parameter

        Raises:
            ValueError: When invalid Output Type is given
            URLError: When no Ingenuity instance could be found at given EigenServer, or no internet connection is available
            RemoteServerException: When the provided historian could not be found, or the API response contains an error
            RunTimeError/HTTPError: No response from the API
        """
        validOutputTypes = ["raw", "json", "df", "csv", "string"]
        if output not in validOutputTypes:
            raise ValueError("output must be one of %r." % validOutputTypes)
        args = {}
        args['tag'] = force_list(tags)
        args['start'] = time_to_epoch_millis(start)
        args['end'] = time_to_epoch_millis(end)
        args['maxpoints'] = maxpoints
        response = self._doJsonRequest("getraw", args)
        items = response["items"]

        if response['unknown'] != []:
            if items == {}:
                raise EigenException("None of the provided tags could be found in historian " + self.historian)
            logging.warning("Could not find tags: " + str(response["unknown"]) + " in historian " + self.historian)

        if output == "raw":
            return response
        elif output == "json":
            if len(force_list(tags)) == 1:
                return items[tags]
            else:
                return items
        elif output == "string":
            return json.dumps(items)
        elif output == "df":
            return jsonToDf(items)
        elif output == "csv":
            return csvWriter(items,self.historian,filepath,multi_csv,"GetRaw")
        return None



    def getInterpolatedRange(self, tags: Union[str, list], start: Union[int, float, str, datetime],
                             end: Union[int, float, str, datetime], count: int = 1000, output: str = "json", filepath:str=None, multi_csv:bool=False):
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
        validOutputTypes = ["raw", "json", "df", "csv", "string"]
        if output not in validOutputTypes:
            raise ValueError("output must be one of %r." % validOutputTypes)
        args = {}
        args['tag'] = force_list(tags)
        args['start'] = time_to_epoch_millis(start)
        args['end'] = time_to_epoch_millis(end)
        args['count'] = count
        response = self._doJsonRequest("getrange", args)
        items = response["items"]

        if response['unknown'] != []:
            if items == {}:
                raise EigenException("None of the provided tags could be found in historian " + self.historian)
            logging.warning("Could not find tags: " + str(response["unknown"]) + " in historian " + self.historian)

        if output == "raw":
            return response
        elif output == "json":
            if len(force_list(tags)) == 1:
                return items[tags]
            else:
                return items
        elif output == "string":
            return json.dumps(items)
        elif output == "df":
            return jsonToDf(items)
        elif output == "csv":
            return csvWriter(items,self.historian,filepath,multi_csv,"GetInterpolatedRange")
        return None

    def getAggregates(self, tags: Union[str, list], start: Union[int, float, str, datetime],
                      end: Union[int, float, str, datetime], fields: Union[str, list] = None, count: int = 1,
                      output: str = "json", filepath:str=None, multi_csv:bool=False):
        """
        Return specified aggregates of tags over a given time window, optionally divided into equal parts

        Args:
            tags: A datatag, or list of datatags
            start: Start of the time range. Accepts epoch milliseconds, python datetime objects, or strings of format dd-mm-YYYYTHH:MM:DD
            end: End of the time range. Accepts epoch milliseconds, python datetime objects, or strings of format dd-mm-YYYYTHH:MM:DD
            fields (Optional): The aggregates to be calculated, accepts any subset of ["min","max","mean","stddev","var","numgood","numbad"]. Defaults to all aggregates.
            count (Optional): Number of intervals to split the time window into, returning aggregates over each interval. Defaults to 1
            output (Optional): The format in which to return the data. Accepts one of: "raw" - The raw json returned by the API, "json" - A processed version of the json response, "df" - A formatted pandas dataframe object. Defaults to "json".

        Returns:
            Timestamps, values and statuses for each datapoint returned, the format is dependent on the output parameter

        Raises:
            ValueError: When invalid Output Type is given
            URLError: When no Ingenuity instance could be found at given EigenServer, or no internet connection is available
            RemoteServerException: When the provided historian could not be found, or the API response contains an error
            RunTimeError/HTTPError: No response from the API
        """
        validOutputTypes = ["raw", "json", "df", "csv", "string"]
        if output not in validOutputTypes:
            raise ValueError("output must be one of %r." % validOutputTypes)
        args = {}
        args['tag'] = force_list(tags)
        args['start'] = time_to_epoch_millis(start)
        args['end'] = time_to_epoch_millis(end)
        args['count'] = count
        args['aggfields'] = fields

        response = self._doJsonRequest("getagg", args)

        keys = set(response.keys())
        missing = [x for x in args['tag'] if x not in keys]

        if missing != []:
            if response == {}:
                raise EigenException("None of the provided tags could be found in historian " + self.historian)
            logging.warning("Could not find tags: " + str(missing) + " in historian " + self.historian)

        if output == "raw":
            return response
        elif output == "json":
            if len(force_list(tags)) == 1:
                return response[tags]
            else:
                return response
        elif output == "string":
            return json.dumps(response)
        elif output == "df":
            return aggToDf(response,fields)
        elif output == "csv":
            order = ["tag","start","end","min","max","avg","var","stddev","count","numgood","numbad"]
            return csvWriter(response,self.historian,filepath,multi_csv,"GetAggregates",order,True)
        return None


    def getAggregateIntervals(self, tags, start: Union[int, float, str, datetime],
                              end: Union[int, float, str, datetime], window: str = None,
                              fields: Union[str, list] = None, output: str = "json", filepath:str=None, multi_csv:bool=False):
        """
        Return specified aggregates of tags over a given time window, optionally divided into equal parts

        Args:
            tags: A datatag, or list of datatags
            start: Start of the time range. Accepts epoch milliseconds, python datetime objects, or strings of format dd-mm-YYYYTHH:MM:DD
            end: End of the time range. Accepts epoch milliseconds, python datetime objects, or strings of format dd-mm-YYYYTHH:MM:DD
            window (Optional): Sub-interval of time to divide the timeframe into as a multiple of seconds,minutes,hours,days or years. (e.g. "1d" for 1 day or "2h" for 2 hours etc). Defaults to the entire timeframe.
            fields (Optional): The aggregates to be calculated, accepts any subset of ["min","max","mean","stddev","var","numgood","numbad"]. Defaults to all aggregates.
            output (Optional): The format in which to return the data. Accepts one of: "raw" - The raw json returned by the API, "json" - A processed version of the json response, "df" - A formatted pandas dataframe object. Defaults to "json".

        Returns:
            Timestamps, values and statuses for each datapoint returned, the format is dependent on the output parameter

        Raises:
            ValueError: When invalid Output Type is given
            URLError: When no Ingenuity instance could be found at given EigenServer, or no internet connection is available
            RemoteServerException: When the provided historian could not be found, or the API response contains an error
            RunTimeError/HTTPError: No response from the API
        """
        validOutputTypes = ["raw", "json", "df", "csv", "string"]
        if output not in validOutputTypes:
            raise ValueError("output must be one of %r." % validOutputTypes)

        epoch_ms_start = time_to_epoch_millis(start)
        epoch_ms_end = time_to_epoch_millis(end)

        if window is not None:
            windowDuration = parse_duration(window)
            totalDuration = epoch_ms_end - epoch_ms_start
            count = math.floor(totalDuration / windowDuration)
            epoch_ms_end = epoch_ms_end - totalDuration % windowDuration
        else:
            count = 1
        if count > 1000:
            logging.warning(
                "getAggregateIntervals is only designed to return up to 1000 aggregate sets, currently returning " + str(
                    count) + " sets. This may return overlapping intervals")

        args = {}
        args['tag'] = force_list(tags)
        args['start'] = epoch_ms_start
        args['end'] = epoch_ms_end
        args['count'] = count
        args['aggfields'] = fields
        response = self._doJsonRequest("getagg", args)

        keys = set(response.keys())
        missing = [x for x in args['tag'] if x not in keys]

        if missing != []:
            if response == {}:
                raise EigenException("None of the provided tags could be found in historian " + self.historian)
            logging.warning("Could not find tags: " + str(missing) + " in historian " + self.historian)

        if output == "raw":
            return response
        elif output == "json":
            if len(force_list(tags)) == 1:
                return response[tags]
            else:
                return response
        elif output == "string":
            return json.dumps(response)
        elif output == "df":
            return aggToDf(response,fields)
        elif output == "csv":
            order = ["tag","start","end","min","max","avg","var","stddev","count","numgood","numbad"]
            return csvWriter(response,self.historian,filepath,multi_csv,"GetAggregateIntervals",order,True)


    def countPoints(self, tags, start, end, output="json"):
        """
        Return the number of raw points of tags over a given time window

        Args:
            tags: A datatag, or list of datatags
            start: Start of the time range. Accepts epoch milliseconds, python datetime objects, or strings of format dd-mm-YYYYTHH:MM:DD
            end: End of the time range. Accepts epoch milliseconds, python datetime objects, or strings of format dd-mm-YYYYTHH:MM:DD
            output (Optional): The format in which to return the data. Accepts one of: "raw" - The raw json returned by the API, "json" - A processed version of the json response, "df" - A formatted pandas dataframe object. Defaults to "json".

        Returns:
            The number of raw datapoints in the interval, per tag.

        Raises:
            ValueError: When invalid Output Type is given
            URLError: When no Ingenuity instance could be found at given EigenServer, or no internet connection is available
            RemoteServerException: When the provided historian could not be found, or the API response contains an error
            RunTimeError/HTTPError: No response from the API
        """
        validOutputTypes = ["raw", "json", "df", "csv", "string"]
        if output not in validOutputTypes:
            raise ValueError("output must be one of %r." % validOutputTypes)
        ret = {}
        aggs = self.getAggregates(force_list(tags), start, end, "COUNT", 1, "raw")
        for tag in aggs.keys():
            ret[tag] = aggs[tag][0]["count"]

        response = self._matchArgumentCardinality(tags, ret)

        if output == "raw" or output == "json":
            return response
        elif output == "string":
            return json.dumps(response)
        elif output == "df":
            df = jsonToDf({"No. of Points": response})
            return df
        return None


    def _writeDataPoints(self, data) -> bool:
        rawdata = {}
        for tag in list(data.keys()):
            rawdps = []
            for dp in force_list(data[tag]):
                rawdps.append([int(dp.getTimestamp() * 1000), dp.getValue(), dp.getStatus()])
            rawdata[tag] = rawdps

        return self._doJsonRequest("write", {'write': json.dumps(rawdata)})

    def createDataTag(self, tag:str, units:str, description:str) -> bool:
        """
        Create a new tag, or update the metadata of an existing tag

        Args:
            tag: The unique identifier of the tag
            units: The unit of the values stored in the tag
            description: A short explanation of the tags purpose or content

        Returns:
            A boolean representing the success of the creation. True means tag was created, False means the operation failed.
        """
        args = {}
        args['tag'] = tag
        args['units'] = units
        args['description'] = description
        return self._doJsonRequest("create", args)

    def _doJsonRequest(self, cmd, params):
        # self._testConnection()
        url = self.serverurl + "?cmd=" + urlquote(cmd)
        return _do_eigen_json_request(url, self.auth, **params)

    def _matchArgumentCardinality(self, proto, ret):
        """Takes in ret (a dict) and proto. If proto is a list, it returns
        ret. If proto is a single value, it extracts that key from ret and
        returns that instead.
        The intention is that:
            getTagThing("myTag") returns Thing for myTag
            getTagThing(["myTag", "myOtherTag"]) returns {'myTag': Thing, 'myOtherTag': OtherThing}
        and for clarification:
            getTagThing(["myTag"]) returns {'myTag': Thing}
        """
        try:
            badTags = []
            if is_list(proto):
                if ret != {}:
                    if len(ret) < len(proto):
                        for i in proto:
                            if i not in ret:
                                badTags.append(i)
                    return ret
                else:
                    raise KeyError
            return ret[proto]
        except KeyError:
            raise KeyError("Could not find tag(s): " + str(proto))
        
    def writePoints(self, tag:str, points:list) -> bool:
        """
        Writes point data to a single existing tag.

        Args:
            tag: Id of tag to write to
            points: The points to add to the tag (takes form [{value: ... , timestamp: ... , status: ...}, { ... }, ... ])

        Returns:
            Success: A boolean representing the successful push of data.
        """
        points = force_list(points)

        datapoints = {tag : []}
        for point in points:
            if type(point["timestamp"]) is datetime:
                point["timestamp"] = point["timestamp"].timestamp()
            datapoints[tag].append(DataPoint(point["value"],point["timestamp"],point["status"]))

        return self._writeDataPoints(datapoints)
    
    
    def batchCSVImport(self, filepaths: Union[str,list]) -> bool:
        """
        Writes tag data from one or more csv file to Ingenuity. Will create a tag if it does not exist.

        Args:
            filepaths: The paths to one or more csv files. CSV Layouts must be as follows, with one point per line: tag,value,timestamp,status,units,description

        Returns:
            Success: A boolean representing the successful push of data. True means all csvs were successfully imported, False means at least one csv failed.
        """
        success = []
        for filepath in force_list(filepaths):
            with open(filepath, "r") as file:
                csv_reader = csv.reader(file, delimiter=',')
                data = list(csv_reader)
                # Upload in batches of 500 to avoid API timeouts/throttling
                chunks = divide_chunks(data, 500)
                for chunk in chunks:
                    datapoints = {}
                    for item in chunk:

                        self.createDataTag(item[0], item[4], item[5])
                        try:
                            datapoints[item[0]].append(DataPoint(item[1], int(item[2]), item[3]))
                        except KeyError:
                            datapoints[item[0]] = [DataPoint(item[1], int(item[2]), item[3])]
                    success.append(self._writeDataPoints(datapoints))
            file.close()
        return all(success)


    def batchJsonImport(self, data:Union[dict,list]) -> bool:
        """
        Writes datapoints from dict objects to tags in the Ingenuity historian.

        Args:
            data: a dict (or list of dicts) with format {"tag1": [{value,timestamp,status},{value,..},...], "tag2": {{value,..},...],...}

        Returns:
            A boolean indicating whether the push of data was successful. True means all data was successfully pushed, False means at least one batch failed to push.
        """
        success = []
        data = force_list(data)
        for datum in data:
            datapoints = {}
            totalPoints = 0
            tags = datum.keys()
            for tag in tags:
                # Upload in batches of 500 to avoid API timeouts/throttling
                if totalPoints >= 500:
                    self._writeDataPoints(datapoints)
                    datapoints = {}
                    totalPoints = 0

                for item in datum[tag]:
                    try:
                        datapoints[tag].append(DataPoint(item["value"],item["timestamp"],item["status"]))
                    except:
                        datapoints[tag] = [DataPoint(item["value"], item["timestamp"], item["status"])]
                totalPoints += len(datapoints[tag])

            success.append(self._writeDataPoints(datapoints))
        return all(success)


class DataPoint(object): # LEGACY OBJECT
    """This class represents a data point which has a value and a python timestamp, and optionally a status of 'OK' or 'BAD'.
       Timestamp is stored in epochseconds. The constructor will convert datetime and tuples into floating point epoch seconds.
    """

    def __init__(self, value, timestamp, status = 'OK'):
        """This constructor takes in a value, a python timestamp (epoch floating point seconds or datetime or tuple)
        and an optional status.  Status is either "OK" or "BAD" and will default to "OK"
        """

        self.value = value

        if status is None:
            self.status = "OK"
        elif status == "OK" or status == "BAD":
            self.status = status
        else:
            raise EigenException("Unrecognised Status")

        # Convert timestamp from python datetime or tuple into python floating point epoch seconds
        self.datetime = datetime.fromtimestamp(time_to_epoch_millis(timestamp)/1000)
        self.timestamp = pythonTimeToFloatingSecs(time_to_epoch_millis(timestamp)/1000)


    def __str__(self):
        """Return a nicely formatted version of the datapoint"""
        val = self.value
        if type(val) != str:
            val = str(number_to_string(val))
        else:
            val = val.ljust(12)
        return val + " @ " + get_timestamp_string(self.timestamp) + " - " + self.status

    def __repr__(self):
        return "DataPoint[" + str(self) + "]"

    def getValue(self):
        """Return the value of the datapoint"""
        return self.value

    def getTimestamp(self):
        """Return the timestamp of the datapoint in python floating point epoch seconds"""
        return self.timestamp

    def getTimestampMillis(self):
        """Return the timestamp of the datapoint in epochmillis"""
        return pythonTimeToServerTime(self.timestamp)

    def getTimestampAsDatetime(self):
        """Return the timestamp of the datapoint as Datetime"""
        return get_datetime(self.timestamp)

    def getTimestampAsTuple(self):
        """Return the timestamp of the datapoint as Tuple"""
        return get_time_tuple(self.timestamp)

    def getStatus(self):
        """Return the status of the datapoint - either 'OK' or 'BAD'"""
        return self.status

    def isBad(self):
        """Returns either True if status = "BAD" or false if status = "OK" """
        return self.status != "OK"

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def getAsJson(self):
        """Return as a json map with the timestamp in milliseconds"""
        return "{" + "\"value\":" + str(self.value) + ",\"timestamp\":" + self.getTimestampMillis(
            self) + ",\"status\":\"" + self.status + "\"}"


def get_datapoint(dp):
    tag = dp["tag"]
    value = dp["value"]
    timestamp = dp["timestamp"]
    timestampinmillis = dp["timestamp"]
    timestamp = serverTimeToPythonTime(timestampinmillis)
    status = dp["status"]
    return DataPoint(tag, value, timestamp, status)


def get_historian(instance: str = None, eigenserver: EigenServer = None) -> JsonBridgeHistorian:
    """Instantiate a historian object for the given instance.

    Args:
        instance (Optional): The name of the historian to connect to. Defaults to the default historian of the EigenServer.
        eigenserver (Optional): An EigenServer Object linked to the ingenuity url containing the historian. Can be omitted if environmental variable "EIGENSERVER" exists and is equal to the Ingenuity base url

    Returns:
        An Object that can be used to query historian data.

    """
    if eigenserver is None:
        eigenserver = get_default_server()
    elif type(eigenserver) == str:
        eigenserver = EigenServer(eigenserver)

    if instance is not None and (instance.startswith("http:") or instance.startswith("https:")):
        return JsonBridgeHistorian(instance)

    if instance is None:
        instance = get_default_historian_name(eigenserver=eigenserver)
        if instance is None:
            raise EigenException("No default historian instance found")
    return JsonBridgeHistorian(eigenserver.getEigenServerUrl() + "historian-servlet" + "/jsonbridge/" + instance, eigenserver.auth)


def list_historians(eigenserver=None) -> list:
    """List all historian instances in EigenServer.

    Args:
        eigenserver (Optional): An EigenServer Object linked to the ingenuity url containing the historian. Can be omitted if environmental variable "EIGENSERVER" exists and is equal to the Ingenuity base url

    Returns:
        A list of all historians on the server
    """
    if eigenserver is None:
        eigenserver = get_default_server()

    return eigenserver._listDataSources_legacy("historian")


def get_default_historian_name(eigenserver=None) -> str:
    """Get the default historian of an EigenServer.

    Args:
        eigenserver (Optional): An EigenServer Object linked to the ingenuity url containing the historian. Can be omitted if environmental variable "EIGENSERVER" exists and is equal to the Ingenuity base url

    Returns:
        The name of the default historian
    """
    if eigenserver is None:
        eigenserver = get_default_server()

    return eigenserver.getDefaultDataSource("historian")

def createPoint(value:Union[str,int,float],timestamp:int,status:str):
    return {"value": value, "timestamp": timestamp, "status": status}
