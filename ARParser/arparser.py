#!/home/praveen/anaconda3/bin/python3.6
r'''
Arxml parser.
This module gives data model of comunication details in an arxml.
'''

from lxml import etree

class BaseParser:
    '''
    Base class for parsers
    '''
    def __init__(self, element, datamodel, nsmap):
        self.element = element
        self.datamodel = datamodel
        self.nsmap = nsmap
        self.parse_dict = {'{'+self.nsmap['default']+'}'+'SHORT-NAME':'name',
                           '{'+self.nsmap['default']+'}'+'FRAME-LENGTH':'length',
                           '{'+self.nsmap['default']+'}'+'LENGTH':'length',
                           '{'+self.nsmap['default']+'}'+'L-2':'description'}

    def getname(self):
        '''
        Get the name of the container
        '''
        return self.element.find('./default:SHORT-NAME', self.nsmap).text

    def setattribute(self, childelement, datamodel):
        '''
        Set the attributes of the container
        '''
        datamodel[self.parse_dict[childelement.tag]] = childelement.text

    def parse_children(self, attribkey):
        datamodel = DataModel()

        for subelement in self.element.iterchildren():
            if subelement.tag in self.parse_dict:
                try:
                    self.parse_dict[subelement.tag](subelement)
                except TypeError:
                    self.setattribute(subelement, datamodel)

        self.datamodel[attribkey].append(datamodel['name'], datamodel)

class DataModel(dict):
    '''
    Data model of the arxml
    '''
    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except KeyError:
            return 'missing'

    def __getattr__(self, attr):
        return self.__getitem__(attr)

    def __repr__(self):
        string = '\n'.join([key for key in self.keys()])
        return string

    def __str__(self):
        string = '\n'.join([key for key in self.keys()])
        return string

    def append(self, name, datamodel):
        '''
        Add the member if the member is not already present. If the member is
        already present, then update its value.
        '''
        if not name in self:
            self[name] = datamodel
        else:
            self[name].update(datamodel)

class ISignalParser(BaseParser):
    def parse(self):
        '''
        Parse the element
        '''
        self.parse_children('signal')

class SystemSignalParser(BaseParser):
    def parse(self):
        '''
        Parse the element
        '''
        self.parse_children('signal')

class CompuMethodParser(BaseParser):
    def parse(self):
        '''
        Parse the element
        '''
        self.parse_children('compumethods')

class IPduParser(BaseParser):
    def parse(self):
        '''
        Parse the element
        '''
        self.parse_children('pdus')

class FrameParser(BaseParser):
    def parse(self):
        '''
        Parse the element
        '''
        self.parse_children('frames')

class PhysicalChannelParser(BaseParser):
    def parse(self):
        '''
        Parse the element
        '''
        self.parse_children('networks')

class MainParser:
    '''
    Manager class for parsing the arxml
    '''
    def __init__(self, filename):
        self.filename = filename
        self.xmldoc = etree.parse(self.filename)
        self.root = self.xmldoc.getroot()
        self.nsmap = self.get_nsmap()
        self.arxmlversion = self.checkarxml()
        self.datamodel = DataModel()
        self.parse_dict = {'{'+self.nsmap['default']+'}'+'I-SIGNAL':ISignalParser,
                           '{'+self.nsmap['default']+'}'+'SYSTEM-SIGNAL':SystemSignalParser,
                           '{'+self.nsmap['default']+'}'+'COMPU-METHOD':CompuMethodParser,
                           '{'+self.nsmap['default']+'}'+'SIGNAL-I-PDU':IPduParser,
                           '{'+self.nsmap['default']+'}'+'FRAME':FrameParser,
                           '{'+self.nsmap['default']+'}'+'PHYSICAL-CHANNEL':PhysicalChannelParser}

    def parse(self):
        '''
        Parse the complete arxml
        '''
        self.prepare_datamodel()
        self.parse_children(self.root, self.datamodel)
        return self.datamodel

    def parse_children(self, element, datamodel):
        '''
        Parse function for Manager class
        '''
        if element.tag in self.parse_dict:
            parser = self.parse_dict[element.tag](element, datamodel, self.nsmap)
            parser.parse()
        else:
            for subelement in element:
                self.parse_children(subelement, datamodel)

    def prepare_datamodel(self):
        '''
        Create the initial parts of the Data Model
        '''
        self.datamodel['networks'] = DataModel()
        self.datamodel['pdus'] = DataModel()
        self.datamodel['signals'] = DataModel()
        self.datamodel['compumethods'] = DataModel()
        self.datamodel['frames'] = DataModel()

    def checkarxml(self):
        '''
        check and validate the Ecu extract
        '''
        #for schema in schemas:
        #if self.xmldoc.xmlschema(schemas[schema]):
        #    get_parsedict(schema)
        #else:
        #    raise InvalidArxml('Schema validation failed')
        return None

    def get_nsmap(self):
        '''
        Obtain the namespace mapping
        '''
        nsmap = self.root.nsmap
        nsmap['default'] = nsmap.pop(None)
        return nsmap

