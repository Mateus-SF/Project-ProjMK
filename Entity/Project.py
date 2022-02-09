from BaseFiles.Notification import Notification
import os

class Project:
    __slots__ = '__ptype', '__directory', '__notification'

    PROJECT_TYPES = {
        'emd': {
            'folders': ('BaseFiles', 'Entity', 'DataModules', 'DataBases', 'Model', 'Server'),
            'files': {
                'BaseFiles': (
                    '\\Exceptions.py', '\\GenericFunctions.py', '\\Notification.py', '\\EnumTypes.py',
                    '\\RegExPatterns.py'
                )
            }
        },

        'mvc': '',
        'simple': ''
    }

    def __init__(self, directory, ptype='simple'):
        self.__ptype = ptype
        self.__directory = directory
        self.__notification = Notification()

    def create(self):
        if self.__notification:
            try:
                os.mkdir(self.__directory)

                for folder in self.PROJECT_TYPES[self.__ptype]['folders']:
                    os.mkdir(self.__directory + '\\' + folder)

                    for file in self.PROJECT_TYPES[self.__ptype]['files'].get(folder, ()):
                        with open(self.__directory + '\\' + folder + '\\' + file, 'w') as _file:
                            pass

            except Exception as ex:
                self.__notification.set_valid(False)
                self.__notification.set_message(ex)

        return self.__notification

    def __process__(self):
        self.__verify()
        return self

    def __verify(self):
        self.__notification.set_valid(True)
        self.__notification.set_message('Project Created')
        self.__verify_dir()

    def __verify_dir(self):
        if os.path.isdir(self.__directory):
            self.__notification.set_valid(False)
            self.__notification.set_message('Project directiory already exists')