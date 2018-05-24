from app.models import APIProjects, APIModules, APIDoc, APICases



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

    def get_module_by_id(self,project_id,project_name):
        """past project_name, and get it's modules"""
        if id:
            module = APIModules.query.fileter(id=project_id)
        else:
            module = []
        return module

