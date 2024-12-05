import pickle
import os
import sys
import random
import time
from inspect import currentframe, getframeinfo
import requests
import yaml

from jira import JIRA, JIRAError
from requests import ReadTimeout
from yaml import YAMLError
from openapi_client.api_client import ApiClient
from openapi_client.api.tests_api import TestsApi

class JiraFunctions:

    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client

    def preprocess_url(self, url):
        """Preprocess URL to ensure format is correct for API."""
        if url[-1] == '/':
            return url[:-1]
        return url


    def server_auth(self, raw_url, pa_token, retry_count=-1):
        """Perform server setup and check for successful login."""
        retry_count_req = os.getenv('JIRA_RETRY_COUNT')
        if retry_count_req == '' or retry_count_req is None:
            retry_count_req = 10
        else:
            retry_count_req = int(retry_count_req)
        retry_count_req = os.getenv('JIRA_RETRY_COUNT')
        if retry_count_req == '' or retry_count_req is None:
            retry_count_req = 10
        else:
            retry_count_req = int(retry_count_req)
        url = self.preprocess_url(raw_url)
        # connect to server
        server = JIRA(server=url, token_auth=pa_token)
        try:
            server.myself()
        except JIRAError as ex:
            response = ex.response.headers
            status_code = ex.status_code
            if status_code == 429:
                if retry_count == -1:
                    retry_count_inc = 0
                else:
                    retry_count_inc = retry_count
                backoff_time = int(response['retry-after']) + \
                    random.randint(60, 80) + (retry_count_inc * 5)
                if retry_count < retry_count_req:
                    time.sleep(backoff_time)
                    retry_count += 1
                    self.server_auth(raw_url, pa_token, retry_count)
                else:
                    print('Error raised from line: ' +
                        str(getframeinfo(currentframe()).lineno))
                    raise JIRAError from ex

            else:
                print(
                    'Error! Could not authenticate with JIRA. Ensure your JIRA_PA_TOKEN is correct.')
                sys.exit(1)
        return server, url


    def check_xray_file(self):
        """Function to return filename of XRAY Configuration File."""
        projpath = os.environ['CI_PROJECT_PATH']
        runnerfilepath_yml = os.path.join('/builds', projpath, 'xray_filepath.yml')
        runnerfilepath_yaml = os.path.join(
            '/builds', projpath, 'xray_filepath.yaml')
        if os.path.exists(runnerfilepath_yml):
            file_name = runnerfilepath_yml
        elif os.path.exists(runnerfilepath_yaml):
            file_name = runnerfilepath_yaml
        else:
            raise FileNotFoundError('Could not find xray_filepath.yaml or' +
                                    ' xray_filepath.yaml in your project root!')
        return file_name


    def get_yaml_value(self, model_name, yaml_key):
        """Function to get value from a YAML file, by specified key"""
        xray_file_name = self.check_xray_file()
        if xray_file_name != '':
            # Load XRAY File
            with open(xray_file_name, 'r', encoding='UTF-8') as xray_file_id:
                xray_file = yaml.safe_load(xray_file_id)
            # Try to get YAML key for specified model name
            xray_path = xray_file.get(model_name)
            try:
                # If the model name is not specified in the YAML
                if xray_path is None:
                    # Look for the default key and use the value from there
                    xray_path = xray_file.get('default')
                    pid_val = xray_path.get(yaml_key)
                # If the model name is specified, return PID ticket value if
                # present
                else:
                    pid_val = xray_path.get(yaml_key)
                    if pid_val is None:
                        default_section = xray_file.get('default')
                        pid_val = default_section.get(yaml_key)
                return pid_val
            except YAMLError as e:
                print('Failed to find ' + yaml_key + ' in XRAY File!')
                raise e


    def get_pid(self, model_name):
        """Wrapper function to get PID Ticket # from XRAY Config File"""

        return self.get_yaml_value(model_name, 'PID Ticket')


    def get_model_xray_repo_path(self, model_name):
        """Wrapper function to get XRAY Test Repository Path from XRAY Config File"""
        return self.get_yaml_value(model_name, 'Test Repository Path')


    def get_retry_count(self) -> int:
        """Returns the value of JIRA_RETRY_COUNT, or a default value (10) if none given"""
        retry_count_req = os.getenv('JIRA_RETRY_COUNT')
        if retry_count_req == '' or retry_count_req is None:
            retry_count_req = 10
        else:
            retry_count_req = int(retry_count_req)

        return retry_count_req


    def common_backoff_handler(self, ex, retry_count):
        """Function to handle backoff from calls to the JIRA API."""
        retry_count_req = self.get_retry_count()
        status_code = ex.status_code
        response = ex.response.headers
        if status_code == 429:
            if retry_count == -1:
                retry_count_inc = 0
            else:
                retry_count_inc = retry_count
            backoff_time = int(response['retry-after']) + \
                random.randint(60, 80) + (retry_count_inc * 5)
            if retry_count < retry_count_req:
                time.sleep(backoff_time)
                retry_count += 1
                return retry_count
            print('Exit Code: ' + str(status_code))
            print('Response Headers: ' + str(response))
            print('Response Text: ' + str(ex.text))
            return -2
        if str(status_code).startswith('2'):
            return 0
        print('Exit Code: ' + str(status_code))
        print('Response Headers: ' + str(response))
        print('Response Text: ' + str(ex.text))
        return -2


    def get_post_put_backoff_handler(self, response, retry_count):
        """Function for POST/PUT requests to handle rate limit backoffs."""
        response_headers = response.headers
        retry_count_req = self.get_retry_count()
        if str(response.status_code).startswith('2'):
            return -3
        if response.status_code == 429:
            if retry_count == -1:
                retry_count_inc = 0
            else:
                retry_count_inc = retry_count
            backoff_time = int(
                response_headers['retry-after']) + random.randint(60, 80) + (retry_count_inc * 5)
            if retry_count < retry_count_req:
                time.sleep(backoff_time)
                retry_count += 1
                return retry_count
            print('ERROR: Rate Limit Exceeded for Adding Test to Test Plan!')
            return -2


    def get_issue_handle_ratelim(self, server, issue_id, retry_count=-1):
        """Function to get an issue from JIRA, handling rate limits."""
        try:
            issu = server.issue(issue_id)
            print('Retrieved issue: ' + issue_id)
            return issu
        except JIRAError as ex:
            retry_count = self.common_backoff_handler(ex, retry_count)
            if retry_count > -2:
                self.get_issue_handle_ratelim(server, issue_id, retry_count)
            else:
                print('ERROR: Rate Limit Exceeded for Issue Collection!')
                print('Error raised from line: ' +
                    str(getframeinfo(currentframe()).lineno))
                raise JIRAError from ex


    def create_issue_handle_ratelim(self, server, target_dict, retry_count=-1):
        """Function to create an issue using a dictionary, handling rate limits."""

        try:
            issue = TestsApi.call_10_api_settings_teststatuses_get(fields=target_dict)
            return issue
        except JIRAError as ex:
            retry_count = self.common_backoff_handler(ex, retry_count)
            if retry_count > -2:
                self.create_issue_handle_ratelim(server, target_dict, retry_count)
            else:
                print('ERROR: Rate Limit Exceeded for Issue Creation!')
                print('Error raised from line: ' +
                    str(getframeinfo(currentframe()).lineno))
                raise JIRAError from ex


    def transition_issue_handle_ratelim(
            self,
            server,
            issue_object,
            transition_id,
            retry_count=-1,
            comment=''):
        """Function to transition issue using an object, handling rate limits"""
        try:
            server.transition_issue(issue_object, transition_id, comment=comment)
        except JIRAError as ex:
            retry_count = self.common_backoff_handler(ex, retry_count)
            if retry_count > -2:
                self.transition_issue_handle_ratelim(
                    server, issue_object, transition_id, retry_count, comment)
            else:
                print('ERROR: Rate Limit Exceeded for Transitions!')
                print('Error raised from line: ' +
                    str(getframeinfo(currentframe()).lineno))
                raise JIRAError from ex


    def update_issue_handle_ratelim(self,issue_obj, update_dict, retry_count=-1):
        """Function to update an issue with a specified field name and content, handling rate limits."""
        try:
            issue_obj.update(fields=update_dict)
        except JIRAError as ex:
            retry_count = self.common_backoff_handler(ex, retry_count)
            if retry_count > -2:
                self.update_issue_handle_ratelim(issue_obj, update_dict, retry_count)
            else:
                print('ERROR: Rate Limit Exceeded for Issue Update!')
                print('Error raised from line: ' +
                    str(getframeinfo(currentframe()).lineno))
                raise JIRAError from ex


    def add_field_value_handle_ratelim(
            self,
            issue_obj,
            field_name,
            field_value,
            retry_count=-1):
        """Function to update field value, handling rate limits."""
        try:
            issue_obj.add_field_value(field_name, field_value)
        except JIRAError as ex:
            retry_count = self.common_backoff_handler(ex, retry_count)
            if retry_count > -2:
                self.add_field_value_handle_ratelim(
                    issue_obj, field_name, field_value, retry_count)
            else:
                print('ERROR: Rate Limit Exceeded for Adding Field Value!')
                print('Error raised from line: ' +
                    str(getframeinfo(currentframe()).lineno))
                raise JIRAError from ex


    def get_custom_field_option(self, server, option_id, retry_count=-1):
        """Function to retrieve custom field from server, handle backoff and
        perform local pickling of server response for later reuse."""
        pickle_filename = option_id + '_jiracustomfield.pkl'
        if os.path.exists(pickle_filename):
            with open(pickle_filename, 'rb') as pickle_file:
                # nosemgrep
                return pickle.load(pickle_file)
        else:
            try:
                custom_field = server.custom_field_option(option_id)
            except JIRAError as ex:
                retry_count = self.common_backoff_handler(ex, retry_count)
                if retry_count > -2:
                    self.get_custom_field_option(server, option_id, retry_count)
                else:
                    print('ERROR: Rate Limit Exceeded for Get Custom Field Option!')
                    print('Error raised from line: ' +
                        str(getframeinfo(currentframe()).lineno))
                    raise JIRAError from ex
            # pickle custom field for later retrieval
            with open(pickle_filename, 'wb') as pickle_file:
                # nosemgrep
                pickle.dump(custom_field, pickle_file)
            return custom_field


    def post_request_handle_ratelim(
            self,
            request_url,
            request_headers,
            request_json,
            retry_count=-1):
        """Function to perform POST request with rate limit handling."""
        try:
            response = requests.post(
                request_url,
                json=request_json,
                headers=request_headers,
                timeout=60)
            retry_count = -2
        except ReadTimeout:
            retry_count = self.get_post_put_backoff_handler(response, retry_count)
        if retry_count > -2:  # Keep retrying
            self.post_request_handle_ratelim(
                request_url, request_headers, request_json, retry_count)
        else:
            return response.status_code

    def validate_url(self, url):
        if url.endswith(('.jlr-apps.com', '.jlrmotor.com')):
            return True
        else:
            return False

    def put_request_handle_ratelim(self, request_url,request_headers,retry_count=-1):
        """Function to perform PUT request with rate limit handling."""
        if self.validate_url(request_url):
            try:
                response = requests.put(request_url,headers=request_headers,timeout=60)
                retry_count = -2
            except ReadTimeout:
                retry_count = self.get_post_put_backoff_handler(response,retry_count)
            if retry_count > -2: #Keep retrying
                self.put_request_handle_ratelim(request_url,request_headers,retry_count)
            else:
                return 'Error: Expected URL to end in .jlr-apps.com or .jlrmotor.com'

    def put_request_handle_ratelim(self, request_url, request_headers, retry_count=-1):
        """Function to perform PUT request with rate limit handling."""
        try:
            response = requests.put(
                request_url, headers=request_headers, timeout=60)
            retry_count = -2
        except ReadTimeout:
            retry_count = self.get_post_put_backoff_handler(response, retry_count)
        if retry_count > -2:  # Keep retrying
            self.put_request_handle_ratelim(request_url, request_headers, retry_count)
        else:
            return 'Error: Expected URL to end in .jlr-apps.com or .jlrmotor.com'


    def get_request_handle_ratelim(self, request_url, request_headers, retry_count=-1):
        """Function to perform GET requests whilst handling rate limiting."""
        try:
            response = requests.get(
                request_url, headers=request_headers, timeout=60)
            retry_count = -2
        except ReadTimeout:
            retry_count = self.get_post_put_backoff_handler(response, retry_count)
        if retry_count > -2:  # Keep retrying
            self.get_request_handle_ratelim(request_url, request_headers, retry_count)
        else:
            return response


    def transition_to_approved(self, server, testcase_obj):
        """Function to transition to Approved state based on current state."""
        testcase_status = testcase_obj.fields.status.name
        if testcase_status == 'In Progress':
            # Transition Issue to Under Review State
            self.transition_issue_handle_ratelim(server, testcase_obj, '21')
            # Transition Issue to Approved State
            self.transition_issue_handle_ratelim(server, testcase_obj, '101')
        elif testcase_status == 'Under Review':
            # Transition Issue to Approved State
            self.transition_issue_handle_ratelim(server, testcase_obj, '101')
        elif testcase_status == 'Cancelled':
            # Transition Issue to New State
            self.transition_issue_handle_ratelim(server, testcase_obj, '41')
            # Transition to 'In Progress'
            self.transition_issue_handle_ratelim(server, testcase_obj, '91')
            # Transition Issue to Under Review State
            self.transition_issue_handle_ratelim(server, testcase_obj, '21')
            # Transition Issue to Approved State
            self.transition_issue_handle_ratelim(server, testcase_obj, '101')
        elif testcase_status == 'Rejected':
            # Transition to 'In Progress'
            self.transition_issue_handle_ratelim(server, testcase_obj, '81')
            # Transition Issue to Under Review State
            self.transition_issue_handle_ratelim(server, testcase_obj, '21')
            # Transition Issue to Approved State
            self.transition_issue_handle_ratelim(server, testcase_obj, '101')
        elif testcase_status == 'New':
            # Transition to 'In Progress'
            self.transition_issue_handle_ratelim(server, testcase_obj, '91')
            # Transition Issue to Under Review State
            self.transition_issue_handle_ratelim(server, testcase_obj, '21')
            # Transition Issue to Approved State
            self.transition_issue_handle_ratelim(server, testcase_obj, '101')


    def transition_to_in_progress(self, server, testcase_obj):
        """Function to transition to In Progress state based on current state."""
        testcase_status = testcase_obj.fields.status.name
        if testcase_status == 'New':
            # Transition to 'In Progress'
            self.transition_issue_handle_ratelim(server, testcase_obj, '91')
        elif testcase_status == 'Under Review':
            # Transition to 'Rejected'
            self.transition_issue_handle_ratelim(
                server,
                testcase_obj,
                '51',
                comment='Rejected as part of Transition to In Progress')
            # Transition to 'In Progress'
            self.transition_issue_handle_ratelim(server, testcase_obj, '81')
        elif testcase_status == 'Rejected':
            # Transition to 'In Progress'
            self.transition_issue_handle_ratelim(server, testcase_obj, '81')
        elif testcase_status == 'Cancelled':
            # Transition to 'New'
            self.transition_issue_handle_ratelim(server, testcase_obj, '41')
            # Transition to 'In Progress'
            self.transition_issue_handle_ratelim(server, testcase_obj, '91')
        elif testcase_status == 'Approved':
            # Transition to 'In Progress'
            self.transition_issue_handle_ratelim(server, testcase_obj, '81')


    def create_test_set(self, url, pa_token, project_key, ts_name):
        """Function to create XRAY Test Set for Simulink Test Suite"""
        server, url = self.server_auth(url, pa_token)
        ts_dict = {
            'project': {
                'key': project_key},
            'summary': (
                'Simulink Test Suite ' +
                ts_name),
            'issuetype': {
                'name': 'Test Set'},
            'description': (
                'Test Set created automatically for Simulink Test Suite ' +
                ts_name)}
        new_test_suite = self.create_issue_handle_ratelim(server, ts_dict)
        print('Successfully created Test Set with ID ' + new_test_suite.key)
        return new_test_suite.key


    def add_test_to_test_plan(self, testcase_key, testplan_key, url, pa_token):
        """Function to add test cases to a specified test plan"""
        assoctestcaseurl = url + '/rest/raven/1.0/api/testplan/' + testplan_key + '/test'
        assoctestcasejson = {'add': [testcase_key]}
        bearerauth = {'Authorization': 'Bearer ' + pa_token}
        response_code = self.post_request_handle_ratelim(
            assoctestcaseurl, bearerauth, assoctestcasejson)
        if str(response_code).startswith('2'):
            print('Successfully added Test Case ' +
                testcase_key + ' to Test Plan ' + testplan_key)
        else:
            print(
                'Error ' +
                str(response_code) +
                ' updating Test Plan ' +
                testplan_key +
                ' with Test Case ' +
                testcase_key)


    def create_test_case(self, url, pa_token, project_key, testcase_name, testcase_desc,
                        model_name, test_type, test_suite_id):
        """Function to create XRAY Test Case from Simulink Test Case"""
        # look for file specifying model-specific storage path
        testcase_path = self.get_model_xray_repo_path(model_name)
        pid_val = self.get_pid(model_name)
        # connect to server
        server, url = self.server_auth(url, pa_token)
        if len(testcase_desc) < 10:
            testcase_desc = (test_type + ' Test Case automatically created for '
                            + model_name + ' Simulink model.')
        # create issue
        if 'jira-test' not in url:
            test_type_xray = self.get_custom_field_option(server, '10823')  # 10600
            test_design_technique = self.get_custom_field_option(
                server, '26573')  # 16112
            test_design_technique_subitem = self.get_custom_field_option(
                server, '27002')
            test_method = self.get_custom_field_option(server, '29812')  # 16113
            det_event_rating_field = self.get_custom_field_option(
                server, '26540')  # 16110
            if test_type == 'SIL':
                test_target_level = self.get_custom_field_option(
                    server, '19203')  # 14701
            else:
                test_target_level = self.get_custom_field_option(
                    server, '19202')  # 14701
            tc_dict = {
                'project': {'key': project_key},
                'summary': ('Simulink ' + test_type + ' Test: ' + testcase_name +
                            ' for ' + model_name + ' Model'),
                'description': testcase_desc,
                'issuetype': {'name': 'Test'},
                'priority': {'name': 'Medium'},
                'customfield_10600': {'value': test_type_xray.value},
                'customfield_10611': testcase_path,  # XRAY Test Repository Path
                'customfield_16112': {'id': test_design_technique.id,
                                    'child': {'id': test_design_technique_subitem.id}},
                'customfield_16113': {'value': test_method.value},
                'customfield_14701': [{'id': str(test_target_level.id)}],
                'customfield_10609': [pid_val],
                'customfield_16110': {'value': det_event_rating_field.value},
                'customfield_10607': [test_suite_id],
                'customfield_16115': ['1'],  # Offcycle: None for PCDS Gateway
                'customfield_14056': {'value': 'Automated'}
            }
        else:
            print('WARNING: Creating Test Case in non-production Jira Instance!!')
            test_type_xray = self.get_custom_field_option(server, '30894')  # 10600
            tc_dict = {
                'project': {'key': project_key},
                'summary': ('Simulink ' + test_type + ' Test: ' + testcase_name +
                            ' for ' + model_name + ' Model'),
                'description': testcase_desc,
                'issuetype': {'name': 'Test'},
                'priority': {'name': 'Medium'},
                'customfield_10600': {'value': test_type_xray.value},
                'customfield_10611': testcase_path,
                'customfield_10609': [pid_val],
                'customfield_14056': {'value': 'Automated'}
            }
        new_test_case = self.create_issue_handle_ratelim(server, tc_dict)
        print('Successfully created Test Case with ID ' + new_test_case.key)
        if pid_val != '':
             self.add_test_to_test_plan(new_test_case.key, pid_val, url, pa_token)
        if 'jira-test' not in url:
            # Transition to Approved state.
            self.transition_to_approved(server, new_test_case)
        else:
            server.transition_issue(new_test_case, 'Start Progress')
        print('Sucessfully transitioned Test Case ' +
              new_test_case.key + ' to Approved State.')
        return new_test_case.key
        # return tc_dict, pid_val

    def add_test_cases_to_test_execution(
            self,
            url,
            pa_token,
            new_test_execution,
            testcase_keys):
        """Function to add Test Cases to Test Execution, with Retry handling logic."""
        assoctestcaseurl = url + '/rest/raven/1.0/api/testexec/' + \
            new_test_execution.key + '/test'
        assoctestcasejson = {'add': testcase_keys}
        bearerauth = {'Authorization': 'Bearer ' + pa_token}
        response_code = self.post_request_handle_ratelim(
            assoctestcaseurl, bearerauth, assoctestcasejson)
        if str(response_code).startswith('2'):
            print('Successfully added Test Cases to Test Execution')
        else:
            print(
                'Error ' +
                str(response_code) +
                ' updating Test Execution ' +
                new_test_execution.key +
                ' with test cases.')


    def create_test_execution(
            self,
            url,
            pa_token,
            project_key,
            testfile_name,
            model_name,
            testcase_keys,
            test_type):
        """Function to create XRAY Test Execution from run of Simulink Test Case"""
        # connect to server
        pid_val = self.get_pid(model_name)
        server, url = self.server_auth(url, pa_token)
        for tc_key in testcase_keys:
            tc = self.get_issue_handle_ratelim(server, tc_key)
            self.transition_to_in_progress(server, tc)
        if os.environ['CI_PIPELINE_SOURCE'] == 'merge_request_event':
            mr_url = os.environ['CI_PROJECT_URL'] + \
                '/-/merge_requests/' + os.environ['CI_MERGE_REQUEST_IID']
            desc = (test_type + ' Test Execution for ' + testfile_name +
                    ' Simulink Test File, executed on branch ' +
                    os.environ['CI_MERGE_REQUEST_SOURCE_BRANCH_NAME'] +
                    ' by Assignee ' + os.environ['GITLAB_USER_NAME'] +
                    ' (' + os.environ['GITLAB_USER_EMAIL'] + '), see GitLab MR: ' +
                    mr_url + ' for more information about this change.')
        else:
            desc = (
                test_type +
                ' Test Execution for ' +
                testfile_name +
                ' Simulink Test File, executed on branch ' +
                os.environ['CI_COMMIT_REF_NAME'] +
                ' by Assignee ' +
                os.environ['GITLAB_USER_NAME'] +
                ' (' +
                os.environ['GITLAB_USER_EMAIL'] +
                '), see GitLab Commit ID: ' +
                os.environ['CI_COMMIT_SHA'] +
                ' for more information about this change. ' +
                'The type of pipeline execution was: ' +
                os.environ['CI_PIPELINE_SOURCE'] +
                '.')
        if test_type.upper() == 'MIL':
            tams_key = 'TAMS-1665'
        else:
            tams_key = 'TAMS-1666'
        te_dict = {
            'project': {'key': project_key},
            'summary': ('Automated ' + test_type + ' Test Execution of: ' +
                        testfile_name + ' for ' + model_name + ' Model'),
            'description': desc,
            'issuetype': {'name': 'Test Execution'},
            'customfield_10627': [pid_val],
            'customfield_15004': tams_key
        }
        if 'jira-test' in url:
            print('WARNING: Creating Test Case in non-production Jira Instance!!')
        new_test_execution = self.create_issue_handle_ratelim(server, te_dict)

        # Associate Test Cases being executed with Test Execution
        self.add_test_cases_to_test_execution(
            url, pa_token, new_test_execution, testcase_keys)
        # Transition TCs to Approved
        for tc_key in testcase_keys:
            tc = self.get_issue_handle_ratelim(server, tc_key)
            self.transition_to_approved(server, tc)
        return new_test_execution.key


    def update_test_run(
            self,
            url,
            pa_token,
            test_case_key,
            test_execution_key,
            test_status):
        """Function to add a Test Run for a given Test Case and Test Execution"""
        # Get Test Run for given Test Case and Test Execution
        url = self.preprocess_url(url)
        bearerauth = {'Authorization': 'Bearer ' + pa_token}
        req_url = url + '/rest/raven/2.0/api/testrun/?testExecIssueKey=' + \
            test_execution_key + '&testIssueKey=' + test_case_key
        tr_req = self.get_request_handle_ratelim(req_url, bearerauth)
        testrun_id = tr_req.json()['id']
        # Update Test Run Status
        if test_status.upper() not in [
            'PASS',
            'FAIL',
            'TODO',
            'ABORTED',
                'EXECUTING']:
            raise ValueError(
                'Value of test_status must be PASS, FAIL, TODO, ABORTED or EXECUTING.')

        req_url = url + '/rest/raven/1.0/api/testrun/' + str(testrun_id) + \
            '/status?status=' + test_status.upper()
        response_code = self.put_request_handle_ratelim(req_url, bearerauth)
        if str(response_code).startswith('2'):
            print('Successfully updated Test Run to ' + test_status.upper() +
                ' for Test Case: ' + test_case_key)
        else:
            print(
                'Error ' +
                str(response_code) +
                ' updating Test Execution ' +
                test_execution_key +
                ' for Test Case ' +
                test_case_key +
                ' with correct status.')


    def detect_testcase_changes(
            self,
            url,
            pa_token,
            testcase_key,
            testcase_name,
            model_name,
            sl_testcase_desc,
            test_type,
            test_suite_id):
        """Function to detect changes in Simulink Test Case and update XRAY accordingly."""
        summary_string = ('Simulink ' + test_type + ' Test: '
                        + testcase_name + ' for ' + model_name + ' Model')
        update_list = []
        update_dict = {}
        # connect to server
        server, url = self.server_auth(url, pa_token)
        testcase_obj = self.get_issue_handle_ratelim(server, testcase_key)

        # Check Test Case Issue State, Move to In Progress to Update
        self.transition_to_in_progress(server, testcase_obj)

        testcase_summary = testcase_obj.fields.summary
        testcase_desc = testcase_obj.fields.description
        if 'jira-test' not in url:
            xray_path = testcase_obj.fields.customfield_10611
            pids_from_xray = testcase_obj.fields.customfield_10609
            test_suite_from_xray = testcase_obj.fields.customfield_10607
            der_from_xray = testcase_obj.fields.customfield_16110
            pcds_from_xray = testcase_obj.fields.customfield_16115
        else:
            xray_path = ''
            pids_from_xray = ''

        if testcase_summary is not summary_string:
            update_dict['summary'] = summary_string
            update_list.append('Summary')
        if testcase_desc is not None:
            if len(testcase_desc) < 10:
                if sl_testcase_desc is not None:
                    if len(sl_testcase_desc) < 10:
                        updated_desc = (
                            test_type +
                            ' Test Case automatically created for ' +
                            model_name +
                            ' Simulink model.')
                    else:
                        updated_desc = sl_testcase_desc
                else:
                    updated_desc = (
                        test_type +
                        ' Test Case automatically created for ' +
                        model_name +
                        ' Simulink model.')
                update_dict['description'] = updated_desc
                update_list.append('Description')
        else:
            updated_desc = (test_type + ' Test Case automatically created for '
                            + model_name + ' Simulink model.')
            update_dict['description'] = updated_desc
            update_list.append('Description')

        testcase_path = self.get_model_xray_repo_path(model_name)
        pid_val = self.get_pid(model_name)
        if (xray_path is not testcase_path) and testcase_path != '' and 'jira-test' not in url:
            update_dict['customfield_10611'] = testcase_path
            update_list.append('Repository Path')
        elif testcase_path == '':
            print('Test Case Path is blank - not updating.')

        if pid_val not in pids_from_xray and 'jira-test' not in url and len(
                pid_val) != 0:
            update_dict['customfield_10611'] = pids_from_xray.append(pid_val)
            update_list.append('PID')
        elif testcase_path == '' or len(pid_val) == 0:
            print('PID Ticket is blank or missing - not updating.')

        der_custfield = self.get_custom_field_option(server, '26540')
        if der_from_xray is None:
            update_dict['customfield_106110'] = {'id': str(der_custfield.id),
                                                'value': der_custfield.value}
            update_list.append('DER')

        tsfound = False
        for item in test_suite_from_xray:
            if item == test_suite_id:
                tsfound = True
        if not tsfound:
            # Associate Test Cases being executed with Test Execution
            assoctestcaseurl = url + '/rest/raven/1.0/api/testset/' + test_suite_id + '/test'
            assoctestcasejson = {'add': [testcase_key]}
            bearerauth = {'Authorization': 'Bearer ' + pa_token}
            response_code = self.post_request_handle_ratelim(
                assoctestcaseurl, bearerauth, assoctestcasejson)
            if str(response_code).startswith('2'):
                update_list.append('Test Suite')
            else:
                print(
                    'Error ' +
                    str(response_code) +
                    ' updating Test Suite ' +
                    test_suite_id +
                    ' with test cases.')

        if pcds_from_xray is None:
            try:
                self.add_field_value_handle_ratelim(
                    testcase_obj, 'customfield_16115', '1')
                update_list.append('PCDS Gateway')
            except JIRAError as e:
                print('Failed to update PCDS Gateway of ' + testcase_key + '.')
                print(e)

        # Perform issue update in one call
        if len(update_dict) > 0:
            self.update_issue_handle_ratelim(testcase_obj, update_dict)
        # Transition Issue to Approved State
        self.transition_to_approved(server, testcase_obj)

        print('Successfully Updated ' + ','.join(update_list) +
            ' for Test Case ' + testcase_key)
    