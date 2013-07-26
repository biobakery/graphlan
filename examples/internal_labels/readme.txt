This is a quick guide that helps you to use graphlan and it is referred only to the folder "newops".
If you need more hepl, you can open each file .txt or .sh. You can find a comment for each step line (#comment) that specifies what you are going to do with the option written below.

GraPhlAn is a software tool for producing high-quality circular representations of taxonomic and phylogenetic trees.
If want to understand how to use this sofware you should open the files in this order:
 archaea.txt
 step0.sh
 annot_0.txt
 step1.sh
 annot_1.txt
 step2.sh 
 annot_2.txt
 step3.sh
 annot_3.txt
 step4.sh

The two main script are:
 1- graphlan.py
 2- graphlan_annotate.py
The first one is used to generate the output image in two different formats (png/svg). The second one is used to tie the annotation file to the input tree. This two options are contained in the "script#.sh".

"annot_#.txt" is an annotation file in which you can set the options you want to give your tree.
"step#.sh" is a sript that ties an annotation file to the input tree to create an output image.




