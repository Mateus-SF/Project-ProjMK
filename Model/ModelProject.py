from copy import deepcopy
from BaseFiles.Notification import Notification
import os
from DataModules.DataModuleMain import DataModuleMain

class ModelProject:
    __slots__ = '__project', '__notification'

    def __init__(self, project):
        self.__project = deepcopy(project)
        self.__notification = self.__project.notification

    def new_project(self):
        if self.__notification:
            try:
                self.__create_project_dir()

                with DataModuleMain() as dm:
                    project = dm.get_project(self.__project.ptype)

                self.__create_project_folders(project)
                self.__create_project_files(project)

            except Exception as ex:
                self.__notification.set_valid(False)
                self.__notification.set_message(str(ex))

        return deepcopy(self.__notification)

    @classmethod
    def register_project(cls, ptype, folders, files):
        try:
            with DataModuleMain() as dm:
                if dm.add_project(ptype, folders, files):
                    return Notification(True, f'Project {ptype} registerd')
                else:
                    return Notification(False, f'Failed to register project {ptype}')

        except Exception as ex:
            return Notification(False, str(ex))

    @classmethod
    def delete_project(cls, project_type):
        with DataModuleMain() as dm:
            if dm.delete_project(project_type):
                return Notification(True, f'Project {project_type} deleted')
            else:
                return Notification(False, f'Failed to delete project {project_type}')

    def __create_project_dir(self):
        os.mkdir(self.__project.directory)

    def __create_project_folders(self, project):
        for folder in project['folders']:
            os.mkdir(self.__project.directory + '\\' + folder)

    def __create_project_files(self, project):
        if self.__project.create_files:
            for file in project['files']:
                with open(self.__project.directory + '\\' + file, 'w') as _file:
                    pass