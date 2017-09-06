"""
Test Module
"""
import os
import sys
import json

from os.path import join, dirname
from random import randint
from queue import Queue
from threading import Thread
from time import sleep
from dotenv import load_dotenv
from optparse import IndentedHelpFormatter, OptionGroup, OptionParser

import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
os.sys.path.insert(0,parentdir)
import classes
import inquirer

DELAY = 1
NUM_QUERIER_THREADS = 2
ROOT = {'author': None, 'aliases': [], 'articles': []}
THE_QUEUE = Queue()

def find_article(article, parent=None):
    if parent is not None:
        for p in ROOT['articles']:
            if p['id'] == parent and p['cites']:
                 for art in p['cites']:
                     if art['id'] == article:
                         return art
    else:
        for art in ROOT['articles']:
            if art['id'] == article:
                return art
    return None

def querier_enclosure(i, q):
    """
    Wrapper for the query procedure in order to be used in a Worker
    """
    while True:
        print('Worker {}: Looking for the next query'.format(i))
        args = q.get()
        query = inquirer.AcademicQuerier(args['query_type'], args['payload'])
        if query is not None:
            results = query.post()
            if results:
                if args['query_type'] == inquirer.AcademicQueryType.INTERPRET:
                    expr = 'OR({})'.format(','.join([interpretation['rules'][0]['value']
                                                     for interpretation in results]))
                    THE_QUEUE.put({
                        'query_type': inquirer.AcademicQueryType.EVALUATE,
                        'payload':    {
                            'expr':       expr,
                            'attributes': '*'
                        },
                        'parent': None
                    })
                elif args['query_type'] == inquirer.AcademicQueryType.EVALUATE:
                    parent = args.get('parent', None)
                    branch = ROOT['articles'] if parent is None else (find_article(parent))['cites']
                    for result in results:
                        article = find_article(result['id'], parent)
                        if article is None:
                            branch.append(result)
                            if parent is None:
                                expr = 'RId={}'.format(result['id'])
                                THE_QUEUE.put({
                                    'query_type': inquirer.AcademicQueryType.EVALUATE,
                                    'payload':    {
                                        'expr':       expr,
                                        'attributes': '*'
                                    },
                                    'parent': result['id']
                                })
                    total = len(branch)
                    if total%50 == 0:
                        new_payload = args['payload'].copy()
                        new_payload['offset'] = total
                        THE_QUEUE.put({
                            'query_type': args['query_type'],
                            'payload': new_payload,
                            'parent': args['parent']
                        })
        q.task_done()
        sleep(DELAY)

def main():
    """
    The method called when running this script
    """
    usage = """author.py --author "albert einstein"
A command-line interface to Microsoft's Academic Knowledge."""

    fmt = IndentedHelpFormatter(max_help_position=50, width=100)
    parser = OptionParser(usage=usage, formatter=fmt)
    group = OptionGroup(parser, 'Query arguments',
                                 'These options define search query arguments and parameters.')
    group.add_option('-a', '--author', metavar='AUTHORS', default=None,
                     help='Author name(s)')
    parser.add_option_group(group)
    options, _ = parser.parse_args()

    # Show help if we have neither keyword search nor author name
    if len(sys.argv) == 1:
        parser.print_help()
        return 1
    
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    for i in range(NUM_QUERIER_THREADS):
        worker = Thread(target=querier_enclosure, args=(i, THE_QUEUE,))
        worker.setDaemon(True)
        worker.start()

    ROOT['author'] = options.author
    THE_QUEUE.put({
        'query_type': inquirer.AcademicQueryType.INTERPRET,
        'payload': {
           'query': 'papers by {}'.format(options.author)
        }
    })
    print('*** Main thread waiting')
    THE_QUEUE.join()
    with open('{}.json'.format(ROOT['author'].replace(' ', '')), 'w') as outfile:
        json.dump(ROOT, outfile, cls=classes.AcademicEncoder, indent=4)
    print('*** Done')

if __name__ == "__main__":
    sys.exit(main())
