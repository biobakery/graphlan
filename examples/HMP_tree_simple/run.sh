#!/bin/sh
graphlan_annotate.py hmptree.xml hmptree.annot.xml --annot annot.txt
graphlan.py hmptree.annot.xml hmptree.png --dpi 150 --size 14 
