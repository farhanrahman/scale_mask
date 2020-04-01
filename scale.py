#!/usr/bin/env python

import os
import re
import numpy
import optparse
import datetime

from stl import mesh
from os.path import expanduser

class MeshScaler(object):
    '''
    This object reads an STL mesh and provides utility to get a scaling factor.
    The scaling factor is calculated based on the length of the bounding box
    around the mesh and getting the ratio of (reference length : bounding box length).
    '''

    def __init__(self, options, mesh_path):
        self.options = options
        self.mesh_path = expanduser(mesh_path)
        if not os.path.exists(self.mesh_path):
            raise Exception("File not found at {}".format(self.mesh_path))
        self.mesh_name = os.path.basename(self.mesh_path)
        self.mesh_obj = mesh.Mesh.from_file(self.mesh_path)

    def getScaleFactor(self, ref_length):
        '''
        Returns the scale factor compared to a reference object's length

        args:
            ref_length: int. Length of reference object to scale mesh_obj to in centimeters.

        returns:
            The ratio of ref_length * 10 : scale_factor
        '''

        dimensions = [(numpy.max(val) - numpy.min(val))
                        for val in [self.mesh_obj.x, self.mesh_obj.y, self.mesh_obj.z]]
        padding_mm = (float(self.options.padding_in_cm) * 2 * 10.0)
        length_mm = max(dimensions)
        assert(length_mm > padding_mm)
        length_mm -= padding_mm
        scale_factor = (float(ref_length)*10)/length_mm
        return scale_factor

    def writeOutScaled(self, output_dir, scale_factor):
        '''
        Scales the mesh_obj and writes it out into the specified output_dir.

        args:
            output_dir: string. Directory to write the mesh_obj out to.
            scale_factor: float. Scales xyz uniformly by this parameter.
        '''

        self.mesh_obj.x *= scale_factor
        self.mesh_obj.y *= scale_factor
        self.mesh_obj.z *= scale_factor
        output_path = output_dir + os.path.sep + self.mesh_name
        print "writing out {}".format(output_path)
        self.mesh_obj.save(output_path)

if __name__=="__main__":

    parser = optparse.OptionParser("scale_mask.py")

    # Compulsory parameters

    parser.add_option("--mask-file", default=None,
                     dest="mask_file",
                     help="Name of the mask file to use for reference.")

    parser.add_option("--nose-to-chin-in-cm", default=None,
                      dest="nose_to_chin_in_cm",
                      help="Length of protruding bone of nose to chin in centimeters.")

    #Optionals

    parser.add_option("--padding-in-cm", default=0.3,
                      dest="padding_in_cm",
                      help="Extra padding to be applied in the inside of the mask. 0.3 cm by default.")

    parser.add_option("--rest-files-regex", default=None,
                      dest="rest_files_regex",
                      help="Regex to capture other files to scale.")

    parser.add_option("--output-dir", default=None,
                      dest="output_dir",
                      help="Directory where scaled stl files will be created.")

    (opt, args) = parser.parse_args()

    if (opt.mask_file == None):
        raise Exception("Mask file not provided or doesn't exist. Please set --mask-file.")

    if opt.nose_to_chin_in_cm == None:
        raise Exception("Please provide the option --nose-to-chin-in-cm.")

    mask = MeshScaler(opt, opt.mask_file)
    meshes = dict()
    meshes[mask.mesh_name] = mask
    scale_factor = mask.getScaleFactor(opt.nose_to_chin_in_cm)
    print "scale_factor: {}".format(scale_factor)

    dir_name = os.path.dirname(expanduser(opt.mask_file))
    regex = re.compile(str(opt.rest_files_regex) if opt.rest_files_regex != None else ".*.stl")
    for filename in os.listdir(dir_name):
        if regex.search(filename):
            if filename not in meshes:
                meshes[filename] = MeshScaler(opt, dir_name + os.path.sep + filename)

    output_dir = None
    if opt.output_dir != None:
        output_dir = expanduser(opt.output_dir)
    else:
        output_dir = "mesh_" + datetime.datetime.now().strftime("%d.%m.%Y.%H.%m.%S")

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    for m in meshes:
        meshes[m].writeOutScaled(output_dir, scale_factor)
