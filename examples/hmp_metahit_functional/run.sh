#!/bin/bash

export2graphlan.py -i hmp_metahit_functional.txt -o hmp_metahit_functional.lefse.txt -t tree.txt -a annot.txt --title "Functional pathways" --abundance_threshold 45.5 --external_annotations 3 --background_clades "Metabolism.Metabolism_of_Cofactors_and_Vitamins, Metabolism.Carbohydrate_Metabolism, Metabolism.Amino_Acid_Metabolism, Metabolism.Metabolism_of_Terpenoids_and_Polyketides, Metabolism.Metabolism_of_Other_Amino_Acids, Genetic_Information_Processing.Replication_and_Repair, Environmental_Information_Processing.Membrane_Transport" --background_colors "(150.; 100.; 100.), (55.; 100.; 100.), (280.; 80.; 88.)" --ftop 125 --internal_levels --max_clade_size 600 --min_clade_size 40

graphlan_annotate.py --annot annot.txt tree.txt tree.xml
graphlan.py --dpi 300 --size 7.0 tree.xml hmp_metahit_functional.svg
