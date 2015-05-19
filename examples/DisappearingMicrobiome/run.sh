#!/bin/sh

cp annot.txt annot3.txt

# De Filippo
for l in `cat genomes.all.txt | grep g__Prevotella  | cut -f 1 | sed -n '0~4p'` ; do echo $l"\tring_width\t2\t8\n"$l"\tring_height\t2\t0.5\n"$l"\tring_shape\t2\tv\n"$l"\tring_color\t2\tg" >> annot3.txt ; done
for l in `cat genomes.all.txt | grep g__Xylanibacter | cut -f 1` ; do echo $l"\tring_width\t2\t8\n"$l"\tring_height\t2\t0.5\n"$l"\tring_shape\t2\tv\n"$l"\tring_color\t2\tg" >> annot3.txt ; done
for l in `cat genomes.all.txt | grep g__Treponema | cut -f 1 | sed -n '0~4p'` ; do echo $l"\tring_width\t2\t8\n"$l"\tring_height\t2\t0.5\n"$l"\tring_shape\t2\tv\n"$l"\tring_color\t2\tg" >> annot3.txt ; done
for l in `cat genomes.all.txt | grep g__Butyrivibrio | cut -f 1` ; do echo $l"\tring_width\t2\t8\n"$l"\tring_height\t2\t0.5\n"$l"\tring_shape\t2\tv\n"$l"\tring_color\t2\tg" >> annot3.txt ; done

# Yatsunenko
for l in `cat genomes.all.txt | grep s__Streptococcus_alactolyticus | cut -f 1` ; do echo $l"\tring_width\t2\t8\n"$l"\tring_height\t2\t0.5\n"$l"\tring_shape\t2\tv\n"$l"\tring_color\t2\tr" >> annot3.txt ; done
for l in `cat genomes.all.txt | grep g__Clostridium.s__leptum | cut -f 1` ; do echo $l"\tring_width\t2\t8\n"$l"\tring_height\t2\t0.5\n"$l"\tring_shape\t2\tv\n"$l"\tring_color\t2\tr" >> annot3.txt ; done
for l in `cat genomes.all.txt | grep s__Clostridium_orbiscindens | cut -f 1` ; do echo $l"\tring_width\t2\t8\n"$l"\tring_height\t2\t0.5\n"$l"\tring_shape\t2\tv\n"$l"\tring_color\t2\tr" >> annot3.txt ; done
for l in `cat genomes.all.txt | grep s__Clostridium_innocuum | cut -f 1` ; do echo $l"\tring_width\t2\t8\n"$l"\tring_height\t2\t0.5\n"$l"\tring_shape\t2\tv\n"$l"\tring_color\t2\tr" >> annot3.txt ; done

for l in `cat genomes.all.txt | grep g__Lactobacillus.s__ruminis | cut -f 1` ; do echo $l"\tring_width\t2\t8\n"$l"\tring_height\t2\t0.5\n"$l"\tring_shape\t2\tv\n"$l"\tring_color\t2\tg" >> annot3.txt ; done
for l in `cat genomes.all.txt | grep g__Eubacterium | cut -f 1` ; do echo $l"\tring_width\t2\t8\n"$l"\tring_height\t2\t0.5\n"$l"\tring_shape\t2\tv\n"$l"\tring_color\t2\tg" >> annot3.txt ; done
for l in `cat genomes.all.txt | grep g__Dialister | cut -f 1` ; do echo $l"\tring_width\t2\t8\n"$l"\tring_height\t2\t0.5\n"$l"\tring_shape\t2\tv\n"$l"\tring_color\t2\tg" >> annot3.txt ; done
for l in `cat genomes.all.txt | grep g__Oscillospira | cut -f 1` ; do echo $l"\tring_width\t2\t8\n"$l"\tring_height\t2\t0.5\n"$l"\tring_shape\t2\tv\n"$l"\tring_color\t2\tg" >> annot3.txt ; done

# Clemente
for l in `cat genomes.all.txt | grep g__Helicobacter | cut -f 1 | sed -n '0~6p'` ; do echo $l"\tring_width\t2\t8\n"$l"\tring_height\t2\t0.5\n"$l"\tring_shape\t2\tv\n"$l"\tring_color\t2\tg" >> annot3.txt ; done
for l in `cat genomes.all.txt | grep g__Phascolarctobacterium | cut -f 1` ; do echo $l"\tring_width\t2\t8\n"$l"\tring_height\t2\t0.5\n"$l"\tring_shape\t2\tv\n"$l"\tring_color\t2\tg" >> annot3.txt ; done
for l in `cat genomes.all.txt | grep g__Paraprevotella | cut -f 1` ; do echo $l"\tring_width\t2\t8\n"$l"\tring_height\t2\t0.5\n"$l"\tring_shape\t2\tv\n"$l"\tring_color\t2\tg" >> annot3.txt ; done
for l in `cat genomes.all.txt | grep g__Anaeroplasma | cut -f 1` ; do echo $l"\tring_width\t2\t8\n"$l"\tring_height\t2\t0.5\n"$l"\tring_shape\t2\tv\n"$l"\tring_color\t2\tg" >> annot3.txt ; done
for l in `cat genomes.all.txt | grep g__Bulleidia | cut -f 1` ; do echo $l"\tring_width\t2\t8\n"$l"\tring_height\t2\t0.5\n"$l"\tring_shape\t2\tv\n"$l"\tring_color\t2\tg" >> annot3.txt ; done
for l in `cat genomes.all.txt | grep g__Gemella | cut -f 1` ; do echo $l"\tring_width\t2\t8\n"$l"\tring_height\t2\t0.5\n"$l"\tring_shape\t2\tv\n"$l"\tring_color\t2\tg" >> annot3.txt ; done

for l in `cat genomes.all.txt | grep g__Coprococcus | cut -f 1` ; do echo $l"\tring_width\t2\t8\n"$l"\tring_height\t2\t0.5\n"$l"\tring_shape\t2\tv\n"$l"\tring_color\t2\tr" >> annot3.txt ; done

#Martinez
for l in `cat genomes.all.txt | grep g__Weissella | cut -f 1` ; do echo $l"\tring_width\t2\t8\n"$l"\tring_height\t2\t0.5\n"$l"\tring_shape\t2\tv\n"$l"\tring_color\t2\tg" >> annot3.txt ; done
for l in `cat genomes.all.txt | grep g__Slackia | cut -f 1` ; do echo $l"\tring_width\t2\t8\n"$l"\tring_height\t2\t0.5\n"$l"\tring_shape\t2\tv\n"$l"\tring_color\t2\tg" >> annot3.txt ; done
for l in `cat genomes.all.txt | grep g__Gemella | cut -f 1` ; do echo $l"\tring_width\t2\t8\n"$l"\tring_height\t2\t0.5\n"$l"\tring_shape\t2\tv\n"$l"\tring_color\t2\tg" >> annot3.txt ; done
for l in `cat genomes.all.txt | grep g__Streptococcus | cut -f 1 | sed -n '0~14p'` ; do echo $l"\tring_width\t2\t8\n"$l"\tring_height\t2\t0.5\n"$l"\tring_shape\t2\tv\n"$l"\tring_color\t2\tg" >> annot3.txt ; done

for l in `cat genomes.all.txt | grep g__Gordonibacter | cut -f 1` ; do echo $l"\tring_width\t2\t8\n"$l"\tring_height\t2\t0.5\n"$l"\tring_shape\t2\tv\n"$l"\tring_color\t2\tr" >> annot3.txt ; done
for l in `cat genomes.all.txt | grep g__Odoribacter | cut -f 1` ; do echo $l"\tring_width\t2\t8\n"$l"\tring_height\t2\t0.5\n"$l"\tring_shape\t2\tv\n"$l"\tring_color\t2\tr" >> annot3.txt ; done


# Obregon
for l in `cat genomes.all.txt | grep g__Succinivibrio | cut -f 1` ; do echo $l"\tring_width\t2\t8\n"$l"\tring_height\t2\t0.5\n"$l"\tring_shape\t2\tv\n"$l"\tring_color\t2\tg" >> annot3.txt ; done
for l in `cat genomes.all.txt | grep g__Catenibacterium | cut -f 1` ; do echo $l"\tring_width\t2\t8\n"$l"\tring_height\t2\t0.5\n"$l"\tring_shape\t2\tv\n"$l"\tring_color\t2\tg" >> annot3.txt ; done

for l in `cat genomes.all.txt | grep g__Dorea | cut -f 1` ; do echo $l"\tring_width\t2\t8\n"$l"\tring_height\t2\t0.5\n"$l"\tring_shape\t2\tv\n"$l"\tring_color\t2\tr" >> annot3.txt ; done
for l in `cat genomes.all.txt | grep g__Blautia | cut -f 1` ; do echo $l"\tring_width\t2\t8\n"$l"\tring_height\t2\t0.5\n"$l"\tring_shape\t2\tv\n"$l"\tring_color\t2\tr" >> annot3.txt ; done


for l in `cat genomes.all.txt | grep g__Bacteroides | cut -f 1 | sed -n '0~14p'` ; do echo $l"\tring_width\t2\t8\n"$l"\tring_height\t2\t0.5\n"$l"\tring_shape\t2\tv\n"$l"\tring_color\t2\tr" >> annot3.txt ; done
for l in `cat genomes.all.txt | grep g__Faecalibacterium | cut -f 1` ; do echo $l"\tring_width\t2\t8\n"$l"\tring_height\t2\t0.5\n"$l"\tring_shape\t2\tv\n"$l"\tring_color\t2\tr" >> annot3.txt ; done
for l in `cat genomes.all.txt | grep g__Ruminococcus | cut -f 1` ; do echo $l"\tring_width\t2\t8\n"$l"\tring_height\t2\t0.5\n"$l"\tring_shape\t2\tv\n"$l"\tring_color\t2\tr" >> annot3.txt ; done


graphlan_annotate.py DisMic.xml DisMic.annot.xml --annot annot3.txt
graphlan.py DisMic.annot.xml DisMic.png --dpi 200 --size 15 --pad 0.6 
graphlan.py DisMic.annot.xml DisMic.svg --dpi 200 --size 15 --pad 0.6 
