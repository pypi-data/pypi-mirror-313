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


@click.group()
@click.pass_context
def importCmds():
    pass

@importCmds.command()
@click.option('--verbose','-v', is_flag=True,default=False,help='Enable debug information.')
@click.option('--generate','-g', is_flag=True,default=False,help='Generate standalone packages.')
@click.option('--RAADL', default='default.raadl', help='Input RAADL models.')
def importer(verbose):
    """Import standalone RoboSAPIENS Adaptive Platform application package."""
    if verbose:print("Importing the standalone robosapiensIO application package")





