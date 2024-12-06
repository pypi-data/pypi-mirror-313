#**********************************************************************************
# * Copyright (C) 2024-present Bert Van Acker (B.MKR) <bert.vanacker@uantwerpen.be>
# *
# * This file is part of the roboarch R&D project.
# *
# * RAP R&D concepts can not be copied and/or distributed without the express
# * permission of Bert Van Acker
# **********************************************************************************
import os
import re
import sys
from rpio.metamodels.aadl2_IL import *
from textx import metamodel_from_file

class AADL_parser:
    """This is a parser that parses muliple AADL files and puts them into the AADL intermediate language.

        :param [logicalArchitecture]: [Path to the logical architecture AADL model], defaults to [None]
        :type [logicalArchitecture]: [string](, optional)

        :param [logicalArchitecture]: [Path to the logical architecture AADL model], defaults to [None]
        :type [logicalArchitecture]: [string](, optional)

        :param [messages]: [Path to the messages AADL model], defaults to [None]
        :type [messages]: [string](, optional)

        """
    def __init__(self, logicalArchitecture,physicalArchitecture,messages):
        """Constructor method
        """
        self.adaptiveSystem = None
        self.managingSystem = None
        self.managedSystem = None

        self.messages = []
        self.processes = []

        # Read the logical architecture
        try:
            with open(logicalArchitecture, 'r') as file:
                self.logicalArchitectureAADL = file.read()
        except FileNotFoundError:
            self.logicalArchitectureAADL = None
            print(f"Error: File '{logicalArchitecture}' not found.")
            sys.exit(1)

        # Read the physical architecture
        try:
            with open(physicalArchitecture, 'r') as file:
                self.physicalArchitectureAADL = file.read()
        except FileNotFoundError:
            self.physicalArchitectureAADL = None
            print(f"Error: File '{physicalArchitecture}' not found.")
            #sys.exit(1)        #TODO: enable if implemented

        # Read the messages
        try:
            with open(messages, 'r') as file:
                self.messagesAADL = file.read()
        except FileNotFoundError:
            self.messagesAADL = None
            print(f"Error: File '{messages}' not found.")
            sys.exit(1)




    def aadl2aadlIl(self):
        """Function to parse the AADL models and put them into the AADL intermediate language

        :return: [adaptiveSystem]
        :rtype: [Object]
        """

        # 0. Setup adaptive system
        self.adaptiveSystem = system(name="adaptiveSystem", description="Generated from AADL models")

        #1. Setup managing and managed system
        self.managedSystem = system(name="managedSystem", description="managed system part")
        self.managingSystem = system(name="managingSystem", description="managing system part")

        # 1. Parse the messages
        self._generateMessages()
        self.adaptiveSystem.messages = self.messages

        # 2. Parse the processes
        self._generateProcesses()

        # 3. Populate adaptive system
        self.adaptiveSystem.addSystem(self.managingSystem)
        self.adaptiveSystem.addSystem(self.managedSystem)



        return self.adaptiveSystem


    def _generateProcesses(self):
        """Function to parse the AADL processes."""

        # Find all matches with "process" followed by any word
        pattern = r'process\s+([\w:]+)'
        matches = re.findall(pattern, self.logicalArchitectureAADL, re.DOTALL)
        # Filter out matches containing "implementation"
        filtered_matches = [match for match in matches if "implementation" not in match]
        # Generate process components for each of the matches
        for match in filtered_matches:
            p = process(name=match, description=match+" component")

            # add features to the process
            pattern = r"process " + match + "(.*?)end " + match + ";"
            matches = re.findall(pattern, self.logicalArchitectureAADL, re.DOTALL)
            feature_pattern = r'(\w+):\s+(in|out)\s+(event|data|event data)\s+port\s+([\w:]+);'
            matches = re.findall(feature_pattern, matches[0], re.DOTALL)
            for feature in matches:
                # Lambda function to find an object by name
                find_by_name = lambda name: next((item for item in self.messages if item.name == name), None)

                if feature[1] == "in":
                    f = inport(name=feature[0], type=feature[2], message=find_by_name(feature[3].split("::")[1]))
                    p.addFeature(f)
                elif feature[1] == "out":
                    f = outport(name=feature[0], type=feature[2], message=find_by_name(feature[3].split("::")[1]))
                    p.addFeature(f)

            # add threads to the process
            try:
                pattern = r"process implementation " + match + ".impl(.*?)end " + match + ".impl;"
                matches = re.findall(pattern, self.logicalArchitectureAADL, re.DOTALL)
                thread_pattern = r'(\w+): thread\s+([\w:]+);'
                threadComponents = re.findall(thread_pattern, matches[0], re.DOTALL)
                featureList=[]
                #fetch thread content
                for t in threadComponents:
                    pattern = r"thread " + t[0] + "(.*?)end " + t[0] + ";"
                    matches = re.findall(pattern, self.logicalArchitectureAADL, re.DOTALL)
                    matches = re.findall(feature_pattern, matches[0], re.DOTALL)
                    for feature in matches:
                        # Lambda function to find an object by name
                        find_by_name = lambda name: next((item for item in self.messages if item.name == name), None)

                        if feature[1] == "in":
                            f = inport(name=feature[0], type=feature[2],message=find_by_name(feature[3].split("::")[1]))
                            featureList.append(f)
                        elif feature[1] == "out":
                            f = outport(name=feature[0], type=feature[2],message=find_by_name(feature[3].split("::")[1]))
                            featureList.append(f)

                th = thread(name=t[0], featureList=featureList)
                p.addThread(th)

            except:
                print("Process "+ match + " does not have an implementation")



            self.processes.append(p)
            # add to the managing system or managed system
            if 'monitor' in p.name or 'analysis' in p.name or 'plan' in p.name or 'legitimate' in p.name or 'execute' in p.name:        #TODO: check if this is ok for the user
                self.managingSystem.addProcess(p)
            elif 'knowledge' not in p.name:
                self.managedSystem.addProcess(p)
        return self.processes

    def _generateMessages(self):
        """Function to parse the AADL messages."""

        # Gind all matches with the "data" pattern
        pattern = r"data (\w+)(.*?)end \1;"
        matches = re.findall(pattern, self.messagesAADL, re.DOTALL)
        for match in matches:
            name = match[0]

            # --- SIMPLE MESSAGES, EXTRACT FEATURES
            feature_pattern = r"(\w+): provides data access ([\w:]+);"
            features = re.findall(feature_pattern, match[1])
            featureList = []
            for feature in features:
                if '::' in feature[1]:
                    f = data(name=feature[0], dataType=feature[1].split("::")[1])
                else:
                    f = data(name=feature[0], dataType=feature[1])
                featureList.append(f)
            m = message(name=name, featureList=featureList)
            self.messages.append(m)
        return self.messages


class robochart_parser:
    """This is a parser that parses muliple robochart files, as input for the AADL code generator.

        :param [MAPLEK]: [Path to the MAPLE-K roboChart model], defaults to [None]
        :type [MAPLEK]: [string](, optional)

        :param [Monitor]: [Path to the Monitor roboChart model], defaults to [None]
        :type [Monitor]: [string](, optional)

        :param [Analysis]: [Path to the Analysis roboChart model], defaults to [None]
        :type [Analysis]: [string](, optional)

        :param [Plan]: [Path to the Plan roboChart model], defaults to [None]
        :type [Plan]: [string](, optional)

        :param [Legitimate]: [Path to the Legitimate roboChart model], defaults to [None]
        :type [Legitimate]: [string](, optional)

        :param [Execute]: [Path to the Execute roboChart model], defaults to [None]
        :type [Execute]: [string](, optional)

        :param [Knowledge]: [Path to the Knowledge roboChart model], defaults to [None]
        :type [Knowledge]: [string](, optional)

        """
    def __init__(self, MAPLEK,Monitor,Analysis,Plan,Legitimate,Execute,Knowledge):
        """Constructor method
        """
        currentDir = os.path.dirname(os.path.abspath(__file__))
        metamodelPath = os.path.join(currentDir, 'robochart/robochart.tx')
        self.robochart_meta = metamodel_from_file(metamodelPath)

        self.maplek_model = None
        self.monitor_model = None
        self.analysis_model = None
        self.plan_model = None
        self.legitimate_model = None
        self.execute_model = None
        self.knowledge_model = None

        # Read the MAPLE-K robochart model
        try:
            self.maplek_model = self.robochart_meta.model_from_file(MAPLEK)
        except FileNotFoundError:
            self.maplek_model = None
            print(f"Error: File '{MAPLEK}' not found.")
            sys.exit(1)

        # Read the Monitor robochart model
        try:
            self.monitor_model = self.robochart_meta.model_from_file(Monitor)
        except FileNotFoundError:
            self.monitor_model = None
            print(f"Error: File '{Monitor}' not found.")
            sys.exit(1)

        # Read the Analysis robochart model
        try:
            self.analysis_model = self.robochart_meta.model_from_file(Analysis)
        except FileNotFoundError:
            self.analysis_model = None
            print(f"Error: File '{Analysis}' not found.")
            sys.exit(1)

        # Read the Plan robochart model
        try:
            self.plan_model = self.robochart_meta.model_from_file(Plan)
        except FileNotFoundError:
            self.plan_model = None
            print(f"Error: File '{Plan}' not found.")
            sys.exit(1)

        # Read the Legitimate robochart model
        try:
            self.legitimate_model = self.robochart_meta.model_from_file(Legitimate)
        except FileNotFoundError:
            self.legitimate_model = None
            print(f"Error: File '{Legitimate}' not found.")
            sys.exit(1)

        # Read the Execute robochart model
        try:
            self.execute_model = self.robochart_meta.model_from_file(Execute)
        except FileNotFoundError:
            self.execute_model = None
            print(f"Error: File '{Execute}' not found.")
            sys.exit(1)

        # Read the Knowledge robochart model
        try:
            self.knowledge_model = self.robochart_meta.model_from_file(Knowledge)
        except FileNotFoundError:
            self.knowledge_model = None
            print(f"Error: File '{Knowledge}' not found.")
            sys.exit(1)