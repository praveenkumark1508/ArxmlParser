#!/home/praveen/anaconda3/bin/python3.6
r'''
Arxml parser.
This module gives data model of comunication details in an arxml.
'''

from lxml import etree

namespaces = {'a':'http://autosar.org/3.2.3',
              'b':'http://www.w3.org/2001/XMLSchema-instance'}

def parse_element(parse_func):
    '''
    Decorator for parse functions
    '''
    def wrapper(obj, element):
        '''
        Wrapper to parse all the child elements using the parse_func
        '''
        if element.tag in obj.parse_list:
            parse_func(obj, element)
        else:
            for child in element:
                wrapper(obj, child)

    return wrapper

class BaseParser:
    '''
    Base class for parsers
    '''
    parse_list = {'{'+namespaces['a']+'}'+'SHORT-NAME':'name',
                  '{'+namespaces['a']+'}'+'FRAME-LENGTH':'length',
                  '{'+namespaces['a']+'}'+'LENGTH':'length'}

    def __init__(self, element, datamodel):
        self.element = element
        self.datamodel = datamodel

    def getname(self):
        '''
        Get the name of the container
        '''
        return self.element.find('./a:SHORT-NAME', namespaces)

    def setattribute(self, childelement):
        '''
        Set the attributes of the container
        '''
        self.datamodel[self.parse_list[childelement.tag]] = childelement.text

    def parse(self):
        '''
        Parse the element
        '''
        self.parse_children(self.element)

    @parse_element
    def parse_children(self, element):
        '''
        Parsing function
        '''
        try:
            self.parse_list[element.tag](element)
        except TypeError:
            self.setattribute(element)

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

class ISignalParser(BaseParser):
    pass

class SystemSignalParser(BaseParser):
    pass

class CompuMethodParser(BaseParser):
    pass

class IPduParser(BaseParser):
    pass

class FrameParser(BaseParser):
    pass

class PhysicalChannelParser(BaseParser):
    pass

class MainParser:
    '''
    Manager class for parsing the arxml
    '''
    parse_list = {'{'+namespaces['a']+'}'+'I-SIGNAL':ISignalParser,
                  '{'+namespaces['a']+'}'+'SYSTEM-SIGNAL':SystemSignalParser,
                  '{'+namespaces['a']+'}'+'COMPU-METHOD':CompuMethodParser,
                  '{'+namespaces['a']+'}'+'SIGNAL-I-PDU':IPduParser,
                  '{'+namespaces['a']+'}'+'FRAME':FrameParser,
                  '{'+namespaces['a']+'}'+'PHYSICAL-CHANNEL':PhysicalChannelParser}

    def __init__(self, filename):
        self.filename = filename
        self.xmldoc = etree.parse(self.filename)
        self.root = self.xmldoc.getroot()
        self.datamodel = DataModel()

    def parse(self):
        '''
        Parse the complete arxml
        '''
        self.parse_children(self.root)

    @parse_element
    def parse_children(self, element):
        '''
        Parse function for Manager class
        '''
        parser = self.parse_list[element.tag](element, self.datamodel)
        parser.parse()
