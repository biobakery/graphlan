import sys

if sys.version_info[0] > 2:
    raise Exception("GraPhlAn requires Python 2, your current Python version is {}.{}.{}"
                    .format(sys.version_info[0], sys.version_info[1], sys.version_info[2]))

from Bio import Phylo
from Bio.Phylo import PhyloXML
from Bio.Phylo import PhyloXMLIO
from collections import defaultdict as ddict
from Bio.Phylo.PhyloXML import Property as Prop
from Bio.Phylo.PhyloXML import Clade as PClade
from Bio.Phylo.BaseTree import Tree as BTree
from Bio.Phylo.BaseTree import Clade as BClade
import string
from numpy import pi as rpi
rpi2 = 2.0*rpi
import numpy as np
import array as arr
import collections as colls
from matplotlib import collections
import matplotlib.patches as mpatches
import matplotlib.lines as lines
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['svg.fonttype'] = 'none'
from pylab import *
from pyphlan import PpaTree


clade_attr = ( ( 'clade_marker_size',                float, 20.0      ),
               ( 'clade_marker_color',               str,   '#FFFFFF' ),
               ( 'clade_marker_edge_width',          float, 0.5       ),
               ( 'clade_marker_shape',               str,   'o'       ),
               ( 'clade_marker_edge_color',          str,   '#000000' ),
               ( 'clade_marker_label',               str,   ''        ),
               ( 'clade_marker_font_size',           str,   '7'       ),
               ( 'clade_marker_font_color',          str,   'k'       ),
               ( 'class_label',                      str,   ""        ),  # to rem
               ( 'annotation_font_size',             int,   7         ),
               ( 'annotation_font_stretch',          int,   0         ),
               ( 'annotation_background_color',      str,   '#FF0000' ),
               ( 'annotation_background_edge_color', str,   '#FF0000' ),  # not implemented yet
               ( 'annotation',                       str,   ''        ),
               ( 'annotation_rotation',              int,   0         ) )
clade_attr_d = dict([(p,(t,d)) for p,t,d in clade_attr])

ext_attr = ( ( 'ring_color',                        str,   '#000000' ),
             ( 'ring_width',                        float, 1.0       ),
             ( 'ring_height',                       float, -1.0      ),
             ( 'ring_alpha',                        float, 1.0       ),
             ( 'ring_shape',                        str,   "R"       ),
             ( 'ring_label',                        str,   None      ),
             ( 'ring_label_font_size',              int,   11        ),
             ( 'ring_label_color',                  str,   'k'       ),
             ( 'ring_edge_width',                   float, 0.1       ),
             ( 'ring_edge_color',                   str,   None      ),
             ( 'ring_internal_separator_thickness', float, 0.0       ),
             ( 'ring_separator_color',              str,   'k'       ),
             ( 'ring_external_separator_thickness', float, 0.0       ) )
ext_attr_d = dict([(p,(t,d)) for p,t,d in ext_attr])

int_attr = ( ( 'internal_label',           str, None ),
             ( 'internal_label_font_size', int, 8    ) )
int_attr_d = dict([(p,(t,d)) for p,t,d in int_attr])

structural_attr = ( ( 'ignore_branch_len',     int,   0     ),
                    ( 'total_plotted_degrees', float, 360.0 ),
                    ( 'start_rotation',        float, 180.0 ),
                    ( 'clade_separation',      float, 0.0   ),
                    ( 'branch_bracket_width',  float, 0.25  ),
                    ( 'branch_bracket_depth',  float, 1.0   ) )

global_graphical_attr = ( ( 'annotation_background_width',      float, 0.1   ),
                          ( 'annotation_background_alpha',      float, 0.2   ),
                          ( 'annotation_background_separation', float, 0.02  ),
                          ( 'annotation_background_offset',     float, 0.02  ),
                          ( 'class_legend_font_size',           int,   7     ),
                          ( 'title',                            str,   ""    ),
                          ( 'title_font_size',                  int,   15    ),
                          ( 'class_legend_marker_size',         float, 1.0   ),
                          ( 'annotation_legend_font_size',      int,   7     ),
                          ( 'internal_labels_rotation',         float,  None ) )

branch_attr = ( ( 'branch_thickness',           float, 0.75      ),
                ( 'branch_color',               str,   '#000000' ),
                ( 'branch_color_from_ancestor', int,   1         ) )

leg_sep = '_._._'
leg_attr = ( ( 'annotation_background_color',      str,   "w"  ),
             ( 'annotation_background_edge_color', str,   "k"  ),
             ( 'clade_marker_color',               str,   "w"  ),
             ( 'clade_marker_edge_width',          float, 0.5  ),
             ( 'clade_marker_size',                float, 20.0 ),
             ( 'clade_marker_shape',               str,   'o' ),
             ( 'keys',                             str,   "?"  ) )

lev_sep = '.'
legal_options = set(zip(*clade_attr+ext_attr+int_attr+structural_attr+global_graphical_attr+branch_attr+leg_attr)[0]) | set(['class'])

def random_keys(used_keys):
    n = 1
    nl = string.ascii_uppercase+string.ascii_lowercase
    while True:
        nl = [n for n in nl]+[a+b for a in nl for b in nl]
        for l in nl:
            if l not in used_keys:
                yield l

linearized_circle = list(arange( 0, rpi2,0.01))

class CircTree(PpaTree):

    def annotate(   self, inp_file, out_file = None,
                    c = None, p = None, v = None ):
        term_names = set([t.name for t in self.tree.get_terminals() if t.name])
        nterm_names = set([t.name for t in self.tree.get_nonterminals() if t.name])
        clade_names = term_names | nterm_names
        props, gprops, classes = ddict(dict), {}, ddict(dict)

        if c and p and v and not inp_file:
            lines = [ "\t".join([c,p,v]) +"\n" ]
        elif not inp_file:
            lines = []
        else:
            try:
                with open( inp_file ) as inpf:
                    lines = inpf.readlines()
            except IOError:
                sys.stderr.write("Error: annotation file not found: "
                                 ""+inp_file+"\n")
                sys.exit(0)
            except Exception:
                sys.stderr.write("Error in reading the annotation file: "
                                 ""+inp_file+"\n")
                sys.exit(0)

            if not out_file:
                out_file = inp_file

        def legal( prop ):
            if prop not in legal_options:
                sys.stderr.write( "Error: \"%s\" is not a legal option\nExiting...\n\n" % prop )
                sys.exit(0)

        self._tmp_levs = set()
        for line in (l.strip().split('\t') for l in lines if l[0] != '#'):
            if not ''.join(line): # skip empty lines
                continue
    
            ll = len(line)

            if (ll < 2) or (ll > 4):
                sys.stderr.write('Unrecognized annotationline:\n> {}\nMaybe spaces instead of tabs or extra tabs?\n'.format('\t'.join(line)))
                exit(1)
            elif len([l for l in line if l]) != ll:
                sys.stderr.write('Wrong annotation line:\n> {}\nSome of the values are empty!\n'.format('\t'.join(line)))
                exit(1)
            elif ll == 2:
                legal( line[0] ) #  in legal_options, "%s is not a valid option" % line[1]
                gprops[line[0]] = line[1]
            elif ll == 3:
                clade,prop,val = line
                if clade == '*' and prop != 'annotation':
                    legal( prop )
                    gprops[prop] = val
                elif clade in ext_attr_d:
                    prop,lev = clade,prop
                    legal( prop )
                    try:
                        ilev = int(lev)
                    except:
                        print(line)
                        asdasdasd

                    if prop not in gprops:
                        gprops[prop] = {}
                    if ilev not in gprops[prop]:
                        gprops[prop][ilev] = val
                elif clade in int_attr_d:
                    prop,lev = clade,prop
                    legal( prop )
                    flev = float(lev)
                    if prop not in gprops:
                        gprops[prop] = {}
                    gprops[prop][flev] = val
                elif clade[-1] in ['*','+','^']:
                    legal( prop )
                    if len(clade) == 1:
                        cl = self.tree.root
                    else:
                        cl = list(self.tree.find_clades( {"name": clade[:-1]} ))
                        if cl != 1: #??
                            cl = list(self.tree.find_clades( {"name": clade[:-1].split(lev_sep)[-1]} ))
                    for ccl in cl:
                        if clade[-1] in ['*']:
                            for nt in ccl.get_nonterminals():
                                props[nt.full_name][prop] = val
                        for t in ccl.get_terminals():
                            props[t.full_name][prop] = val
                    if not ( clade[-1] in ['^'] or clade[-1] in ['+'] or clade[-1] in ['*']):
                        props[clade[:-1]][prop] = val
                elif clade.split(lev_sep)[-1] in clade_names:
                    legal( prop )
                    props[clade][prop] = val
                else:
                    legal( prop )
                    classes[clade][prop] = val
            elif ll == 4:
                clade,prop,lev,val = line
                legal(prop)
                if clade == '*':
                    ilev = int(lev)
                    if prop in gprops :
                        gprops[prop][ilev] = val
                    else:
                        gprops[prop] = {ilev:val}
                elif clade.split(lev_sep)[-1] in clade_names:
                    try:
                        ilev = int(lev)
                    except:
                        print(line)
                        asdasdasd

                    self._tmp_levs.add( ilev )
                    if prop in props[clade]:
                        # print "clade", clade
                        # print "prop", prop
                        # print "props[clade]", props[clade]
                        # print "val", val
                        # print "ilev", ilev
                        # print

                        props[clade][prop][ilev] = val
                    else:
                        props[clade][prop] = {ilev:val}
                    if prop not in gprops:
                        gprops[prop] = {}
                    if ilev not in gprops[prop]:
                        gprops[prop][ilev] = ext_attr_d[prop][1]
                else:
                    # print ll
                    # print clade.split(lev_sep)[-1]
                    # print clade_names
                    # print line
                    sys.stderr.write( "Classes not implemented for external annotations\n" )
                    exit(1)


        def _rec_annotate_( clade, rkeys_gen, path ):
            name = clade.name if clade.name else ""
            npath = lev_sep.join( ([path] if path else []) + [name] )

            fn = None
            for n in [npath,name]:
                if n in props:
                    lprop = {}
                    if not hasattr( clade, "properties" ):
                        clade.properties = []

                    if 'class' in props[n]:
                        for k,v in classes[props[n]['class']].items():
                            lprop[k] = v
                    for k,v in props[n].items():
                        if type(v) == dict:
                            for kk,vv in v.items():
                                lprop["__".join(['ext',str(kk),k])] = vv
                        else:
                            lprop[k] = v

                    cp = []
                    for k,v in lprop.items():
                        value = v
                        if k == 'annotation':
                            if v.count(":"):

                                try:
                                    kkk,vvv = v.split(":")
                                except:
                                    print(v)
                                    asdasdasd

                                if kkk == '*':
                                    if fn is None:
                                        kkk = rkeys_gen.next()
                                    else:
                                        kkk = fn
                                    fn = kkk
                                if vvv == '*':
                                    vvv = clade.name
                                value = kkk + ": " + vvv
                            elif v == '*':
                                value = clade.name
                        cp.append(  Prop( value=value, ref='A:1', id_ref=k,
                                    applies_to='clade', datatype='xsd:string') )

                    clade.properties = [p for p in clade.properties
                                                    if p.id_ref != k] + cp
                    #break
            for c in clade.clades:
                _rec_annotate_( c, rkeys_gen,  npath )

        all_keys = set()
        for p in props.values():
            if 'annotation' in p and p['annotation'].count(":"):
                all_keys.add( p['annotation'].split(":")[0] )
        rkeys = random_keys(all_keys)


        _rec_annotate_( self.tree.root, rkeys, "" )
        tgprop = []
        for k,v in gprops.items():
            if type(v) == dict:
                for kk,vv in v.items():
                    if k in int_attr_d:
                        pn = "__".join(['int',str(kk),k])
                    else:
                        pn = "__".join(['ext',str(kk),k])
                    tgprop += [Prop(   value=vv, id_ref=pn,
                                       ref='A:1', applies_to='phylogeny',
                                       datatype='xsd:string' )]
            else:
                tgprop += [Prop(   value=v, id_ref=k,
                                   ref='A:1', applies_to='phylogeny',
                                   datatype='xsd:string' )]

        ckeys = sorted([c for c in classes.keys()
                    if not ('label' in classes[c] and classes[c]['label'] in ['none','None'])])
        if ckeys:
            newidrefs = ['leg_keys']
            val = leg_sep.join([classes[k]['label']
                        if 'label' in classes[k] else k for k in ckeys])
            p   = Prop( value = val, id_ref="leg_keys",
                    ref='A:1', applies_to='phylogeny', datatype='xsd:string')
            tgprop.append( p )
            leg_keys = []
            for att in [a for a,b,c in leg_attr if a != 'keys']:
                leg_keys.append( "leg_"+att )
                val = leg_sep.join([classes[k][att]
                    if classes and att in classes[k] else "." for k in ckeys])
                p   = Prop( value = val, id_ref="leg_"+att,
                            ref='A:1', applies_to='phylogeny', datatype='xsd:string')
                tgprop.append( p )
        else:
            newidrefs = []
        self.tree.properties = [p for p in self.tree.properties
                                    if p not in newidrefs] + tgprop

        for att,typ,default in structural_attr:
            if hasattr(self,att):
                np   = Prop( value = getattr(self,att), id_ref=att,
                             ref='A:1', applies_to='phylogeny',
                             datatype='xsd:string')
                self.tree.properties = [p for p in self.tree.properties if p != np] + [np]

        Phylo.write( self.tree, out_file, "phyloxml")


    def set_clade_data( self ):

        # this step sets the rotation distance between nodes with a component
        # proportional to the branch length distance in order to improve the
        # visual separation between subtrees.
        # This is executed if the user sets clade_separatio > 0.0
        self._ord_leaves = []


        def compute_tot_add( clade ):
            if clade.is_terminal():
                self._ord_leaves.append( clade )
                return [clade]
            ret = []
            for c in clade.clades:
                ret += compute_tot_add( c )
            return ret
        tot_dist, last = 0.0, self.tree.root
        if self.clade_separation > 0.0:
            ord_terms = compute_tot_add( self.tree.root )
            for t in ord_terms:
                tot_dist += self.tree.distance( last, t) * 0.5 / self._max_depth
                last = t

        coffset = self.start_rotation + (rpi2 - self.total_plotted_degrees) * 0.5
        circ_step = self.total_plotted_degrees * (1.0 - self.clade_separation) / self._n_terminals
        self.circ_pos = coffset - circ_step
        self._last_leaf = self.tree.root
        self._varf = circ_step

        varf = self.total_plotted_degrees*(self.clade_separation)
        self._varf = varf/tot_dist if self.clade_separation > 0.0 else 0.0
        self._ext_levs = set()
        #self._ext_max_height = {}


        def set_clade_data_rec( clade ):
            if self.ignore_branch_len:
                clade.branch_length = 1.0

            for p in clade.properties:
                typ = clade_attr_d[p.id_ref][0] if p.id_ref in clade_attr_d else lambda x:x
                setattr( clade, p.id_ref, typ(p.value) )
                if p.id_ref.startswith("ext__"):
                    lev,ref = p.id_ref.split("__")[1:]

                    if ref == 'ring_height':
                        if int(lev) not in self._ext_max_height:
                            self._ext_max_height[int(lev)] = float(p.value)
                        elif float(p.value) > self._ext_max_height[int(lev)]:
                            self._ext_max_height[int(lev)]  = float(p.value)


                    """
                    if ref == 'height':
                        if int(lev) not in self._ext_max_height or self._ext_max_height[int(lev)] < float(p.value):
                            self._ext_max_height[int(lev)] = 0.0 # float(p.value)
                        else:
                            if int(lev) not in self._ext_max_height:
                                self._ext_max_height[int(lev)] = 0.0 # self._ext_max_height
                                if int(lev) in self.ext_levs and 'height' in self.ext_levs[int(lev)]:
                                    self._ext_max_height[int(lev)] = self.ext_levs[int(lev)]['height']
                                    #self._ext_max_height[int(lev)] = self.ext_levs[int(lev)]['height']
                    """

                    lev = int(lev)
                    self._ext_levs.add( lev )
                    if not hasattr( clade, "ext" ):
                        clade.ext = {}
                    if not lev in clade.ext:
                        clade.ext[lev] = {}
                    clade.ext[lev][ref] = p.value

            clade.r = float(self._depths[clade.name]) / self._max_depth
            if clade.is_terminal():
                ld = self.tree.distance( self._last_leaf, clade )
                gap = ld * 0.5  / self._max_depth
                self.circ_pos += gap * self._varf
                self.circ_pos += circ_step
                clade.theta = self.circ_pos #% rpi2
                clade.theta_min = clade.theta
                clade.theta_max = clade.theta
                self._last_leaf = clade
            else:
                thetas = [set_clade_data_rec( c ) for c in clade.clades]
                mint, maxt = thetas[0], thetas[-1]
                if mint > maxt:
                    maxt += rpi2
                clade.theta = ((mint + maxt)*0.5 ) # % rpi2
                clade.theta_min = min([c.theta_min for c in clade.clades])
                clade.theta_max = max([c.theta_max for c in clade.clades])

            attr = [hasattr(clade,att) for att,typ,default in clade_attr]

            if clade == self.tree.root:
                return clade.theta

            if any(attr):
                for pres,(att,typ,default) in zip(attr,clade_attr):
                    attl = getattr( self, att )
                    if pres:
                        attl.append(typ(getattr( clade, att )))
                    else:
                        attl.append( getattr( self, "default_"+att ) )
                self._rl.append( clade.r )
                self._tl.append( clade.theta )
            else:
                self._r.append( clade.r )
                self._t.append( clade.theta )
            if hasattr( self, "positions" ) and self.positions:
                sys.stdout.write( "\t".join( [clade.name,str(clade.r),str(clade.theta)] ) + "\n" )

            if self.ignore_branch_len:
                lev = int(self._depths[clade.name])
                if ( hasattr(clade,'annotation_background_color') or hasattr(clade,'annotation') ) and not lev in self._wing_levs:
                    self._wing_levs.append(lev)
            else:
                self._wing_levs.append([1])

            return clade.theta

        set_clade_data_rec( self.tree.root )
        self._ext_levs = list(sorted(self._ext_levs))
        self._ext_bottoms = {}
        val = 0.0
        for k in self._ext_levs:
            self._ext_bottoms[int(k)] = val
            if int(k) in self._ext_max_height and  self._ext_max_height[int(k)] >= 0.0:
                val += self._ext_max_height[k]*0.1
            else:
                val += .1


    def set_exts(self):
        for l in self._ext_levs:
            if l not in self._ext_levs:
                self._ext_levs[l] == {}
                for att,typ,default in ext_attr:
                    self._ext_levs[l] = default
        self._all_ext_attr = [v[0] for v in ext_attr]


        def rec_set_exts( clade ):
            if hasattr( clade, "ext" ):
                ext = clade.ext
                if clade.is_terminal():
                    cpt = clade.pc.theta if clade.pc else clade.theta - (clade.nc.theta-clade.theta) #!!
                    cnt = clade.nc.theta if clade.nc else clade.theta + (clade.theta-clade.pc.theta) #!!
                    fr_theta = ( clade.theta + cpt ) * 0.5
                    to_theta = ( clade.theta + cnt ) * 0.5
                    if fr_theta > to_theta and fr_theta > 2*rpi:
                        fr_theta -= rpi
                        to_theta -= rpi
                    if fr_theta > to_theta:
                        fr_theta -= rpi
                else:
                    fr_theta = ( clade.fc.theta + clade.fc.pc.theta ) * 0.5 if clade.fc.pc else  clade.fc.theta - abs( clade.fc.theta - clade.fc.nc.theta ) * 0.5
                    to_theta = ( clade.lc.theta + clade.lc.nc.theta ) * 0.5 if clade.lc.nc else  clade.lc.theta + abs( clade.lc.theta - clade.lc.pc.theta ) * 0.5
                    if fr_theta > to_theta:
                        fr_theta -= rpi
                for lev in clade.ext:
                    for att,typ,default in ext_attr:
                        if att in ext[lev]:
                            ext[lev][att] = typ(ext[lev][att])
                        elif att in self.ext_levs[lev]:
                            ext[lev][att] = typ(self.ext_levs[lev][att])
                        else:
                            ext[lev][att] = default
                    el = ext[lev]
                    bottom = self._wing_tot_offset + self.annotation_background_offset + self._ext_bottoms[lev]
                    height = (el['ring_height'] if el['ring_height'] >= 0.0 else 1.0)*0.1
                    width =  abs(to_theta - fr_theta) * el['ring_width']
                    theta = ( fr_theta + to_theta ) * 0.5 - width * 0.5
                    if bottom + height > self._tot_offset:
                        self._tot_offset = bottom + height

                    art = None
                    if 'ring_shape' not in el or el['ring_shape'] in ['R','r']:

                        art = mpatches.Rectangle(   (theta,bottom),
                                                    width = width,
                                                    height = height,
                                                    alpha = el['ring_alpha'],
                                                    color = el['ring_color'],
                                                    linewidth = 0.0, #linewidth = el['ring_edge_width'],
                                                    #ec = el['ring_edge_color'] if el['ring_edge_color'] else el['ring_color']
                                                    )
                        if el['ring_edge_width'] > 0.0:
                            arb = mpatches.Rectangle(   (theta,bottom),
                                                        width = width,
                                                        height = height,
                                                        #alpha = 0.0, # el['ring_alpha'],
                                                        color = 'none', #el['ring_color'],
                                                        linewidth = el['ring_edge_width'],
                                                        ec = el['ring_edge_color'] if el['ring_edge_color'] else el['ring_color'],
                                                        zorder = 15,
                                                    )
                            self._ext_patches.append( arb )
                    elif el['ring_shape'] in ['v','V']:
                        art = mpatches.Polygon([ [theta,bottom + height],
                                                 [theta+width/2.0,bottom],
                                                 [theta+width,bottom + height] ],
                                                 alpha = el['ring_alpha'],
                                                 color = el['ring_color'],
                                                 linewidth = 0.0, #el['ring_edge_width'],
                                                 #ec = el['ring_edge_color'] if el['ring_edge_color'] else el['ring_color']
                                                 )
                        if el['ring_edge_width'] > 0.0:
                            arb = mpatches.Polygon([ [theta,bottom + height],
                                                     [theta+width/2.0,bottom],
                                                     [theta+width,bottom + height] ],
                                                     color = 'none', #el['ring_color'],
                                                     linewidth = el['ring_edge_width'],
                                                     ec = el['ring_edge_color'] if el['ring_edge_color'] else el['ring_color'],
                                                     zorder = 15,
                                                    )
                            self._ext_patches.append( arb )
                    elif el['ring_shape'] in ['^']:
                        art = mpatches.Polygon([ [theta,bottom],
                                                 [theta+width/2.0,bottom+height],
                                                 [theta+width,bottom ] ],
                                                 alpha = el['ring_alpha'],
                                                 color = el['ring_color'],
                                                 linewidth = 0.0, #el['ring_edge_width'],
                                                 #ec = el['ring_edge_color'] if el['ring_edge_color'] else el['ring_color']
                                                 )
                        if el['ring_edge_width'] > 0.0:
                            arb = mpatches.Polygon([ [theta,bottom + height],
                                                     [theta+width/2.0,bottom],
                                                     [theta+width,bottom + height] ],
                                                     color = 'none', #el['ring_color'],
                                                     linewidth = el['ring_edge_width'],
                                                     ec = el['ring_edge_color'] if el['ring_edge_color'] else el['ring_color'],
                                                     zorder = 15,
                                                    )
                            self._ext_patches.append( arb )
                    if art:
                        self._ext_patches.append( art )
            for c in clade.clades:
                rec_set_exts(c)

        rec_set_exts( self.tree.root )


    def load_set_attr(self):
        gprops = dict([(p.id_ref,p.value)
                    for p in self.tree.properties if not p.id_ref.startswith("ext__") ])

        eggrops = [( int(p.id_ref.split('__')[1]),p.id_ref.split('__')[2], p.value)
                        for p in self.tree.properties if p.id_ref.startswith("ext__")]
        iggrops = [( float(p.id_ref.split('__')[1]),p.id_ref.split('__')[2], p.value)
                        for p in self.tree.properties if p.id_ref.startswith("int__")]

        for att,typ,default in clade_attr:
            val = typ( gprops[att] ) if att in gprops else default
            setattr( self, "default_"+att, val )

        self.ext_levs = {}
        for l,k,v in eggrops:
            if not l in self.ext_levs:
                self.ext_levs[l] = {}
            self.ext_levs[l][k] = v
        self.int_levs = {}
        for l,k,v in iggrops:
            if not l in self.int_levs:
                self.int_levs[l] = {}
            self.int_levs[l][k] = v
        for k,v in self.ext_levs.items():
            for att,typ,default in ext_attr:
                if att in v:
                    self.ext_levs[k][att] = typ(self.ext_levs[k][att])
                else:
                    self.ext_levs[k][att] = default

        for att,typ,default in global_graphical_attr:
            val = typ( gprops[att] ) if att in gprops else default
            setattr( self, att, val )

        for att,typ,default in branch_attr:
            val = typ( gprops[att] ) if att in gprops else default
            setattr( self, att, val )

        for att,typ,default in structural_attr:
            val = typ( gprops[att] ) if att in gprops else default
            setattr( self, att, val )

        for att,typ,default in leg_attr:
            val = gprops["leg_"+att] if "leg_"+att in gprops and gprops["leg_"+att] != '.' else ""
            val = [typ(v) if v != '.' else default for v in val.split(leg_sep)] if val else []
            setattr( self, "leg_"+att, val )

        self._ext_max_height = {}
        if 'ring_height' in gprops:
            for i,v in gprops['ring_height'].items():
                self._ext_max_height[i] = float(v) if float(v) >= 0.0 else 0.0
        for lev,attr,val in eggrops:
            if attr == 'ring_height':
                self._ext_max_height[int(lev)] = float(val) if float(val) >= 0.0 else 0.0

        self._n_terminals = self.tree.count_terminals()
        # with few leaves, the total rotation is lowered (unless the user set it)
        if self._n_terminals < 16 and 'total_plotted_degrees' not in gprops:
            self.total_plotted_degrees = self._n_terminals * 10.0
        self.total_plotted_degrees = self.total_plotted_degrees * rpi / 180.0
        self.start_rotation = self.start_rotation * rpi / 180.0


    def set_branches( self ):
        def set_branches_rec( clade, fcol ):
            if clade == self.tree.root:
                sbl, sb, rsb, redf = 1.0, 1.0, 0.0, 1.0
            else:
                sbl = self.branch_bracket_depth
                sb,rsb = sbl,1-sbl
                redf = 1.0-self.branch_bracket_width
            rads = [c.theta for c in clade.clades]
            min_rads,max_rads = rads[0],rads[-1]
            if min_rads > max_rads:
                max_rads += rpi2
            mid = ( max_rads + min_rads ) * 0.5
            red,nred = (redf,1-redf) # if abs(max_rads - min_rads) < math.pi else (1.0,0.0)
            midr = mid*nred
            minr, maxr = min_rads*red, max_rads*red
            rads_l = list(arange( minr+midr, maxr+midr,0.05)) + [maxr+midr]

            if hasattr(clade,'clade_marker_color') and self.branch_color_from_ancestor:
                fcol = clade.clade_marker_color

            cl0 = min([c for c in clade.clades],key=lambda x:x.r)
            blc = np.array(   [np.array(  [c, sb*clade.r+rsb*cl0.r] ) for c in rads_l]   )
            self._branches.append( blc )
            self._br_colors.append( fcol )

            corr = 0.0 if clade.theta >= min_rads else rpi2
            blc = np.array( [   np.array( [(clade.theta+corr)*red+midr, sb*clade.r+rsb*cl0.r]),
                                np.array( [clade.theta, clade.r])] )
            self._branches.append( blc )
            self._br_colors.append( fcol )

            for c in clade.clades:
                corr = 0.0 if c.theta >= min_rads else rpi2
                blc = np.array( [   np.array( [(c.theta+corr)*red+midr, sb*clade.r+rsb*cl0.r] ),
                                    np.array( [c.theta, c.r] ) ] )
                self._branches.append( blc )
                self._br_colors.append( fcol )
            for c in clade.clades:
                if not c.is_terminal():
                    set_branches_rec( c, fcol )

        set_branches_rec( self.tree.root, self.branch_color )


    def set_wings( self ):
        if not self._wing_levs:
            # print "not self._wing_levs", not self._wing_levs

            self._wing_tot_offset = 1.0 # self._max_depth
            self._tot_offset = 1.0
            return

        if self.ignore_branch_len:
            # print "self.ignore_branch_len", self.ignore_branch_len

            self._wing_levs.sort(reverse=True)
            nlevs = len(self._wing_levs)
            minl, maxl = min(self._wing_levs), max(self._wing_levs)

            # print "nlevs", nlevs
            # print "minl", minl
            # print "maxl", maxl

        lthetas = [l.theta for l in self.tree.get_terminals()]
        rad_offset = self.annotation_background_separation
        lev_width = self.annotation_background_width

        # print "lthetas", lthetas
        # print "rad_offset", rad_offset
        # print "lev_width", lev_width

        def set_wings_rec( clade ):
            if hasattr(clade, 'annotation') and not hasattr(clade, 'annotation_background_color'):
                if self.warnings:
                    sys.stderr.write('Warning: label "{}" has a default gray background because no color is found for the corresponding "annotation"\n'.format(clade.annotation))

                clade.annotation_background_color = [0.3, 0.3, 0.3]

            if hasattr(clade, 'annotation_background_color'):
                if clade.is_terminal(): # same as non-terminal ??
                    # print "clade.theta", clade.theta
                    # print ''
                    # print "clade.pc", clade.pc
                    # print "clade.nc", clade.nc
                    # print ''
                    # print "clade.pc.theta", clade.pc.theta
                    # print "clade.nc.theta", clade.nc.theta

                    cpc = clade.theta + (clade.theta-clade.nc.theta) if clade.pc is None else clade.pc.theta
                    cnc = clade.theta - (clade.pc.theta-clade.theta) if clade.nc is None else clade.nc.theta

                    if cpc > clade.theta:
                        cpc -= rpi2

                    if cnc < clade.theta:
                        cnc += rpi2

                    lsm = (clade.theta + cpc) * 0.5
                    lgr = (clade.theta + cnc) * 0.5
                else:
                    # print "clade.fc.pc", clade.fc.pc
                    # print "clade.lc.nc", clade.lc.nc
                    # print ''
                    # print "clade.fc.theta", clade.fc.theta
                    # print "clade.lc.theta", clade.lc.theta
                    # print ''
                    # print "clade.fc.pc.theta", clade.fc.pc.theta
                    # print "clade.fc.nc.theta", clade.fc.nc.theta
                    # print ''
                    # print "clade.lc.pc.theta", clade.lc.pc.theta
                    # print "clade.lc.nc.theta", clade.lc.nc.theta

                    f, t = clade.fc.theta, clade.fc.pc.theta if clade.fc.pc else clade.fc.nc.theta
                    cpc = min(abs(f-t), abs(f+rpi2-t), abs(t+rpi2-f))
                    f, t = clade.lc.theta, clade.lc.nc.theta if clade.lc.nc else clade.lc.pc.theta
                    cnc = min(abs(f-t), abs(f+rpi2-t), abs(t+rpi2-f))

                    lsm = clade.fc.theta - cpc * 0.5
                    lgr = clade.lc.theta + cnc * 0.5

                # print ''
                # print "cpc", cpc
                # print "cnc", cnc
                # print "lsm", lsm
                # print "lgr", lgr

                self._wing_thetas.append(lsm)

                if self.ignore_branch_len:
                    rad = 1.0 + lev_width * ( 1 + self._wing_levs.index(int(self._depths[clade.name])) ) - clade.r
                else:
                    rad = (1.0 - clade.r) + lev_width

                # print "rad", rad

                self._wing_radii.append(rad + rad_offset)
                width = abs(lgr - lsm)

                # print "width", width

                self._wing_widths.append(width)
                self._wing_bottoms.append(clade.r)
                self._wing_colors.append(clade.annotation_background_color)

                if clade.r + rad + rad_offset > self._wing_tot_offset:
                    self._wing_tot_offset = clade.r + rad + rad_offset
                    self._tot_offset = self._wing_tot_offset

                    # print ''
                    # print "self._wing_tot_offset", self._wing_tot_offset
                    # print "self._tot_offset", self._tot_offset

                if hasattr( clade, 'annotation') and clade.annotation:
                    lab, ext_key = clade.annotation, None

                    if lab.count(":"):
                        ext_key, lab = lab, lab.split(":")[0]

                    self._label.append(lab)

                    if ext_key:
                        self._ext_key.append( ext_key )

                    avgtheta = (lgr + lsm)*0.5
                    self._label_theta.append( avgtheta )

                    rot90 = hasattr(clade, 'annotation_rotation') and clade.annotation_rotation
                    fract = 0.05 if rot90 else 0.5

                    if self.ignore_branch_len:
                        rad = 1.0 + lev_width * ( 1 + self._wing_levs.index(int(self._depths[clade.name]))  ) - lev_width * fract
                    else:
                        rad = 1.0 + lev_width * fract

                    # print "rad", rad

                    self._label_r.append( rad + rad_offset )
                    rot = avgtheta * 180.0 / rpi + 90.0 if rpi < clade.theta%rpi2 < rpi2 else avgtheta * 180.0 / rpi - 90.0
                    rot = (rot + 360.0) % 360.0 + 1e-10
                    rot = -rot if rot90 else rot

                    # print "rot", rot

                    self._label_rot.append( rot )
                    lfs = clade.annotation_font_size if hasattr(clade,"annotation_font_size") else self.default_annotation_font_size
                    self._annotation_font_size.append( lfs )
                    lfs = clade.annotation_font_stretch if hasattr(clade,"annotation_font_stretch") else self.default_annotation_font_stretch
                    self._annotation_font_stretch.append( lfs )

            for c in clade.clades:
                set_wings_rec( c )

        set_wings_rec( self.tree.root )


    def disambiguate_names(self):
        def disambiguate_names_rec( clade, cnames = set() ):
            if not hasattr(clade,'name'):
                clade.name = "noname_" + str(len(cnames))
            elif clade.name in cnames:
                clade.name = str(clade.name) + "_" + str(len(cnames))
            cnames.add( clade.name )

            for c in clade.clades:
                disambiguate_names_rec( c, cnames )

        disambiguate_names_rec( self.tree.root )


    def get_legend( self ):
        ax1 = plt.subplot(111, visible=False)
        keys = getattr(self, "leg_keys")

        clade_marker_color = getattr(self, "leg_clade_marker_color")
        if not clade_marker_color:
            clade_marker_color = [self.default_clade_marker_color] * len(keys)

        clade_marker_size  = getattr(self, "leg_clade_marker_size")
        if not clade_marker_size:
            clade_marker_size = [self.default_clade_marker_size] * len(keys)

        clade_marker_edge_width = getattr(self, "leg_clade_marker_edge_width")
        if not clade_marker_edge_width:
            clade_marker_edge_width = [self.default_clade_marker_edge_width] * len(keys)

        clade_marker_shape = getattr(self, "leg_clade_marker_shape")
        if not clade_marker_shape:
            clade_marker_shape = [self.default_clade_marker_shape] * len(keys)

        ll = []
        for s,c,lw,m in zip(clade_marker_size, clade_marker_color, clade_marker_edge_width, clade_marker_shape):
            l = ax1.scatter( 0.0, 0.0, s=s, c=c, linewidths=lw, marker=m )
            ll.append(l)

        ax1.set_xlim((0,1))
        ax1.set_ylim((0,1))

        return ll , keys, 'upper right'


    def _init_attr( self ):
        self._depths = dict([(c.name,dist) for c,dist in
            self.tree.depths(self.ignore_branch_len).items()])
        self._max_depth = max(self._depths.values())
        if not self._max_depth:
            self._max_depth = 1.0
        self._r, self._t = arr.array('f'), arr.array('f')
        for att,typ,default in clade_attr:
            setattr( self, att, [] )
        self._rl, self._tl = arr.array('f'), arr.array('f')
        self._branches = []
        self._br_colors = []

        self._wing_levs = []
        self._wing_thetas = arr.array('f')
        self._wing_radii = arr.array('f')
        self._wing_widths = arr.array('f')
        self._wing_bottoms = arr.array('f')
        self._wing_colors = []
        self._wing_alphas = arr.array('f')

        self._label = []
        self._ext_key = []
        self._label_r = arr.array('f')
        self._label_theta = arr.array('f')
        self._label_rot = arr.array('f')
        self._annotation_font_size = []
        self._annotation_font_stretch = []

        self._tot_offset = 1.0
        self._wing_tot_offset = 1.0

        self._ext_patches = []
        self._ext_lines = []


    def draw(self, out_img, out_format=None, out_dpi=72, out_size=7.0, out_pad=0.5, external_legends=False, reorder_tree=True):
        self.reorder_tree(reorder_tree)
        #self.tree.ladderize()
        self.load_set_attr()
        self.disambiguate_names()
        self._init_attr()
        self.set_clade_data()
        self.set_branches()
        self.set_wings()
        self.set_exts()

        size = out_size * self._tot_offset
        fig = plt.figure(figsize=(size,size))

        handles, labels, loc = self.get_legend()

        ax = fig.add_subplot( 111, polar=True, frame_on=False )
        xticks([])
        yticks([])

        if len(self._t) > 0 and len(self._r) > 0:
            ax.scatter( self._t, self._r,
                        marker = self.default_clade_marker_shape,
                        c = self.default_clade_marker_color,
                        edgecolor = self.default_clade_marker_edge_color,
                        lw = self.default_clade_marker_edge_width,
                        s = self.default_clade_marker_size,
                        zorder=12)
            #for x,y,l in zip(self._t,self._r,self.clade_marker_label):
            #    ax.text( x, y, "A", va = 'center', ha = 'center' )

        if self._tl:
            mrkrs = set(self.clade_marker_shape)
            # this needs to be greatly optimized
            for m in mrkrs:
                ax.scatter( [t for i,t in enumerate(self._tl) if self.clade_marker_shape[i] == m],
                            [t for i,t in enumerate(self._rl) if self.clade_marker_shape[i] == m],
                            marker = m, #self.clade_marker_shape,
                            c = [t for i,t in enumerate(self.clade_marker_color) if self.clade_marker_shape[i] == m],
                            edgecolor = [t for i,t in enumerate(self.clade_marker_edge_color) if self.clade_marker_shape[i] == m],
                            lw = [t for i,t in enumerate(self.clade_marker_edge_width) if self.clade_marker_shape[i] == m],
                            s = [t for i,t in enumerate(self.clade_marker_size) if self.clade_marker_shape[i] == m],
                            zorder=12)
            for x,y,l,s,c in zip(self._tl,self._rl,self.clade_marker_label,self.clade_marker_font_size,self.clade_marker_font_color):
                ax.text( x, y, l, va = 'center', ha = 'center', fontstretch = 30, fontsize = s, zorder = 35, color = c )
        bcoll = collections.LineCollection( self._branches,
                                            color=self._br_colors,
                                            linewidth= self.branch_thickness )

        if len( self._wing_thetas ) < 2:
            self._wing_thetas.append(0)
            self._wing_radii.append(0)
            self._wing_widths.append(0)
            self._wing_bottoms.append(0)

        wbar = ax.bar(self._wing_thetas, self._wing_radii, width=self._wing_widths, bottom=self._wing_bottoms, alpha=self.annotation_background_alpha, color=self._wing_colors, edgecolor=self._wing_colors, align='edge')

        for lev,d in self.int_levs.items():
            if 'internal_label' in d:
                start_rot = ( self.internal_labels_rotation
                                 if self.internal_labels_rotation
                                     else self.start_rotation )
                self._label_r.append( 1.0/self._max_depth*lev )
                self._label_theta.append( start_rot*rpi/180.0 )
                self._label.append( d['internal_label'] )
                rot = start_rot+90 if 180.0 < start_rot%360.0 < 360.0 else start_rot-90
                rot = (rot + 360.0) % 360.0
                self._label_rot.append( rot )
                self._annotation_font_size.append( d['internal_label_font_size']
                                                        if 'internal_label_font_size' in d
                                                            else int_attr_d['internal_label_font_size'][1] )
                self._annotation_font_stretch.append( 100 )

        for x,y,s,r,f,fs in zip( self._label_r, self._label_theta,
                                 self._label, self._label_rot,
                                 self._annotation_font_size,
                                 self._annotation_font_stretch ):
            if r < 0.0:
                r = -r
                r %= 360.0
                y2 = y/rpi*180.0%360.0
                if 0 < y2 <= 90:
                    ax.text( y, x, s, rotation = r+90,
                            ha="left", va="bottom",
                            fontsize = f,
                            fontstretch = fs,
                            zorder = 30 )
                if 90 < y2 <= 180:
                    ax.text( y, x, s, rotation = r-90,
                            ha="right", va="bottom",
                            fontsize = f,
                            fontstretch = fs,
                            zorder = 30 )
                if 180 < y2 <= 270:
                    ax.text( y, x, s, rotation = r+90,
                            ha="right", va="top",
                            fontsize = f,
                            fontstretch = fs,
                            zorder = 30 )
                if 270 < y2 <= 360 or y2 == 0.0:
                    ax.text( y, x, s, rotation = r-90,
                            ha="left", va="top",
                            fontsize = f,
                            fontstretch = fs,
                            zorder = 30 )
            else:
                ax.text( y, x, s, rotation = r,
                         ha="center", va="center",
                         fontsize = f,
                         fontstretch = fs,
                         zorder = 30 )
        for e in sorted(self._ext_key):
            ax.scatter( 0.0, 0.0, s = 0.0, label = e)
        ax.add_collection(bcoll)

        for p in self._ext_patches:
            ax.add_patch(p)
        #for l in self._ext_lines:
        #    ax.add_line(l)

        offset = self._wing_tot_offset + self.annotation_background_offset
        for l,v in self.ext_levs.items():
            for p in ['ring_internal_separator_thickness','ring_external_separator_thickness']:
                if p in v and float(v[p]) > 0.0:
                    if l not in self._ext_bottoms.keys():
                        print('[e] External ring #'+str(l), 'defined, but not used. Please check your annotations file')
                        continue

                    bot = offset + self._ext_bottoms[l]
                    if p == 'ring_external_separator_thickness':
                        bot += self._ext_max_height[l]*0.1 if l in self._ext_max_height else 0.1

                    lw = float(v[p])
                    col = v['ring_separator_color']
                    line = lines.Line2D( linearized_circle, [bot]*len(linearized_circle), linewidth = lw, color = col  )
                    ax.add_line(line)
            if 'ring_label' in v and v['ring_label']:
                bot = offset + self._ext_bottoms[l]
                bot1 = offset + ( self._ext_bottoms[l+1] if l+1 in self._ext_bottoms else self._ext_bottoms[l] +
                                 (self._ext_max_height[l]*0.1 if l in self._ext_max_height else 0.1) )

                off = self.start_rotation + (rpi2 - self.total_plotted_degrees) * 0.5
                b = (bot+bot1)*0.5
                s = 180.0 if self.start_rotation == rpi else 0.0
                rot = (self.start_rotation*360.0/rpi2)%180.0 - 90 + s
                fs = v['ring_label_font_size']
                lcol = v['ring_label_color']
                ax.text( self.start_rotation, b, v['ring_label'], rotation = rot,
                         ha="center", va="center", fontsize = fs, color = lcol  )


        if hasattr(self,"title"):
            ax.set_title(self.title,fontdict = {'size':self.title_font_size})

        #a,b = ax.get_ylim()
        ylim((0.0,self._tot_offset*1.075))

        #ax.legend(  frameon = False, markerscale = 0  )
        #for t in self._ext_key:
        #ax.text( 0, 1, t )

        if self._ext_key:
            if external_legends:
                lengths = [len(s) for s in self._ext_key]
                charsize = self.annotation_legend_font_size * 0.0138889
                width = round(max(lengths) * charsize * 10.) / 10.
                height = round(self._tot_offset * len(self._ext_key) * charsize * 10.) / 10.
                fig_annot = plt.figure(figsize=(width, height))
                ax = fig_annot.add_subplot(111, frame_on=False, xticks=[], yticks=[])

            ll = [ax.scatter(0.0, 0.0, s=0.0)] * len(self._ext_key)
            plt.figlegend(ll, sorted(self._ext_key), 'upper left', frameon=False,
                shadow=False, scatterpoints=1, handlelength=0, markerscale=0.0,
                handletextpad=0.2, ncol=1, labelspacing=0.1,
                prop={'size': self.annotation_legend_font_size})

            if external_legends: # add '_annot' to the filename
                if out_format:
                    img_name = out_img + "_annot"
                else:
                    img_name = out_img[:out_img.rfind('.')] + "_annot" + out_img[out_img.rfind('.'):]

                plt.savefig(img_name, dpi=out_dpi, bbox_inches='tight',
                    bbox_extra_artists=handles, pad_inches=out_pad, format=out_format)
                plt.close()
        # else:
        #     print '[w] External annotation not created, no annotated labels!'

        if external_legends:
            if labels: # need to check if there are annotated labels!
                charsize = self.class_legend_font_size * 0.0148889
                width = round(max([len(s) for s in labels]) * charsize * self.class_legend_marker_size * 10.) / 10.
                height = round(self._tot_offset * len(labels) * charsize * self.class_legend_marker_size * 10.) / 10.
                plt.figure(figsize=(width, height))
            else:
                print('[w] External legend not created, no annotated labels!')

        if labels:
            plt.figlegend(handles, labels, loc, labelspacing=0.1, frameon=False,
                markerscale=self.class_legend_marker_size, scatterpoints=1,
                handletextpad=0.2, prop={'size': self.class_legend_font_size})

        if external_legends: # add '_legend' to the filename
            if out_format:
                img_name = out_img + "_legend"
            else:
                img_name = out_img[:out_img.rfind('.')] + "_legend" + out_img[out_img.rfind('.'):]

            if labels:
                plt.savefig(img_name, dpi=out_dpi, pad_inches=out_pad,
                    bbox_extra_artists=handles, format=out_format)
                plt.close()

        if True: #
            plt.savefig(out_img, dpi=out_dpi,
                # facecolor=fc,
                bbox_inches='tight', bbox_extra_artists=handles,
                pad_inches=out_pad, format=out_format,
                # edgecolor=fc
            )
            plt.close()
        else:
            plt.show()
