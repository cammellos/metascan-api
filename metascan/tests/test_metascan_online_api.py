#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Josh Maine'
import vcr
from metascan.metascan_online_api import MetaScanOnline, MetaScanOnlineAPIError
from nose.tools import assert_equals, raises, assert_not_equals


class TestMetaScanOnline:
    def __init__(self):
        self.apikey = ""
        self.client = MetaScanOnline(self.apikey,0.1)
        self.invalid_client = MetaScanOnline("notvalidkey")
        self.clean_file = "fixtures/clean_file.txt"
        self.infected_file = "fixtures/infected_file.txt"

    def test_uses_v2_api(self):
        assert_equals(self.client.base, "https://scan.metascan-online.com/v2/")

    def test_uses_the_apikey_provided(self):
        assert_equals(self.apikey, self.client.apikey)

    @raises(MetaScanOnlineAPIError)
    def test_scan_file_returns_an_apikey_error_if_key_is_invalid(self):
        with vcr.use_cassette('fixtures/vcr_cassettes/metascan_online/scan_file/key_not_valid.yaml'):
            self.invalid_client.scan_file(self.clean_file)

    def test_scan_file_returns_a_data_id(self):
        with vcr.use_cassette('fixtures/vcr_cassettes/metascan_online/scan_file/key_valid/clean_file.yaml',
                              filter_headers=['authorization']):
            response = self.client.scan_file(self.clean_file)
            assert_not_equals(response["data_id"], None)
            assert_not_equals(response["rest_ip"], None)

    @raises(MetaScanOnlineAPIError)
    def test_scan_file_and_get_results_returns_an_api_error_if_key_is_invalid(self):
        with vcr.use_cassette('fixtures/vcr_cassettes/metascan_online/scan_file_and_get_results/key_not_valid.yaml', filter_headers=['authorization']):
            self.invalid_client.scan_file_and_get_results(self.clean_file)

    def test_scan_file_and_get_results_returns_a_complete_scan_result(self):
        with vcr.use_cassette('fixtures/vcr_cassettes/metascan_online/scan_file_and_get_results/valid_key/clean_file.yaml',
                              filter_headers=['authorization']):
            response = self.client.scan_file_and_get_results(self.clean_file)
            assert_equals(response["scan_results"]["scan_all_result_i"], 0)
            assert_equals(response["scan_results"]["progress_percentage"],100)
    def test_scan_file_and_get_results_returns_a_complete_scan_result(self):
        with vcr.use_cassette('fixtures/vcr_cassettes/metascan_online/scan_file_and_get_results/valid_key/infected_file.yaml',
                              filter_headers=['authorization']):
            response = self.client.scan_file_and_get_results(self.infected_file)
            assert_equals(response["scan_results"]["scan_all_result_i"], 1)
            assert_equals(response["scan_results"]["progress_percentage"],100)

    @raises(MetaScanOnlineAPIError)
    def test_get_scan_result_from_data_id_returns_an_api_error_if_key_is_invalid(self):
        with vcr.use_cassette('fixtures/vcr_cassettes/metascan_online/get_scan_result_from_data_id/key_not_valid.yaml', filter_headers=['authorization']):
            response = self.client.scan_file(self.clean_file)
            self.invalid_client.get_scan_result_from_data_id(response["data_id"], response["rest_ip"])

    def test_get_scan_result_from_data_id_returns_a_scan_result(self):
        with vcr.use_cassette('fixtures/vcr_cassettes/metascan_online/get_scan_result_from_data_id/valid_key.yaml', filter_headers=['authorization']):
            response = self.client.scan_file(self.clean_file)
            self.client.get_scan_result_from_data_id(response["data_id"], response["rest_ip"])

    @raises(MetaScanOnlineAPIError)
    def test_get_scan_result_from_hash_returns_an_api_error_if_key_is_invalid(self):
        with vcr.use_cassette('fixtures/vcr_cassettes/metascan_online/get_scan_result_from_hash/key_not_valid.yaml', filter_headers=['authorization']):
            response = self.client.scan_file(self.clean_file)
            self.invalid_client.get_scan_result_from_hash(response["data_id"])

    def test_get_scan_result_from_hash_returns_a_scan_result(self):
        with vcr.use_cassette('fixtures/vcr_cassettes/metascan_online/get_scan_result_from_hash/valid_key.yaml', filter_headers=['authorization']):
            response = self.client.scan_file(self.clean_file)
            self.client.get_scan_result_from_hash(response["data_id"])


