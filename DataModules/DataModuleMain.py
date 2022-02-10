from sqlite3 import connect
from BaseFiles.EnumTypes import Config

class DataModuleMain:
    __slots__ = '__connection'

    def __enter__(self):
        self.__connection = connect(Config.database_path.value)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__connection.close()

    def query(self):
        return self.__connection.cursor()

    def commit(self):
        self.__connection.commit()

    def get_project_types(self):
        return Organizer.org_project_types(Database.select_all_project_types())

    def get_project(self, project_type):
        return Organizer.org_project(
            Database.select_folders(project_type), Database.select_files(project_type)
        )

    def add_project(self, ptype, folders, files):
        return Database.insert_project(ptype, folders, files)

    def delete_project(self, project_type):
        return Database.delete_project(project_type)

class Database:
    @classmethod
    def select_all_project_types(cls):
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
    def select_project_type(cls, project_type):
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
    def select_folders(cls, project_type, folder=None):
        with DataModuleMain() as dm:
            qry = dm.query()

            if folder:
                qry.execute(
                    f'''
                        SELECT  DIR_PATH
                        FROM    DIRECTORY
                        WHERE   DIR_PROJECT = '{project_type}'
                          AND   DIR_PATH    = '{folder}'
                    '''
                )

            else:
                qry.execute(
                    f'''
                        SELECT  DIR_PATH
                        FROM    DIRECTORY
                        WHERE   DIR_PROJECT = '{project_type}'
                    '''
                )

            return qry.fetchall()

    @classmethod
    def select_files(cls, project_type, file=None):
        with DataModuleMain() as dm:
            qry = dm.query()

            if file:
                qry.execute(
                    f'''
                        SELECT  FIL_PATH
                        FROM    FILE
                        WHERE   FIL_PROJECT = '{project_type}'
                          AND   FIL_PATH    = '{file}'
                    '''
                )
            else:
                qry.execute(
                    f'''
                                        SELECT  FIL_PATH
                                        FROM    FILE
                                        WHERE   FIL_PROJECT = '{project_type}'
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

        return not list(Organizer.org_project_types(cls.select_project_type(project_type)))

    @classmethod
    def insert_project(cls, ptype, folders, files):
        return cls.insert_project_type(ptype) \
           and all(cls.insert_folder(ptype, folder) for folder in folders) \
           and all(cls.insert_file(ptype, file) for file in files)

    @classmethod
    def insert_project_type(cls, project_type):
        with DataModuleMain() as dm:
            qry = dm.query()

            qry.execute(
                f'''
                    INSERT INTO PROJECT
                    (
                        PRO_TYPE
                    )
        
                    VALUES
                    (
                        '{project_type}'
                    )
                '''
            )

            dm.commit()

        return bool(list(Organizer.org_project_types(cls.select_project_type(project_type))))

    @classmethod
    def insert_folder(cls, project_type, folder):
        with DataModuleMain() as dm:
            qry = dm.query()

            qry.execute(
                f'''
                    INSERT INTO DIRECTORY
                    (
                        DIR_PROJECT,
                        DIR_PATH
                    )
    
                    VALUES
                    (
                        '{project_type}',
                        '{folder}'
                    )
                '''
            )

            dm.commit()

        return bool(list(Organizer.org_folders(cls.select_folders(project_type, folder))))

    @classmethod
    def insert_file(cls, project_type, file):
        with DataModuleMain() as dm:
            qry = dm.query()

            qry.execute(
                f'''
                    INSERT INTO FILE
                    (
                        FIL_PROJECT,
                        FIL_PATH
                    )

                    VALUES
                    (
                        '{project_type}',
                        '{file}'
                    )
                '''
            )

            dm.commit()

        return bool(list(Organizer.org_files(cls.select_files(project_type, file))))


class Organizer:
    @classmethod
    def org_project_types(cls, raw_iterable):
        if raw_iterable:
            for raw in raw_iterable:
                yield raw[0]

        return ()

    @classmethod
    def org_project(cls, raw_folders, raw_files):
        return {
            'folders': (folder[0] for folder in raw_folders),
            'files': (file[0] for file in raw_files)
        }

    @classmethod
    def org_folders(cls, raw_folders):
        return (folder[0] for folder in raw_folders)

    @classmethod
    def org_files(cls, raw_files):
        return (file[0] for file in raw_files)