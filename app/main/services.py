from app.models import APIProjects, APIModules, APIDoc, APICases, TomcatEnv, ReplaceInfo, ParameterData, RunCase
import re
import requests
import json
import difflib
import copy
import time
from app.models import db
import jsonpath
from copy import deepcopy
import os


class SDProjectData(object):
    """Project Data class"""

    def get_all_projects(self):
        """
        :return: a list, like ['个人中心', '企业家']
        """
        all_project = APIProjects.query.all()
        print(all_project)
        return all_project

    def get_all_modules(self):
        all_modules = APIModules.query.all()
        return all_modules

    def get_all_doc(self):
        all_doc = APIDoc.query.all()
        return all_doc

    def get_all_cases(self):
        all_cases = APICases.query.all()
        return all_cases

    def get_module_by_id(self, project_id):
        """past project_name, and get it's modules"""
        if project_id:
            module = APIModules.query.filter_by(id=project_id).first()
        else:
            module = []
        return module

    def get_doc_by_mod_id(self, module_id):
        doc = APIDoc.query.filter_by(id=module_id).all()
        return doc

    def get_case_by_doc_id(self, doc_id):
        case = APICases.query.filter_by(id=doc_id).all()
        return case

    def get_case_obj_by_case_id(self, case_id):
        case_obj = APICases.query.filter_by(id=case_id).first()
        return case_obj

    def optimize_url(self, url):
        """
        if url start with http/ return is https or http with 1 or 0
        :param url:
        :return:
        """
        match_str = '^https://'
        match_str2 = '^http://'
        form_url = url
        if re.findall(match_str, url):
            get_is_https = 1
        elif re.findall(match_str2, url):
            get_is_https = 0
        else:
            form_url = 'http://' + form_url  # if no http:// string, add it
            get_is_https = 0
        return form_url

    def transfer_body_to_dict(self, case_obj):
        """
        Transfer str>"data={'a':1}" to list>> {"data":"{'a':1}}
        :param case_obj:
        :return:  a dict
        """
        str_body = case_obj.body
        divsion_semi = str_body.split(';')
        dict_body = {}
        for i in divsion_semi:
            first_key = i.split('=', 1)[0]
            second_value = i.split('=', 1)[1]
            dict_body[first_key] = second_value
        return dict_body

    def transfer_body_to_dict_not_contain_data_string(self, case_id):
        """
        Transfer str>"data={'a':1}" to list>> {"data":"{'a':1}}
        :param case_id:
        :return:  a dict
        """
        case = self.get_case_obj_by_case_id(case_id)
        str_body = case.body
        divsion_semi = str_body.split(';')
        dict_body = {}
        for i in divsion_semi:
            first_key = i.split('=', 1)[0]
            second_value = i.split('=', 1)[1]
            dict_body[first_key] = second_value
        return dict_body

    def run_case_id(self, case_id, env_id):
        """
        run case by single, case_id
        :param case_id:
        :param env_id:
        :return:
        """
        db.session.remove()
        case = APICases.query.filter_by(id=case_id).first()
        env = TomcatEnv.query.filter_by(id=env_id).first()
        final_url = self.optimize_url(env.ip + ':' + str(env.port) + '/' + case.url)
        body_dict = self.transfer_body_to_dict(case)
        # final_headers ->> Should be dict, but it is str in mysql database.
        # try:
        #     final_body = json.dumps(case.body)
        # except Exception:
        #     print("@@Error occur: {} ".format(Exception))
        #     return json.dumps({'result': 'error occur! error number: 11', 'resultCode': 0})

        print('------case.http_method is {}-{}-{}'.format(case.http_method, final_url, case.headers))
        if case.http_method == 'get':
            # 1 is get
            result = requests.request('get', final_url, params=case.body)
        elif case.http_method == 'post':
            # 2 is post
            print('--post func')
            result = requests.request('post', final_url, params=body_dict)
            print('--case.body:{}--'.format(body_dict))
            print('--result.request.url:{}--'.format(result.request.url))
        else:
            result = json.dumps({'result': 'error occur! error number: 12', 'resultCode': 0})
            return result
        return result

    def run_case_tool(self, case_id, old_env, new_env):
        """
        run case
        :param case_id:
        :param old_env:
        :param new_env:
        :return: result list
        """
        print('Run case----')
        old_env_result = self.run_case_id(case_id, old_env)
        new_env_result = self.run_case_id(case_id, new_env)
        old_result2 = self.split_text(old_env_result.text)
        new_result2 = self.split_text(new_env_result.text)
        case_name = self.get_case_obj_by_case_id(case_id).name
        case_body = self.get_case_obj_by_case_id(case_id).body
        # Add case id, name to compare results page
        old_result2.insert(0, 'Case_id_' + str(case_id) + '_name_' + case_name)
        new_result2.insert(0, 'Case_id_' + str(case_id) + '_name_' + case_name)
        # Add case parameter
        old_result2.insert(1, 'Case_parameter_' + case_body)
        new_result2.insert(1, 'Case_parameter_' + case_body)
        return {'old': old_result2, 'new': new_result2}

    def split_text(self, origin_text):
        """
        Input origin should be str or list only.
            //use X.splitlines to transfer to list wherher it is str or list
            //splitlines should be deal with list, so we transfer str to list
            //Also try to transfer json to json format to displayed humanityß
        :param origin_text:
        :return: list
        """
        init_text = []
        if isinstance(origin_text, str):
            init_text.append(origin_text)
        elif isinstance(origin_text, list):
            init_text = copy.deepcopy(origin_text)
        else:
            raise TypeError('only support str and list')
        dealed_text = []
        for i in init_text:
            try:
                s_temp = json.loads(i)
                s_temp2 = json.dumps(s_temp, indent=4, ensure_ascii=False)
                s_temp3 = s_temp2.splitlines()
                for j in s_temp3:
                    dealed_text.append(j)
                continue
            except Exception as e:
                print('@@@Cannt loads: {}'.format(i))
                s_temp4 = i
            dealed_text.append(s_temp4)
        return dealed_text

    def get_new_file_name(self, case_id, old_env, new_env):
        """
        :param case_id:
        :param old_env:
        :param new_env:
        :return: a new case name
        """
        date_str = time.strftime("%m-%d-%H:%M:%S")
        file_name = date_str + '_case_' + str(case_id) + '_Compare_env_' + str(old_env) + '-' + str(new_env) + '.html'
        return file_name

    def compare_result(self, case_id, old_env, new_env):
        """
        compare results and make file
        :param case_id:
        :param old_env:
        :param new_env:
        :return:
        """
        file_name = self.get_new_file_name(case_id, old_env, new_env)

        d = difflib.HtmlDiff()
        f = open('./workResults/' + file_name, 'w')

        results_list = self.run_case_tool(case_id, old_env, new_env)
        print('>>results_list: {}'.format(results_list))
        f.writelines(d.make_file(results_list['old'], results_list['new']))
        f.close()
        return file_name

    """
    compare cases with many parameters, using json path
    """

    def get_parameters_list(self, replace_id):
        """
        :param replace_id:
        :return: return a list: e.g. userIdList: 701981,2,1302,  func will split the data to a list
        """
        parameter_obj = ParameterData.query.filter_by(id=replace_id).first()
        parameters = parameter_obj.dataList
        parameters_list = parameters.split(',')
        return parameters_list

    def assemble_body_parameter(self, case_id=0, parameter_id=0, replace_id=''):
        """
        replace the value in json path  with parameters, return body_results
        :param case_id:
        :param parameter_id:
        :param replace_id:
        :return:
        """
        if case_id == 0 or parameter_id == 0 or replace_id == '':
            return "error 14, parameter cannot be null"
        else:
            replace_jsonpath_obj = ReplaceInfo.query.filter_by(id=replace_id).first()
            replace_jsonpath_path = replace_jsonpath_obj.json_path

            case = self.get_case_obj_by_case_id(case_id)
            case_id = case.id
            case_body = case.body
            body_dict = self.transfer_body_to_dict(case)
            body_dict[replace_jsonpath_obj.replace_key] = json.loads(
                body_dict[replace_jsonpath_obj.replace_key].replace("'",
                                                                    '"'))  # e.g. find {'a':1} for dealing the value in {'data':{'a':1}}
            body_result = []
            parameters_list = self.get_parameters_list(parameter_id)

            json_value_of_key = body_dict[replace_jsonpath_obj.replace_key]
            json_path_to_dict_index = jsonpath.jsonpath(json_value_of_key, replace_jsonpath_path,
                                                        result_type='PATH')  # like  "$.foo[0].baz"

            if not json_path_to_dict_index:
                raise Exception('Error16, cannot find the jsonpath in case body!')

            exec_str1 = 'body_dict' + "['" + str(replace_jsonpath_obj.replace_key) + "']" + json_path_to_dict_index[
                0].replace('$', '')

            body_dict_has_string = deepcopy(body_dict)
            for i in parameters_list:
                exec_str2 = exec_str1 + '=' + str(i)
                exec(exec_str2)
                body_dict_has_string[replace_jsonpath_obj.replace_key] = str(
                    body_dict[replace_jsonpath_obj.replace_key])
                body_result.append(deepcopy(body_dict_has_string))

            return body_result

    def compare_single_with_parameters(self, case_id, parameter_list, old_env, new_env):
        raise NotImplementedError

    def run_case_with_parameters(self, case_id, env_id, parameter_id, replace_id):
        """
        run case with different parameters
        :param case_id:
        :param env_id:
        :param parameter_id:
        :param replace_id:
        :return:
        """
        db.session.remove()
        case = APICases.query.filter_by(id=case_id).first()
        env = TomcatEnv.query.filter_by(id=env_id).first()
        final_url = self.optimize_url(env.ip + ':' + str(env.port) + '/' + case.url)
        body_dict = self.transfer_body_to_dict(case)
        # final_headers ->> Should be dict, but it is str in mysql database.

        body_dict_with_parameters = self.assemble_body_parameter(case_id, parameter_id, replace_id)

        #
        # try:
        #     final_body = json.dumps(case.body)
        # except Exception:
        #     print("@@Error occur: {} ".format(Exception))
        #     return json.dumps({'result': 'error occur! error number: 15', 'resultCode': 0})

        all_results = []
        print('------case.http_method is {}-{}-{}'.format(case.http_method, final_url, case.headers))
        for i in body_dict_with_parameters:
            if case.http_method == 'get':
                # 1 is get
                result = requests.request('get', final_url, params=i)
            elif case.http_method == 'post':
                # 2 is post
                print('--post func')
                result = requests.request('post', final_url, params=i)
                print('--case.body:{}=='.format(i))
            else:
                result = json.dumps({'result': 'error occur! error number: 16', 'resultCode': 0})
                return result
            all_results.append('Case ID:' + str(case_id))
            all_results.append(str(i))
            all_results.append(deepcopy(result.text))
        return all_results

    def compare_all_results(self, case_id, old_env, new_env, parameter_id, replace_id):
        """
        compare results and make file
        :param case_id:
        :param old_env:
        :param new_env:
        :param parameter_id:
        :param replace_id:
        :return:
        """
        file_name = self.get_new_file_name(case_id, old_env, new_env)

        d = difflib.HtmlDiff()
        f = open('./workResults/' + file_name, 'w')

        # results_list = self.run_case_tool(case_id, old_env, new_env)
        results_old = self.run_case_with_parameters(case_id, old_env, parameter_id, replace_id)
        split_result_old = self.split_text(results_old)
        results_new = self.run_case_with_parameters(case_id, new_env, parameter_id, replace_id)
        split_result_new = self.split_text(results_new)
        print('>>run all cases')
        f.writelines(d.make_file(split_result_old, split_result_new))
        f.close()
        return file_name

    def compare_by_run_case_id(self, run_id):
        r = RunCase.query.filter_by(id=run_id).first()
        file_name = self.compare_all_results(r.case_id, r.old_env_id, r.new_env_id, r.paramter_list.id, r.replace_id)
        return file_name


class ResultFile(object):
    """Deal result files"""

    def __init__(self):
        self.work_folder = './workResults/'

    def get_files(self):
        if os.path.exists(self.work_folder):
            f_list = os.listdir(self.work_folder)
            file_list = []
            for i in f_list:
                if os.path.isfile(self.work_folder + i):
                    file_list.append(i)
            return file_list
        else:
            return "Error 101, cannot find folder"
