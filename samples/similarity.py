import os
import sys

from os.path import join, dirname
from dotenv import load_dotenv
from optparse import IndentedHelpFormatter, OptionGroup, OptionParser

import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
os.sys.path.insert(0,parentdir)
import inquirer

def main():
    """
    The method called when running this script
    """
    usage = """similarity.py --s1 "this is a test" --s2 "that was a test"
A command-line tool to test similarity to Microsoft's Academic Knowledge."""

    fmt = IndentedHelpFormatter(max_help_position=50, width=100)
    parser = OptionParser(usage=usage, formatter=fmt)
    group = OptionGroup(parser,
                        'Query arguments',
                        'These options define search query arguments and parameters.')
    group.add_option('--s1', metavar='STRING1', default=None, help='First string')
    group.add_option('--s2', metavar='STRING2', default=None, help='Second string')
    parser.add_option_group(group)
    options, _ = parser.parse_args()

    # Show help if we have neither keyword search nor author name
    if len(sys.argv) == 1:
        parser.print_help()
        return 1
    if options.s1 is None or options.s2 is None:
        print('Both strings are mandatory!')
        return 1

    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    query = inquirer.AcademicQuerier(inquirer.AcademicQueryType.SIMILARITY, {
        's1': options.s1,
        's2': options.s2
    })
    if query is not None:
        similarity = query.post()
    print('Similarity between "{}" and "{}" is {}'.
          format(options.s1, options.s2, similarity))

if __name__ == '__main__':
    sys.exit(main())
