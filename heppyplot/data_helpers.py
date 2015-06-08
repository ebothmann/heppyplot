import os
import glob

import pandas as pd

from .configuration import *
from .read_data import *

def read_distribution(data_path, distribution, centered, condition, x_title, y_titles, x_lim,
                      err_estimator=None, settings=None, main_and_diff_distributions=[None, None],
                      config_distributions=None, read_always=False, first_only=False, ignore_normalizations=False):
    has_bands = False
    main_and_diff_dataframes = [[], []]
    normalized_dataframes = [None, None]
    distribution_is_normalized = [False, False]
    path = os.path.join(data_path, read_configuration_value(distribution, key='path'))
    histogram_name = read_configuration_value(distribution, key='histogram_name', default=None)
    bin_heights_column = read_configuration_value(distribution, key='bin_heights_column', default=2)
    if os.path.isdir(path):
        data_file_paths = glob.glob(os.path.join(path, '*.*'))
        if first_only:
            data_file_paths = [data_file_paths[0]]
    else:
        data_file_paths = [path]

    main_and_diff_normalizing_dataframes = [None, None]
    if not ignore_normalizations:
        normalizing_file_paths = read_configuration_subplot_values(distribution, key='normalized_by', defaults=[None, None])
        for i, normalizing_file_path in enumerate(normalizing_file_paths):
            if normalizing_file_path is not None:
                normalizing_distribution = None
                for normalizing_distribution_candidate in config_distributions:
                    if read_configuration_value(normalizing_distribution_candidate, key='path') == normalizing_file_path:
                        normalizing_distribution = normalizing_distribution_candidate
                        break
                if (normalizing_distribution == None):
                    raise Exception("There was no distribution with the file path" + normalizing_file_path + " to normalize by.")
                main_and_diff_normalizing_dataframes[i] = read_distribution(data_path, normalizing_distribution, centered, condition, x_title, y_titles, x_lim,
                                                                            read_always=True, first_only=True, ignore_normalizations=True)[0]

    for i, data_file_path in enumerate(data_file_paths):

        if has_bands == False and i > 0:
            has_bands = True
        bins = bins_from_path(data_file_path,
                              histogram_name=histogram_name,
                              bin_heights_column=bin_heights_column,
                              centered=centered)
        dataframe = pd.DataFrame(bins,
                                 columns=[x_title, y_titles[0]])
        scale_factor = read_configuration_value(distribution, key='scale', default=None)
        if scale_factor is not None:
            dataframe[y_titles[0]] *= scale_factor
        dataframe['unit'] = i
        condition_name = read_configuration_value(distribution, key='label', default=path)
        dataframe[condition] = condition_name

        # Truncate data not being used
        # For step plots we make sure that we do not cut bins
        if x_lim is not None:
            dataframe = dataframe[dataframe[x_title] > x_lim[0]]
            if (not centered) and dataframe.count()[0] % 2 == 1:
                dataframe.drop(dataframe.head(1).index, inplace=True)
            dataframe = dataframe[dataframe[x_title] < x_lim[1]]
            if (not centered) and dataframe.count()[0] % 2 == 1:
                dataframe.drop(dataframe.tail(1).index, inplace=True)

        if not ignore_normalizations:
            normalized_dataframes[0] = update_normalized_dataframe(dataframe, normalized_dataframes[0], distribution)

        if not first_only:
            diff_dataframe = dataframe.copy()
            diff_dataframe.rename(columns={y_titles[0]: y_titles[1]}, inplace=True)
            try:
                normalized_dataframes[1] = update_normalized_dataframe(diff_dataframe, normalized_dataframes[1], distribution['diff'])
            except KeyError:
                pass

        if main_and_diff_normalizing_dataframes[0] is not None:
            dataframe[y_titles[0]] /= main_and_diff_normalizing_dataframes[0][y_titles[0]]
            distribution_is_normalized[0] = True
        append_to_dataframes(dataframe, main_and_diff_dataframes[0], distribution)

        if not first_only:
            if main_and_diff_normalizing_dataframes[1] is not None:
                diff_dataframe[y_titles[1]] /= main_and_diff_normalizing_dataframes[1][y_titles[0]]
                distribution_is_normalized[1] = True
            try:
                append_to_dataframes(diff_dataframe, main_and_diff_dataframes[1], distribution['diff'], hidden_default=True)
            except KeyError:
                pass

    for i in range(2):
        if main_and_diff_distributions[i] is not None:
            main_and_diff_distributions[i].append(main_and_diff_dataframes[i])

    if settings is not None:
        settings.append({'err_estimator': err_estimator})

    return main_and_diff_dataframes[0][0], normalized_dataframes, has_bands, (distribution_is_normalized[0], distribution_is_normalized[1])

def append_to_dataframes(dataframe, dataframes, distribution, hidden_key='hidden', hidden_default=False, should_copy=False):
    if not read_configuration_value(distribution, key=hidden_key, default=hidden_default):
        if should_copy:
            dataframes.append(dataframe.copy())
        else:
            dataframes.append(dataframe)

def update_normalized_dataframe(dataframe, normalized_dataframe, distribution, normalized_key='normalized'):
    if (normalized_dataframe is None) and read_configuration_value(distribution, key=normalized_key, default=False):
        return dataframe.copy()
    else:
        return normalized_dataframe
