import os

import numpy as np
import yoda

def bins_from_path(path, histogram_name=None, centered=True):
    if is_YODA(path):
        return bins_from_yoda(path, histogram_name, centered=centered) 
    else:
        return bins_from_dat(path, centered=centered)

def has_extension(path, extension=''):
    fileExtension = os.path.splitext(path)[-1].lower()
    return fileExtension == '.' + extension

def is_YODA(path):
    return has_extension(path, 'yoda')

def bins_from_yoda(path, histogram_name, centered=True):
    yoda_histos = yoda.readYODA(path)
    yoda_histo = yoda_histos[histogram_name]
    bins = yoda_histo.bins
    bin_heights = [bin.height for bin in bins]
    if centered:
        bin_centers = [sum(bin.xEdges)/2.0 for bin in bins]
        array = np.ndarray(shape=(2, len(bin_centers)), dtype=float)
        array[0] = bin_centers
        array[1] = bin_heights
    else:
        left_bin_edges = [bin.xEdges[0] + bin.xWidth/1000 for bin in bins]
        left_bin_edges[0] = bins[0].xEdges[0]
        right_bin_edges = [bin.xEdges[1] - bin.xWidth/1000 for bin in bins]
        right_bin_edges[-1] = bins[-1].xEdges[1]
        array = np.ndarray(shape=(2, len(left_bin_edges)*2), dtype=float)
        array[0] = np.ravel(zip(left_bin_edges, right_bin_edges))
        array[1] = np.ravel(zip(bin_heights, bin_heights))
    return array.transpose()
    
def bins_from_dat(path, centered=True):
    dat_histo = np.loadtxt(path, usecols = (0,1,2))
    bin_heights = [row[2] for row in dat_histo]
    if centered:
        bin_centers = [(row[1] + row[0]) / 2.0 for row in dat_histo]
        array = np.ndarray(shape=(2, len(bin_centers)), dtype=float)
        array[0] = bin_centers
        array[1] = bin_heights
    else:
        left_bin_edges = [row[0] + (row[1] - row[0])/1000 for row in dat_histo]
        left_bin_edges[0] = dat_histo[0][0]
        right_bin_edges = [row[1] - (row[1] - row[0])/1000 for row in dat_histo]
        right_bin_edges[-1] = dat_histo[-1][1]
        array = np.ndarray(shape=(2, len(left_bin_edges)*2), dtype=float)
        array[0] = np.ravel(zip(left_bin_edges, right_bin_edges))
        array[1] = np.ravel(zip(bin_heights, bin_heights)) 
    return array.transpose()
