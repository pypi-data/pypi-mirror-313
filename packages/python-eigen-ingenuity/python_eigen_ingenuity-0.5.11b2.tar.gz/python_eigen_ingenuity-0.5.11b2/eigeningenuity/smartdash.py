"""Eigen Ingenuity - Smart Dash

This package deals with the Eigen Ingenuity Smart Dash API.

To get a smart object to work with, use get_historian(xxx) with either
an instance name (which will be resolved via the the usual methods in
eigeningenuity.core) or a full URL to a JSON Bridge Historian instance.

  from eigeningenuity.smartdash import get_smartdash

  sd = get_smartdash()
  sd.addItem("foobar", "HistorianTagTotaliser", "pi-af/testsim00001", "year")
  vals = sd.getValues()

  print vals['foobar']

 """

from __future__ import (absolute_import, division, print_function, unicode_literals)

import requests

from eigeningenuity.core import get_default_server, EigenServer
from eigeningenuity.util import _do_eigen_json_request, force_list, time_to_epoch_millis, is_list, get_datetime, number_to_string, EigenException, get_timestamp_string, pythonTimeToFloatingSecs, serverTimeToPythonTime, pythonTimeToServerTime, get_time_tuple
from urllib.parse import quote_plus as urlquote_plus



class SmartDashSet (object):
    def __init__(self, baseurl, auth):
        self.__items = {}
        self.__key = None
        self.__baseurl = baseurl
        self.__itemcount = 0
        self.auth = auth

    def addAutoItem(self, itype, *args):
        self.__itemcount += 1
        id = "item%04d" % self.__itemcount
        self.addItem(id, itype, *args)

        return id
        
    def clear(self):
        self.__key = None
        self.__items = {}
        
    def removeItem(self, kname):
        self.__key = None
        del self.__items[kname]

    def addItem(self, kname, itype, *args):
        self.__key = None
        encodedargs = []
        for i in ((itype,) + args):
            encodedargs.append(urlquote_plus(str(i)))

        itemSpec = ":".join(encodedargs)
        self.__items[urlquote_plus(kname)] = itemSpec

    def getKey(self):
        if self.__key is None:
            self.getValues()
        return self.__key

    def getValues(self):
        res = None

        if self.__key is not None:
            try:
                res = _do_eigen_json_request(self.__baseurl, self.auth, key = self.__key)
            except EigenException:
                res = None

        if res is None:
            items = []
            for k,spec in self.__items.items():
                items.append(k + "=" + spec)

            res = _do_eigen_json_request(self.__baseurl, self.auth, item = items)

        self.__key = res['key']
        return res['data']

def get_smartdash(eigenserver = None):
    if eigenserver is None:
        eigenserver = get_default_server()
    elif type(eigenserver) == str:
        eigenserver = EigenServer(eigenserver)

    url = eigenserver.getEigenServerUrl() + "smartdash-servlet"

    x = requests.get(url, verify=False).status_code

    if x != 200:
        url = eigenserver.getAppUrl("dashboards-applet")

    if url is None:
        raise EigenException("No smartdash found")

    return SmartDashSet(url + "/smartdash", eigenserver.auth)


