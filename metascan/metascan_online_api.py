import time
import requests

__author__ = 'Josh Maine'

class MetaScanOnlineAPIError(Exception):
    pass

class MetaScanOnline():
    """ Metascan Online Public API v 2.0

        The Metascan Online Public API allows you to harness the power of our cloud-based multi-scanning technology
        integrated directly into your software solution.

        https://www.metascan-online.com/en/public-api
    """

    def __init__(self, apikey, poll_interval=3):
        self.host = "https://scan.metascan-online.com"
        self.api_version = "v2"
        self.base = self.host + "/" + self.api_version + "/"
        self.apikey = apikey
        self.poll_interval = poll_interval

    def scan_file(self, this_file, filename='', archivepwd='', samplesharing=1):
        """
        Initiate scan request

        On Metascan Online, scan is done asynchronously and each scan request is tracked by data id.

        @param this_file:     Contents of the file for scan	[REQUIRED]
        @param filename:      Name of files to preserve extension during scan and meta data	[RECOMMENDED]
        @param archivepwd:    If submitted file is password protected archive	[OPTIONAL]
        @param samplesharing: This flag is only available to users that have purchased access to private scanning
                                through the Metascan Online API. If '0', scanned files will not be stored or shared
                                by Metascan Online, although hashed results will remain available.	[OPTIONAL]
        @return: data_id rest_ip	Data ID used for retrieving scan results rest_ip is the server to query (JSON)
        @raise MetaScanOnlineAPIError: Any HTTP error returned by MetaScan
        """
        url = self.base + 'file'
        params = {'filename': filename, 'archivepwd': archivepwd, 'samplesharing': samplesharing}
        headers = {'apikey': self.apikey}
        files = {'file': (this_file, open(this_file, 'rb'))}
        return self.__call_api__('post',{'url': url, 'files': files, 'params':params})

    def get_scan_result_from_hash(self, this_hash):
        """
        Retrieve scan reports using data hash.

        @param this_hash: SHA1 or MD5 or SHA256	[REQUIRED]
        @return: scan results (JSON)
        """
        url = self.base + 'hash/' + this_hash
        return self.__call_api__('get', {'url': url})


    def get_scan_result_from_data_id(self, data_id, rest_ip):
        """
        Retrieve scan results

        On Metascan Online, scan is done asynchronously and each scan request is tracked by data id.
        Initiating a file scan and retrieving the scan results needs to be done with two separate API calls.
        This request needs to be made multiple times until scan is complete.
        Scan completion can be traced using scan_results.progress_percentage value from the response.

        @param data_id: Get from (Scanning a file)	[REQUIRED]
        @param rest_ip: The url to poll                 [REQUIRED]
        @return: scan results (JSON)
        @raise MetaScanOnlineAPIError: Any HTTP error returned by MetaScan
        """

        url = "https://" + rest_ip + '/file/' + data_id
        return  self.__call_api__('get', {'url': url})

    def scan_file_and_get_results(self, this_file):
        response = self.scan_file(this_file)
        data_id = response['data_id']
        rest_ip = response['rest_ip']
        while True:
            response = self.get_scan_result_from_data_id(data_id=data_id, rest_ip=rest_ip)
            if response['scan_results']['progress_percentage'] == 100:
                break
            else:
                time.sleep(self.poll_interval)
        return response

    def __call_api__(self, method, params):
        http_parameters = {'headers': {'apikey': self.apikey}}
        http_parameters.update(params)

        request = getattr(requests,method)(**http_parameters)

        if request.status_code != requests.codes.ok:
            raise MetaScanOnlineAPIError("Request failed with status code: " + str(request.status_code))
        return request.json()

