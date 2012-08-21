#!/bin/sh
graphlan_annotate.py core_genes.txt core_genes.annot.xml --annot annot.txt
graphlan.py core_genes.annot.xml core_genes.png --dpi 150 --size 4 --pad 0.2
