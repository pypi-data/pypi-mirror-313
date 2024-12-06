CONTENTS <!-- omit in toc --> 
============
- [About](#about)
- [Eigen Ingenuity](#eigen-ingenuity)
  - [Installation](#installation)
  - [Getting Started](#getting-started)
  - [Historian Multi](#historian-multi)
      - [Data Format](#data-format)
      - [Query Multiple Tags](#query-multiple-tags)
  - [Functions](#functions)
    - [General Functions:](#general-functions)
      - [List Historians](#list-historians)
    - [Read Functions](#read-functions)
      - [Get Current Data Points](#get-current-data-points)
      - [Get Interpolated Points in a Time Range](#get-interpolated-points-in-a-time-range)
      - [Get Values at Given Times](#get-values-at-given-times)
      - [Get Raw Points in a Time Range](#get-raw-points-in-a-time-range)
      - [Get Closest Raw Point](#get-closest-raw-point)
      - [List Data Tags Matching Wildcard](#list-data-tags-matching-wildcard)
      - [Get Tag Metadata](#get-tag-metadata)
    - [Write Functions](#write-functions)
      - [Write Data Points to Single Tag](#write-data-points-to-single-tag)
      - [Write Data Points to Multiple Tags](#write-data-points-to-multiple-tags)
- [Historian (Legacy)](#historian-legacy)
    - [Functions (Legacy)](#functions-legacy)
    - [General Functions (Legacy):](#general-functions-legacy)
      - [List Historians (Legacy)](#list-historians-legacy)
      - [Get Default Historian (Legacy)](#get-default-historian-legacy)
    - [Read Functions (Legacy)](#read-functions-legacy)
      - [List Data Tags Matching Wildcard (Legacy)](#list-data-tags-matching-wildcard-legacy)
      - [Get Tag Metadata (Legacy)](#get-tag-metadata-legacy)
      - [Get Aggregates for a Time Range (Legacy)](#get-aggregates-for-a-time-range-legacy)
      - [Get Aggregates on Intervals over a Time Range (Legacy)](#get-aggregates-on-intervals-over-a-time-range-legacy)
      - [Get Number of Points (Legacy)](#get-number-of-points-legacy)
    - [Write Functions (Legacy)](#write-functions-legacy)
      - [Create Or Update Data Tag (Legacy)](#create-or-update-data-tag-legacy)
      - [Write Points to Single Tag (Legacy)](#write-points-to-single-tag-legacy)
      - [Write Points to Multiple Tags (Legacy)](#write-points-to-multiple-tags-legacy)
  - [Asset Model](#asset-model)
      - [Execute a Raw Cypher Query](#execute-a-raw-cypher-query)
- [Asset Model Builder](#asset-model-builder)
  - [Running the tool](#running-the-tool)
  - [Command Line options](#command-line-options)
  - [The Config File](#the-config-file)
  - [Project structure](#project-structure)
- [Coming soon](#coming-soon)
- [Planned](#planned)
- [License](#license)

# About<a id="about"></a>

This library supports python 3.10 onwards. It may work for earlier versions of python3, but these are not supported. We do not support python 2 in any form.

The python-eigen-ingenuity library contains 2 modules:

# Note <!-- omit in toc -->
This version of the library includes a CLI tool for building assetmodels on Eigen Systems (See [ModelBuilder Section](#asset-model-builder)). On some secured machines this cli tool may cause the library to fail to install, or raise an error.

if this occurs, install the version without the CLI tool [here](https://pypi.org/project/python-eigen-ingenuity-nocli/)

### 1. Eigen Ingenuity <!-- omit in toc --> 
This module is used to query data from many of the databases in the Ingenuity Platform, including:
- timeseries historians (influx, PI, IP21, cognite)
- A Neo4j Graph database
- Sql sources (Oracle, msql, psql)
- Elasticsearch

The data can be returned in several formats, and supports multiple query types

### 2. Model Builder <!-- omit in toc --> 
We provide a portable CLI tool that can be used to build a model onto a neo4j instance from a list of csv files that define a set of nodes/properties and their relationships.

It can be used either to create a model from scratch (Though it does require an existing blank neo4j container/machine), or it can be directed to an existing neo4j to perform a merge/update.

It includes options for version nodes to track history and changes to nodes when a model is updated.

---

# Eigen Ingenuity<a id="eigen-ingenuity"></a>

## Installation<a id="installation"></a>


Install python (3.10+), then in the terminal run:

```
pip install python-eigen-ingenuity
```

All required Third party libraries will be automatically installed.

## Getting Started<a id="getting-started"></a>

Begin by Importing the module at the top of a script with

```
import eigeningenuity as eigen
```

To use this module, you must first set an Ingenuity server to query, and a datasource within the server.

For example, for a historian with Ingenuity instance "https://demo.eigen.co/" and datasource "Demo-influxdb",


```
server = eigen.EigenServer("https://demo.eigen.co/")
demo = eigen.get_historian("Demo-influxdb",server) (or demo = eigen.get_historian_multi(eigenserver=server))
```
Alternatively, it is possible to set the Ingenuity instance as the environmental variable "EIGENSERVER",
```
os.environ["EIGENSERVER"] = "https://demo.eigen.co/"
demo = get_historian("Demo-influxdb") (or demo = eigen.get_historian_multi())
```


With the datasource set, the historian data can be queried with the functions detailed in the below section,

## Historian Multi<a id="historian"></a>


#### Data Format<a id="data-format"></a>

The historian multi method, as the name implies allows querying from multiple historians in a single request, however a default historian can be configured, which will allow the user to pass tag names without historian, which will be assumed to belong to the default

```
from eigeningenuity import EigenServer, get_historian_multi

ei = EigenServer("demo.eigen.co")
datasource = get_historian_multi(default_historian="Demo-influxdb", eigenserver=ei)
```


Once the server and datasource have been configured, the historian data can be queried through functions we define in
the EXAMPLE FUNCTIONS section.

These functions can be used to query a single tag, or multiple tags at once. A tag in ingenuity with the form "datasource/tagname", 
we query with, for example:

```
datasource = eigen.get_historian("datasource")
tagdata = datasource.getCurrentDataPoints("tagname")
```

Functions have multiple options on how to return the data, that can be specified using the "output" parameter:

- The Raw Response. (output="raw")
- A preformatted python dict (default: output="json")
- a pandas dataframe (default: output="df")

##### Example <!-- omit in toc --> 

For a query like

```
x = datasource.getInterpolatedRange("DEMO_02TI301.PV","1 hour ago","now",3)
```
- ##### Raw:

  ```
  {'items': {'DEMO_02TI301.PV': [{'value': 38.0, 'timestamp': 1701166741139, 'status': 'OK'}, {'value': 37.5, 'timestamp': 1701168541139, 'status': 'OK'}, {'value': 38.0, 'timestamp': 1701170341139, 'status': 'OK'}]}, 'unknown': []}
  ```
- ##### Json

  ```
  [{'value': 35.88444444444445, 'timestamp': 1701166983980, 'status': 'OK'}, {'value': 33.5, 'timestamp': 1701168783980, 'status': 'OK'}, {'value': 34.0, 'timestamp': 1701170583980, 'status': 'OK'}]
  ```
- ##### Dataframe
  ```
  ---
                          DEMO_02TI301.PV
  2023-11-28 11:23:39.201             38.0
  2023-11-28 10:53:39.201             36.0
  2023-11-28 10:23:39.201             33.0
  ```



  
#### Query Multiple Tags<a id="query-multiple-tags"></a>


if multiple tags are queried in a single request, the data will be returned as a dictionary, with the tag IDs as its keys.
The individual dictionary entries will retain the same format returned when querying a single tag
____

## Functions<a id="functions"></a>

### General Functions:<a id="general-functions"></a>

Simple Functions to check server defaults

#### List Historians<a id="list-historians"></a>
###### Method: list_historians <!-- omit in toc --> 

Find all historians on the instance
```
from eigeningenuity import EigenServer, list_historians

eigenserver = EigenServer("demo.eigen.co")
list_historians(eigenserver)
```
Where:
- (Optional) eigenserver is the ingenuity instance of interest (If omitted will look for environmental variable EIGENSERVER)

Returns a list of strings

Where:
- (Optional) eigenserver is the ingenuity instance of interest (If omitted will look for environmental variable EIGENSERVER)

Returns a string, or None

### Read Functions<a id="read-functions"></a>

##### The following functions are designed to help the user pull and process data from historians into a python environment <!-- omit in toc --> 

#### Get Current Data Points<a id="get-current-data-points"></a>
###### Method: getCurrentDataPoints <!-- omit in toc --> 

Find the most recent raw datapoint for each tag
```
demo.getCurrentDataPoints(tags,output)
```
Where:
- tags is a list of IDs of tags to query
- output (optional) [See DATA FORMAT section](#data-format)
  - multi-csv (optional) [See DATA FORMAT section](#data-format)
  - filepath (optional) [See DATA FORMAT section](#data-format)

Returns one datapoint object per tag


#### Get Interpolated Points in a Time Range<a id="get-interpolated-points-in-a-time-range"></a>
###### Method: getInterpolatedRange <!-- omit in toc --> 

Find a number of interpolated points of a tag, equally spaced over a set timeframe
```
demo.getInterpolatedRange(tag, start, end, count, output)
```
Where:
- tags is a list of IDs of the tags to query
- start is the datetime object (or epoch timestamp in ms) of the beginning of the query window
- end is the datetime object (or epoch timestamp in ms) of the end of the query window
- count is the total number of points to be returned
- output (optional) [See DATA FORMAT section](#data-format)

  
Returns a list of count-many datapoints per tag

#### Get Values at Given Times<a id="get-values-at-given-times"></a>
###### Method: getInterpolatedpoints <!-- omit in toc --> 

Find datapoints at given timestamps
```
demo.getInterpolatedPoints(tags, timestamps, output)
```
Where:
- tags is a list of IDs of the tags to query
- timestamps is a list of timestamps at which to query data
- output (optional) [See DATA FORMAT section](#data-format)


Returns a list of datapoints (one at each timestamp) per tag


#### Get Raw Points in a Time Range<a id="get-raw-points-in-a-time-range"></a>
###### Method: getRawDataPoints <!-- omit in toc --> 

Find the first n Raw datapoints from a time window
```
demo.getRawDataPoints(tags, start, end, count, output)
```
Where:
- tags is a list of IDs of the tags to query
- start is the datetime object (or epoch timestamp in ms) of the beginning of the query window
- end is the datetime object (or epoch timestamp in ms) of the end of the query window
- (Optional) count is the maximum number of raw datapoints to return. (default is 1000)
- output (optional) [See DATA FORMAT section](#data-format)


Returns a list of count-many datapoints per tag

#### Get Closest Raw Point<a id="get-raw-points-in-a-time-range"></a>
###### Method: getClosestRawPoint <!-- omit in toc --> 

Find the nearest raw point before or after a provided timestamp
```
demo.getClosestRawPoint(tags, timestamps, before_or_after, output)
```
Where:
- tags is a list of IDs of the tags to query
- timestamps is a list of timestamps of accepted formats ([See DATA FORMAT section](#data-format))
- (Optional) before_or_after is the position of the raw point relative to provided timestamp. Accepts ("BEFORE","AFTER","BEFORE_OR_AT","AFTER_OR_AT"). Defaults to "AFTER_OR_AT"
- output (optional) ([See DATA FORMAT section](#data-format))


Returns a list of count-many datapoints per tag

#### List Data Tags Matching Wildcard<a id="list-data-tags-matching-wildcard"></a>
###### Method: listDataTags <!-- omit in toc --> 

Find all tags in datasource, or all tags in datasource that match a search parameter
```
demo.listDataTags(datasource, match,limit)
```
Where:
- (optional) match is the regex wildcard to match tags to (i.e. DEMO* will match all tags beginning with DEMO, \*DEMO* will match all tags containing DEMO anywhere. Default returns every tag
- (optional) limit is the max number of tags to return. Defults to 100.
- (optional) datasource is the historian to search for the tags within. Defaults to the default configured when instantiating historian multi

Returns a list of strings

#### Get Tag Metadata<a id="get-tag-metadata"></a>
###### Method: getMetaData <!-- omit in toc --> 

Find units, unitMultiplier and description of each tag
```
demo.getMetaData(datasource, match,limit)
```

Where:
- (optional) match is the regex wildcard to match tags to (i.e. DEMO* will match all tags beginning with DEMO, \*DEMO* will match all tags containing DEMO anywhere. Default returns every tag
- (optional) limit is the max number of tags to return. Defaults to 100.
- (optional) datasource is the historian to search for the tags within. Defaults to the default configured when instantiating historian multi

Returns a list of dicts, each dict containing all metadata for a single tag

### Write Functions<a id="write-functions"></a>
The following functions are intended for users to update/create historian tags using data processed/loaded in python. They can only be run against Eigen's internal influx historians, not production systems. <!-- omit in toc -->

#### Write Data Points to Single Tag<a id="write-data-points-to-single-tag"></a>
###### Method: writePoints <!-- omit in toc --> 

Writes sets of datapoints to the historian
```
from eigeningenuity.historianmulti import createPoint

dataPoints = []
point = createPoint(value, timestamp, "OK") (or point = {"value": value, "timestamp": timestamp, "status": "OK"})

dataPointList.append(dataPoint)

demo.writePoints(tag,dataPointList)
```
Where:
- value if the value of the datapoint at the timestamp
- timestamp is the datetime object (or epoch timestamp in ms) of the point
- "OK" is the status we give to a point that contains non-null data

Returns a boolean representing success/failure to write data

#### Write Data Points to Multiple Tags<a id="write-data-points-to-multiple-tags"></a>
###### Method: writePointsBatch <!-- omit in toc --> 

Writes sets of datapoints to the historian
```
from eigeningenuity.historianmulti import createPoint

dataPoints = {}
point = createPoint(value, timestamp, "OK") (or point = {"value": value, "timestamp": timestamp, "status": "OK"})
dataPoints[tagName] = point

demo.writePoints(dataPoints)
```
Where:
- value if the value of the datapoint at the timestamp
- timestamp is the datetime object (or epoch timestamp in ms) of the point
- "OK" is the status we give to a point that contains non-null data

Returns a boolean representing success/failure to write data

# Historian (Legacy)<a id="historian-legacy"></a>
  
### Functions (Legacy)<a id="functions-legacy"></a>

### General Functions (Legacy):<a id="general-functions-legacy"></a>

Simple Functions to check server defaults

#### List Historians (Legacy)<a id="list-historians-legacy"></a>
###### Method: list_historians <!-- omit in toc --> 

Find all historians on the instance
```
from eigeningenuity import list_historians
list_historians(eigenserver)
```
Where:
- (Optional) eigenserver is the ingenuity instance of interest (If omitted will look for environmental variable EIGENSERVER)

Returns a list of strings

#### Get Default Historian (Legacy)<a id="get-default-historian-legacy"></a>
###### Method: get_default_historian_name <!-- omit in toc --> 
Find the name of the default historian of the instance, if one exists
```
from eigeningenuity import get_default_historian_name
get_default_historian_name(eigenserver)
```
Where:
- (Optional) eigenserver is the ingenuity instance of interest (If omitted will look for environmental variable EIGENSERVER)

Returns a string, or None

### Read Functions (Legacy)<a id="read-functions-legacy"></a>

##### The following functions are designed to help the user pull and process data from historians into a python environment <!-- omit in toc --> 

The legacy method has all the same methods as above with the same parameters with the exception and additions of the following

#### List Data Tags Matching Wildcard (Legacy)<a id="list-data-tags-matching-wildcard-legacy"></a>
###### Method: listDataTags <!-- omit in toc --> 

Find all tags in datasource, or all tags in datasource that match a search parameter
```
demo.listDataTags(match)
```
Where:
- (optional) match is the regex wildcard to match tags to (i.e. DEMO* will match all tags beginning with DEMO, \*DEMO* will match
all tags containing DEMO, and *DEMO will match all tags ending with DEMO) (Leave blank to return all tags in historian)

Returns a list of strings

#### Get Tag Metadata (Legacy)<a id="get-tag-metadata-legacy"></a>
###### Method: getMetaData <!-- omit in toc --> 

Find units, unitMultiplier and description of each tag
```
demo.getMetaData(tags, output)
```
Where:
- tags is a list of IDs of tags to query
- output (optional) Does Not Accept CSV. Otherwise, [See DATA FORMAT section](#data-format) 

Returns a dict with keys [units, unitMultiplier, description] per tag

#### Get Aggregates for a Time Range (Legacy)<a id="get-aggregates-for-a-time-range-legacy"></a>
###### Method: getAggregates <!-- omit in toc --> 

Finds a set of aggregate values for tags over a timeframe
```
demo.getAggregates(tags, start, end, count, aggfields, output)
```
Where:
- tags is a list of IDs of the tags to query
- start is the datetime object (or epoch timestamp in ms) of the beginning of the query window
- end is the datetime object (or epoch timestamp in ms) of the end of the query window
- (Optional) count is the number of divisions to split the time window into (i.e. if time window is one day, and count is 2, we return separate sets of aggregate data for first and second half of day). omit for count=1
- (Optional) aggfields is a list of aggregate functions to calculate, a subset of 
["min","max","avg","var","stddev","numgood","numbad"].  Leave blank to return all aggregates.
- output (optional) [See DATA FORMAT section](#data-format)
  - multi-csv (optional) [See DATA FORMAT section](#data-format)
  - filepath (optional) [See DATA FORMAT section](#data-format)
  
Returns a list of count-many Aggregate Data Sets per tag

#### Get Aggregates on Intervals over a Time Range (Legacy)<a id="get-aggregates-on-intervals-over-a-time-range-legacy"></a>
###### Method: getAggregateInterval <!-- omit in toc --> 

A variation of getAggregates which finds aggregates on fixed length intervals dividing the overall window
```
demo.getAggregateInterval(tags, start, end, interval, aggfields, output)
```
Where:
- tags is a list of IDs of the tags to query
- start is the datetime object (or epoch timestamp in ms) of the beginning of the query window
- end is the datetime object (or epoch timestamp in ms) of the end of the query window
- (Optional) interval is the length of the sub-intervals over which aggregates are calculated, it accepts values such as ["1s","1m","1h","1d","1M","1y"]
being 1 second, 1 minute, 1 hour etc. Default is whole time window.
- (Optional) aggfields is a list of aggregate functions to calculate, a subset of 
["min","max","avg","var","stddev","numgood","numbad"]. Default is all Aggregates.
- output (optional) [See DATA FORMAT section](#data-format)
  - multi-csv (optional) [See DATA FORMAT section](#data-format)
  - filepath (optional) [See DATA FORMAT section](#data-format)
  
Returns a list of Aggregate Data Sets (One per interval) per tag


#### Get Number of Points (Legacy)<a id="get-number-of-points-legacy"></a>
###### Method: countPoints <!-- omit in toc --> 

Find the number of datapoints in the given time frame
```
demo.countPoints(tag, start, end, output)
```
Where:
- tags is a list of IDs of tags to query
- start is the datetime object (or epoch timestamp in ms) of the beginning of the query window
- end is the datetime object (or epoch timestamp in ms) of the end of the query window
- output (optional) [See DATA FORMAT section](#data-format)

  
Returns one integer per tag

### Write Functions (Legacy)<a id="write-functions-legacy"></a>
The following functions are intended for users to update/create historian tags using data processed/loaded in python. They can only be run against Eigen's internal influx historians, not production systems. <!-- omit in toc --> 

#### Create Or Update Data Tag (Legacy)<a id="create-or-update-data-tag-lagacy"></a>
###### Method: createDataTag <!-- omit in toc --> 

Creates a datatag with a specified ID, Unit type/label, and Description. You can use an existing tag name to update the metadata
```
demo.createDataTag(Name, Units, Description)
```
Where:
- Name is the unique ID/Identifier of the tag
- Units is the unit specifier of the data in the tag e.g. "m/s","Days" etc. (This will be shown on axis in ingenuity trends)
- Description is text/metadata describing the content/purpose of the tag (This will show up in search bar for ingenuity trends)

Returns a boolean representing success/failure to create tag

#### Write Points to Single Tag (Legacy)<a id="write-points-to-single-tag-legacy"></a>
###### Method: writePoints <!-- omit in toc --> 

Writes sets of datapoints to the historian
```
from eigeningenuity.historian import createPoint

dataPointList = []
dataPoint = createPoint(value, timestamp, "OK") (or point = {"value": value, "timestamp": timestamp, "status": "OK"})

dataPointList.append(dataPoint)

demo.writePoints(tag,dataPointList)
```
Where:
- value if the value of the datapoint at the timestamp
- timestamp is the datetime object (or epoch timestamp in ms) of the point
- "OK" is the status we give to a point that contains non-null data

Returns a boolean representing success/failure to write data

#### Write Points to Multiple Tags (Legacy)<a id="write-data-points-to-tags-legacy"></a>
###### Method: batchJsonImport <!-- omit in toc --> 
Writes sets of datapoints to the historian
```
from eigeningenuity.historian import createPoint

dataPoints = {}
point = createPoint(value, timestamp, "OK") (or point = {"value": value, "timestamp": timestamp, "status": "OK"})
dataPoints[tagName] = point

demo.batchJsonImport(dataPoints)
```
Where:
- value if the value of the datapoint at the timestamp
- timestamp is the datetime object (or epoch timestamp in ms) of the point
- "OK" is the status we give to a point that contains non-null data

Returns a boolean representing success/failure to write data

## Asset Model<a id="asset-model"></a>

Currently the AM tools only support direct queries using cypher queries directly with the executeRawQuery method. More structured methods are planned.

#### Execute a Raw Cypher Query<a id="execute-a-raw-cypher-query"></a>
###### Method: executeRawQuery <!-- omit in toc --> 

Executes a cypher query directly against our asset model
```
from eigeningenuity import get_assetmodel, EigenServer

demo = EigenServer("demo.eigen.co")
am = get_assetmodel(demo)

wells = demo.executeRawQuery(query)
```

Where:
- query is a string containing a valid neo4j/cypher language query e.g. "Match (n:Well) return n limit 25"

Returns the json response from neo4j

---------------------------------------------------------------------------------------------------------------------------------------

# Asset Model Builder<a id="asset-model-builder"></a>

A tool for updating a Neo4j model using .csv anf .cypher files as input

## Running the tool<a id="running-the-tool"></a>

The tool is invoked by executing, anywhere on the cli

```
assetmodel
```

## Command Line options<a id="command-line-options"></a>

*-p* - sets the default path for input files. The program will look first in the current folder, and then in the default folder if it's not find locally.
Output files are always created in the default folder

*-dr* - Set the frequency of progress update messages. No effect if -v present
*-sf* - The first query to process in a .csv file. No effect on cypher files. Default is 1

*-d* - specifies the target database, as defined in the config file. Can specify the DB name (as defined in config.ini), or a position in the list 
e.g. -d 0 will connect to the first database defined

*-c* - the name of the config file if not config.ini, or it's not in the default folder

*-s* - the separator used in the .csv files. Default is ";"

*-v* - run in verification mode. Queries are generated and displayed on screen, but are not processed

*-sq* - show queries on screen as they are processed. Has no effect if *-v* present

*-sr* - causes data from RETURN clauses to be displayed on screen.  No effect if *-v* present

*-wq* - causes the processed queries to be writen to the specified file. This is very useful to review all the queries that have been executed.
It includes all the queries used to create and update Version nodes too. No effect if *-v* present

*-wr* - causes data from RETURN clauses to be writen to the specified file.  No effect if *-v* present

*-f* - list of input files. Can be a mix of .csv and .cypher files. Also supports .lst files, which are a simple text file
containing a list of files to process (can also include more .lst files). See *-o* for information on the order the files are processed in

*-q* - list of Cypher queries explicitly entered on the command line. These are processed before any files specified with *-f*, unless the
default order is overriden by the *-o* switch

*-pre* - list of Cypher queries explicitly entered on the command line. These are processed first, before anything else

*-da*  - delete all nodes with the specified labels. More than one set of labels can be specified. The delete is performed AFTER any *-pre* queries. Using *-da* with no labels will delete all nodes, so use with caution! 
Examples:  
* *-da :Person :EI_VERSION:Pump* deletes all nodes with a Person label, and then all nodes with both EI_VERSION and Pump labels. Note: the leading ':' is optional so *-da Person* will also delete all *Person* nodes
* *-da* (with no labels) deletes ALL nodes - be careful!  

*-post* - list of Cypher queries explicitly entered on the command line. These are processed last, after everything else

*-o* - defines the order the file types are processed in. Accepts up to 5 chars: 'n' for node csv files, 'r' for relationship csv files, 
'c' for cypher files, 'q' for command line queries and 'x' for any unspecified file type, processed in the order given.  The default is qnrc. 
Examples:  
* *-o x* processes all the inputs in the order listed  
* *-o c* will process all .cypher files first (in the order listed), then others *in the default order*. This is the same as *-o cqnr*  
* *-o cx* will process all .cypher files first, then others *in the order listed*  
* *-o nxr* processes nodes, then cypher files and command line queries in the order listed, and finally relationship files  

*-nov*  - suppresses the creation and update of version nodes

*-in*  - treat node columns in a relationship csv file as properties of the relationship. This allow a 
relationship to have a property that is the same as that used to identify a node. Without using this
qualifier, the system will report an 'Ambiguous data' error because it cannot determine if the csv file 
is intended to be a node file or a relationship file.

*-sd* - prevents the creation of a version node if none of the node properties or labels will be changed by the update

*-ab* - Update a property even if it is blank

*-b* - group queries into batches of the given size. Note: creation of version nodes is disabled in batch mode i.e. *-nov* is in effect

### Examples <!-- omit in toc --> 
```
assetmodelbuilder -p models/Testing -d neo4j-test -f People.csv "Extended.cypher" -v  
```

Looks in a folder models/Testing for the file People.csv and config.ini. It uses this csv file to generate queries that it simulates executing against the server configured with name neo4j-test in config.ini. However the database is not written to due to -v flag.

```
assetmodelbuilder -p models/Testing -d neo4j-test -q "MATCH (n) RETURN n" -sr  
```

Looks in a folder models/Testing for the file config.ini. Then executes cypher command "MATCH (n) RETURN n" against the server configured with name neo4j-test in config.ini and returns the neo4j response to the console due to -sr flag

```
python src/assetmodelbuilder.py -p models/Testing -d 1 -f Rebuild.lst Versions.csv RelationVersions.csv -o x  
```

Deletes all the nodes and recreate them, with Version nodes and updated Relationships.

## The Config File<a id="the-config-file"></a>

This file contains key information about the structure of the Asset Model. The layout is

**[DEFAULT]**
  
  

**[Database]**  
#Define the database connections here. The name is used by the program to identify the db to connect to  
DatabaseNames=Database0 Name,Database1 Name  
URLs=Database0 URL,Database1 URL  
passwords=Database0 password,Database1 password  

**[Model]**  

#The **PrimaryIDProperty** is the property that is used to uniquely identify it. It is created and managed  
#by the model builder. The default value is **uuid**  
**PrimaryIDProperty=uuid**  

#The **PrimaryProperty** is the default property to use to match on when creating relationships  
#This can be overriden by specifying the required property in the csv files  
**PrimaryProperty=node**  
  
#Specify any labels that are required by ALL nodes. This is a shortcut so that are not needed in the .csv file  
#Labels defined in the .csv file can be REMOVED by listing them here with a leading !  
#In this example, any nodes with a Person label will have that removed, and all nodes will get a People label  
**RequiredLabels= !Person , People**  
  
#Similar to labels, list any properties that a node must have together with a default value. If a value is provided  
#in the input file, that value is used rather than the default value here  
#Also like labels, properties can be removed by using the ! prefix (no need to give a default)  
#In this example, everyone will have a Nationality property equal to British, apart from those whose Nationality is in the input  
#Everyone will have their Weight property removed. Phew!  
**RequiredProperties=Nationality=British , !Weight**  

#All nodes are timestamped when they are created or updated. Specify the name of the node property to be used  
#for these using **CreationTime** and **UpdateTime**  
**CreationTime=CreationTime**  
**UpdateTime=UpdatedTime**  

#Sometimes there are columns in the .csv files that have the wrong name. These can be changed using a mapping  
#in the format of old_name=new_name. The new_name can then be used in the **[Alias]** section (see below)  
#In the example, the .csv files use as mix of _Node_ and _node_ for the name of the node. Both of these are mapped to  
#_name_, so that all the nodes in the model have a _name_ property. _name_ can then be used to create relationships, for example.
**Mappings=node=name,Node=name**  

#To set a default data use, use DataType=. The given format will be used, unless a format is specified in the CSV header. For example, to treat
data as strings use **DataType=str**

**[Aliases]**  
#The Alias section defines how to map column headings onto meaning in the tool  
#Nodes and Labels are used to define nodes in a 'Properties' type file  
**Labels=Label, Code**  
**Nodes=Node**  
#FromNodes, ToNodes and Relationships are used to create relationships, in the obvious way  
**FromNodes=From, Start Node, Start, From Node, StartNode,Start Node**  
**ToNodes=To,To Node,ToNode,End**  
#FromLabels and ToLables are added to the From and To nodes in the obvious way to speed up Relationship matches  
**FromLabels=**  
**ToLables=**  
**Relationships=Relation,Relationship**  

**[Versions]**


**Versions=**  
**FrozenLabels=Person**  
**VersionLabels=!Current,Version**  
**VersionPrefix=Version**  
**VersionCounterProperty=VersionCount**  
**VersionNumberProperty=VersionNumber**  
**FirstVersionProperty=FirstVersion**  
**LastVersionProperty=LastVersion**  
**VersionRelationship=HasVersion**  
**NextVersionRelationship=NextVersion**  
**VersionValidFromProperty=ValidFrom**  
**VersionValidToProperty=ValidTo**  

Leading and training spaces are ignored in all the entries in the file so feel free to add spaces to improve readability.  
For example, the provided aliases for FromNode are "From", "Start Node", "Start", "From Node", "StartNode" and "Start Node"  
Note: you can see "Start Node" is in the list twice - this is not a problem  
The program will treat any column in the csv file with any of those headings as FromNode

### Example Config File <!-- omit in toc --> 

```
[DEFAULT]


[Database]
DatabaseNames=lunappi,lunappd,local
URLs=https://demo.eigen.co/ei-applet/neo4j/query,https://demo.eigen.co/ei-applet/neo4j/query,bolt://localhost:7687
users=,,neo4j
passwords=,,neo4j4neo

[Model]
PrimaryProperty=name
RequiredLabels=MoviesDB
RequiredProperties=
PrimaryIDProperty=uuid
CreationTime=creationDate
UpdateTime=updatedDate
Mappings=

[Aliases]
Labels=
Nodes=name
FromNodes=
FromLabels=
ToNodes=
ToLabels=
Relationships=

[Versions]
Versions=
FrozenLabels=
VersionLabels=Version,!Current
VersionLabelPrefix=Version
VersionCounterProperty=versionCount
VersionNumberProperty=versionNumber
FirstVersionProperty=firstVersion
LastVersionProperty=lastVersion
VersionRelationship=has_version
NextVersionRelationship=next_version
VersionValidFromProperty=validFrom
VersionValidToProperty=validTo
```

## Project structure<a id="project-structure"></a>

```shell
assetmodelbuilder/
├── README.md  # Project general information
├── src/  # All source code
│   ├── connectors              # Folder for the database connector code
│   │    ├── boltconnector.py       # Connection for the Bolt protocol (i.e. neo4j) 
│   │    ├── dbconnectors.py        # Connector manager
│   │    ├── genericconnector.py    # Super class for all connectors
│   │    └── httpsconnector.py      # Connector for https protocol
│   ├── queries                 # Folder to build and manager Cypher queries
│   │    ├── cypherbuilder.py       # Main class to build a query. Modified version of Cymple
│   │    ├── query.py               # A custom Neo4jQuery class
│   │    └── typedefs.py            # Defines the 'properties' type used by Cymple
│   ├── assetmodelbuilder.py    # Main program
│   ├── assetmodelutilities.py  # Miscellaneous utility functions
│   ├── configmanager.py        # Reads the config.ini file and manages the model configuration
│   ├── csvcontentsmanager.py   # Reads a csv file and provides the format and content
│   ├── filemanager.py          # Works out the file format of each input file and arranges them in process order
│   ├── fileprocessors.py       # Processors for each type of input file
│   ├── messages.py             # Formats and displays all messages to the user
│   └── versionmanager.py       # Create a new version of a node when it is updated
└── models/  # Tests
    ├── default
    │   └── config.ini          # Contains default model parameters if not present in the model folder
    └── Testing                 # Test data files, such as input/output files, mocks, etc.
        ├── config.ini          # Model parameters for the Test model
        ├── DeleteAll.cypher    # Cypher to delete all the Family nodes
        ├── People.csv          # File containing some data defining People nodes
        ├── Relations.csv       # And some relationships between them
        ├── Extended Family.cypher  # Some Cypher queries creating extended family members and relations
        ├── Versions.csv        # File with some updates to nodes to test Versioning
        ├── RelationVersions.csv    # File with some updates to Relations to test Versioning
        └── Rebuild.lst         # File listing all the input files. Use with -o x to process in the listed order
        
```

# Coming soon<a id="coming-soon"></a>
### Eigen Ingenuity <!-- omit in toc --> 
- Improvements to Azure Authentication functionality, and client integration
- Implementation of CSV output for Historian Multi
- Implementation of GetAggregates for Historian Multi


### Asset Model Builder <!-- omit in toc --> 
- Options for special processing. For example, an option to over-write existing nodes, rather than just update them  

# Planned<a id="planned"></a>

### Eigen Ingenuity <!-- omit in toc --> 
- Integration with 365 Events and Power Automate
- Sphynx/Jupyter notebook with worked examples for all functionality

### Asset Model Builder <!-- omit in toc --> 
- Options for special processing. For example, an option to over-write existing nodes, rather than just update them 
- Options to remove nodes, relations and/or properties and labels from them  

# License<a id="license"></a>
Apache License 2.0

 Copyright 2022 Eigen Ltd.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.