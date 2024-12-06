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
from rpio.transformations.transformations import *
from rpio.parsers.parsers import *
from rpio.metamodels.aadl2_IL import *




@click.group()
@click.pass_context
def transformationCmds():
    pass

@transformationCmds.command()
@click.option('--verbose','-v', is_flag=True,default=False,help='Enable debug information.')
@click.option('--roboarch2aadl', is_flag=True,default=False,help='Perform the roboArch2AADL transformation.')
@click.option('--aadl2aadlil', is_flag=True,default=False,help='Perform the AADL2AADLIL transformation.')
@click.option('--aadlil2code', is_flag=True,default=False,help='Perform the AADLIL2CODE transformation.')
def transformation(verbose,roboarch2aadl,aadl2aadlil,aadlil2code):
    """Performing one of the model-to-model or model-to-code transformations."""

    if roboarch2aadl:
        if verbose:print("WARNING: RoboArch2AADL transformation is not implemented yet.")

    if aadl2aadlil:
        if verbose: print("WARNING: AADL2AADLIL transformation is under development.")

        # 1. Setup the AADL parser
        try:
            parser = AADL_parser(logicalArchitecture='Design/logicalArchitecture.aadl',physicalArchitecture='Design/physicalArchitecture.aadl', messages='Design/messages.aadl')
        except:
            parser = None
            if verbose:print("ERROR: AADL parser could not be instantiated, check if AADL models are available (Design/*.aadl).")


        # 2. parse the aadl models and store in AADLIL
        try:
            s = parser.aadl2aadlIl()
        except:
            s = None
            if verbose:print("ERROR: AADL parsing failed, check if AADL models are available (Design/*.aadl).")

        # 3. dump to aadlil json
        try:
            s.object2json(fileName='Design/design.json')
        except:
            if verbose:print("ERROR: AADLIL model could not be generated.")


    if aadlil2code:
        if verbose: print("WARNING: AADLIL2CODE transformation is under development.")

        # 1. LOAD THE AADL INTERMEDUATE LANGUAGE
        try:
            design = system(name="adaptiveSystem", description="Design generated from the AADLIL file",JSONDescriptor='Design/design.json')
        except:
            design = None
            if verbose:print("ERROR: The AADIL file could not be loaded, please check if it exists (Design/design.json).")

        # 2. GENERATE CUSTOM MESSAGES FROM AADL INTERMEDIATE LANGUAGE
        try:
            message2code_py(system=design, path="Realization/ManagingSystem/Messages")
            message2code_py(system=design, path="Realization/ManagedSystem/Messages")
        except:
            if verbose:print("ERROR: Messages could not be generated, no design loaded.")

        # 3. GENERATE SWC CODE FROM AADL INTERMEDIATE LANGUAGE
        try:
            swc2code_py(system=design, path="Realization/ManagingSystem/Nodes")
        except:
            if verbose:print("ERROR: Code could not be generated, no design loaded.")

        # 3. GENERATE PLATFORM LAUNCH FILES
        try:
            swc2launch(system=design.systems[0], path="Realization/ManagingSystem/Platform")
            swc2launch(system=design.systems[1], path="Realization/ManagedSystem/Platform")
        except:
            if verbose: print("ERROR: Platform-specific launch file could not be generated, no design loaded.")

        # 3. GENERATE PLATFORM MAIN FILES
        try:
            current_folder_path, current_folder_name = os.path.split(os.getcwd())
            swc2main(system=design.systems[0],package=current_folder_name,prefix=None,path="Resources")
        except:
            if verbose: print("ERROR: Platform(s) main file could not be generated.")

        # 4. GENERATE PLATFORM DOCKER COMPOSE
        try:
            swc2dockerCompose(system=design.systems[0], path="Realization/ManagingSystem/Platform")
            add_backbone_config(system=design, path="Resources")
        except:
            if verbose: print("ERROR: Platform(s) docker compose file could not be generated.")

        # 8. update the roboSapiensIO.ini file based on the generation
        try:
            update_robosapiensIO_ini(system=design, path=None)
        except:
            if verbose: print("ERROR: robosapiensIO.ini file could not be updated.")