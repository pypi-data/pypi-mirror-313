# Copyright (c) 2023-present Bert Van Acker (UA) <bert.vanacker@uantwerpen.be>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import click
import os
import subprocess
from rpio.pyLauncher.pyLauncher import launch,launch_main, launch_docker_compose

@click.group()
@click.pass_context
def runCmds():
    pass

@runCmds.command()
@click.option('--verbose','-v', is_flag=True,default=False,help='Enable debug information.')
@click.option('--platform','-p', default='none', help='Specify on which platform you want to run the adaptive application, based on the AADL deployment.')
@click.option('--launchfile', is_flag=True,default=False,help='Specify the use of the launchfile to run the adaptive application.')
@click.option('--docker', is_flag=True,default=False,help='Specify the use of docker to run the adaptive application.')
def run(verbose,platform,launchfile,docker):
    """Run standalone RoboSAPIENS Adaptive Platform application package."""
    if verbose:print("Run command under construction...")

    if platform is None:
        if verbose:print("Executing the run.py action (Realization/ManagingSystem/Actions/run.py)")
        _directory = os.getcwd()
        runFile = "Realization/ManagingSystem/Actions/run.py"
        arguments = ""
        if verbose:print(runFile)

        try:
            subprocess.run(['py.exe',runFile, arguments])
        except:
            print("FAIL - Running standalone robosapiensIO application failed")
    else:
        if docker:
            if verbose: print("Executing the adaptive application using the provided docker compose file for platform {}".format(platform))
            try:
                launch_docker_compose(path='Realization/ManagingSystem/Platform/' + platform)
            except:
                print("FAIL - Launching the standalone robosapiensIO application failed")
        elif launchfile:
            if verbose: print(
                "Executing the adaptive application using the provided launch file for platform {}".format(platform))
            try:
                launch('Realization/ManagingSystem/Platform/' + platform + '/launch.xml')
            except:
                print("FAIL - Launching the standalone robosapiensIO application failed")
        else:
            if verbose:print("Executing the adaptive application using the provided main file for platform {}".format(platform))
            try:
                launch_main('Resources/main_'+platform+'.py')
            except:
                print("FAIL - Launching the standalone robosapiensIO application failed")






