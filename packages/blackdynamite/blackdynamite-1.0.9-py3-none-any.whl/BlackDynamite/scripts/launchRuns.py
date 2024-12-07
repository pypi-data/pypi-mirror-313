#!/usr/bin/env python3
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
import BlackDynamite as BD
################################################################
import os
import sys
import socket
################################################################


def main(argv=None):

    parser = BD.BDParser(description="launchRuns")
    group = parser.register_group("launchRuns")
    group.add_argument("--outpath", type=str, default=os.path.realpath('./'))
    group.add_argument("--generator", type=lambda s: parser.parseModuleName(s),
                       default='bashCoat',
                       help="Set job generator")

    group.add_argument(
        "--nruns", type=int, default=-1,
        help=('Specify the number of runs to launch. '
              'This is useful when we want to launch '
              'only the first run from the stack.'))
    group.add_argument("--machine_name", type=str,
                       default=socket.gethostname())

    params = parser.parseBDParameters(argv)
    mybase = BD.Base(**params)

    if "outpath" not in params:
        print('A directory where to create temp files '
              'should be provided. use --outpath ')
        sys.exit(-1)

    runSelector = BD.RunSelector(mybase)
    constraints = []
    if "constraints" in params:
        constraints = params["constraints"]

    def item_matcher(name, item):
        return item.lower().lstrip().startswith(name)

    if not any([item_matcher("state", item) for item in constraints]):
        constraints.append("state = CREATED")
    if not any([item_matcher("machine_name", item)
                for item in constraints]):
        constraints.append("machine_name = {0}".format(
            params["machine_name"]))

    run_list = runSelector.selectRuns(constraints)

    if (params["nruns"] > 0):
        run_list = [run_list[i]
                    for i in range(0, min(params["nruns"],
                                          len(run_list)))]

    print(f"Shall run {len(run_list)} runs")
    mybase.launchRuns(run_list, params)


if __name__ == "__main__":
    main()
