import seaborn as sns

from .statistics import *

def plot_dataframe(dataframe,
                   axis=None,
                   condition='',
                   legend=True,
                   band_style=['ci_band'],
                   err_estimator=asymmetric_hessian_error,
                   **kwargs):
    sns.tsplot(dataframe,
               time=dataframe.columns[0],
               unit='unit',
               value=dataframe.columns[1],
               condition=condition,
               n_boot=0,
               estimator=central_value_member,
               err_estimator=err_estimator,
               err_style=band_style,
               ax=axis,
               legend=legend,
               # err_kws={'alpha': 0.3}  # Use this to change the appearance of the band/traces
               **kwargs
               )
