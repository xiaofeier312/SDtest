from app.models import APIProjects, APIModules, APIDoc, APICases, TomcatEnv
import re
import requests
import json
import difflib


class SDData(object):
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
        case = APICases.query.filter_by(id=case_id).first()
        env = TomcatEnv.query.fileter_by(id=env_id).first()
        final_url = self.optimize_url(case.url)
        try:
            final_body = json.dumps(case.body)
        except Exception:
            print("@@Error occur: {} ".format(Exception))
            return json.dumps({'result': 'error occur! error number: 11', 'resultCode': 0})

        if case.http_method == 'get':
            result = requests.request(case.http_method, final_url, headers=case.headers)
        elif case.http_method == 'post':
            result = requests.request(case.http_method, final_url, headers=case.headers, data=final_body)
        else:
            result = json.dumps({'result': 'error occur! error number: 12', 'resultCode': 0})
        return result

    def differ_case_tool(self, old_case_list, new_case_list):
        """compare case results, make a compare result file,/ only support single case"""
        old_case_result = self.run_case_id(old_case_list)
        new_case_result = self.run_case_id(new_case_list)



    def split_text(self,origin_text):
        """use X.splitlines to transfer to list wherher it is str or list"""
        init_text = []
        for i in origin_text:
            init_temp = i.splitlines()
            init_text += init_temp
        return init_text


    def format_json_for_differ(self,text):
        """format json to display json with spaces, return a list"""
        init_text = []
        init_text.append(text)  #deal with text whether it is a list or a string
        result_list = []
        init_text=self.split_text(init_text)
        for i in init_text:
            init_temp = i.splitlines()
            init_text += init_temp

        for j in init_text:
            """try to format json text for look easy"""
            try:
                s_temp = json.loads(str(i))
                s_temp2 = json.dumps(s_temp, indent=4, ensure_ascii=False)
            except Exception as e:
                print('@@@Cannt loads: {}'.format(i))
                s134 = j




