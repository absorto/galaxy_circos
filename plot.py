#!/usr/bin/env python



import pprint
import argparse
import sys, os, shutil
import subprocess

from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))



parser = argparse.ArgumentParser(description='Generate a Circos Plot configuration set')
parser.add_argument('--circos_path', required=True, help="path to circos command")
parser.add_argument('--path', required=True, help="path to a working directory")
parser.add_argument('--karyotype', type=argparse.FileType('r'), required=True )
# links
parser.add_argument('--links',  type=argparse.FileType('r'), required=False, nargs='*' )
parser.add_argument('--links_colors', required=False, nargs='*')
parser.add_argument('--links_radius', required=False)
parser.add_argument('--links_bezier_radius', required=False)
# tracks
parser.add_argument('--tracks', type=argparse.FileType('r'), required=False, nargs='*')
parser.add_argument('--types', required=False, nargs='*', choices=['histogram', 'line', 'scatter','heatmap'])
parser.add_argument('--orientations', required=False, nargs='*', choices=['in', 'out'])
parser.add_argument('--r0', required=False, nargs='*')
parser.add_argument('--r1', required=False, nargs='*')
parser.add_argument('--tracks_colors', required=False, nargs='*')


if __name__ == '__main__':
    args       = parser.parse_args()
    circos_path = args.circos_path
    path       = args.path
    karyotype  = args.karyotype

    links      = args.links
    links_colors = args.links_colors
    links_radius = args.links_radius
    links_bezier_radius = args.links_bezier_radius

    tracks     = args.tracks
    radii0     = args.r0
    radii1     = args.r1
    tracks_colors     = args.tracks_colors
    types      = args.types
    orientations = args.orientations

    # maybe sanity check on input files?
    karyotype_path = karyotype.name
    karyotype.close()
    
    if links:
        l = list()
        for n in range(0,len(links)):
            l.append({'path': links[n].name,
                      'color': links_colors[n]})
    else:
        l = None


    if tracks:
        t = list()
        for n in range(0,len(tracks)):                      
            t.append({'path': tracks[n].name,
                      'type': types[n],
                      'color': colors[n],
                      'r0': "%sr" % radii0[n],
                      'r1': "%sr" % radii1[n],
                      'orientation': orientations[n] })
    else:
        t = None


    print "links"
    pprint.pprint(l)

    print "tracks"
    pprint.pprint(t)
    
    # create directory for templates
    os.makedirs(path)    

    # shutil.copy('templates/bands.conf', path )
    shutil.copy('templates/ideogram.conf', path )
    # shutil.copy('templates/ideogram.label.conf', path )
    # shutil.copy('templates/ideogram.position.conf', path )


    with open( path + '/circos.conf', 'w') as f:
        circos_conf = env.get_template('circos.conf')
        f.write( circos_conf.render( links        = l,
                                     links_radius = "%sr" % links_radius,
                                     links_bezier_radius = "%sr" % links_bezier_radius,
                                     tracks       = t,
                                     karyotype    = karyotype_path  ) )





    os.chdir(path)
    p = subprocess.Popen(circos_path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        print line,
    retval = p.wait()
