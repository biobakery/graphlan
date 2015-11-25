GraPhlAn is a software tool for producing high-quality circular 
representations of taxonomic and phylogenetic trees. GraPhlAn focuses on 
concise, integrative, informative, and publication-ready representations of 
phylogenetically- and taxonomically-driven investigation.

You can find below the instruction for installing and using the software.
If you have any questions or comment please refer to the project home page at
https://bitbucket.org/nsegata/graphlan
or to the GraPhlAn google group:
https://groups.google.com/d/forum/graphlan-users
or email me at 
nsegata@hsph.harvard.edu


==============================================================================
	INSTALLATION
..............................................................................

GraPhlAn is available in bitbucket and should be obtained using Mercurial 
(http://mercurial.selenic.com/) at https://bitbucket.org/nsegata/graphlan/


In a Unix environment, this means you have to type:
$ hg clone ssh://hg@bitbucket.org/nsegata/graphlan
or
$ hg clone https://hg@bitbucket.org/nsegata/graphlan

This will download the GraPhlAn repository locally in the "graphlan" 
subfolder. You then have to put this subfolder into the system path so that
you can use GraPhlAn from any location in your system:
$ export PATH=`pwd`/graphlan/:$PATH

Adding the above line into the bash configuration file will make the path 
addition permanent.

For Windows or MacOS systems a similar procedure should be followed. Is is also
possible (but not recommended) to obtain the software using the download link
available at https://bitbucket.org/nsegata/graphlan/src ("get source" on the
top right corner).



==============================================================================
	PREREQUISITES
..............................................................................

You need to have the following programs and libraries installed:
- python 2.7 or higher ( http://www.python.org/ )
- the biopython python library 1.6 or higher ( http://biopython.org )
- the matplotlib python library 1.1 or higher 
  ( http://matplotlib.sourceforge.net )



==============================================================================
	USAGE
..............................................................................

The GraPhlAn package consists in two main scripts:
1- graphlan.py
2- graphlan_annotate.py

The first produces graphical output of an input tree in any of the three most
popular format: Newick, PhyloXML, or text format. The second modifies any 
input tree (in any of the three standard format) adding additional 
information regarding structural or graphical aspects of the tree (like colors 
and style of the taxa, labels, shadows, heatmaps, ...); graphlan_annotate.py
generates PhyloXML files that can be converted into images by graphlan.py.


				...........


More specifically, here are all the options one can set for graphlan.py:

usage: graphlan.py [-h] [--format ['output_image_format']]
                   [--warnings WARNINGS] [--positions POSITIONS]
                   [--dpi image_dpi] [--size image_size] [--pad pad_in]
                   [--external_legends] [-v]
                   input_tree output_image

GraPhlAn 0.9.7 (21 July 2014) AUTHORS: Nicola Segata
(nsegata@hsph.harvard.edu)

positional arguments:
  input_tree            the input tree in PhyloXML format
  output_image          the output image, the format is guessed from the
                        extension unless --format is given. Available file
                        formats are: png, pdf, ps, eps, svg

optional arguments:
  -h, --help            show this help message and exit
  --format ['output_image_format']
                        set the format of the output image (default none
                        meaning that the format is guessed from the output
                        file extension)
  --warnings WARNINGS   set whether warning messages should be reported or not
                        (default 1)
  --positions POSITIONS
                        set whether the absolute position of the points should
                        be reported on the standard output. The two
                        cohordinates are r and theta
  --dpi image_dpi       the dpi of the output image for non vectorial formats
  --size image_size     the size of the output image (in inches, default 7.0)
  --pad pad_in          the distance between the most external graphical
                        element and the border of the image
  --external_legends    specify whether the two external legends should be put
                        in separate file or keep them along with the image
                        (default behavior)
  -v, --version         Prints the current GraPhlAn version and exit

				...........


Input tree files for graphlan.py can be generated, personalized, and annotated
using the graphlan_annotate.py module. In addition to the tree topology and
(possibly) branch lengths, graphlan_annotate.py reads an "annotation file" 
(--annot option) which specifies the graphical options for the tree. The
syntax of the annotation file is described comprehensively below. Here is the
command line invocation syntax.

usage: graphlan_annotate.py [-h] [--annot annotation_file] [-v]
                            input_tree [output_tree]

GraPhlAn annotate module 0.9 (22 August 2012) AUTHORS: Nicola Segata
(nsegata@hsph.harvard.edu)

positional arguments:
  input_tree            the input tree in Newick, Nexus, PhyloXML or plain
                        text format
  output_tree           the output tree in PhyloXML format containing the
                        newly added annotations. If not specified, the input
                        tree file will be overwritten

optional arguments:
  -h, --help            show this help message and exit
  --annot annotation_file
                        specify the annotation file
  -v, --version         Prints the current GraPhlAn version and exit




==============================================================================
	COMMAND AND SYNTAX OF THE ANNOTATION FILE
..............................................................................

The annotation file is a tab-delimited file listing the graphical options for
clades. Usually each line has three fields: the name of the clade, the name of
the option, and the value to assign to the option. Lines can however have two
fields (typically for "global" option not referred to a specific clade) or 
four fields when the external rings (a sort of circular heatmap) is specified.

Below we report and describe all available options and their syntax subdivided
by option types.


------------------------------------------------------------------------------
    GLOBAL TREE OPTIONS:
------------------------------------------------------------------------------

Global structural and visual characteristics affecting the entire tree are
specified in the annotation file with a two-column tab separated syntax with the
following pattern:

global_tree_option	global_tree_option_value

where global_tree_option can be any of the following: 

ignore_branch_len [def. 0 = False] : specify whether to display the tree with
    fixed branch length (i.e. 0) or with the values specified in the input 
    tree. If the input tree is not containing branch length information, branch 
    lengths will not be showed regardless of this option 

total_plotted_degrees [def. 360] : the total circular portion used in plotting 
    the tree. 360 means that the tree uses the full rotational space. Small 
    trees are usually best displayed with a limited total_plotted_degrees value.

start_rotation [def 0] : the default starting rotational position for the first 
    leaf of the tree 

clade_separation [def 0.0] : specify a fractional separation between clades 
    which is proportional to the branch distance between subtrees. It option can
    be used to visually separate more clades that are reciprocally deep 
    branching.  

branch_bracket_depth [def 0.25] : the relative position of the branch bracket 
    which is the radial segment from which the child taxa branches originate.  

branch_bracket_width [def 1.0] : the width of the branch bracket relative to 
    the position of the most separated child roots

branch_thickness [def 0.75] : the global thickness of the lines connecting taxa

branch_color [def black] : the global thickness of the lines connecting taxa

branch_color_from_ancestor [def 1] : whether to use the color of the closest
    ancestor colored taxa for the downstream branches


------------------------------------------------------------------------------
    GLOBAL GRAPHICAL OPTIONS:
------------------------------------------------------------------------------

Global options affecting the graphical appearance of annotations, legends, and
markers specified in the annotation file with a two-column tab separated syntax
with the following pattern:

global_graphical_option  global_graphical_option_value

where global_graphical_option can be any of the following:

title : set the title of the output image

title_font_size [def. 15] : set the font size used to display the title

annotation_background_width [def. 0.1] : set the width of the annotation, you
    can think of it as inserting a space before and after the label of the
    annotation

annotation_background_alpha [def. 0.2] : set the transparency level of the
    background. Keep in mind that some annotations can overlap

annotation_background_separation [def. 0.02] : set how much space keep between
    leafs and the last labels

annotation_background_offset [def. 0.02] : set the end of the circle that
    contains the tree, where the exteran optional barplots start

annotation_legend_font_size [def. 7] : set the font size used in the annotation
    legend

class_legend_font_size [def. 7] : set the font size used in the class legend

class_legend_marker_size [def. 1.0] : the size of the markers in the legend

internal_labels_rotation [def. None] : set the internal labels orientation. It 
    does not work well, already put in the known issues list

------------------------------------------------------------------------------
    GRAPHICAL TREE OPTIONS:
------------------------------------------------------------------------------

The graphical tree options are the most common way of personalizing the trees.
They can be referred to specific clade, to set of clades, or to all clade. The
syntax is the following:

[clade_name{+|*|^}]	graphical_tree_option	graphical_tree_option_value

If the clade name is omitted the option is applied to ALL clades. The clade
can be specified with the full label comprising all names from the root of the
tree or with the last level only (if last level names are not unique, multiple
matching clades will be affected by the command). Optionally, at the end of the
clade name, one of the following character can be added (see below for the
meaning of these symbols): +, *, ^

The "graphical_tree_option" can be:

clade_marker_size [def. 20.0] : the size of the marker representing the root 
    of the clade inside the tree

clade_marker_color [def. #FFFFFF, i.e. white] : the fill color of the marker 
    representing the root of the clade inside the tree

clade_marker_shape [def. 'o', i.e. circle] : the shape of the clade marker. 
    See the Marker Shapes table below for the allowed options

clade_marker_edge_width [def. 0.5] : the thickness of the border for clade 
    markers

clade_marker_edge_color [def. #000000, i.e. black] : the color of the markers' 
    border

clade_marker_label : specify a label to insert in the specified clade

clade_marker_font_size [def. 7] : the size of the font color for the clade
    marker label specified

clade_marker_font_color [def 'k', i.e. black] : the font color of the clade
    marker label specified

When added after the name of a valid clade, the following three characters can
be used to apply the same property to multiple parts of the clade' subtree

* : the specified clade and all its descendants are affected by the property
+ : the specified clade and all its terminal nodes are affected 
^ : all (and only) the terminal nodes of the specified clade are affected

------------------------------------------------------------------------------
    ANNOTATION OPTIONS
------------------------------------------------------------------------------

[clade_name]	annotation_option	graphical_tree_option_value

We call annotations the shadings highlighting clades and the corresponding
subtree. Annotations can be colored, their alpha-channel can be globally
regulated, and have a label associated with them. Specifically, the options
available for annotations are:

annotation [def. no annotation] : the label the be associated and displayed for
    the annotation. This can assume several formats:
      1. str (a string not containing ':'): the string to be displayed entirely 
         (an only) on the shading
      2. key:str : the (supposedly short) key will be displayed on the 
         annotation shading, whereas the full key:string label will be reported 
         as external legend
      3. *:str : a key will be generated and used as the 2. "key:str" case
      4. * : the name of the clade (specifically the last taxonomic level only) 
         will be used as the 'str' in the 1. case above
      5. *:* : the combination of the 3. and 4. cases above

annotation_font_size [def. 7] : the font size of the annotation label

annotation_font_stretch [def. 0] : horizontal font compactness (0 is minimal)

annotation_rotation [def. 0] : the rotation of the label. As default the rotation
    is perpendicular to the radial position of the label. It can be changed to 
    90 so that the labels are less likely to overlap

annotation_background_color [def. grey] : the color of the annotation background

annotation_background_edge_color [def annotation_background_color] : the color 
    of the edge for the annotation background. NOT IMPLEMENTED YET


------------------------------------------------------------------------------
    INTERNAL ANNOTATION OPTIONS
------------------------------------------------------------------------------

annotation_option	annotation_r	annotation_value

Internal annotations are used to label the levels in a tree (e.g. specify the
level of bacterial species in a taxonomic tree). annotation_r specifies the
radial distance from the center (i.e. the number of levels). Currently,
annotation_option can be:

internal_label : the label to be displayed

internal_label_font_size [def. 8] : the font

The rotational position of the labels can be specified with the 
internal_labels_rotation parameter (see GLOBAL GRAPHICAL OPTIONS) 

------------------------------------------------------------------------------
    RING OPTIONS
------------------------------------------------------------------------------

We call rings the graphical elements external to the tree itself that can be
seen as "circular heatmaps", "circular barplots", and actually more (like
indicator elements). These "rings" are linked directly to the internal tree as
each segment of the rings correspond to a tree leaf (and potentially to internal
nodes as well). Multiple rings can be specified for the same image and each must
have a progressive associated number (level "1" being the most internal ring).

The general syntax for rings is:

[clade_name]	ring_option	ring_level	ring_option_value

If clade_name is not present or if it is "*" the ring option is applied to all
the ring sectors in the "ring_level". The "ring_level" is a integer number that
must always be specified.

Here are the possible ring options:

ring_color [def. black] : the color of the ring segment 

ring_width [def. 1.0] : the width of the ring segment a fraction of the total 
    circular width available for the specific clade

ring_height [def. highest height for the rings in the same level, or 0.1 if no
    heights are specific] : the height of the circular segment. If not specific 
    the same default height (0.1*size of the tree) is applied for all ring 
    segment in the level, otherwise the height is equal to the biggest height 
    value in the level.

ring_alpha [def. 1.0]: the transparency value. 0.0 means completely transparent
    (thus invisible), 1.0 means completely opaque (no transparencies) 

ring_shape [def. R]: the shape of the ring. Default is 'R' for rectangular which
    means that the whole available area is used. The alternatives are currently 
    'v' or '^' which mean triangular shape (with opposite directions) that can 
    be used as pointing arrow for highlighting specific clades. 

ring_edge_width [def 0.1]: the width of the border of the ring segment

ring_edge_color [def None, which means 'ring_color']: the color of the border 
    of the ring segment

Some additional ring options refer to non clade-specific aspects like the label
of the ring itself or the graphical separation between rings. These options are
specified without a clade name in the following tree-column format:

global_ring_option     ring_level      global_ring_option_value

Specifically, the ring options can be:

ring_label [def. None]: the label to be displayed at "stat_rotation" position 
    for the rings. total_plotted_degrees should be less than 360 to make space 
    for these labels

ring_label_color [def. black]: the color of the ring label

ring_label_font_size [def. 11]: the font size of the ring labels

ring_internal_separator_thickness [def.  0.0 which means absent]: the thickness 
    of the circular line separating different ring levels. This is referred 
    to the most internal of the two sides of each ring.

ring_external_separator_thickness [def.  0.0 which means absent]: the thickness
    of the circular line separating different ring levels. This is referred to 
    the most external of the two sides of each ring.

ring_separator_color [def. 'k' for black]: the color of the circular line 
    separating different ring levels.


				...........


------------------------------------------------------------------------------
    COLORS
------------------------------------------------------------------------------

Colors are strings that can be:
- one of the following 'default' colors: blue, green, red, cyan, magenta, 
    yellow, black, white
- a one-letter shortcut for the above colors: 'b' (blue), 'g' (green), 
    'r' (red), 'c' (cyan), 'm' (magenta), 'y' (yellow), 'k' (black), 
    'w' (white) 

- a RGB color code in the hexadecimal format: #rrggbb, for example #FF0000
    corresponds to (full) red

------------------------------------------------------------------------------
    MARKER SHAPES:
------------------------------------------------------------------------------

As of August 2012 we support the marker types available in matplotlib version
1.1.1. Specifically here are the codes for the markers. Note that some of them
are shapes with internal color-filled space, other are edge- or point-only
markers.

'.' : point marker
',' : pixel marker
'o' : circle marker
'v' : triangle_down marker
'^' : triangle_up marker
'<' : triangle_left marker
'>' : triangle_right marker
'1' : tri_down marker
'2' : tri_up marker
'3' : tri_left marker
'4' : tri_right marker
's' : square marker
'p' : pentagon marker
'*' : star marker
'h' : hexagon1 marker
'H' : hexagon2 marker
'+' : plus marker
'x' : x marker
'D' : diamond marker
'd' : thin_diamond marker
'|' : vline marker
'_' : hline marker


==============================================================================

