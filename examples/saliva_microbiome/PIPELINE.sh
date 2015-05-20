# !/bin/bash

# remove the generated files, if any
echo "Removing files"
rm -f annot.txt tree.txt outtree.txt outimg.png

# convert it!
echo "Converting to GraPhlAn"
export2graphlan.py -i otu_table.biom -a annot.txt -t tree.txt --discard_otus --most_abundant 40 --annotations 2,3,4,5 \
--external_annotations 6,7 --title "Saliva microbiome" --internal_levels --def_na 0 --max_clade_size 350

echo "Running Graphlan"
graphlan_annotate.py --annot annot.txt tree.txt outtree.txt # attach annotation to the tree
graphlan.py --dpi 300 --size 7.0 outtree.txt outimg.png # generate the beautiful image
