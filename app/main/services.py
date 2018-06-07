from app.models import APIProjects, APIModules, APIDoc, APICases, TomcatEnv
import re
import requests
import json
import difflib
import copy
import time
from app.models import db

class SDProjectData(object):
    def get_all_projects(self):
        """return a list, like ['个人中心', '企业家']"""
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
        doc = APIDoc.query.filter_by(id=module_id)
        return doc

    def get_case_by_doc_id(self, doc_id):
        case = APICases.query.filter_by(id=doc_id)
        return case

    def optimize_url(self, url):
        ''' if url start with http/ return is https or http with 1 or 0'''
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

    def run_case_id(self, case_id, env_id):
        """run case by single, case_id"""
        db.session.remove()
        case = APICases.query.filter_by(id=case_id).first()
        env = TomcatEnv.query.filter_by(id=env_id).first()
        final_url = self.optimize_url(env.ip + ':' + str(env.port) +'/' + case.url)
        # final_headers ->> Should be dict, but it is str in mysql database.
        try:
            final_body = json.dumps(case.body)
        except Exception:
            print("@@Error occur: {} ".format(Exception))
            return json.dumps({'result': 'error occur! error number: 11', 'resultCode': 0})


        print('------case.http_method is {}-{}-{}'.format(case.http_method,final_url,case.headers))
        if case.http_method == 'get':
            # 1 is get
            result = requests.request('get', final_url)
        elif case.http_method == 'post':
            # 2 is post
            result = requests.request('post', final_url, data=final_body)
        else:
            result = json.dumps({'result': 'error occur! error number: 12', 'resultCode': 0})
        return result.text

    def run_case_tool(self, case_id, old_env, new_env):
        """run case//return result list"""
        print('Run case----')
        old_env_result = self.run_case_id(case_id, old_env)
        new_env_result = self.run_case_id(case_id, new_env)
        old_result2 = self.split_text(old_env_result)
        new_result2 = self.split_text(new_env_result)
        return {'old':old_result2, 'new':new_result2}

    def split_text(self, origin_text):
        """Input origin should be str or list only.
            //use X.splitlines to transfer to list wherher it is str or list
            //splitlines should be deal with list, so we transfer str to list
            //Also try to transfer json to json format to displayed humanity
            //return list"""
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

    # def format_json_for_differ(self, text):
    #     """format json to display json with spaces, return a list"""
    #     init_text = []
    #     init_text.append(text)  # deal with text whether it is a list or a string
    #     result_list = []
    #     init_text = self.split_text(init_text)
    #     for i in init_text:
    #         init_temp = i.splitlines()
    #         init_text += init_temp
    #
    #     for j in init_text:
    #         """try to format json text for look easy"""
    #         try:
    #             s_temp = json.loads(str(i))
    #             s_temp2 = json.dumps(s_temp, indent=4, ensure_ascii=False)
    #         except Exception as e:
    #             print('@@@Cannt loads: {}'.format(i))
    #             s134 = j


    def compare_result(self, old_case_id, new_case_id):
        """compare results and make file"""
        old_case_obj = APICases.query.filter_by(id=old_case_id).first()
        new_case_obj = APICases.query.filter_by(id=new_case_id).first()
        date_str = time.strftime("%m/%d-%H:%M:%S")
        file_name = date_str + '_Compare_' + old_case_obj.name + '-' + new_case_obj.name + '.html'

        d = difflib.HtmlDiff()
        f = open('../workResults/' + file_name, 'w')

        results_list = self.run_case_id(old_case_id, new_case_id)
        f.writelines(d.make_file(results_list[0], results_list[1]))
        f.close()

        return file_name
