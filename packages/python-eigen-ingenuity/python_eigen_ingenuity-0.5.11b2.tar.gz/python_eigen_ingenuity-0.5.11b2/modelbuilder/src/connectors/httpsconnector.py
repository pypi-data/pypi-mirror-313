from connectors.genericconnector import GenericConnector
import eigeningenuity.settings as settings
import eigeningenuity.auth as auth
import requests
from time import sleep
from queries.query import QueryResult
from messages import *
import assetmodelutilities


class HTTPSConnector(GenericConnector):

    def __init__(self, db_connection_details, config_manager, output_file, results_file):
        super().__init__(db_connection_details, output_file, results_file)
        self.url = db_connection_details['url']
        self.config_manager = config_manager

    def close(self):
        super().close()

    def convert_result(self, this_result, code=-1):
        converted_result = QueryResult(False)
        try:
            converted_result.set_status(this_result.status_code)
        except:
            converted_result.set_status(code)

        json_result = None
        try:
            json_result = this_result.json()
        except:
            converted_result.set_response(None)

        if json_result:
            try:
                converted_result.set_response(json_result['data'])
                try:
                    update_dict = {}
                    result = json_result['summary']
                    converted_result.set_updates_made(result['containsUpdates'])
                    update_dict['nodes created'] = result['nodesCreated']
                    update_dict['nodes deleted'] = result['nodesDeleted']
                    update_dict['properties set'] = result['propertiesSet']
                    update_dict['relationships created'] = result['relationshipsCreated']
                    update_dict['relationships deleted'] = result['relationshipsDeleted']
                    update_dict['labels added'] = result['labelsAdded']
                    update_dict['labels removed'] = result['labelsRemoved']
                    update_dict['indexes added'] = result['indexesAdded']
                    update_dict['indexes removed'] = result['indexesRemoved']
                    update_dict['constraints added'] = result['constraintsAdded']
                    update_dict['constraints removed'] = result['constraintsRemoved']
                    # 'systemUpdates' is not returned by the ei-applet
#                    update_dict['system updates'] = result['systemUpdates']
                    converted_result.set_updates(update_dict)
                except:
                    converted_result.set_updates_made(False)
            except:
                converted_result.set_response(json_result)

        return converted_result

    def execute(self, query, query_num=-1):
        super().execute(query, query_num)
        query_text = query.text
        if self.output_file is not None:
            self.output_file.write(query_text + '\n')
        update = {'cmd': 'EXECUTE', 'q': query_text}
        try_count = 0
        all_good = False
        while not all_good and try_count < 3:
            status_code = 0
            try:
                headers = {}
                if settings._azure_auth_enabled_:
                    headers = auth._authenticate_azure_user(self.url.split("ei-applet")[0])
                result = requests.get(url=self.url, params=update, headers=headers, verify=False)
                status_code = result.status_code
                all_good = True
                if result.text.startswith('<h1>ERROR</h1>'):
                    if 'Invalid input' in result.text:
                        status_code = 505
                    elif 'ServiceUnavailable' in result.text:
                        status_code = 502
                    else:
                        status_code = 600
                elif "<!-- Copyright (C) Microsoft Corporation. All rights reserved. -->" in result.text and "<title>Sign in to your account</title>" in result.text:
                    status_code = 401
            except Exception as e:
                info_message(
                    f'Query {self.query_id} failed at {assetmodelutilities.get_formatted_time_now_noms()} with error type {type(e)}, retrying...')
                status_code = 600
            finally:
                if status_code != 200:
                    try_count += 1
                    all_good = False
                    if status_code == 414:
                        info_message(
                            f'Query {self.query_id} failed at {assetmodelutilities.get_formatted_time_now_noms()} - data too long!')
                        break
                    elif status_code == 505:
                        info_message(
                            f'Query {self.query_id} failed at {assetmodelutilities.get_formatted_time_now_noms()} - returned "ERROR"')
                        break
                    elif status_code == 401:
                        info_message(
                            f'Query {self.query_id} failed at {assetmodelutilities.get_formatted_time_now_noms()} - Missing Required Azure Auth Credentials')
                        exit()
                    elif status_code != 600:
                        info_message(
                            f'Query {self.query_id} failed at {assetmodelutilities.get_formatted_time_now_noms()} with error code {status_code}, retrying...')
                        sleep(2)

        if not all_good:
            warning_message(f'Query {self.query_id} not processed!')
        elif try_count > 0:
            info_message(f'Query {self.query_id} processed successfully on attempt {try_count + 1}')

        converted_result = self.convert_result(result, status_code)
        if self.results_file is not None:
            self.write_response(converted_result.get_response())

        return converted_result

    def print_response(self, response):
        if response is not None:
            for r in response:
                print(r)

    def write_response(self, response):
        if response is not None:
            for r in response:
                self.results_file.write(str(r) + '\n')
