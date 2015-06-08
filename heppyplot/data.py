from .configuration import *
from .statistics import *
from .data_helpers import *

def dataframes_from_config(config):

    default_normalizing_dataframes = [None, None]
    main_and_diff_distributions = [[], []]
    already_normalized = [[], []]
    settings = []
    has_bands = False

    # use axis labels as data column headers
    x_title = read_configuration_value(config, key='x_title')
    y_titles = read_configuration_subplot_values(config, key='y_title', defaults=[None, '__use_main__'])

    # condition will be used as legend title by tsplot
    condition = read_configuration_value(config, key='legend_title', default='')

    bin_style = read_configuration_value(config, key='bin_style', default='step')
    centered = bin_style == 'center'

    x_lim = read_configuration_value(config, key='x_lim', default=None)

    if read_configuration_value(config, key='err_estimator', default='asymmetric_hessian_error') == 'asymmetric_hessian_error':
        err_estimator = asymmetric_hessian_error
    else:
        err_estimator = standard_error

    data_path = read_configuration_value(config, key='data_path', default=".")

    config_distributions = read_configuration_value(config, key='distributions')

    for distribution in config_distributions:

        main_and_diff_normalized_dataframe_or_none, distribution_has_bands, \
        main_and_diff_distributions_are_normalized = read_distribution(data_path,
                                                                       distribution,
                                                                       centered,
                                                                       condition,
                                                                       x_title,
                                                                       y_titles,
                                                                       x_lim,
                                                                       err_estimator=err_estimator,
                                                                       settings=settings,
                                                                       main_and_diff_distributions=main_and_diff_distributions,
                                                                       config_distributions=config_distributions)[1:]

        for i in range(2):
            if main_and_diff_normalized_dataframe_or_none[i] is not None:
                default_normalizing_dataframes[i] = main_and_diff_normalized_dataframe_or_none[i]
            already_normalized[i].append(main_and_diff_distributions_are_normalized[i])

        if distribution_has_bands:
            has_bands = distribution_has_bands

    for i, default_normalizing_dataframe in enumerate(default_normalizing_dataframes):
        if default_normalizing_dataframe is not None:
            for distribution, is_already_normalized in zip(main_and_diff_distributions[i], already_normalized[i]):
                if not is_already_normalized:
                    for df in distribution:
                        df[y_titles[i]] /= default_normalizing_dataframe[y_titles[i]]

    for i in range(2):
        main_and_diff_distributions[i] = [pd.concat(dataframes) if len(dataframes) else None for dataframes in main_and_diff_distributions[i]]

    return main_and_diff_distributions[0], main_and_diff_distributions[1], settings, has_bands
