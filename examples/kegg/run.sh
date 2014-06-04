#!/bin/bash
graphlan_annotate.py --annot annot.txt ppa_kegg_raxml.names.nn.nwk kegg.xml
graphlan.py --dpi 300 kegg.xml kegg.png
