#!/bin/sh
graphlan_annotate.py gut_microbiome.txt gut_microbiome.annot.xml --annot annot.txt
graphlan.py gut_microbiome.annot.xml gut_microbiome.png --dpi 300 --size 4.5 --pad 0
