# !/bin/bash

export2graphlan.py -i hmp_metahit.txt -o hmp_metahit.lefse.txt -t tree.txt -a annot.txt --title "MetaHIT vs. HMP (MetaPhlAn2)" --max_clade_size 250 --min_clade_size 40 --annotations 5 --external_annotations 6,7 --abundance_threshold 40.5 --fname_row 0 --ftop 200 --annotation_legend_font_size 11

graphlan_annotate.py --annot annot.txt tree.txt tree.xml
graphlan.py --dpi 300 --size 7.0 tree.xml hmp_metahit.svg
