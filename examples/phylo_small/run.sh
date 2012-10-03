#!/bin/sh
graphlan_annotate.py phylo_small.xml phylo_small.annot.xml --annot annot.txt
graphlan.py phylo_small.annot.xml phylo_small.png --dpi 150  
