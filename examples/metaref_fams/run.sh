#!/bin/sh
graphlan_annotate.py mr1.txt mr1.xml --annot mr1.a.txt
graphlan.py mr1.xml mr1.png --dpi 150 --size 4 --pad 0.2
graphlan.py mr1.xml mr1.svg --dpi 150 --size 4 --pad 0.2

graphlan_annotate.py mr1.txt mr2.xml --annot mr2.a.txt
graphlan.py mr2.xml mr2.png --dpi 150 --size 4 --pad 0.2
graphlan.py mr2.xml mr2.svg --dpi 150 --size 4 --pad 0.2
