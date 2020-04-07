"""
Collection of classes used to make requests to the
Microsoft Academic Knowledge site
"""
from enum import Enum

import os
import sys

import requests

import .classes

# Support unicode in both Python 2 and 3. In Python 3, unicode is str.
if sys.version_info[0] == 3:
    unicode = str # pylint: disable-msg=W0622
    encode = lambda s: unicode(s) # pylint: disable-msg=C0103
else:
    def encode(text):
        if isinstance(text, basestring):
            return text.encode('utf-8') # pylint: disable-msg=C0103
        else:
            return str(text)

class AcademicConf(object):
    """
    Helper class for global settings.
    """

    VERSION = 'latest'
    LOG_LEVEL = int(os.getenv('LOG_LEVEL', 1))
    MAX_PAGE_RESULTS = 50
    BASE_URL = 'https://westus.api.cognitive.microsoft.com/academic/v1.0'
    USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0'

class AcademicUtils(object):
    """A wrapper for various utensils that come in handy."""

    LOG_LEVELS = {
        'error': 1,
        'warn':  2,
        'info':  3,
        'debug': 4
    }

    @staticmethod
    def ensure_int(arg, msg=None):
        """
        Validates that the passed arg is an integer.
        Otherwise it raises an exception.
        """
        try:
            return int(arg)
        except ValueError:
            raise classes.FormatError(msg)

    @staticmethod
    def log(level, msg):
        """
        Method to log a message.
        Currently it logs to the system's error fd.
        """
        if level not in AcademicUtils.LOG_LEVELS.keys():
            return
        if AcademicUtils.LOG_LEVELS[level] > AcademicConf.LOG_LEVEL:
            return
        sys.stderr.write('[%5s]  %s' % (level.upper(), msg + '\n'))
        sys.stderr.flush()

class AcademicQueryType(Enum): # pylint: disable=too-few-public-methods
    """
    Enumeration for the types of queries existing in MAKA
    """
    HISTOGRAM = 0
    INTERPRET = 1
    EVALUATE = 2
    SIMILARITY = 3
    GRAPH_TRAVERSAL = 4

class AcademicQuery(object):
    """
    The base class for any kind of results query we send to Microsoft's Academic Knowledge API.
    """
    def __init__(self):
        self.url = None
        self.body = None
        # Queries may have global result attributes, similar to
        # per-article attributes in ScholarArticle. The exact set of
        # attributes may differ by query type, but they all share the
        # basic data structure:
        self.attrs = {}

    def get_url(self):
        """
        Returns a complete, submittable URL string for this particular
        query instance. The URL and its arguments will vary depending
        on the query.
        """
        return None

    def _add_attribute_type(self, key, label, default_value=None):
        """
        Adds a new type of attribute to the list of attributes
        understood by this query. Meant to be used by the constructors
        in derived classes.
        """
        if not self.attrs:
            self.attrs[key] = [default_value, label, 0]
            return
        idx = max([item[2] for item in self.attrs.values()]) + 1
        self.attrs[key] = [default_value, label, idx]

    def __getitem__(self, key):
        """Getter for attribute value. Returns None if no such key."""
        if key in self.attrs:
            return self.attrs[key][0]
        return None

    def __setitem__(self, key, item):
        """Setter for attribute value. Does nothing if no such key."""
        if key in self.attrs:
            self.attrs[key][0] = item

    def _parenthesize_phrases(self, query):
        """
        Turns a query string containing comma-separated phrases into a
        space-separated list of tokens, quoted if containing
        whitespace. For example, input
          'some words, foo, bar'
        becomes
          '"some words" foo bar'
        This comes in handy during the composition of certain queries.
        """
        if query.find(',') < 0:
            return query
        phrases = []
        for phrase in query.split(','):
            phrase = phrase.strip()
            if phrase.find(' ') > 0:
                phrase = '"' + phrase + '"'
            phrases.append(phrase)
        return ' '.join(phrases)


class InterpretQuery(AcademicQuery):
    """
    This class represents a query to the Interpret endpoint
    """
    INTERPRET_URL = AcademicConf.BASE_URL + '/interpret'

    def __init__(self, query=None):
        AcademicQuery.__init__(self)
        self.query = query
        self.complete = 0
        self.count = AcademicConf.MAX_PAGE_RESULTS
        self.offset = 0
        self.timeout = 1000
        self.model = 'latest'

    def set_query(self, value):
        """
        Sets the query used to interpret.
        """
        self.query = value

    def set_complete(self, value):
        """
        Sets the autocomplete option.
        1 means that auto-completion suggestions are generated based on the grammar and graph data.
        """
        msg = 'complete must be numeric'
        self.complete = AcademicUtils.ensure_int(value, msg)

    def set_count(self, value):
        """
        Sets the maximum number of interpretations to return.
        """
        msg = 'count must be numeric'
        self.count = AcademicUtils.ensure_int(value, msg)

    def set_offset(self, value):
        """
        Sets the index of the first interpretation to return.
        """
        msg = 'offset must be numeric'
        self.offset = AcademicUtils.ensure_int(value, msg)

    def set_timeout(self, value):
        """
        Sets the timeout in milliseconds.
        Only interpretations found before the timeout has elapsed are returned.
        """
        msg = 'timeout must be numeric'
        self.timeout = AcademicUtils.ensure_int(value, msg)

    def set_model(self, value):
        """
        Sets the name of the model that you wish to query.
        Currently, the value defaults to "latest".
        """
        self.model = value

    def get_url(self):
        """
        Returns the POST endpoint's URL
        """
        return self.INTERPRET_URL

    def get_body(self):
        """
        Creates and returns the body for the POST request
        """
        if self.query is None:
            raise classes.RequiredArgumentError('Interpret needs a query')

        args = {
            'query': self.query,
            'complete': self.complete,
            'count': self.count,
            'offset': self.offset,
            'timeout': self.timeout,
            'model': self.model
        }

        return args

class EvaluateQuery(AcademicQuery):
    """
    This class represents a query to the Interpret endpoint
    """
    EVALUATE_URL = AcademicConf.BASE_URL + '/evaluate'

    def __init__(self, expr=None):
        AcademicQuery.__init__(self)
        self.expr = expr
        self.attributes = 'Id'
        self.count = AcademicConf.MAX_PAGE_RESULTS
        self.offset = 0
        self.model = 'latest'

    def set_expr(self, value):
        """
        Sets the expr used to evaluate.
        """
        self.expr = value

    def set_attributes(self, value):
        """
        Sets the attributes used to evaluate.
        """
        self.attributes = value

    def set_count(self, value):
        """
        Sets the maximum number of entities to return.
        """
        msg = 'count must be numeric'
        self.count = AcademicUtils.ensure_int(value, msg)

    def set_offset(self, value):
        """
        Sets the index of the first entity to return.
        """
        msg = 'offset must be numeric'
        self.offset = AcademicUtils.ensure_int(value, msg)

    def set_model(self, value):
        """
        Sets the name of the model that you wish to query.
        Currently, the value defaults to "latest".
        """
        self.model = value

    def get_url(self):
        return self.EVALUATE_URL

    def get_body(self):
        """
        Creates and returns the body for the POST request
        """
        if self.expr is None:
            raise classes.RequiredArgumentError('Evaluate needs an expr')

        args = {
            'expr': self.expr,
            'attributes': self.attributes,
            'count': self.count,
            'offset': self.offset,
            'model': self.model
        }

        return args

class SimilarityQuery(AcademicQuery):
    """
    This class represents a query to the Similarity endpoint
    """
    SIMILARITY_URL = AcademicConf.BASE_URL + '/similarity'

    def __init__(self, s1=None, s2=None):
        AcademicQuery.__init__(self)
        self.s1 = s1
        self.s2 = s2

    def set_s1(self, value):
        """
        Sets the first string to compare.
        """
        self.s1 = value

    def set_s2(self, value):
        """
        Sets the second string to compare.
        """
        self.s2 = value

    def get_url(self):
        return self.SIMILARITY_URL

    def get_body(self):
        """
        Creates and returns the body for the POST request
        """
        if self.s1 is None or self.s2 is None:
            raise classes.RequiredArgumentError('Similarity needs two strings to compare')

        args = {
            's1': self.s1,
            's2': self.s2
        }

        return args

class CalcHistogramQuery(EvaluateQuery):
    """
    This class represents a query to the calc histogram endpoint
    """
    CALC_HISTOGRAM_URL = AcademicConf.BASE_URL + '/calchistogram'

    def __init__(self, expr=None):
        EvaluateQuery.__init__(self, expr)

    def get_url(self):
        return self.CALC_HISTOGRAM_URL

class AcademicQuerier(object):
    """
    Class in charge of making the requests to the Microsoft's Academic
    Knowledge site.
    """

    def __init__(self, query_type, arguments=None):
        """
        Constructor that receives the type of query and a set of arguments
        to pass to the query
        """
        self.query_type = query_type
        # step 1: parameters sanity check
        if not isinstance(query_type, AcademicQueryType):
            raise classes.QueryTypeError('Query type must be of type AcademicQueryType.')
        if arguments is None:
            arguments = {}

        # step 2: build the query
        self.query = None
        if query_type == AcademicQueryType.INTERPRET:
            self.query = InterpretQuery()
            self.query.set_query(arguments.get('query', self.query.query))
            self.query.set_complete(arguments.get('complete', self.query.complete))
            self.query.set_count(arguments.get('count', self.query.count))
            self.query.set_offset(arguments.get('offset', self.query.offset))
            self.query.set_timeout(arguments.get('timeout', self.query.timeout))
            self.query.set_model(arguments.get('model', self.query.model))
        elif query_type == AcademicQueryType.EVALUATE:
            self.query = EvaluateQuery()
            self.query.set_expr(arguments.get('expr', self.query.expr))
            self.query.set_attributes(arguments.get('attributes', self.query.attributes))
            self.query.set_count(arguments.get('count', self.query.count))
            self.query.set_offset(arguments.get('offset', self.query.offset))
            self.query.set_model(arguments.get('model', self.query.model))
        elif query_type == AcademicQueryType.SIMILARITY:
            self.query = SimilarityQuery()
            self.query.set_s1(arguments.get('s1', self.query.s1))
            self.query.set_s2(arguments.get('s2', self.query.s2))
        elif query_type == AcademicQueryType.HISTOGRAM:
            self.query = CalcHistogramQuery()
            self.query.set_expr(arguments.get('expr', self.query.expr))
            self.query.set_attributes(arguments.get('attributes', self.query.attributes))
            self.query.set_count(arguments.get('count', self.query.count))
            self.query.set_offset(arguments.get('offset', self.query.offset))
            self.query.set_model(arguments.get('model', self.query.model))
        else:
            raise classes.QueryTypeError('Query type not supported.')

    def post(self):
        if os.getenv('MAKA_SUBSCRIPTION_KEY', None) is None:
             raise KeyError('MAKA_SUBSCRIPTION_KEY')
        headers = {
            'user-agent': AcademicConf.USER_AGENT,
            'Ocp-Apim-Subscription-Key': os.environ['MAKA_SUBSCRIPTION_KEY']
        }
        url = self.query.get_url()
        data = self.query.get_body()
        AcademicUtils.log('debug', 'Sending {}/{}'.format(url, data))
        the_request = requests.post(url, data=data, headers=headers)
        AcademicUtils.log('debug', 'Received {}'.format(the_request.text))
        if  the_request.status_code < 300:
            if self.query_type == AcademicQueryType.INTERPRET:
                jobject = the_request.json()
                return [classes.AcademicInterpretationParser.parse(interpretation)
                        for interpretation in jobject['interpretations']]
            elif self.query_type == AcademicQueryType.EVALUATE:
                jobject = the_request.json()
                return [classes.AcademicPaperParser.parse(entity) for entity in jobject['entities']]
            elif self.query_type == AcademicQueryType.SIMILARITY:
                return float(the_request.text)
            elif self.query_type == AcademicQueryType.HISTOGRAM:
                jobject = the_request.json()
                return [classes.AcademicHistogramParser.parse(entity)
                        for entity in jobject['histograms']]
        else:
            raise classes.Error('An error ocurred while processing the request. Code: {}'
                                .format(the_request.status_code))
