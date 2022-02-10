from sqlite3 import connect
from os import path

class DataModuleMain:
    __slots__ = '__connection'

    def __enter__(self):
        #path.dirname(__file__) + '\\DataBases\\' + 'DB.db'
        self.__connection = connect('D:\\Projetos\\Project ProjMK\\DataBases\\DB.db')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__connection.close()

    def query(self):
        return self.__connection.cursor()

    def commit(self):
        self.__connection.commit()

    def get_project_types(self):
        return Organizer.org_project_types(Database.select_project_types())

    def delete_project(self, project_type):
        return Database.delete_project(project_type)

class Database:
    @classmethod
    def select_project_types(cls):
        with DataModuleMain() as dm:
            qry = dm.query()

            qry.execute(
                '''
                    SELECT  PRO_TYPE
                    FROM    PROJECT
                '''
            )

            return qry.fetchall()

    @classmethod
    def select_project(cls, project_type):
        with DataModuleMain() as dm:
            qry = dm.query()

            qry.execute(
                f'''
                    SELECT  PRO_TYPE
                    FROM    PROJECT
                    WHERE   PRO_TYPE = '{project_type}'
                '''
            )

            return qry.fetchall()

    @classmethod
    def delete_project(cls, project_type):
        with DataModuleMain() as dm:
            qry = dm.query()

            qry.execute(
                f'''
                    DELETE FROM PROJECT
                    WHERE  PRO_TYPE = '{project_type}'
                '''
            )

            qry.execute(
                f'''
                                DELETE FROM DIRECTORY
                                WHERE  DIR_PROJECT = '{project_type}'
                            '''
            )

            qry.execute(
                f'''
                                DELETE FROM FILE
                                WHERE  FIL_PROJECT = '{project_type}'
                            '''
            )

            dm.commit()

        return not list(Organizer.org_project_types(cls.select_project(project_type)))

class Organizer:
    @classmethod
    def org_project_types(cls, raw_iterable):
        if raw_iterable:
            for raw in raw_iterable:
                yield raw[0]

        return ()

