# !/bin/bash

########################################################################################################################
# The following lines of code contains all the steps for downloading the HMP and MetaHIT data, process it through      #
# MetaPhlAn2, merging the MetaPhlAn2 results into a single dataset, perform some string manipulation, process the data #
# using LEfSe for biomarkers discovery, exploit the export2graphlan framework for generating the tree and the          #
# annotation file for GraPhlAn, and finally draw the image using GraPhlAn.                                             #
# For time reasons, we provide the two intermediate files: the clean merge of the two datasets (HMP & MetaHIT) and the #
# results of LEfSE.                                                                                                    #
# If the user wants to test the complete pipeline, it is enough to uncommet all the commented part.                    #
########################################################################################################################

# # remove the generated files, if any
# echo "Removing files"
# rm -f merge.txt new-stool/* merge-good.txt merge-good-1.txt merge-good-2.txt merge-good-3.txt merge-very-good.txt \
#     merge-very-good.txt.in merge-very-good.txt.out tree.txt annot.txt outtree.txt outimg.png

# # set MetaPhlAn2 directory
# mpa_dir=`$HOME/metaphlan2`

# # download samples
# echo "Downloading HMP stool samples"
# mkdir new-stool
# cd new-stool/
# for i in SRS011239 SRS013215 SRS013476 SRS014459 SRS015065 SRS056259 SRS058770 SRS062427 SRS063985 SRS015854 SRS016203 \
#     SRS016335 SRS017307 SRS017701 SRS018656 SRS019161 SRS019968 SRS020233 SRS020328 SRS022609 SRS023583 SRS024265 \
#     SRS047044 SRS052697 SRS053214 SRS015190 SRS015217 SRS015578 SRS015663 SRS016056 SRS016989 SRS017191 SRS017433 \
#     SRS018351 SRS018427 SRS018984 SRS019582 SRS019601 SRS022071 SRS022137 SRS024009 SRS024132 SRS024549 SRS024625 \
#     SRS043001 SRS045004 SRS045713 SRS050422 SRS050925 SRS051031 SRS011405 SRS011529 SRS011586 SRS012902 SRS014923 \
#     SRS055982 SRS011084 SRS011134 SRS011452 SRS013951 SRS014613 SRS014979 SRS054956 SRS057717 SRS058723 SRS064557 \
#     SRS064645 SRS065504 SRS015264 SRS015782 SRS015960 SRS016495 SRS016517 SRS017103 SRS018313 SRS018575 SRS019267 \
#     SRS019787 SRS019910 SRS020869 SRS021484 SRS023176 SRS023526 SRS023971 SRS024331 SRS024435 SRS048870 SRS049900 \
#     SRS049959 SRS049995 SRS050299 SRS050752 SRS052027 SRS011302 SRS012273 SRS013158 SRS014313 SRS015133 SRS053335 \
#     SRS054590 SRS063040 SRS077730 SRS078176 SRS015369 SRS015890 SRS016018 SRS016095 SRS016753 SRS016954 SRS017521 \
#     SRS017821 SRS018133 SRS019030 SRS019685 SRS022713 SRS023829 SRS024388 SRS042628 SRS047014 SRS048164 SRS049712 \
#     SRS051882 SRS011061 SRS011271 SRS013521 SRS013687 SRS013800 SRS014235 SRS014287 SRS014683 SRS053398 SRS056519 \
#     SRS057478 SRS064276 SRS075398 SRS015431 SRS015794 SRS016267 SRS016585 SRS017247 SRS018817 SRS019068 SRS019381 \
#     SRS019397 SRS021948 SRS022524 SRS023346 SRS023914 SRS024075 SRS042284 SRS043411 SRS043701 SRS045645 SRS049164; do

#     wget ftp://public-ftp.hmpdacc.org/Illumina/stool/${i}.tar.bz2 # download
#     tar jxf -d ${i}.tar.bz2 # decompress
#     cat ${i}/* > ${i}.fastq
#     metaphlan2.py ${i}.fastq --mpa_pkl ${mpa_dir}/db_v20/mpa_v20_m200.pkl --bowtie2db ${mpa_dir}/db_v20/mpa_v20_m200 \
#     --input_type fastq > ${i}.profile
# done

# echo "Downloading MetaHIT healthy stool samples"
# for i in `cat ../metahit.txt`; do
#     s=`echo ${i} | cut -f1`
#     u=`echo ${i} | cut -f2`

#     for j in `echo ${u} | tr ';' '\n'`; do
#         f=`echo ${j} | cut -f6 -d'/'`
#         ff=`echo ${f} | cut -f1-2 -d'.'`

#         wget ftp://${j} # download
#         gunzip ${f} # decompress
#         cat ${ff} >> ${s}.fastq # cat forward and reverse
#     done

#     metaphlan2.py ${s}.fastq --mpa_pkl ${mpa_dir}/db_v20/mpa_v20_m200.pkl --bowtie2db ${mpa_dir}/db_v20/mpa_v20_m200 \
#     --input_type fastq > ${s}.profile
# done
# cd ../

# # discard taxon rows in .profile files
# echo "Removing \"t__\" from taxonomy"
# for i in `ls new-stool/`; do
#     file=new-stool/${i}
#     grep -v t__ $file > $file.clean
# done
# rm -f new-stool/*.profile

# # merge tables
# echo "Merging tables"
# merge_metaphlan_tables.py new-stool/* > merge.txt

# # fix taxonomy
# echo "Cleaning taxonomy"
# sed 's/.__//g' merge.txt > merge-good.txt

# # put the dataset information (e.g., HMP or MetaHIT)
#     # change "ID" with "dataset"
# sed 's/ID/dataset/' merge-good.txt > merge-good-1.txt
#     # all "MH00*" must become "MetaHIT"
# sed 's/MH00[0-9]*.profile/MetaHIT/g' merge-good-1.txt > merge-good-2.txt
#     # all "V1.CD-* must become "MetaHIT"
# sed 's/V1.[A-Z]*-[0-9]*.profile/MetaHIT/g' merge-good-2.txt > merge-good-3.txt
#     # all "SRS*" must become "HMP"
# sed 's/SRS[0-9]*.profile/HMP/g' merge-good-3.txt > merge-very-good.txt

# # execute LEfSe
# echo "Running LEfSe"
# format_input.py merge-very-good.txt merge-very-good.txt.in -c 1 -o 1000000
# run_lefse.py -l 3.0 merge-very-good.txt.in merge-very-good.txt.out

# convert it!
echo "Converting to GraPhlAn"
export2graphlan.py -i merge-very-good.txt -o merge-very-good.txt.out -t tree.txt -a annot.txt \
--title "MetaHIT vs. HMP (MetaPhlAn 2)" --max_clade_size 250 --min_clade_size 40 --annotations 5 \
--external_annotations 6,7 --abundance_threshold 40.5 --fname_row 0 --ftop 200 --annotation_legend_font_size 11

echo "Running Graphlan"
graphlan_annotate.py --annot annot.txt tree.txt outtree.txt # attach annotation to the tree
graphlan.py --dpi 300 --size 7.0 outtree.txt aaa.svg # generate the beautiful image

