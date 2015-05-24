import os

import numpy as np
import yoda

def bins_from_path(path, histogram_name=None, bin_heights_column=None, centered=True):
    if is_YODA(path):
        return bins_from_yoda(path, histogram_name, centered=centered) 
    else:
        return bins_from_dat(path, bin_heights_column, centered=centered)

def has_extension(path, extension=''):
    fileExtension = os.path.splitext(path)[-1].lower()
    return fileExtension == '.' + extension

def is_YODA(path):
    return has_extension(path, 'yoda')

def bins_with_object(data_object, height_from_entry, edges_from_entry, left_edge_from_entry, right_edge_from_entry, centered=True):
    bin_heights = [height_from_entry(entry) for entry in data_object]
    if centered:
        bin_centers = [sum(edges_from_entry(entry)) / 2.0 for entry in data_object]
        array = np.ndarray(shape=(2, len(bin_centers)), dtype=float)
        array[0] = bin_centers
        array[1] = bin_heights
    else:
        left_bin_edges = [left_edge_from_entry(entry) + (right_edge_from_entry(entry) - left_edge_from_entry(entry))/1000
                          for entry in data_object]
        left_bin_edges[0] = left_edge_from_entry(data_object[0])
        right_bin_edges = [right_edge_from_entry(entry) - (right_edge_from_entry(entry) - left_edge_from_entry(entry))/1000
                           for entry in data_object]
        right_bin_edges[-1] = right_edge_from_entry(data_object[-1])
        array = np.ndarray(shape=(2, len(left_bin_edges)*2), dtype=float)
        array[0] = np.ravel(zip(left_bin_edges, right_bin_edges))
        array[1] = np.ravel(zip(bin_heights, bin_heights)) 
    return array.transpose()

def bin_height_from_yoda_Scatter2D(entry):
    return entry.y

def bin_edges_from_yoda_Scatter2D(entry):
    return left_bin_edge_from_yoda_Scatter2D(entry), right_bin_edge_from_yoda_Scatter2D(entry)

def left_bin_edge_from_yoda_Scatter2D(entry):
    return entry.xMin

def right_bin_edge_from_yoda_Scatter2D(entry):
    return entry.xMax

def bin_height_from_yoda_Histo1D(entry):
    return entry.height

def bin_edges_from_yoda_Histo1D(entry):
    return entry.xEdges

def left_bin_edge_from_yoda_Histo1D(entry):
    return bin_edges_from_yoda_Histo1D(entry)[0]

def right_bin_edge_from_yoda_Histo1D(entry):
    return bin_edges_from_yoda_Histo1D(entry)[1]

def bins_from_yoda(path, histogram_name, centered=True):
    yoda_histos = yoda.readYODA(path)
    yoda_histo = yoda_histos[histogram_name]
    if isinstance(yoda_histo, yoda.Scatter2D):
        return bins_with_object(yoda_histo.points,
                                bin_height_from_yoda_Scatter2D,
                                bin_edges_from_yoda_Scatter2D,
                                left_bin_edge_from_yoda_Scatter2D,
                                right_bin_edge_from_yoda_Scatter2D,
                                centered=centered)
    else:
        return bins_with_object(yoda_histo.bins,
                                bin_height_from_yoda_Histo1D,
                                bin_edges_from_yoda_Histo1D,
                                left_bin_edge_from_yoda_Histo1D,
                                right_bin_edge_from_yoda_Histo1D,
                                centered=centered)

def bin_height_from_dat_entry(entry):
    return entry[2]

def bin_edges_from_dat_entry(entry):
    return left_bin_edge_from_dat_entry(entry), right_bin_edge_from_dat_entry(entry)

def left_bin_edge_from_dat_entry(entry):
    return entry[0]

def right_bin_edge_from_dat_entry(entry):
    return entry[0]

def bins_from_dat(path, bin_heights_column, centered=True):
    dat_histo = np.loadtxt(path, usecols = (0,1,bin_heights_column))
    return bins_with_object(dat_histo,
                            bin_height_from_dat_entry,
                            bin_edges_from_dat_entry,
                            left_bin_edge_from_dat_entry,
                            right_bin_edge_from_dat_entry,
                            centered=centered)
