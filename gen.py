#!/usr/bin/env python
# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader
import os, uuid, argparse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

def generate_sln(context):
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)
    print j2_env.get_template('DebugProject.template').render(context)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a Debugger Project (VS2012)')
    parser.add_argument('app_path', metavar='FILE', type=str, nargs='?',
                       help='absolute path to executable file to be debugged')
    parser.add_argument('-w', dest='working_directory', metavar='DIR', default=False, nargs='?',
                       help='absolute path to working directory')
    args = parser.parse_args()
    
    #executable path is required
    if not(args.app_path):
        parser.error("Must provide absolute path to executable.")

    #if working directory not provided, use directory of executable
    if not (args.working_directory):
        args.working_directory = os.path.split(args.app_path)[0]

    #generate UUIDs for solution, required for dependencies
    args.guid_1 = uuid.uuid1()
    args.guid_2 = uuid.uuid1()
    #computer name (remote debugging = debug on local)
    args.computer_name = os.environ['COMPUTERNAME']
    #app name is executable name sans extension.
    temp = os.path.split(args.app_path)[1]
    args.app_name = os.path.splitext(temp)[0]

    generate_sln(vars(args))