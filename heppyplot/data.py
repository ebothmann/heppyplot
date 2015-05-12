import sys
import os
import glob

import pandas as pd

from .configuration import *
from .read_data import *
from .statistics import *

def dataframes_from_config(config):


    dataframe = None
    diff_dataframe = None

    normalized_dataframe = None
    normalized_diff_dataframe = None

    has_bands = False

    settings = []
    distributions = []
    diff_distributions = []

    # use axis labels as data column headers
    x_title = read_configuration_value(config, key='x_title')
    y_titles = read_configuration_subplot_values(config, key='y_title', defaults=[None, '__use_main__'])

    # condition will be used as legend title by tsplot
    condition = read_configuration_value(config, key='legend_title', default='')

    bin_style = read_configuration_value(config, key='bin_style', default='step')

    x_lim = read_configuration_value(config, key='x_lim', default=None)

    data_path = read_configuration_value(config, key='data_path', default=".")

    for distribution in read_configuration_value(config, key='distributions'):
        dataframes = []
        diff_dataframes = []
        path = os.path.join(data_path, read_configuration_value(distribution, key='path'))
        histogram_name = read_configuration_value(distribution, key='histogram_name', default=None)
        if os.path.isdir(path):
            data_file_paths = glob.glob(os.path.join(path, '*.*'))
        else:
            data_file_paths = [path]
        for i, data_file_path in enumerate(data_file_paths):

            if has_bands == False and i > 0:
                has_bands = True
            centered = bin_style == 'center'
            bins = bins_from_path(data_file_path, histogram_name=histogram_name, centered=centered)
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

            append_to_dataframes(dataframe, dataframes, distribution)
            normalized_dataframe = update_normalized_dataframe(dataframe, normalized_dataframe, distribution)

            diff_dataframe = dataframe.copy()
            diff_dataframe.rename(columns={y_titles[0]: y_titles[1]}, inplace=True)

            try:
                append_to_dataframes(diff_dataframe, diff_dataframes, distribution['diff'], hidden_default=True)
                normalized_diff_dataframe = update_normalized_dataframe(diff_dataframe, normalized_diff_dataframe, distribution['diff'])
            except KeyError:
                pass
        distributions.append(dataframes)
        diff_distributions.append(diff_dataframes)

        if read_configuration_value(config, key='err_estimator', default='asymmetric_hessian_error') == 'asymmetric_hessian_error':
            err_estimator = asymmetric_hessian_error
        else:
            err_estimator = standard_error
        settings.append({'err_estimator': err_estimator})

    if normalized_dataframe is not None:
        for distribution in distributions:
            for df in distribution:
                df[y_titles[0]] /= normalized_dataframe[y_titles[0]]

    if normalized_diff_dataframe is not None:
        for distribution in diff_distributions:
            for df in distribution:
                df[y_titles[1]] /= normalized_diff_dataframe[y_titles[1]]

    distributions = [pd.concat(dataframes) if len(dataframes) else None for dataframes in distributions]
    diff_distributions = [pd.concat(dataframes) if len(dataframes) else None for dataframes in diff_distributions]

    return distributions, diff_distributions, settings, has_bands


def append_to_dataframes(dataframe, dataframes, distribution, hidden_key='hidden', hidden_default=False, should_copy=False):
    if not read_configuration_value(distribution, key=hidden_key, default=hidden_default):
        if should_copy:
            dataframes.append(dataframe.copy())
        else:
            dataframes.append(dataframe)

def update_normalized_dataframe(dataframe, normalized_dataframe, distribution, normalized_key='normalized', should_copy=True):
    if (normalized_dataframe is None) and read_configuration_value(distribution, key=normalized_key, default=False):
        return dataframe.copy()
    else:
        return normalized_dataframe
