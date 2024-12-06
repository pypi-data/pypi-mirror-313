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
from rpio.package.manager import *



@click.group()
@click.pass_context
def packageCmds():
    pass

@packageCmds.command()
@click.option('--verbose','-v', is_flag=True,default=False,help='Enable debug information.')
@click.option('--check','-c', is_flag=True,default=False,help='Check if standalone robosapiensIO package is valid.')
@click.option('--create', is_flag=True,default=False,help='Create new standalone robosapiensIO package.')
@click.option('--name','-n', default='project', help='Name of the new standalone robosapiensIO package [default:"project"].')
def package(verbose,check,create,name):
    """Check correctness of standalone robosapiensIO application package."""
    if verbose:print("Checking the standalone robosapiensIO application package")

    if check:
        m = PackageManager(verbose=verbose)
        isValid=m.check(path=None)

        if isValid:
            print("SUCCESS - Valid robosapiensIO application package")
        else:
            print("FAIL - Invalid robosapiensIO application package")

    elif create:
        m = PackageManager(verbose=verbose)
        m.create(name=name,standalone=True,path=None)




