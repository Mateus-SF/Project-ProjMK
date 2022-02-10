import argparse

from BaseFiles.GenericFunctions import process
from Entity.Project import Project
from DataModules.DataModuleMain import DataModuleMain

parser = argparse.ArgumentParser(description='Welcome to ProjMK')
subparsers = parser.add_subparsers(dest='command')

parser_new_proj = subparsers.add_parser('newproj')
parser_register_project = subparsers.add_parser('regproj')
parser_delete_project = subparsers.add_parser('delproj')
parser_update_project = subparsers.add_parser('updproj')

# parser_new_proj -----------------------------------------------------------------------------------------------------
with DataModuleMain() as dm:
    parser_new_proj.add_argument(
        '-t', '--project_type', dest='type', type=str, metavar='', help='Define the project type', default='simple',
        choices=dm.get_project_types()
    )


parser_new_proj.add_argument(
    '-d', '--project_directory', dest='dir', type=str, metavar='', help='Define the project directory', required=True
)

parser_new_proj.add_argument(
    '-nf', '--nofile', dest='file', action='store_false', help='Set files not to be created'
)

# parser_register_project ---------------------------------------------------------------------------------------------
parser_register_project.add_argument(
    '-t', '--project_type', dest='type', type=str, metavar='', help='Define the project type', required=True
)

parser_register_project.add_argument(
    '-fos', '--project_folders', dest='folders', type=str, metavar='', help='Define the project folders',
    required=True, nargs='+'
)

parser_register_project.add_argument(
    '-fis', '--project_files', dest='files', type=str, metavar='', help='Define the project files',
    nargs='+'
)

# parser_delete_project -----------------------------------------------------------------------------------------------
parser_delete_project.add_argument(
    'project_type', type=str, metavar='', help='Set the project to be deleted'
)

# parser_update_project -----------------------------------------------------------------------------------------------
# SOON

def run():
    args = parser.parse_args()

    if args.command == 'newproj':
        print(process(Project(directory=args.dir, type=args.type, create_files=args.file)).new_project())

    elif args.command == 'regproj':
        print(Project.register_project(ptype=args.type, folders=args.folders, files=args.files))

    elif args.command == 'delproj':
        print(Project.delete_project(args.project_type))

    elif args.command == 'updproj':
        ...


if __name__ == '__main__':
    run()

