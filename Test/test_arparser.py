#test_arparser.py
'''
Test module for testing the arparser
'''

from unittest import TestCase
import sys

sys.path.append('..')
from ARParser import arparser

class TestMainParser(TestCase):
    '''
    Test case for MainPareser class
    '''
    def setUp(self):
        self.obj = arparser.MainParser('Test/EcuExtract.arxml')

    def test_parser(self):
        self.obj.parse(self.obj.root)

