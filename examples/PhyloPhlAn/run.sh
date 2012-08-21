#!/bin/sh
graphlan_annotate.py ppa_tol.xml ppa_tol.annot.xml --annot annot.txt
graphlan.py ppa_tol.annot.xml ppa_tol.png --dpi 200 --size 15 --pad 0.6 
