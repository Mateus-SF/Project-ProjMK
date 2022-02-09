import argparse

from BaseFiles.GenericFunctions import process
from Entity.Project import Project

parser = argparse.ArgumentParser(description='Welcome to ProjMK')
parser.add_argument(
    '-t', '--project_type', type=str, metavar='', help='Define the project type', default='simple',
    choices=['emd', 'mvc', 'simple']
)

parser.add_argument(
    '-d', '--project_directory', type=str, metavar='', help='Define the project directory', required=True
)

def run():
    args = parser.parse_args()
    print(process(Project(args.project_directory, args.project_type)).create())


if __name__ == '__main__':
    run()

