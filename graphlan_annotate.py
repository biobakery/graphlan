#!/usr/bin/env python

#------------------------------------------------------------------------------
# NAME: circlader_annotate.py
# DESCRIPTION:  TBA 
#
# Author:   Nicola Segata
# email:    nsegata@hsph.harvard.edu
#
# Copyright: (c) 2012
# Licence: <your licence>
#
#------------------------------------------------------------------------------


import sys 
import sys,argparse
from src.graphlan_lib import CircTree as CTree

def read_params(args):
    parser = argparse.ArgumentParser(description='Circlader')
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
    arg('-c', type=str, metavar='clade_name', default=None,
        help = "For command line annotation specifies the clade to be "
               "annotated (\* means global setting)")
    arg('-p', type=str, metavar='property_name', default=None,
        help = "For command line annotation specifies the property to be "
               "annotated")
    arg('-v', type=str, metavar='property_name', default=None,
        help = "For command line annotation specifies the value to be "
               "annotated")
    return vars(parser.parse_args())

if __name__ == "__main__":
    args = read_params( sys.argv )
    ctree = CTree( args['intree'] )
    ctree.annotate( args['annot'], args['outtree'] if args['outtree'] else args['intree'],
                    c = args['c'], p = args['p'], v = args['v']) 
    #ctree.draw( args['outimg'], 
    #            out_format = args['format'], 
    #            out_dpi = args['dpi'] )

