import json
import pandas as pd
import numpy as np
import requests
import datetime
import time
import os
import urllib3

from progress.bar import Bar


def load_file(file_path):
    with open(file_path, 'rb') as inp:
        file = inp.read()
        return file

def write_file(file, file_path):
    with open(file_path, 'wb') as out:
        out.write(file)

def parsing_login_file(file):
    with open(file, 'r') as f:
        return {e.split('\t')[0].strip(): e.split('\t')[1].strip() for e in f.readlines()}

def check_type(var):
    if var == type(object):
        return "Text"
    elif (var == type(float)) or var == np.dtype(float):
        return "Float"
    elif (var == type(bool)) or var == np.dtype(bool):
        return "Boolean"
    elif var == type(str):
        return "Text"
    elif (var == type(int)) or var == np.dtype(int):
        return "Integer"
    else:
        raise Exception(f'Cannot put to BioUML column of type {type(var)}')

def dictionary_converter(dic_for_parsing):
    converted_dictionary = {}
    for k, v in dic_for_parsing.items():
        if '[' in k:
            for k1, v1 in v.items():
                if not isinstance(v1, dict):
                    if k1 not in converted_dictionary.keys():
                        converted_dictionary[k1] = [v1]
                    else:
                        converted_dictionary[k1].append(v1)
                else:
                    PyBiouml().as_name_value(v1)
    return converted_dictionary

def adder(object, dictionary, value):
    if len(object) != 1:
        dictionary.setdefault(object[0], {})
        dictionary[object[0]].update({})
        adder(object[1:], dictionary[object[0]], value)
    else:
        dictionary[object[0]] = value

def list_to_dataframe():
    pass

def deexpand(dic, final_list, key=None):
    for k, v in dic.items():
        for e in v:
            if isinstance(dict(), type(e)):
                deexpand(e, final_list, key=k)
            else:
                if key is None:
                    final_list.append(f'{k}/{e}')
                else:
                    final_list.append(f'{key}/{k}/{e}')

def expand(e, prop):
    if 'type' in e.keys() and e['type'] == 'composite':
        result = []
        for el in e['value']:
            result.append(expand(el, prop))
        return {e[prop]: result}
    else:
        return e[prop]

def column(params, prop):
    result = []
    for e in params:
        try:
            expand_result = expand(e, prop)
        except:
            expand_result = None
        if isinstance(dict(), type(expand_result)):
            deexpand(expand_result, result)
        else:
            result.append(expand_result)
    return result

class PyBiouml:
    """
    This library is a python API interface for using BioUML Web service
    """

    def __init__(self):
        self.options = {}
        self.info = {}
        self.stats = []  # List to store statistics for each request

    def get(self, path):
        """
        Method fetches table data from BioUML server.

        :param path: Path to table in BioUML repository.
        :type path: str
        :return crafted_table: return DataFrame representation of BioUML table from path.
        :rtype crafted_table: pandas.DataFrame
        """
        TABLES_CONST = '/web/table/'
        table_info = pd.DataFrame(self.query_json(server_path=''.join([TABLES_CONST, 'columns']), de=path)['values'])
        table_data = self.query_json(server_path=''.join([TABLES_CONST, 'rawdata']), de=path)['values']
        if 'hidden' in table_info.columns:
            table_info = table_info[table_info['hidden'] != True]
        crafted_table = pd.DataFrame(table_data, index=table_info['name'].to_list()).T
        return crafted_table.loc[:, crafted_table.columns != 'ID']

    def get_connection(self):
        """
        Service method for creation a connection with BioUML Web Service, which checks if user was logged into BioUML

        :return connection: connection link
        """
        urllib3.disable_warnings()
        connection = self.options
        if len(connection.keys()) == 0:
            LINK_TO_CONF_FILE = '/home/jovyan/work/.user.txt'
            if os.path.exists(LINK_TO_CONF_FILE):
                params = parsing_login_file(LINK_TO_CONF_FILE)
                self.login(url=params['url'], user=params['user'], password=params['pass'])
                return self.options
            else:
                raise Exception('Not logged into biouml, run PyBiouml().login() first')
        return connection

    def query(self, servers_path, data, file=None, binary=False):
        """
        Service method for making post request with time and size logging

        :return: result of post request
        """



        connection = self.get_connection()
        url = ''.join([connection['url'], servers_path])
        if file:
            response = requests.post(url, data=data, cookies=self.options['cookie'], verify=False, files=file)
        else:
            response = requests.post(url, data=data, cookies=self.options['cookie'], verify=False)

        return response

    def query_json(self, server_path, reconnect=True, parameters=None, **params):
        """
        Service method for json return of connection with time and size logging

        :param server_path: path to required server.
        :type server_path: str
        :param reconnect: try to reconnect or not.
        :type reconnect: bool
        :param parameters: a dictionary with parameters for connection. Default None, this method can take parameters through **params.
        :type parameters: dict
        :param params: This parameter collect any other parameters which are give to the method and return a dictionary with them.
        :return json_content: return a result of the request in json format.
        :rtype json_content: json
        """
        if parameters is None:
            parameters = {}
            parameters.update(params)
        connect = self.query(server_path, parameters)
        json_content = connect.json()

        response_type = json_content.get('type')
        if response_type == 3 & reconnect:
            self.reconnect()
            return self.query_json(server_path=server_path, reconnect=False, parameters=parameters)
        elif response_type != 0:
            raise Exception(json_content.get('message'))

        return json_content

    def get_stats(self):
        """
        Retrieve statistics for all requests

        :return: List of statistics dictionaries
        """
        return self.stats

    def login(self, url='http://localhost:8080/biouml', user='', password=''):
        """
        Method which LogintoBioUMLserver. Theconnectionwillbesavedinglobaloptionsundernamebiouml_connection for future reuse.

        :param url: URLof running biouml server. Default it is http://localhost:8080/biouml, like an example of local biouml service.
        :type url: str
        :param user: BioUML user, empty string for anonymous login.
        :type user: str
        :param password: password.
        :type password: str
        """
        HTTP_CONST = 'http://'
        HTTPS_CONST = 'https://'
        BIOUML_CONST = '/biouml'
        if not (url.startswith(HTTP_CONST) or url.startswith(HTTPS_CONST)):
            url = ''.join([HTTP_CONST, url])
        if not url.endswith(BIOUML_CONST):
            url = ''.join([url, BIOUML_CONST])
        self.options.update([('url', url), ('username', user), ('password', password)])
        self.reconnect()

    def reconnect(self):
        """
        Service method for reconnection to BioUML web service
        """
        options = self.options
        url = options.pop('url')
        new_url = ''.join([url, '/web/login'])
        session = requests.Session()
        req = session.post(new_url, data=options)
        json_req = req.json()
        if json_req['type'] != 0:
            raise Exception(json_req.get('message'))
        self.options.update([('url', url), ('cookie', req.cookies)])
        self.options.update(options)

    def logout(self):
        """
        Method which Logouts from BioUML server.

        """
        self.query_json('/web/logout')

    def analysis(self, analysis_name, wait=True, verbose=True, parameters=None, **params):
        """
        Method for run BioUML analysis, optionally tracking progress

        :param analysis_name: name of BioUML analysis to run, use PyBiouml.analysis_list to get the list of possible values
        :type analysis_name: str
        :param wait: whether to wait for analysis completion or return immediately
        :type wait: bool
        :param verbose: print messages and progress from BioUML analysis, only meaningful if wait is TRUE
        :type verbose: bool
        :param parameters: a dictionary of parameters to BioUML analysis, use PyBiouml.analysis_parameters to get the table of parameters. Default None, this method can take parameters through **params.
        :type parameters: dict
        :param params: parameters to BioUML analysis, use PyBiouml.analysis_parameters to get the table of parameters. Collect any other parameters which are give to the method and return a dictionary with them.
        :return: job_id: return a job id of started work, that can be passed to PyBiouml.job_info and PyBiouml.job_wait.
        :rtype: str
        """
        job_id = self.next_job_id()
        if parameters is None:
            parameters = self.as_tree(params)
        else:
            parameters = self.as_tree(parameters)
        self.query_json('/web/analysis', jobID=job_id, de=analysis_name, json=parameters)
        if wait:
            self.job_wait(job_id=job_id, verbose=verbose)

        return print(job_id)

    def next_job_id(self):
        """
        Service method for creation a new job id.

        :return: job_id
        :rtype: str
        """
        last_job_id = self.info.setdefault('last_job_id', 0)
        n_job_id = last_job_id + 1
        self.info['last_job_id'] = n_job_id
        return ''.join(['RJOB', str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')), str(n_job_id)])

    def job_info(self, job_id):
        """
        Method info fetches info about BioUML job.

        :param job_id: ID of job usually returned from PyBiouml.analysis
        :type job_id: str
        :return: info: json with information about requested process (status, results, values, percent)
        """
        info = self.query_json('/web/jobcontrol', jobID=job_id)
        info['status'] = ['CREATED',
                          'RUNNING',
                          'PAUSED',
                          'COMPLETED',
                          'TERMINATED_BY_REQUEST',
                          'TERMINATED_BY_ERROR'][info['status']]
        return info

    def job_wait(self, job_id, verbose=True):
        """
        Waits for BioUML job completion

        :param job_id: ID of job usually returned from biouml.analysis
        :param verbose: print messages and progress from BioUML job
        :return: json with information about requested process (status, results, values, percent)
        """
        message_length = 0
        STATUSES = ['COMPLETED', 'TERMINATED_BY_REQUEST', 'TERMINATED_BY_ERROR']
        with Bar(message='Processing', max=100, suffix='%(percent)d%%') as bar:
            while True:
                info = self.job_info(job_id)
                if verbose:
                    if info['percent'] is not None:
                        bar.index = int(info['percent'])
                        bar.next()
                    if info['values'] is not None:
                        print(info['values'][0][message_length:])
                        message_length = len(info['values'][0])
                if info['status'] in STATUSES:
                    return info
                time.sleep(1)

    def as_tree(self, params_dictionary):
        """
        Service method for parsing dictionary with parameters to json, which can be used by BioUML Web service.

        :param params_dictionary: dictionary with parameters
        :type params_dictionary: dict
        :return: parameters in json format
        """
        heirarhical_dictionary = {}
        for e in params_dictionary.keys():
            if '/' in e:
                splited_name = e.split('/')
                adder(splited_name, heirarhical_dictionary, params_dictionary[e])

            else:
                heirarhical_dictionary[e] = params_dictionary.get(e)

        name_values = self.as_name_value(heirarhical_dictionary)
        return json.dumps(name_values)

    def as_name_value(self, dictionary):
        local_list = []
        c = 0
        for k, v in dictionary.items():
            if not isinstance(v, dict):
                local_list.append({'name': k, 'value': v})
            else:
                if '[' in k:
                    if c == 0:
                        local_list.append(dictionary_converter(dictionary))
                        c += 1
                    else:
                        continue
                else:
                    local_list.append({'name': k, 'value': self.as_name_value(v)})
        return local_list

    def put(self, path, value):
        """
        Method to put usere's table on BioUML Web Service.

        :param path: path to repository for table.
        :type path: str
        :param value: pandas DataFrame table to put
        :type value: DataFrame
        """
        columns = []
        columns.append({'name': 'ID', 'type': 'Text'})
        data = []
        v_c = value.index.values.astype(str, copy=True)
        data.append(v_c.tolist())
        for i, v in enumerate(value.columns):
            columns.append({'name': v, 'type': check_type(value.dtypes[v])})
            str_column = value[v].astype(str, copy=True)
            data.append(str_column.tolist())

        self.query_json('/web/table/createTable', de=path, columns=json.dumps(columns), data=json.dumps(data))

    def export(self, path, exporter_params=None, exporter='Tab-separated text (*.txt)', target_file='biouml.out'):
        """
        Method exports data from BioUML server to local file in given format

        :param path: path in BioUML repository.
        :type path: str
        :param exporter_params: dictionary of parameters to exporter. Default None.
        :param exporter: character string specifying format, PyBiouml_exporters provides possible values.
        :type exporter: str
        :param target_file: a character string naming a file to export to. Default biouml.out
        :type target_file: str
        """
        if exporter_params is None:
            exporter_params = []
        else:
            exporter_params = self.as_tree(exporter_params)

        start_time = time.time()

        data = {'exporter': exporter,
                'type': 'de',
                'detype': 'Element',
                'de': path,
                'parameters': exporter_params}
        content = self.query('/web/export', data=data, binary=True)

        end_time = time.time()
        elapsed_time = round(end_time - start_time, 6)

        self.stats.append({
            'Type': 'Exporting',
            'File name': os.path.basename(target_file),
            'Upload time': f'{elapsed_time} seconds'
        })
        write_file(content.content, target_file)

    def to_import(self, file, parentPath, importer, importer_params=None):
        """
        Method imports file to BioUML repository.

        :param file: The name of file to import.
        :param parentPath: Path to folder in BioUML repository.
        :type parentPath: str
        :param importer: character string specifying format, PyBiouml.importers() provides list of posible values
        :type importer: str
        :param importer_params: dictionary of parameters to importer
        :return: Resulting path in BioUML repository
        :rtype: str
        """

        if importer_params is None:
            importer_params = []
        else:
            importer_params = self.as_tree(importer_params)

        start_time = time.time()

        file_id = self.next_job_id()
        job_id = self.next_job_id()
        data = {'fileID': file_id}
        filename = os.path.basename(file)
        start_time = time.time()
        self.query('/web/upload', data=data, file={'file': (filename, load_file(file))})
        params = {'type': 'import',
                  'fileID': file_id,
                  'de': parentPath,
                  'jobID': job_id,
                  'format': importer,
                  'json': importer_params
                  }
        self.query_json('/web/import', parameters=params)

        end_time = time.time()
        elapsed_time = round(end_time - start_time, 6)

        file_size = os.path.getsize(file)

        self.stats.append({
            'Type': 'Importing',
            'File name': filename,
            'jobID': job_id,
            'fileID': file_id,
            'Upload time': f'{elapsed_time} seconds',
            'File size': f'{file_size} bytes'
        })

        return self.job_wait(job_id)['results'][0]

    def ls(self, path, extended=False):
        """
        Method lists children data elements by path in BioUML repository.

        :param path: path to data collection in BioUML repository.
        :type path: str
        :param extended: whether to return additional attributes for each children.
        :type extended: bool
        :return: df: If extended is False a DataFrame with child names, otherwise a DataFrame wich contains row with names corresponding to child names and columns hasChildren and type.
        :rtype: pandas.DataFrame
        """
        resp = self.query_json('/web/data', service='access.service', command=29, dc=path)
        content = resp.get('values')
        d = json.loads(content)
        if len(d.get('names')) == 0:
            return pd.DataFrame()
        df = pd.DataFrame(d['names'])
        return df[['name', 'hasChildren', 'class']]

    def analysis_list(self):
        """
        Method that fetches list of available analyses from current BioUML server

        :return: DataFrame table of analysis with two column ’Group’ and ’Name’.
        :rtype: pandas.DataFrame
        """
        resp = self.query_json("/web/analysis/list")['values']
        r = {'Group': [], 'Name': []}
        for e in resp:
            splitted = e.split('/')
            r['Group'].append(splitted[0])
            r['Name'].append(splitted[1])
        return pd.DataFrame(r)

    def exporters(self):
        """
        Method fetches the list of exporters from BioUML server, these exporters can be used in PyBiouml.export method

        :return: list with expoters
        """
        return self.query_json("/web/export/list")['values']

    def importers(self):
        """
        Method fetches the list of importers from BioUML server, these importers can be used in PyBiouml.to_import method

        :return: list with expoters
        """
        return self.query_json("/web/import/list")['values']

    def workflow(self, path, parameters=None, wait=True, verbose=True):
        """
        Method run BioUML workflow optionaly tracking progress.

        :param path: path to BioUML workflow
        :type path: str
        :param parameters: list of parameters to BioUML workflow.
        :param wait: whether to wait for workflow completion or return immediately
        :type wait: bool
        :param verbose: print messages and progress from BioUML workflow, only meaningful if wait is TRUE
        :type verbose: bool
        :return: job_id: return a job id of started work, that can be passed to PyBiouml.job_info and PyBiouml.job_wait.
        :rtype: str
        """
        if parameters is None:
            parameters = []
        else:
            parameters = self.as_tree(parameters)
        job_id = self.next_job_id()
        self.query_json('/web/research',
                        jobID=job_id,
                        action='start_workflow',
                        de=path,
                        json=parameters)
        if wait:
            self.job_wait(job_id, verbose)
        return job_id

    def parameters(self, server_path, **params):
        """
        Service method, which create a request to get parameters

        :param server_path: path to target of the request for which need to take parameters
        :type server_path: str
        :param params: This parameter collect any other parameters which are give to the method and return a dictionary with them.
        :return: DataFrame with all parameters
        :rtype: pandas.DataFrame
        """
        query_params = self.query_json(server_path=server_path,
                                       parameters=params)['values']
        name = column(query_params, 'name')
        desc = column(query_params, 'description')
        param_type = column(query_params, 'type')
        return pd.DataFrame({'Name': name, 'Description': desc, 'Type': param_type})

    def analysis_parameters(self, analysis_name):
        """
        Get BioUML analysis parameters names and description

        :param analysis_name: me of BioUML analysis, , use PyBiouml.analysis_list to get the list of possible values
        :type analysis_name: str
        :return: DataFrame which contains row with names corresponding to parameter names and one column ’description’ with parameter description
        :rtype: pandas.DataFrame
        """
        return self.parameters('/web/bean/get', de=''.join(['properties/method/parameters/', analysis_name]))

    def export_parameters(self, path, exporter):
        """
        Method get BioUML export parameters

        :param path: path to data element in BioUML repository to export
        :type path: str
        :param exporter: name of BioUML exporter, use PyBiouml.exporters to get the table of possible values
        :type exporter: str
        :return: DataFrame which contains row with names corresponding to parameter names and one column ’description’ with parameter description
        :rtype: pandas.DataFrame
        """
        return self.parameters('/web/export',
                               de=path,
                               detype='Element',
                               type='deParams',
                               exporter=exporter
                               )

    def import_parameters(self, path, importer):
        """
        Method Get BioUML import parameters

        :param path: path to data element in BioUML repository to import
        :type path: str
        :param importer: name of BioUML importer, use biouml.importers to get the list of possible values
        :type importer: str
        :return: DataFrame which contains row with names corresponding to parameter names and one column ’description’ with parameter description
        :rtype: pandas.DataFrame
        """
        return self.parameters('/web/import',
                               de=path,
                               detype='Element',
                               type='properties',
                               format=importer,
                               jobID=self.next_job_id()
                               )