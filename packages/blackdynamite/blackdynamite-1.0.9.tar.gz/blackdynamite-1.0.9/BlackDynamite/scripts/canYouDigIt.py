#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
# -*- coding: utf-8 -*-
# -*- py-which-shell: "python"; -*-
# This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

################################################################
from . import createDB
from . import createJobs
from . import createRuns
from . import getRunInfo
from . import getJobInfo
from . import launchRuns
from . import cleanRuns
from . import plotRuns
from . import pushQuantity
from . import enterRun
from . import updateRuns
from . import bd_zeo_server
from . import open_zeodb
from . import fix_zeodb
from . import streamlitInfo
################################################################
import argparse
import argcomplete
import sys
import subprocess
################################################################


def clean_debug_filestream():
    if argcomplete.debug_stream != sys.stderr:
        argcomplete.debug_stream.close()

################################################################


class BDCompleter(argcomplete.CompletionFinder):

    def collect_completions(
            self, active_parsers, parsed_args, cword_prefix, debug):

        if parsed_args.target == 'init':
            createDB.main([])
        elif parsed_args.target == 'info':
            getRunInfo.main([])
        elif parsed_args.target == 'jobs':
            if parsed_args.command == 'create':
                createJobs.main([])
            elif parsed_args.command == 'info':
                getJobInfo.main([])
        elif parsed_args.target == 'runs':
            if parsed_args.command == 'create':
                createRuns.main([])
            elif parsed_args.command == 'info':
                getRunInfo.main([])
            elif parsed_args.command == 'launch':
                launchRuns.main([])
            elif parsed_args.command == 'clean':
                cleanRuns.main([])
            elif parsed_args.command == 'plot':
                plotRuns.main([])
            elif parsed_args.command == 'exec':
                enterRun.main([])
            elif parsed_args.command == 'update':
                updateRuns.main([])
            if parsed_args.command == 'quantity':
                pushQuantity.main([])
        elif parsed_args.target == 'server':
            bd_zeo_server.main([])

        return argcomplete.CompletionFinder.collect_completions(
            self, active_parsers, parsed_args, cword_prefix, debug)

################################################################


def main_PYTHON_ARGCOMPLETE_OK():
    parser = argparse.ArgumentParser(description="""
CanYouDigIt is the central client script for BlackDynamite parametric studies.
Every command may apply to db (database), jobs or runs.
""")
    target_parsers = parser.add_subparsers(
        dest='target', help='Principal command: info, init, jobs or runs')
    target_parsers.required = True

    #  subparsers
    parser_info = target_parsers.add_parser(
        'info', help='Claim info on the database')
    parser_info.add_argument('--streamlit', action='store_true',
                             help='renders a streamlit web page report')

    target_parsers.add_parser(
        'init', help='initialize the database')
    parser_full = target_parsers.add_parser(
        'full-update',
        help='update job list, attach and launch additional runs')
    parser_jobs = target_parsers.add_parser(
        'jobs', help='command specific to jobs')
    parser_runs = target_parsers.add_parser(
        'runs', help='command specific to runs')
    parser_server = target_parsers.add_parser(
        'server', help='command specific to TCP server')
    parser_zeodb = target_parsers.add_parser(
        'zeodb', help='command to the specific to the zeo db')

    parser_full.add_argument('--run_name', type=str,
                             required=True,
                             help='run_name to give to newly created runs')

    zeodb_parsers = parser_zeodb.add_subparsers(
        dest='command', help='command to the zeo database')
    zeodb_parsers.add_parser(
        'shell', help='Ask for a shell', add_help=False)
    zeodb_parsers.add_parser(
        'repair', help='Perform several check and reconstruction',
        add_help=False)

    server_parsers = parser_server.add_subparsers(
        dest='command', help='command to the server daemon')
    server_parsers.add_parser(
        'start', help='Start server', add_help=False)
    server_parsers.add_parser(
        'stop', help='Stop server', add_help=False)
    server_parsers.add_parser(
        'status', help='Print status', add_help=False)

    # # add subcommands
    parsers_jobs = parser_jobs.add_subparsers(dest='command')
    parsers_jobs.required = True
    parsers_runs = parser_runs.add_subparsers(dest='command')
    parsers_runs.required = True

    # jobs parsers
    parsers_jobs.add_parser(
        'create', help='Creation of jobs', add_help=False)
    parsers_jobs.add_parser(
        'info', help='Info on jobs', add_help=False)

    # run parsers
    parsers_runs.add_parser(
        'create', help='Creation of runs', add_help=False)
    parsers_runs.add_parser(
        'info', help='Info on runs', add_help=False)
    parsers_runs.add_parser(
        'launch', help='Launch runs', add_help=False)
    parsers_runs.add_parser(
        'clean', help='Clean runs', add_help=False)
    parsers_runs.add_parser(
        'exec', help='Execute a command in a run directory', add_help=False)
    parsers_runs.add_parser(
        'plot', help='Plot the result of runs', add_help=False)
    parsers_runs.add_parser(
        'update', help='Update the state of runs', add_help=False)
    parsers_runs.add_parser(
        'quantity', help='Push quantity to a run', add_help=False)

    autocomplete = BDCompleter()
    autocomplete(parser, exclude=['-h'])

    pre_args, unknown = parser.parse_known_args()

    if pre_args.target == 'init':
        createDB.main(unknown)
    elif pre_args.target == 'info':
        if pre_args.streamlit:
            subprocess.call(
                f'streamlit run {streamlitInfo.__file__}', shell=True)
        else:
            unknown.append('--summary')
            getRunInfo.main(unknown)
    elif pre_args.target == 'full-update':
        createJobs.main(unknown)
        args = f'--run_name {pre_args.run_name} ' + ' '.join(unknown)
        createRuns.main(args.split())
        launchRuns.main(unknown)
    elif pre_args.target == 'jobs':
        if pre_args.command == 'create':
            createJobs.main(unknown)
        if pre_args.command == 'info':
            getJobInfo.main(unknown)
    elif pre_args.target == 'runs':
        if pre_args.command == 'create':
            createRuns.main(unknown)
        if pre_args.command == 'info':
            getRunInfo.main(unknown)
        if pre_args.command == 'launch':
            launchRuns.main(unknown)
        if pre_args.command == 'clean':
            cleanRuns.main(unknown)
        if pre_args.command == 'plot':
            plotRuns.main(unknown)
        if pre_args.command == 'exec':
            enterRun.main(unknown)
        if pre_args.command == 'update':
            updateRuns.main(unknown)
        if pre_args.command == 'quantity':
            pushQuantity.main(unknown)
    elif pre_args.target == 'server':
        if pre_args.command:
            args = f'--action {pre_args.command} ' + ' '.join(unknown)
        else:
            args = '--action status ' + ' '.join(unknown)
        bd_zeo_server.main(args.split())
    elif pre_args.target == 'zeodb':
        if pre_args.command == 'shell':
            bd_zeo_server.main(['--action', 'stop'])
            open_zeodb.main(unknown)
        if pre_args.command == 'repair':
            fix_zeodb.main(unknown)
