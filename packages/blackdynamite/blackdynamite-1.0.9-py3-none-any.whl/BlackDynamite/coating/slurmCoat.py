#!/usr/bin/env python
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

from __future__ import print_function
import subprocess
import re


def register_param(parser):
    group = parser.register_group("slurmCoat")
    group.add_argument(
        "--email", type=str,
        help="email to send info messages to", default=None)
    group.add_argument("--module", type=str, nargs="*",
                       help="list of modules to load before launching the job")
    group.add_argument("--current_cwd", action='store_true',
                       help="Asks to run the job where the script is launched",
                       default=False)
    group.add_argument(
        "--slurm_options", type=str, nargs='*',
        help="Additional option to pass to SLURM (to be called several times)")


def launch(run, params):

    _exec = run.getExecFile()
    head = "#!/bin/bash\n\n"

    head += f"#SBATCH --time={params['walltime']}\n"

    if "email" in params or params['email'] is not None:
        head += "#SBATCH --mail-type=ALL\n"
        head += f"#SBATCH --mail-user={params['email']}\n"

    slurm_head_name = f"#SBATCH --job-name={run.id}_{run['run_name']}\n"
    head += slurm_head_name

    run["state"] = "SLURM submit"

    if "slurm_options" in params:
        for option in params["slurm_option"].split(params["option_delimeter"]):
            m = re.match(r'^--(\S+)$', option)
            if m:
                option = m.group(1)
            head += f"#SBATCH --{option}\n"

    if params["current_cwd"] is False:
        head += "#SBATCH --chdir=__BLACKDYNAMITE__run_path__\n"

    if "module" in params:
        head += "\nmodule purge\n"
        for i in params["module"]:
            head += f"module load {i}\n"

    run.update()

    head += """

export BLACKDYNAMITE_HOST=__BLACKDYNAMITE__dbhost__
export BLACKDYNAMITE_SCHEMA=__BLACKDYNAMITE__study__
export BLACKDYNAMITE_STUDY=__BLACKDYNAMITE__study__
export BLACKDYNAMITE_RUN_ID=__BLACKDYNAMITE__run_id__
export BLACKDYNAMITE_USER=""" + params["user"] + """

on_kill()
{
updateRuns.py --updates \"state = SLURM killed\" --truerun
exit 0
}

on_stop()
{
updateRuns.py --updates \"state = SLURM stopped\" --truerun
exit 0
}

# Execute function on_die() receiving TERM signal
#
trap on_stop SIGUSR1
trap on_stop SIGTERM
trap on_kill SIGUSR2
trap on_kill SIGKILL
"""

    _exec["file"] = run.replaceBlackDynamiteVariables(head) + _exec["file"]

    f = open(_exec["filename"], 'w')
    f.write(_exec["file"])
    f.close()
    # os.chmod(_exec["filename"], stat.S_IRWXU)
    print("execute sbatch ./" + _exec["filename"])
    print("in dir ")
    subprocess.call("pwd")
    if params["truerun"] is True:
        ret = subprocess.call("sbatch " + _exec["filename"], shell=True)
        print(f"return type {ret}")
