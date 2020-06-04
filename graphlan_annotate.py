#!/usr/bin/env python

#------------------------------------------------------------------------------
# NAME: graphlan_annotate.py
# DESCRIPTION:  TBA 
#
# Author:   Nicola Segata
# email:    nsegata@hsph.harvard.edu
#
#
#------------------------------------------------------------------------------

__author__ = 'Nicola Segata (nsegata@hsph.harvard.edu)'
__version__ = '1.1.3'
__date__ = '5 June 2018'


import sys

if sys.version_info[0] > 2:
    raise Exception("GraPhlAn requires Python 2, your current Python version is {}.{}.{}"
                    .format(sys.version_info[0], sys.version_info[1], sys.version_info[2]))

from sys import argv
from argparse import ArgumentParser
from src.graphlan_lib import CircTree as CTree


def read_params(args):
    parser = ArgumentParser(
            description="GraPhlAn annotate module "+__version__+" ("+__date__+") "
                        "AUTHORS: "+__author__)
    arg = parser.add_argument

    arg('intree', type=str, metavar='input_tree',
        help = "the input tree in Newick, Nexus, PhyloXML or "
               "plain text format" )
    arg('outtree', type=str, metavar='output_tree', nargs='?',
        default = None,
        help = "the output tree in PhyloXML format containing the newly "
               "added annotations. If not specified, the input tree file "
               "will be overwritten")
    arg('--annot', default=None, metavar="annotation_file", type=str, 
        help = "specify the annotation file" )
    #arg('-c', type=str, metavar='clade_name', default=None,
    #    help = "For command line annotation specifies the clade to be "
    #           "annotated (\* means global setting)")
    #arg('-p', type=str, metavar='property_name', default=None,
    #    help = "For command line annotation specifies the property to be "
    #           "annotated")
    #arg('-v', type=str, metavar='property_name', default=None,
    #    help = "For command line annotation specifies the value to be "
    #           "annotated")
    arg( '-v','--version', action='version', version="GraPhlAn version "+__version__+" ("+__date__+")",  
        help="Prints the current GraPhlAn version and exit" )
    return vars(parser.parse_args())

def main():
    args = read_params( argv )
    ctree = CTree( args['intree'] )
    ctree.annotate( args['annot'], args['outtree'] if args['outtree'] else args['intree'] ) # ,
    #                c = args['c'], p = args['p'], v = args['v']) 

if __name__ == "__main__":
    main()