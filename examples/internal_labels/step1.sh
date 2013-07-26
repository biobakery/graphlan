# graphlan_annotate.py put the annotation file (annot_0.txt) and the plot of the tree (archaea.txt) together, to create "guide.xml". This new file contains both .txt files. Than we launch the images (look at step0.sh). 
graphlan_annotate.py --annot annot_0.txt archaea.txt guide_1.xml
graphlan.py guide_1.xml step1.png --dpi 300 --size 10.5
graphlan.py guide_1.xml step1.svg --dpi 300 --size 10.5
