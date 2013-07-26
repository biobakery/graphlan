#look at step1.sh
graphlan_annotate.py --annot annot_2.txt guide_2.xml guide_3.xml
graphlan.py guide_3.xml step3.png --dpi 300 --size 10.5
graphlan.py guide_3.xml step3.svg --dpi 300 --size 10.5
