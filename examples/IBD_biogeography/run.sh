#!/bin/sh                                                                                                                                                                                                                                                                      
graphlan_annotate.py IBDgeo.txt IBDgeo.annot.xml --annot annotation.txt 
graphlan.py IBDgeo.annot.xml IBDgeo.png --dpi 150 
