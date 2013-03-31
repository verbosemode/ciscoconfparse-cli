#!/usr/bin/env python
#
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <jochen.bartl@gmail.de> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Jochen Bartl
# ----------------------------------------------------------------------------
#
# Dependencies:
#
# $ pip install ciscoconfpars
#
# https://pypi.python.org/pypi/ciscoconfparse/


import sys
from optparse import OptionParser

from ciscoconfparse import CiscoConfParse


def find_parent_w_child(cfg, parentspec, childspec, invertmatch=False):

    if invertmatch:
        result = cfg.find_parents_wo_child(parentspec, childspec)
    else:
        result = cfg.find_parents_w_child(parentspec, childspec)

    return result


def find_all_children(cfg, linespecs, exactmatch=True):

    l = []
    
    for line in linespecs:
        l.append(cfg.find_all_children(line, exactmatch=exactmatch))

    return l


def output_lines(lines):

    for l in lines:
        if type(l) is list:
            for e in l:
                print e
        else:
            print l


def show_usage_examples():

    examples = """
Show all interfaces with a specific ip helper
---------------------------------------------

    %s interface \"ip helper-address 192.168.0.100\" router-config.txt

Show all interfaces without VLAN tagging
----------------------------------------

    %s -v ^interface \"encapsulation dot1q\" router-config.txt
""" % (sys.argv[0], sys.argv[0])

    print (examples)


if __name__ == '__main__':
    optparser = OptionParser(usage="Usage: %prog [OPTION]... SECTION_SEARCH_PATTERN CHILD_SEARCH_PATTERN FILE")

    optparser.add_option('', '--examples', dest='examples', action='store_true',
                            help='Show usage examples', default=False)
    optparser.add_option('-v', '--invert-match', dest='invertmatch', action='store_true',
                            help='Select non-matching config sections', default=False)
    optparser.add_option('-A', '--after-context', dest='aftercontext', action='store_true',
                            help='Print all lines of the matching config section(s)', default=False)

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

    parentspec = args[0]
    childspec = args[1]
    configfile = args[2]


    cfg = CiscoConfParse(configfile)


    if options.invertmatch:
        result = find_parent_w_child(cfg, parentspec, childspec, invertmatch=True)
    else:
        result = find_parent_w_child(cfg, parentspec, childspec)


    if options.aftercontext:
        result = find_all_children(cfg, result)
    
    output_lines(result)

    sys.exit(0)
