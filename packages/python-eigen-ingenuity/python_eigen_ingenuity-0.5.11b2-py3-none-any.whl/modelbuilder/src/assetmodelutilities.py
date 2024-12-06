from pathlib import Path
import datetime
from datetime import timezone
import re

# Define special types that are used by the Neo4j importer
# They are also used in Java asset model builder
# Could add these to the config file at some point, but they are unlikely to change
node_types = ['ID']
from_types = ['START_ID']
to_types = ['END_ID']
relation_types = ['TYPE']
label_types = ['LABEL', 'ALABEL']
all_types = node_types + from_types + to_types + relation_types + label_types


def find_file(path, filename):
    # try the provided path file first, then with the current path. Otherwise, return None to indicate file not found
    if Path(path + filename).is_file():
        full_name = path + filename
    elif Path(filename).is_file():
        full_name = filename
    else:
        full_name = None
    return full_name

def get_formatted_time_now():
    now = datetime.datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    return now

def get_formatted_time_now_noms():
    now = datetime.datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")
    return now

def get_formatted_future_time():
    future = datetime.datetime(2199, 12, 31).strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    return future

def get_time_for_filename():
    now = datetime.datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H-%M-%S-%f")[0:-3]
    return now

def validate(input, prefix = ''):
    output = f'{prefix}{input}'
    if input:
        if input.startswith('`!'):
            output = f'{prefix}{input}`'
        elif ''.join(re.findall("[A-Za-z0-9_]", input)) != input or ''.join(re.findall("[A-Za-z]", input[0])) != input[0]:
            output = f'{prefix}`{input.replace("`","``")}`'

    return output
