#!/bin/sh
graphlan_annotate.py archaea.txt archaea.annot.xml --annot annot.txt
graphlan.py archaea.annot.xml archaea.png --dpi 150 --pad 0 
