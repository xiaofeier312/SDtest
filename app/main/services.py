from app.models import APIProjects, APIModules, APIDoc, APICases, TomcatEnv
import re
import requests
import json

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

    def optimize_url(self,url):
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


    def run_case_id(self,case_id,env_id):
        """run case by single, case_id"""
        case = APICases.query.filter_by(id=case_id).first()
        env = TomcatEnv.query.fileter_by(id=env_id).first()
        final_url = self.optimize_url(case.url)
        try:
            final_body = json.dumps(case.body)
        except Exception:
            print("@@Error occur: {} ".format(Exception))
            return json.dumps({'result':'error occur! error number: 11', 'resultCode':0})

        if case.http_method == 'get':
            result = requests.request(case.http_method,final_url,headers=case.headers)
        elif case.http_method == 'post':
            result = requests.request(case.http_method, final_url, headers=case.headers, data=final_body)
        else :
            result = json.dumps({'result':'error occur! error number: 12', 'resultCode':0})
        return result


