#**********************************************************************************
# * Copyright (C) 2024-present Bert Van Acker (B.MKR) <bert.vanacker@uantwerpen.be>
# *
# * This file is part of the roboarch R&D project.
# *
# * RAP R&D concepts can not be copied and/or distributed without the express
# * permission of Bert Van Acker
# **********************************************************************************
import json

class namedObject(object):

    def __init__(self, name='tbd', description='tbd', verbose=False):
        self._name = name
        self._description = description
        self._verbose = verbose

    @property
    def name(self):
        """The name property (read-only)."""
        return self._name

    @property
    def description(self):
        """The description property (read-only)."""
        return self._description




class process(namedObject):

    def __init__(self, name='tbd',description='tbd',verbose=False,featureList = None,threadList=None,formalism="python",containerization=False):
        super().__init__(name=name, description=description, verbose=verbose)

        if featureList is not None:
            self._featureList = featureList
        else:
            self._featureList = []

        if threadList is not None:
            self._threadList = threadList
        else:
            self._threadList = []

        self._formalism = formalism
        self._containerization = containerization

    @property
    def features(self):
        return self._featureList

    def addFeature(self, feature):
        """Add a feature to the system """
        self._featureList.append(feature)

    @property
    def threads(self):
        return self._threadList

    def addThread(self, t):
        """Add a thread to the system """
        self._threadList.append(t)

    @property
    def formalism(self):
        return self._formalism

    @formalism.setter
    def formalism(self,f):
        self._formalism = f

    @property
    def containerization(self):
        return self._containerization

    @containerization.setter
    def containerization(self,c):
        self._containerization = c

class thread(namedObject):

    def __init__(self, name='tbd',description='tbd',verbose=False,featureList = None,eventTrigger=None):
        super().__init__(name=name, description=description, verbose=verbose)

        if featureList is not None:
            self._featureList = featureList
        else:
            self._featureList = []

        self._eventTrigger = eventTrigger

    @property
    def features(self):
        return self._featureList
    def addFeature(self, feature):
        """Add a feature to the system """
        self._featureList.append(feature)

    @property
    def eventTrigger(self):
        return self._eventTrigger

class characteristic(namedObject):

    def __init__(self, name='tbd',description='tbd',verbose=False,value="",dataType='-'):
        super().__init__(name=name, description=description, verbose=verbose)

        self._value = value
        self._dataType = dataType

class event(namedObject):

    def __init__(self, name='tbd',description='tbd',verbose=False):
        super().__init__(name=name, description=description, verbose=verbose)

class mode(namedObject):

    def __init__(self, name='tbd',description='tbd',verbose=False,callback = None):
        super().__init__(name=name, description=description, verbose=verbose)

        self._callback = callback

    @property
    def callback(self):
        """The callback property (read-only)."""
        return self._callback

class transition(namedObject):

    def __init__(self, name='tbd',description='tbd',verbose=False,callback = None,source=None,destination=None):
        super().__init__(name=name, description=description, verbose=verbose)

        self._source = source
        self._destination = destination
        self._callback = callback

    @property
    def source(self):
        """The source (read-only)."""
        return self._source

    @property
    def destination(self):
        """The source (read-only)."""
        return self._destination

    @property
    def callback(self):
        """The callback property (read-only)."""
        return self._callback

class feature(namedObject):

    def __init__(self, name='tbd',description='tbd',verbose=False,featureType="feature"):
        super().__init__(name=name, description=description, verbose=verbose)

        self._featureType = featureType

    @property
    def featureType(self):
        return self._featureType

    @featureType.setter
    def featureType(self,type):
        self._featureType = type

class port(feature):

    def __init__(self, name='tbd',description='tbd',initialValue = 1.0,valueReference=1,type='data',message=None,verbose=False):
        super().__init__(name=name, description=description, verbose=verbose)

        self._featureType = 'port'
        self._initialValue = initialValue
        self._valueReference = valueReference
        self._type = type
        self._message = message


    @property
    def value(self):
        """The value property (read)."""
        return self._initialValue

    @value.setter
    def value(self,value):
        """The value property (write)."""
        self._initialValue = value

    @property
    def valueReference(self):
        """The valueReference property (read)."""
        return self._valueReference

    @valueReference.setter
    def valueReference(self, value):
        """The valueReference property (write)."""
        self._valueReference = value

    @property
    def type(self):
        """The type property (read-only)."""
        return self._type

    @property
    def message(self):
        """The message property"""
        return self._message

class inport(port):
    def __init__(self, name='tbd',description='tbd',initialValue = 1.0,valueReference=1,type='data',verbose=False,message=None):
        super().__init__(name=name, description=description, verbose=verbose,initialValue=initialValue,valueReference=valueReference,type=type,message=message)

        self._featureType = 'inport'
class outport(port):
    def __init__(self, name='tbd',description='tbd',initialValue = 1.0,valueReference=1,type='data',verbose=False,message=None):
        super().__init__(name=name, description=description, verbose=verbose,initialValue=initialValue,valueReference=valueReference,type=type,message=message)

        self._featureType = 'outport'

class connection(namedObject):

    def __init__(self, name='tbd',description='tbd',verbose=False,source=None,destination=None):
        super().__init__(name=name, description=description, verbose=verbose)

        self._source = source
        self._destination = destination

    @property
    def source(self):
        """The source (read-only)."""
        return self._source

    @property
    def destination(self):
        """The source (read-only)."""
        return self._destination

class message(namedObject):

    def __init__(self, name='tbd',description='tbd',verbose=False,featureList = None):
        super().__init__(name=name, description=description, verbose=verbose)

        if featureList is not None:
            self._featureList = featureList
        else:
            self._featureList = []

    @property
    def features(self):
        return self._featureList

    def addFeature(self, feature):
        """Add a feature to the system """
        self._featureList.append(feature)

class data(feature):

    def __init__(self, name='tbd',description='tbd',dataType='Float_64',verbose=False):
        super().__init__(name=name, description=description, verbose=verbose)

        self._dataType = dataType

    @property
    def dataType(self):
        return self._dataType

class processor(namedObject):

    def __init__(self,name='tbd', description='tbd', verbose=False,featureList = None,propertyList = None, bindingList=None,IP="localhost"):
        super().__init__(name=name,description = description,verbose=verbose)

        if featureList is not None:
            self._featureList = featureList
        else:
            self._featureList = []
        if propertyList is not None:
            self._propertyList = propertyList
        else:
            self._propertyList = []
        if bindingList is not None:
            self._bindingList = bindingList
        else:
            self._bindingList = []
        self._IP = IP
        self.rap_backbone = False


    def addFeature(self, feature):
        """Add a feature to the system """
        self._featureList.append(feature)

    def addProperty(self, p):
        """Add a property to the system """
        self._propertyList.append(p)

    def addProcessorBinding(self,process):
        """Add a processor binding to the processor """
        self._bindingList.append(process)

    @property
    def processorBinding(self):
        return self._bindingList

    @property
    def IP(self):
        return self._IP

    @IP.setter
    def IP(self,ip):
        self._IP = ip

    @property
    def runs_rap_backbone(self):
        return self.rap_backbone

    @runs_rap_backbone.setter
    def runs_rap_backbone(self, flag):
        self.rap_backbone = flag



class memory(namedObject):

    def __init__(self,name='tbd', description='tbd', verbose=False,propertyList = None):
        super().__init__(name=name,description = description,verbose=verbose)

        if propertyList is not None:
            self._propertyList = propertyList
        else:
            self._propertyList = []

    def addProperty(self, p):
        """Add a property to the system """
        self._propertyList.append(p)

class bus(namedObject):

    def __init__(self,name='tbd', description='tbd', verbose=False,propertyList = None):
        super().__init__(name=name,description = description,verbose=verbose)

        if propertyList is not None:
            self._propertyList = propertyList
        else:
            self._propertyList = []

        self._connectionList = []

    def addProperty(self, p):
        """Add a property to the bus """
        self._propertyList.append(p)

    def addConnection(self, p):
        """Add a connection to the bus """
        self._connectionList.append(p)


class system(namedObject):

    def __init__(self,name='tbd', description='tbd', verbose=False,systemList = None,processList = None,featureList=None,messageList=None,processorList=None,JSONDescriptor=None):
        super().__init__(name=name,description = description,verbose=verbose)

        if featureList is not None:
            self._featureList = featureList
        else:
            self._featureList = []
        if systemList is not None:
            self._systemList = systemList
        else:
            self._systemList = []
        if processList is not None:
            self._processList = processList
        else:
            self._processList = []
        if messageList is not None:
            self._messageList = messageList
        else:
            self._messageList = []
        if processorList is not None:
            self._processorList = processorList
        else:
            self._processorList = []


        if JSONDescriptor is not None:
            self.json2object(JSONDescriptor=JSONDescriptor)

    def addProcess(self,process):
        """Add a process to the process list """
        self._processList.append(process)

    @property
    def processes(self):
        return self._processList

    @property
    def systems(self):
        return self._systemList
    def addSystem(self,system):
        """Add a system to the system list """
        self._systemList.append(system)

    def addFeature(self,feature):
        """Add a feature to the system """
        self._featureList.append(feature)

    def addMessage(self,message):
        """Add a process to the process list """
        self._messageList.append(message)

    @property
    def messages(self):
        return self._messageList
    @messages.setter
    def messages(self,d):
        self._messageList = d

    def addProcessor(self,processor):
        """Add a processor to the system list """
        self._processorList.append(processor)

    @property
    def processors(self):
        return self._processorList

    def object2json(self,fileName):
        """
               Function to generate a json file
        """
        data = json.dumps(self, default=lambda o: o.__dict__, indent=4)
        with open(fileName, 'w', encoding='utf-8') as f:
            f.write(data)

    def json2object(self, JSONDescriptor='system.json'):
        """
             Function to generate an AADLIL system from a JSON file

             :param string JSONDescriptor: absolute path to the json file for the AADLIL system

        """
        # --interpret JSON file--
        with open(JSONDescriptor, "r") as read_file:
            jsonObject = json.load(read_file)
        # --setup object--
        self._name = jsonObject['_name']
        self._description = jsonObject['_description']
        # -- load messages --
        for m in jsonObject['_messageList']:
            features = []
            for d in m['_featureList']:
                tempD = data(name=d['_name'], dataType=d['_dataType'])
                features.append(tempD)
            tempMessage = message(name=m['_name'], featureList=features)
            self.addMessage(tempMessage)
        # -- load systems and containing processes --
        for s in jsonObject['_systemList']:
            tempS=system(name=s['_name'], description=s['_description'])
            for p in s['_processList']:
                tempP=process(name=p['_name'], description=p['_description'])
                features = []
                for f in p['_featureList']:
                    _m = None
                    for m in self.messages:
                        if f['_message'] is not None:
                            if m.name == f['_message']['_name']:
                                _m = m
                    if f['_featureType'] == 'inport':
                        tempF = inport(name=f['_name'], type=f['_type'], message=_m)
                    elif f['_featureType'] == 'outport':
                        tempF = outport(name=f['_name'], type=f['_type'], message=_m)
                    else:
                        tempF = ''
                    tempP.addFeature(tempF)
                threads = []
                for t in p['_threadList']:
                    Tfeatures = []
                    for f in t['_featureList']:
                        _m = None
                        for m in self.messages:
                            if f['_message'] is not None:
                                if m.name == f['_message']['_name']:
                                    _m = m
                        if f['_featureType'] == 'inport':
                            tempF = inport(name=f['_name'], type=f['_type'], message=_m)
                        elif f['_featureType'] == 'outport':
                            tempF = outport(name=f['_name'], type=f['_type'], message=_m)
                        else:
                            tempF = ''
                        Tfeatures.append(tempF)
                    tempT = thread(name=t["_name"],featureList=Tfeatures,eventTrigger=t["_eventTrigger"])
                    tempP.addThread(tempT)
                tempP.formalism=p['_formalism']
                tempP.containerization=p['_containerization']
                tempS.addProcess(tempP)
            self.addSystem(tempS)
        # -- load processors --
        for s in jsonObject['_systemList']:
            for p in s['_processorList']:
                tempProcessor = processor(name=p['_name'],description=p['_description'])
                tempProcessor.runs_rap_backbone=p['rap_backbone']
                tempProcessor.IP=p['_IP']
                # processor bindings
                for binding in p['_bindingList']:
                    # find the system and append
                    for sys in self.systems:
                        if sys.name == s["_name"]:
                            for comp in sys.processes:
                                if binding["_name"] == comp.name:
                                    tempProcessor.addProcessorBinding(process=comp)
                #processor properties
                for prop in p["_propertyList"]:
                    tempProp = ""
                    #TODO: extend the AADLIL TO SUPPORT PROCESSOR PROPERTIES

                #processor features
                for f in p['_featureList']:
                    _m = None
                    for m in self.messages:
                        if f['_message'] is not None:
                            if m.name == f['_message']['_name']:
                                _m = m
                    if f['_featureType'] == 'inport':
                        tempF = inport(name=f['_name'], type=f['_type'], message=_m)
                    elif f['_featureType'] == 'outport':
                        tempF = outport(name=f['_name'], type=f['_type'], message=_m)
                    elif f['_featureType'] == 'port':
                        tempF = outport(name=f['_name'], type=f['_type'],initialValue=f["_initialValue"],valueReference=f["_valueReference"], message=_m)
                    else:
                        tempF = ''
                    tempProcessor.addFeature(feature=tempF)
                for _s in self.systems:
                    if _s.name == s["_name"]:
                        _s.addProcessor(processor=tempProcessor)

    def __eq__(self, other):
        if not isinstance(other, system):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.__dict__ == other.__dict__
