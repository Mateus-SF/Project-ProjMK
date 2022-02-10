from BaseFiles.Notification import Notification
from os import path
from Model.ModelProject import ModelProject
from copy import deepcopy

class Project:
    __slots__ = '__ptype', '__directory', '__notification', '__create_files', '__folders', '__files'

    def __init__(self, np=True, **kwargs):
        self.__ptype = kwargs['type']
        self.__directory = kwargs['directory']
        self.__create_files = kwargs['create_files']

        self.__notification = Notification()

    @property
    def notification(self):
        return deepcopy(self.__notification)

    @property
    def directory(self):
        return self.__directory

    @property
    def ptype(self):
        return self.__ptype

    @property
    def create_files(self):
        return self.__create_files

    @property
    def folders(self):
        return self.__folders

    @property
    def files(self):
        return self.__files

    @classmethod
    def delete_project(cls, project_type):
        return ModelProject.delete_project(project_type)

    @classmethod
    def register_project(cls, ptype, folders=None, files=None):
        return ModelProject.register_project(ptype, [] if folders is None else folders, [] if files is None else files)

    def __process__(self):
        self.__verify()
        return ModelProject(self)

    def __verify(self):
        self.__notification.set_valid(True)
        self.__notification.set_message('Project Created')
        self.__verify_dir()

    def __verify_dir(self):
        if path.isdir(self.__directory):
            self.__notification.set_valid(False)
            self.__notification.set_message('Project directiory already exists')
