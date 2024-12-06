import os
import requests
import chardet
import json
import logging
import xml.etree.ElementTree as ET

from pathlib import Path
from time import sleep


# class to download or upload data from/to .Stat Suite
class Client():

    # private constants
    __ERROR_OCCURRED  = "An error occurred: "
    __EXECUTION_IN_QUEUED = "Queued"
    __EXECUTION_IN_PROGRESS = "InProgress"
    __CONNECTION_ABORTED = "An existing connection was forcibly closed by the remote host"
    __DOWNLOAD_SUCCESS = "Successful download"
    __UPLOAD_SUCCESS = "The request was successfully processed "
    __UPLOAD_FAILED = "The request failed with status code "

    __NAMESPACE_MESSAGE = "{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}"
    __NAMESPACE_COMMON = "{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common}"

    # private variables
    __access_token = None
    __authentication_obj = None

    # Prepare logging format
    FORMAT = '%(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    __log = logging.getLogger(__name__)

    # Initialise Client
    def __init__(self,
	    access_token: str = None,
        authentication_obj: object = None):
        self.__access_token = access_token
        self.__authentication_obj = authentication_obj


    # 
    def __enter__(self):
        return self

    # 
    def __exit__(self, exc_type, exc_value, traceback):
        self.__access_token = None
        self.__authentication_obj = None


    #           
    @classmethod
    def init_with_access_token(
        cls, 
        access_token: str
    ):
        return cls(
            access_token=access_token
        )
    
    #           
    @classmethod
    def init_with_authentication_obj(
        cls, 
        authentication_obj: object
    ):
        return cls(
            authentication_obj=authentication_obj
        )
    

    # Download a data file from .Stat Suite
    def download_data_file(self, dotstat_url: str, content_format: str, file_path: Path):
        try:
            returned_result = ""

            # 
            if self.__authentication_obj is not None:
                self.__access_token = self.__authentication_obj.get_token()

            headers = {
                'accept': content_format,
                'authorization': 'Bearer '+self.__access_token
            }

            #
            response = requests.get(dotstat_url, verify=True, headers=headers)
        except Exception as err:
            returned_result = self.__ERROR_OCCURRED  + str(err) + os.linesep

            # Write the result to the log
            for line in returned_result.split(os.linesep):
                if len(line) > 0:
                    self.__log.info('   ' + line)
        else:
            if response.status_code != 200:
                returned_result = self.__ERROR_OCCURRED  + 'Error code: ' + \
                    str(response.status_code) + ' Reason: ' + str(response.reason)
                if len(response.text) > 0:
                    returned_result += os.linesep + 'Text: ' + response.text
            else:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                with open(file_path, "wb") as file:
                    file.write(response.content)
                    returned_result = self.__DOWNLOAD_SUCCESS
            
            # Write the result to the log
            for line in returned_result.split(os.linesep):
                if len(line) > 0:
                    self.__log.info('   ' + line)
        finally:
            return returned_result


    # Download streamed content from .Stat Suite
    def download_data_stream(self, dotstat_url: str, content_format: str):
        try:
            returned_result = ""

            # 
            if self.__authentication_obj is not None:
                __access_token = self.__authentication_obj.get_token()

            headers = {
                'accept': content_format,
                'Transfer-Encoding': 'chunked',
                'authorization': 'Bearer '+self.__access_token
            }

            #
            return requests.get(dotstat_url, verify=True, headers=headers, stream=True)
        except Exception as err:
            returned_result = self.__ERROR_OCCURRED  + str(err) + os.linesep
            return returned_result


    # Upload a data file to .Stat Suite
    def upload_data_file(self, 
                    transfer_url: str, 
                    file_path: Path, 
                    space: str, 
                    validationType: int, 
                    use_filepath: bool = False):
        try:
            returned_result = ""

            # 
            if self.__authentication_obj is not None:
                self.__access_token = self.__authentication_obj.get_token()

            payload = {
                'dataspace': space,
                'validationType': validationType
            }

            headers = {
                'accept': 'application/json',
                'authorization': "Bearer "+self.__access_token
            }

            if  use_filepath:
                files = {
                    'dataspace': (None, payload['dataspace']),
                    'validationType': (None, payload['validationType']),
                    'filepath': (None, str(file_path))
                }
            else:
                files = {
                    'dataspace': (None, payload['dataspace']),
                    'validationType': (None, payload['validationType']),
                    'file': (os.path.realpath(file_path), open(os.path.realpath(file_path), 'rb'), 'text/csv', '')
                }

            #
            response = requests.post(transfer_url, verify=True, headers=headers, files=files)
        except Exception as err:
            returned_result = self.__ERROR_OCCURRED  + str(err) + os.linesep

            # Write the result to the log
            for line in returned_result.split(os.linesep):
                if len(line) > 0:
                    self.__log.info('   ' + line)
        else:
            # If the response object cannot be converted to json, return an error
            results_json = None
            try:
                results_json = json.loads(response.text)
                if response.status_code == 200:
                    result = results_json['message']
                    # Write the result to the log
                    for line in result.split(os.linesep):
                        if len(line) > 0:
                            self.__log.info('   ' + line)

                    returned_result = result + os.linesep

                    # Check the request status
                    if (result != "" and result.find(self.__ERROR_OCCURRED ) == -1):
                        # Extract the request ID the returned message
                        start = 'with ID'
                        end = 'was successfully'
                        requestId = result[result.find(
                            start)+len(start):result.rfind(end)]

                        # Sleep a little bit before checking the request status
                        sleep(3)

                        # To avoid this error: maximum recursion depth exceeded while calling a Python object
                        # replace the recursive calls with while loops.
                        result = self.__check_request_status(transfer_url, requestId, space)

                        # Write the result to the log
                        for line in result.split(os.linesep):
                            if len(line) > 0:
                                self.__log.info('   ' + line)
                        sleep(3)

                        previous_result = result
                        while (result in [self.__EXECUTION_IN_PROGRESS, self.__EXECUTION_IN_QUEUED]
                                 or self.__CONNECTION_ABORTED in result):
                            result = self.__check_request_status(transfer_url, requestId, space)

                            # Prevent loging again the same information such as "Queued" or "InProgress" 
                            if previous_result != result:
                               previous_result = result

                            # Write the result to the log
                            for line in previous_result.split(os.linesep):
                              if (len(line) > 0 and line not in [self.__EXECUTION_IN_PROGRESS, self.__EXECUTION_IN_QUEUED]
                                    and self.__CONNECTION_ABORTED not in line):
                                 self.__log.info('   ' + line)
                            sleep(3)

                        returned_result = returned_result + result + os.linesep
                else:
                    returned_result = self.__ERROR_OCCURRED  + 'Error code: ' + str(response.status_code) + os.linesep
                    if len(str(response.reason)) > 0:
                        returned_result += 'Reason: ' + str(response.reason) + os.linesep
                    if len(response.text) > 0:
                        returned_result = returned_result + os.linesep + 'Text: ' + response.text

                    returned_result = returned_result + os.linesep
                    # Write the result to the log
                    for line in returned_result.split(os.linesep):
                        if len(line) > 0:
                            self.__log.info('   ' + line)
            except ValueError as err:
                if len(response.text) > 0:
                    self.init_status = self._ERROR + os.linesep + str(response.text)
                else:
                    self.init_status = self._ERROR + os.linesep + str(err)
        finally:
            return returned_result


    # Upload a structure file to .Stat Suite
    def upload_structure(self, transfer_url: str, file_path: Path):
        try:
            returned_result = ""

            # 
            if self.__authentication_obj is not None:
                self.__access_token = self.__authentication_obj.get_token()

            # Detect the encoding used in file 
            detected_encoding = self.__detect_encode(file_path)

            # Read file as a string "r+" with the detected encoding
            with open(file=file_path, mode="r+", encoding=detected_encoding.get("encoding")) as file:
                xml_data = file.read()

            # Make sure the encoding is "utf-8"
            tree = ET.fromstring(xml_data)
            xml_data = ET.tostring(tree, encoding="utf-8", method='xml', xml_declaration=True)

            headers = {
                'Content-Type': 'application/xml',
                'authorization': "Bearer "+self.__access_token
            }

            #
            response = requests.post(transfer_url, verify=True, headers=headers, data=xml_data)
        except Exception as err:
            returned_result = self.__ERROR_OCCURRED  + str(err) + os.linesep

            # Write the result to the log
            for line in returned_result.split(os.linesep):
                if len(line) > 0:
                    self.__log.info('   ' + line)
        else:
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                returned_result = f'{self.__UPLOAD_FAILED}{response.status_code}: {e}'

                # Write the result to the log
                for line in returned_result.split(os.linesep):
                    if len(line) > 0:
                        self.__log.info('   ' + line)
            else:
                response_tree = ET.XML(response.content)
                for self.__ERROR_OCCURRED in response_tree.findall("./{0}ErrorMessage".format(self.__NAMESPACE_MESSAGE)):
                    text_element = self.__ERROR_OCCURRED.find("./{0}Text".format(self.__NAMESPACE_COMMON))
                    if (text_element is not None):
                        if returned_result == "":
                            returned_result = f'{self.__UPLOAD_SUCCESS}with status code: {response.status_code}' + os.linesep
                        returned_result = returned_result + text_element.text + os.linesep

                # Write the result to the log
                for line in returned_result.split(os.linesep):
                    if len(line) > 0:
                        self.__log.info('   ' + line)
        finally:
            return returned_result
        

    # Detect the encoding used in file
    def __detect_encode(self, file_path):
        detector = chardet.UniversalDetector()
        detector.reset()
        with open(file=file_path, mode="rb") as file:
            for row in file:
                detector.feed(row)
                if detector.done: 
                    break

        detector.close()

        return detector.result


    # Check request sent to .Stat Suite status
    # To avoid this error: maximum recursion depth exceeded while calling a Python object
    # replace the recursive calls with while loops.
    def __check_request_status(self, transfer_url, requestId, space):
        try:
            returned_result = ""

            # 
            if self.__authentication_obj is not None:
                self.__access_token = self.__authentication_obj.get_token()

            headers = {
                'accept': 'application/json',
                'authorization': "Bearer "+self.__access_token
            }

            payload = {
                'dataspace': space,
                'id': requestId
            }

            transfer_url = transfer_url.replace("import", "status")
            transfer_url = transfer_url.replace("sdmxFile", "request")

            #
            response = requests.post(transfer_url, verify=True, headers=headers, data=payload)
        except Exception as err:
            returned_result = self.__ERROR_OCCURRED  + str(err)
        else:
            # If the response object cannot be converted to json, return an error
            results_json = None
            try:
                results_json = json.loads(response.text)
                if response.status_code == 200:
                    executionStatus = 'Execution status: ' + results_json['executionStatus']
                    if (results_json['executionStatus'] in [self.__EXECUTION_IN_PROGRESS, self.__EXECUTION_IN_QUEUED]
                        or self.__CONNECTION_ABORTED in results_json['executionStatus']):
                        returned_result = results_json['executionStatus']
                    else:
                        returned_result = executionStatus + os.linesep + 'Outcome: ' + results_json['outcome'] + os.linesep
                        index = 0
                        while index < len(results_json['logs']):
                            returned_result = returned_result + 'Log' + str(index) + ': ' + results_json['logs'][index]['message'] + os.linesep
                            index += 1
                else:
                    returned_result = self.__ERROR_OCCURRED  + 'Error code: ' + \
                        str(response.status_code) + ' Reason: ' + str(response.reason)
                    if len(response.text) > 0:
                        returned_result = returned_result + os.linesep + 'Text: ' + response.text
            except ValueError as err:
                if len(response.text) > 0:
                    self.init_status = self._ERROR + os.linesep + str(response.text)
                else:
                    self.init_status = self._ERROR + os.linesep + str(err)
        finally:
            return returned_result
    