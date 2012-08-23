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
__version__ = '0.9'
__date__ = '22 August 2012'

import sys 
import sys,argparse
from src.graphlan_lib import CircTree as CTree

def read_params(args):
    parser = argparse.ArgumentParser(
            description='GraPhlAn annotate module '+__version__+" ("+__date__+")\n"
                        "AUTHORS: "+__author__+"\n\n")
    arg = parser.add_argument

    arg('intree', type=str, metavar='input_tree',
        help = "the input tree (in Newick, Nexus, PhyloXML or "
               "plain textformat " )
    arg('outtree', type=str, metavar='output_tree', nargs='?',
        default = None,
        help = "the output tree in PhyloXML format containing the newly "
               "added annotations. If not specified, the input tree file "
               "will be overwritten ")
    arg('--annot', default=None, metavar="the annotation file", type=str, 
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
    arg( '-v','--version', action='store_true', 
        help="Prints the current GraPhlAn version and exit\n" )
    return vars(parser.parse_args())

if __name__ == "__main__":
    args = read_params( sys.argv )
    if args['version']:
        sys.stdout.write("GraPhlAn version "+__version__+"\t("+__date__+")"+"\n")
        sys.exit(0)
    ctree = CTree( args['intree'] )
    ctree.annotate( args['annot'], args['outtree'] if args['outtree'] else args['intree'] ) # ,
    #                c = args['c'], p = args['p'], v = args['v']) 

