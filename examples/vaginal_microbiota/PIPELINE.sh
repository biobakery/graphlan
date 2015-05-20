# !/bin/bash

# remove the generated files, if any
echo "Removing files"
rm -f annot.txt tree.txt outtree.txt outimg.png outimg.svg

# convert it!
echo "Converting to GraPhlAn"
export2graphlan.py -i stm_otu_table_with_taxonomy.biom -a annot.txt -t tree.txt --discard_otus --most_abundant 50 \
--annotations 2,3,4,5,6 --external_annotations 7 --title "STM" --internal_levels --max_clade_size 300

echo "Running GraPhlAn"
graphlan_annotate.py --annot annot.txt tree.txt outtree.txt # attach annotation to the tree
graphlan.py --dpi 300 --size 7.0 outtree.txt outimg.png # generate the beautiful image
