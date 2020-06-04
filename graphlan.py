#!/usr/bin/env python

#------------------------------------------------------------------------------
# NAME: graphlan.py
# DESCRIPTION:  GraPhlAn is a python program for creating images of circular
#               cladogram starting from a tree given in PhyloXML format. The
#               PhyloXML input tree can be formatted and annotated using the
#               graphlan_annotate.py script.
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
    parser = ArgumentParser(description= "GraPhlAn "+__version__+" ("+__date__+") "
                                         "AUTHORS: "+__author__)
    arg = parser.add_argument

    arg('intree', type=str, default = None, metavar='input_tree',
        help = "the input tree in PhyloXML format " )
    arg('outimg', type=str, default = None, metavar='output_image',
        help = "the output image, the format is guessed from the extension "
               "unless --format is given. Available file formats are: png, "
               "pdf, ps, eps, svg" )
    arg('--format', choices=['png','pdf','ps','eps','svg'], default=None,
        type = str, metavar=['output_image_format'],
        help = "set the format of the output image (default none meaning that "
               "the format is guessed from the output file extension)")
    arg('--warnings', default=1, type=int,
        help = "set whether warning messages should be reported or not (default 1)")
    arg('--positions', default=0, type=int,
        help = "set whether the absolute position of the points should be reported on "
               "the standard output. The two cohordinates are r and theta")
    arg('--dpi', default=72, type=int, metavar='image_dpi',
        help = "the dpi of the output image for non vectorial formats")
    arg('--size', default=7.0, type=float, metavar='image_size',
        help = "the size of the output image (in inches, default 7.0)")
    arg('--pad', default=0.5, type=float, metavar='pad_in',
        help = "the distance between the most external graphical element and "
               "the border of the image")
    arg('--external_legends', default=False, action='store_true',
        help = "specify whether the two external legends should be put in separate file or keep them "
               "along with the image (default behavior)")
    arg('--avoid_reordering', default=True, action='store_false',
        help = "specify whether the tree will be reorder or not (default the tree will be reordered)")
    arg( '-v','--version', action='version', version="GraPhlAn version "+__version__+" ("+__date__+")",
        help="Prints the current GraPhlAn version and exit" )
    return vars(parser.parse_args())


def main():
    args = read_params( argv )
    ctree = CTree( args['intree'], args['warnings'] )
    ctree.positions = args['positions']
    ctree.draw(args['outimg'],
               out_format=args['format'],
               out_dpi=args['dpi'],
               out_size=args['size'],
               out_pad=args['pad'],
               external_legends=args['external_legends'],
               reorder_tree=args['avoid_reordering'])

if __name__ == "__main__":
    main()