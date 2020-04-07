#! /usr/bin/env python
"""
This module provides classes for querying Microsoft's Academic Knowledge API.
Read more at: https://docs.microsoft.com/en-us/azure/cognitive-services/academic-knowledge
"""
from enum import Enum

import json

class Error(Exception):
    """Base class for any Request error."""

class FormatError(Error):
    """A value is not of the expected type."""

class RequiredArgumentError(Error):
    """A required argument is not specified."""

class QueryTypeError(Error):
    """The query type specified is either not support nor valid."""

class AcademicEncoder(json.JSONEncoder):
    """
    An extended version of JSONEncoder in order to properly
    serialize Academic objects
    """
    def default(self, obj): # pylint: disable=E0202
        if isinstance(obj, AcademicObject):
            return obj.as_dict()
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

class Entities(Enum):
    """
    An enumeration class for the entities available at Microsoft's Academic Knowledge API
    """
    PAPER = 0
    AUTHOR = 1
    JOURNAL = 2
    CONFERENCE_SERIES = 3
    CONFERENCE_INSTANCE = 4
    AFFILIATION = 5
    FIELD_OF_STUDY = 6

class AcademicObject(object):
    """
    An abstract class that is used to define common methods
    for other classes defined for the Microsoft's Academic Knowledge API.
    The class provides basic dictionary-like behavior.
    """
    def __init__(self):
        self.attrs = {}

    def __getitem__(self, key):
        if key in self.attrs:
            return self.attrs[key][0]
        else:
            for attr in self.attrs:
                if self.attrs[attr][1] == key:
                    return self.attrs[attr][0]
        return None

    def __len__(self):
        return len(self.attrs)

    def __setitem__(self, key, item):
        if key in self.attrs:
            self.attrs[key][0] = item
        else:
            for attr in self.attrs:
                if self.attrs[attr][1] == key:
                    self.attrs[attr][0] = item
                    break
            #self.attrs[key] = [item, key, len(self.attrs)]

    def __delitem__(self, key):
        if key in self.attrs:
            del self.attrs[key]
        else:
            for attr in self.attrs:
                if self.attrs[attr][1] == key:
                    del self.attrs[attr]

    def as_dict(self):
        """
        Returns the object as a dictionary.
        """
        return dict([(key, value[0]) for key, value in self.attrs.items()])

    def as_json(self, ensure_ascii=True, indent=None, separators=None, sort_keys=False):
        """
        Returns the object in JSON format.
        All the optional arguments are passed to json.dumps().
        """
        return json.dumps(
            self.as_dict(),
            ensure_ascii=ensure_ascii,
            indent=indent,
            separators=separators,
            sort_keys=sort_keys,
            cls=AcademicEncoder
        )

class AcademicPaper(AcademicObject):
    """
    A class representing an article listed on Microsoft's Academic Knowledge API.
    """
    def __init__(self):
        AcademicObject.__init__(self)
        # The triplets for each keyword correspond to
        # (0) the actual value,
        # (1) the field name for MAKA,
        # (2) a user-suitable label for the item, and
        # (3) an ordering index.
        self.attrs = {
            'id':             [0,    'Id',  'ID',             0],  # pylint: disable-msg=C0326
            'title':          [None, 'Ti',  'Title',          1],  # pylint: disable-msg=C0326
            'authors':        [None, 'AA',  'Authors',        2],  # pylint: disable-msg=C0326
            'year':           [0,    'Y',   'Year',           3],  # pylint: disable-msg=C0326
            'date':           [None, 'D',   'Date',           4],  # pylint: disable-msg=C0326
            'num_citations':  [0,    'CC',  'Nbr of Cites',   5],  # pylint: disable-msg=C0326
            'cites':          [[],   'Ci',  'Cites',          6],  # pylint: disable-msg=C0326
            'field_of_study': [None, 'F',   'Field of Study', 7],  # pylint: disable-msg=C0326
            'journal':        [None, 'J',   'Journal',        8],  # pylint: disable-msg=C0326
            'conference':     [None, 'C',   'Conference',     9],  # pylint: disable-msg=C0326
            'references':     [None, 'RId', 'References',     10], # pylint: disable-msg=C0326
            'excerpt':        [None, 'W',   'Excerpt',        11], # pylint: disable-msg=C0326
            'metadata':       [None, 'E',   'Metadata',       12], # pylint: disable-msg=C0326
            'doi':            [None, 'DOI', 'DOI',            13], # pylint: disable-msg=C0326
            'display_name':   [None, 'DN',  'Display Name',   14], # pylint: disable-msg=C0326
        }

class AcademicPaperMetadata(AcademicObject):
    """
    A class representing the metadata for articles listed on Microsoft's Academic Knowledge API.
    """
    def __init__(self):
        AcademicObject.__init__(self)
        # The triplets for each keyword correspond to
        # (0) the actual value,
        # (1) the field name for MAKA,
        # (2) a user-suitable label for the item, and
        # (3) an ordering index.
        self.attrs = {
            'name':              [None, 'DN',  'Display Name',      0], # pylint: disable-msg=C0326
            'sources':           [None, 'S',   'Sources',           1], # pylint: disable-msg=C0326
            'venue':             [None, 'VFN', 'Venue',             2], # pylint: disable-msg=C0326
            'volume':            [0,    'V',   'Volume',            3], # pylint: disable-msg=C0326
            'issue':             [0,    'I',   'Issue',             4], # pylint: disable-msg=C0326
            'first_page':        [None, 'FP',  'First Page',        5], # pylint: disable-msg=C0326
            'last_page':         [None, 'LP',  'Last Page',         6], # pylint: disable-msg=C0326
            'doi':               [None, 'DOI', 'Digital Object Id', 7], # pylint: disable-msg=C0326
            'citation_contexts': [None, 'CC',  'Citation Contexts', 8], # pylint: disable-msg=C0326
            'inverted_abstract': [None, 'IA',  'Inverted Abstract', 9]  # pylint: disable-msg=C0326
        }

class AcademicAuthor(AcademicObject):
    """
    A class representing an author retrieved from Microsoft's Academic Knowledge API.
    """
    def __init__(self):
        AcademicObject.__init__(self)
        # The triplets for each keyword correspond to
        # (0) the actual value,
        # (1) the field name for MAKA,
        # (2) a user-suitable label for the item, and
        # (3) an ordering index.
        self.attrs = {
            'id':            [0,    'AuId', 'ID',              0], # pylint: disable-msg=C0326
            'name':          [None, 'AuN',  'Normalized Name', 1], # pylint: disable-msg=C0326
            'display_name':  [None, 'DAuN', 'Name',            2], # pylint: disable-msg=C0326
            'num_citations': [0,    'CC',   'Citations',       3], # pylint: disable-msg=C0326
            'metadata':      [None, 'E',    'Metadata',        4]  # pylint: disable-msg=C0326
        }

class AcademicAuthorMetadata(AcademicObject):
    """
    A class representing the metadata for authors
    retrieved from Microsoft's Academic Knowledge API.
    """
    def __init__(self):
        AcademicObject.__init__(self)
        # The triplets for each keyword correspond to
        # (0) the actual value,
        # (1) the field name for MAKA,
        # (2) a user-suitable label for the item, and
        # (3) an ordering index.
        self.attrs = {
            'affiliation': [None, 'LKA', 'Affiliation', 0]
        }

class AcademicAffiliation(AcademicObject):
    """
    A class representing an affiliation of authors
    retrieved from Microsoft's Academic Knowledge API.
    """
    def __init__(self):
        AcademicObject.__init__(self)
        # The triplets for each keyword correspond to
        # (0) the actual value,
        # (1) the field name for MAKA,
        # (2) a user-suitable label for the item, and
        # (3) an ordering index.
        self.attrs = {
            'id':            [0,    'AfId', 'ID',              0], # pylint: disable-msg=C0326
            'name':          [None, 'AfN',  'Normalized Name', 1], # pylint: disable-msg=C0326
            'display_name':  [None, 'DAfN', 'Name',            2], # pylint: disable-msg=C0326
            'num_citations': [0,    'CC',   'Citations',       3], # pylint: disable-msg=C0326
            'metadata':      [None, 'E',    'Metadata',        4]  # pylint: disable-msg=C0326
        }

class AcademicAffiliationMetadata(AcademicObject):
    """
    A class representing the metadata for an affiliation of authors
    retrieved from Microsoft's Academic Knowledge API.
    """
    def __init__(self):
        AcademicObject.__init__(self)
        # The triplets for each keyword correspond to
        # (0) the actual value,
        # (1) the field name for MAKA,
        # (2) a user-suitable label for the item, and
        # (3) an ordering index.
        self.attrs = {
            'paper_count': [None, 'PC', 'Paper Count', 0]
        }

class AcademicFieldOfStudy(AcademicObject):
    """
    A class representing an affiliation of authors
    retrieved from Microsoft's Academic Knowledge API.
    """
    def __init__(self):
        AcademicObject.__init__(self)
        # The triplets for each keyword correspond to
        # (0) the actual value,
        # (1) the field name for MAKA,
        # (2) a user-suitable label for the item, and
        # (3) an ordering index.
        self.attrs = {
            'id':              [0,    'FId', 'ID',                 0], # pylint: disable-msg=C0326
            'name':            [None, 'FN',  'Normalized Name',    1], # pylint: disable-msg=C0326
            'display_name':    [None, 'DFN', 'Name',               2], # pylint: disable-msg=C0326
            'num_citations':   [0,    'CC',  'Citations',          3], # pylint: disable-msg=C0326
            'hierarchy_level': [0,    'FL',  'Level in hierarchy', 4], # pylint: disable-msg=C0326
            'parent':          [None, 'FP',  'Parent',             5], # pylint: disable-msg=C0326
            'children':        [None, 'FC',  'Children',           6]  # pylint: disable-msg=C0326
        }

class AcademicConferenceSeries(AcademicObject):
    """
    A class representing a conference serie
    available at Microsoft's Academic Knowledge API.
    """
    def __init__(self):
        AcademicObject.__init__(self)
        # The triplets for each keyword correspond to
        # (0) the actual value,
        # (1) the field name for MAKA,
        # (2) a user-suitable label for the item, and
        # (3) an ordering index.
        self.attrs = {
            'id':             [0,    'Id',  'ID',              0], # pylint: disable-msg=C0326
            'name':           [None, 'CN',  'Normalized Name', 1], # pylint: disable-msg=C0326
            'display_name':   [None, 'DCN', 'Name',            2], # pylint: disable-msg=C0326
            'num_citations':  [0,    'CC',  'Citations',       3], # pylint: disable-msg=C0326
            'field_of_study': [None, 'F',   'Field of Study',  4]  # pylint: disable-msg=C0326
        }

class AcademicConferenceInstance(AcademicObject):
    """
    A class representing a conference instance
    retrieved from Microsoft's Academic Knowledge API.
    """
    def __init__(self):
        AcademicObject.__init__(self)
        # The triplets for each keyword correspond to
        # (0) the actual value,
        # (1) the field name for MAKA,
        # (2) a user-suitable label for the item, and
        # (3) an ordering index.
        self.attrs = {
            'id':                [0,    'Id',   'ID',                0], # pylint: disable-msg=C0326
            'name':              [None, 'CIN',  'Normalized Name',   1], # pylint: disable-msg=C0326
            'display_name':      [None, 'DCN',  'Name',              2], # pylint: disable-msg=C0326
            'location':          [None, 'CIL',  'Location',          3], # pylint: disable-msg=C0326
            'start_date':        [None, 'CISD', 'Start Date',        4], # pylint: disable-msg=C0326
            'end_date':          [None, 'CIED', 'End Date',          5], # pylint: disable-msg=C0326
            'conference_series': [None, 'PCS',  'Conference Series', 6], # pylint: disable-msg=C0326
            'num_citations':     [0,    'CC',   'Citations',         7]  # pylint: disable-msg=C0326
        }

class AcademicConferenceInstanceMetadata(AcademicObject):
    """
    A class representing the metadata for a conference instance
    retrieved from Microsoft's Academic Knowledge API.
    """
    def __init__(self):
        AcademicObject.__init__(self)
        # The triplets for each keyword correspond to
        # (0) the actual value,
        # (1) the field name for MAKA,
        # (2) a user-suitable label for the item, and
        # (3) an ordering index.
        self.attrs = {
            'full_name': [None, 'FN', 'Full Name', 0]
        }

class AcademicJournal(AcademicObject):
    """
    A class representing a journal instance
    retrieved from Microsoft's Academic Knowledge API.
    """
    def __init__(self):
        AcademicObject.__init__(self)
        # The triplets for each keyword correspond to
        # (0) the actual value,
        # (1) the field name for MAKA,
        # (2) a user-suitable label for the item, and
        # (3) an ordering index.
        self.attrs = {
            'id':                [0,    'Id',   'ID',                0], # pylint: disable-msg=C0326
            'name':              [None, 'JN',   'Normalized Name',   1], # pylint: disable-msg=C0326
            'display_name':      [None, 'DJN',  'Name',              2], # pylint: disable-msg=C0326
            'num_citations':     [0,    'CC',   'Citations',         3]  # pylint: disable-msg=C0326
        }

class AcademicInterpretation(AcademicObject):
    """
    A class representing an interpretation of a query
    retrieved from Microsoft's Academic Knowledge API.
    """
    def __init__(self):
        AcademicObject.__init__(self)
        # The triplets for each keyword correspond to
        # (0) the actual value,
        # (1) the field name for MAKA,
        # (2) a user-suitable label for the item, and
        # (3) an ordering index.
        self.attrs = {
            'parse': [None, 'parse', 'Parsing Explanation', 0], # pylint: disable-msg=C0326
            'rules': [None, 'rules', 'Rules',               1]  # pylint: disable-msg=C0326
        }

class AcademicInterpretationRule(AcademicObject):
    """
    A class representing an interpretation's rule for an interpretation
    retrieved from Microsoft's Academic Knowledge API.
    """
    def __init__(self):
        AcademicObject.__init__(self)
        # The triplets for each keyword correspond to
        # (0) the actual value,
        # (1) the field name for MAKA,
        # (2) a user-suitable label for the item, and
        # (3) an ordering index.
        self.attrs = {
            'name':  [None, 'name',  'Name',  0], # pylint: disable-msg=C0326
            'type':  [None, 'type',  'Type',  1], # pylint: disable-msg=C0326
            'value': [None, 'value', 'Value', 2]  # pylint: disable-msg=C0326
        }

class AcademicHistogram(AcademicObject):
    """
    A class representing an histogram of an attribute
    retrieved from Microsoft's Academic Knowledge API.
    """
    def __init__(self):
        AcademicObject.__init__(self)
        # The triplets for each keyword correspond to
        # (0) the actual value,
        # (1) the field name for MAKA,
        # (2) a user-suitable label for the item, and
        # (3) an ordering index.
        self.attrs = {
            'attribute': [None, 'attribute',       'Attribute', 0], # pylint: disable-msg=C0326
            'values':    [None, 'distinct_values', 'Values',    1], # pylint: disable-msg=C0326
            'count':     [None, 'total_count',     'Count',     2], # pylint: disable-msg=C0326
            'data':      [None, 'data',            'Data',      3]  # pylint: disable-msg=C0326
        }

class AcademicHistogramValue(AcademicObject):
    """
    A class representing the value of an attribute of an histogram
    retrieved from Microsoft's Academic Knowledge API.
    """
    def __init__(self):
        AcademicObject.__init__(self)
        # The triplets for each keyword correspond to
        # (0) the actual value,
        # (1) the field name for MAKA,
        # (2) a user-suitable label for the item, and
        # (3) an ordering index.
        self.attrs = {
            'value':       [None, 'value', 'Values',      0], # pylint: disable-msg=C0326
            'probability': [None, 'prob',  'Probability', 1], # pylint: disable-msg=C0326
            'count':       [None, 'count', 'Count',       2]  # pylint: disable-msg=C0326
        }

class AcademicParser(object):
    """
    Default parser for Academic objects
    """
    @staticmethod
    def _parse(response, cls=None):
        target = cls()
        for key in response.keys():
            value = response[key]
            target[key] = value
        return target

class AcademicPaperParser(AcademicParser):
    """
    Parser for AcademicPaper objects
    """
    @staticmethod
    def parse(response):
        target = AcademicPaper()
        for key in response.keys():
            value = response[key]
            if key == 'AA':
                target[key] = [AcademicAuthorParser.parse(author) for author in value]
            elif key == 'F':
                target[key] = [AcademicParser._parse(fos, AcademicFieldOfStudy) for fos in value]
            elif key == 'E':
                if isinstance(value, str):
                    value = json.loads(value)
                target[key] = AcademicParser._parse(value, AcademicPaperMetadata)
            elif key == 'logprob':
                continue #ignore
            else:
                target[key] = value
        return target

class AcademicAuthorParser(AcademicParser):
    """
    Parser for AcademicAuthor objects
    """
    @staticmethod
    def parse(response):
        target = AcademicAuthor()
        for key in response.keys():
            value = response[key]
            if key == 'FN':
                target[key] = [AcademicParser._parse(fos, AcademicFieldOfStudy) for fos in value]
            elif key == 'E':
                if isinstance(value, str):
                    value = json.loads(value)
                target[key] = AcademicParser._parse(value, AcademicPaperMetadata)
            elif key == 'logprob':
                continue #ignore
            else:
                target[key] = value
        return target

class AcademicInterpretationParser(AcademicParser):
    """
    Parser for AcademicInterpretation objects
    """
    @staticmethod
    def parse(response):
        target = AcademicInterpretation()
        target['parse'] = response['parse']
        target['rules'] = [AcademicInterpretationRuleParser.parse(rule)
                           for rule in response['rules']]
        return target

class AcademicInterpretationRuleParser(AcademicParser):
    """
    Parser for AcademicInterpretationRule objects
    """
    @staticmethod
    def parse(response):
        target = AcademicInterpretationRule()
        target['name'] = response['name']
        target['type'] = response['output']['type']
        target['value'] = response['output']['value']
        return target

class AcademicHistogramParser(AcademicParser):
    """
    Parser for AcademicHistogramAttribute objects
    """
    @staticmethod
    def parse(response):
        target = AcademicHistogram()
        target['attribute'] = response['attribute']
        target['values'] = response['distinct_values']
        target['count'] = response['total_count']
        target['data'] = [AcademicParser._parse(val, AcademicHistogramValue)
                          for val in response['histogram']]
        return target
