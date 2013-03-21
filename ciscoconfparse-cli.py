#!/usr/bin/env python
#
# Requires ciscoconfparse ;-)
#
# https://pypi.python.org/pypi/ciscoconfparse/

import sys
from optparse import OptionParser

from ciscoconfparse import CiscoConfParse

def parent_w_child(config, parent, child, invertmatch=False):

    parse = CiscoConfParse(config)

    if invertmatch:
        result = parse.find_parents_wo_child(parent, child)
    else:
        result = parse.find_parents_w_child(parent, child)

    if len(result) > 0:
        for e in result:
            print e


def show_usage_examples():

    examples = """Show all interfaces with a specific ip helper: %s interface \"ip helper-address 192.168.0.100\" router-config.txt
Show all interfaces without VLAN tagging: %s -v ^interface \"encapsulation dot1q\" router-config.txt""" % (sys.argv[0], sys.argv[0])

    print (examples)

if __name__ == '__main__':
    optparser = OptionParser(usage="usage: %prog [options] parent-pattern child-pattern cisco-ios-config-file")

    optparser.add_option('', '--examples', dest='examples', action='store_true',
                            help='Show usage examples', default=False)
    optparser.add_option('-v', '--invert-match', dest='invertmatch', action='store_true',
                            help='Negate search pattern', default=False)

    (options, args) = optparser.parse_args()

    #--------------------------------------------------------------------------
    # Show usage examples 
    #--------------------------------------------------------------------------
    if options.examples:
        show_usage_examples()
        sys.exit(0)

    #--------------------------------------------------------------------------
    # TODO Argument error handling 
    #--------------------------------------------------------------------------
    if not len(args) > 2:
        optparser.print_help()
        sys.exit(-1)

    parentrgx = args[0]
    childrgx = args[1]
    configfile = args[2]

    if options.invertmatch:
        parent_w_child(configfile, parentrgx, childrgx, invertmatch=True)
    else:
        parent_w_child(configfile, parentrgx, childrgx)
