import pandas as pd

import numpy as np

from distfit import distfit

from tqdm.auto import tqdm

from matplotlib import pyplot as plt

from seaborn import countplot, histplot, boxplot, violinplot, kdeplot, move_legend

from typing import Optional, Union, Tuple, List

import numpy.typing as npt

from .._utils import SEQUENCE_LIKE, itr_plot, PlotMixin

from .._logr import _z_log

###################################################################

class Dist(PlotMixin):
    """
    Visualizing and finding the best fit distribution for parametric, non-parametric 
    and discrete distributions.
    
    Visualizations includes the following plots `Seaborn Module`:

    - Count plot
    - Histograms
    - Box plot
    - Violin plot
    - Kernel density estimation(kde) plot
        
    Notes
    -----
    - Categorical features are considered irrespective of their dtype, either string 
      or numbers, users of this class are advised to explicitly specify whether the
      columns are categorical using ``cat_cols`` parameter as this will affect both
      grouping and plots.
    - If not explicitly specified then it is assumed that if features ``cols`` are 
      categorical then ``target`` must be numeric and vise versa. This is only to 
      dictate the direction of categorical grouping of numeric data.
    - Categories are preprocessed to highlight `rare` levels; only frequent levels are 
      displayed as is while others are grouped into a single level called `rare`. This 
      behavior can be controlled by ``top_n`` and ``rare_thresh`` parameters. For 
      severely imbalanced datasets, ensure that ``rare_thresh`` parameter account for 
      minority class when plotting conditional distributions.
    - Missing values `NaN` in categorical features are not removed, rather, 
      considered as a separate level called `missing`. If missing values happens to be 
      also rare, then they will be labeled as `rare` instead of `missing`.
    - Keep in mind the ``frac`` parameter when using the preprocessed DataFrame out of 
      this class.
      
    Parameters
    ----------
    df: pandas dataframe
        data source
    cols: sequence (lists, tuples, NumPy arrays or Pandas Base Index),
        column names of features to plot. Better to use homogeneous subsets, example:
        either all categorical or all numeric features; categorical subset can have
        multiple dtypes (object or numeric) depending on the nature of the feature
    target: str or None
        target column name
    cat_cols: Bool or None
        indicate whether ``cols`` are categorical in nature or not and in-turn the 
        direction of categorical grouping of numeric data, for Example: for 
        `binary target`, numeric ``cols`` are to be grouped by the categorical 
        ``target`` and vise versa. If `None`, inferred automatically.
    rare_thresh, top_n: float, int
        max cardinality beyond which lvls are grouped and analysed as a single level;
        If ``rare_thresh`` = 0 or ``top_n`` < 2 then all levels are analysed as is,
        otherwise these levels are grouped as a single `rare` level.

        Notes
        -----
        - both are independent, for example considering categorical level to be 
          `rare` (1% - 5%) can still result in a high cardinality categorical
          feature (> N levels)
        - missing values will be displayed as `rare` rather than `missing` if the 
          new `missing` category is below ``rare_thresh``
    frac: float or None
        fraction of dataframe to use as a sample 
        for analysis:

            - 0 < ``frac`` < 1 returns a random sample with size ``frac``. 
            - ``frac`` = 1 returns shuffled dataframe.
            - ``frac`` > 1 up-sample the dataframe, sampling of the same row more 
              than once.
    random_state: int
        for reproducibility, controls the random number generator for ``frac``
        parameter and `best_fit` method.
    figsize: tuple or None 
        dimensions of matplotlib figure (width, height)
    n_rows: int
        number of rows in matplotlib subplot figure
    n_cols: int
        number of columns in matplotlib subplot figure
    silent: Bool
        solicit user input for continuation during iterative plotting. If `True`,
        plotting proceeds without user interaction.
    hide_p_bar: Bool
        triggers hiding progress bar (tqdm module); Default 'False'
        
    Attributes
    ----------
    z_df: pandas dataframe
        preprocessed dataframe that was used internally
    z_freq_lvls_map: dict
        where keys are column(s) name(s) and values are frequent levels. Only 
        applicable when ``cols`` are categorical
    xludd_feats: numpy array
        categorical column names excluded from the analysis being dominated by 
        rare levels. Only applicable when ``cols`` are categorical

    """

    def __init__(self, 
                 df: pd.DataFrame,
                 cols: SEQUENCE_LIKE,
                 target: Optional[str] = None,
                 cat_cols: Optional[bool] = None,
                 rare_thresh: float = 0.05,
                 top_n: int = 25,
                 frac: Optional[float] = None,
                 random_state: int = 45,
                 figsize: Optional[Tuple[int, int]] = None,
                 n_rows: Optional[int] = None,
                 n_cols: Optional[int] = None,
                 silent: bool = False,
                 hide_p_bar: bool = False):
        
        # input checks  
        if not isinstance(cols, (list, tuple, np.ndarray, pd.Index)):
            raise TypeError("'cols' parameter accepts a sequence e.g: Lists, Tuples, NumPy Arrays or Pandas Base Index. "
                            f"However, '{type(cols)}' was received!")
        if target and not isinstance(target, str):
            raise TypeError("please pass 'target' column name as string")
        if np.any(~np.isin(list(set(np.r_[np.array(cols), [target] if target else []])), df.columns)):
            raise KeyError("Missing columns! Please ensure that all columns to analyze are included in the DataFrame")
        if np.any([df[col].dtype.kind in 'M' for col in cols]) and cat_cols: 
            raise TypeError("Datetime columns are casted as categorical, Please ensure 'cat_cols' parameter is set to 'False'")
        
        # prepare data for preprocessing
        if frac:
            replace = True if frac > 1 else False
            self.z_df_ = df.sample(frac = frac, replace = replace, random_state = random_state).copy()
        else:
            self.z_df_ = df.copy()

        self._ori_df = df.copy() # to be used in `best_fit` and dtype checks. TODO: Alternative for this excess overhead
        self._cols = cols
        self._target = target
        self._cat_cols = cat_cols
        self._rare_thresh = rare_thresh
        self._top_n = top_n
        self._random_state = random_state
        self._figsize = figsize
        self._n_rows = n_rows
        self._n_cols = n_cols
        self._silent = silent
        self._hide_p_bar = hide_p_bar
        
        # preprocess categorical columns
        self._preprocess()


    @itr_plot
    def cp(self, 
           stat: str = 'count',
           native_scale: bool = False,
           legend: Union[str, bool] = 'auto',
           hue_agg: List[str] = ['mean'],
           log_scale: Optional[Union[int, bool, Tuple[int, bool]]] = False,
           color: str = 'lightblue',
           palette: str = 'Paired',
           nbins: Union[int, str] = 'auto',
           axis: str = 'x',
           tight: Optional[bool] = None,
           x_ax_rotation: Optional[int] = None,
           theme: str = 'darkorange'):
        """
        Visualize categorical feature distribution using Seaborn's Count Plot
        
        Note
        ----
        Categorical features plagued with rare levels (< rare_thresh) will be skipped;
        Only those having at least 2 frequent levels are plotted
        
        Parameters
        ----------
        stat: str
            One of 'count', 'percent', 'proportion' or 'probability'. Statistic to compute; 
            when not 'count', bar heights will be normalized so that they sum to 100 
            (for 'percent') or 1 (otherwise) across the plot.
        native_scale: bool
            When True, numeric or datetime values on the categorical axis will maintain
            their original scaling rather than being converted to fixed indices.
        legend: "auto", "brief", "full", or False
            How to draw the legend. If "brief", numeric `hue` and `size`
            variables will be represented with a sample of evenly spaced values.
            If "full", every group will get an entry in the legend. If "auto",
            choose between brief or full representation based on number of levels.
            If `False`, no legend data is added and no legend is drawn.
        hue_agg: list
            list of functions and/or function names, e.g.: [np.sum, 'mean']
            to use for aggregating the data. Functions, must either work 
            when passed a Series/DataFrame or when passed to Series/DataFrame.apply.
            Only applicable for conditional distributions between numeric and categorical 
            variable, otherwise data is sorted ascendingly following the frequency(count) 
            of categorical levels. e.g.:
            pandas.DataFrame.groupby(category)[value].agg(hue_agg).sort_values(hue_agg)
        log_scale: bool or number, or pair of bools or numbers
            Set axis scale(s) to log. A single value sets the data axis for any numeric
            axes in the plot. A pair of values sets each axis independently.
            Numeric values are interpreted as the desired base (default 10).
            When `None` or `False`, seaborn defers to the existing Axes scale.
        color: str
            adjust color of seaborn plots as desired
        palette: str
            adjust color of 'hue' as desired; See seaborn.color_palette('palette_name')
        nbins: int or 'auto'
            For plot decoration, maximum number of axis intervals; one less than max 
            number of ticks. If the string 'auto', the number of bins will be 
            automatically determined based on the length of the axis.
        axis: str
            For plot decoration, one of ['both', 'x', 'y'], axis on which to apply 
            'nbins'.
        tight: bool or None
            For plot decoration, controls expansion of axis limits, if 'True' axis limits 
            are only expanded using the margins; This does *not* set the margins to zero. 
            If 'False', further expand the axis limits using the axis major locator.
        x_ax_rotation: int or None
            For plot decoration, set degree of x_ticks rotation.
        theme: str
            adjust axis and title colors as desired

        """

        # prepare data        
        mask, feat, hue = self._grouping(self._col, self._target)
        
        # sort
        if hue:
            if mask[feat].dtype.kind != 'O':
                order = mask.groupby(hue)[feat].agg(hue_agg).sort_values(hue_agg).index
            else:
                order = mask.groupby(hue)[feat].agg(['count']).sort_values(['count']).index
        elif self._cat_cols:
            order = mask[feat].value_counts().sort_values().index
        else:
            order = None
        
        # plot
        ax = self._fig.add_subplot(self._n_rows, self._n_cols, self._n)
        countplot(mask, x = feat, hue = hue, order = order if not hue else None, 
                  hue_order = order if hue else None, stat = stat, native_scale = native_scale,  
                  legend = legend, color = color, palette = palette if hue else None, 
                  log_scale = log_scale, ax = ax)
        
        # decorate
        if hue and hue != feat:
            move_legend(ax, 'center', bbox_to_anchor = (.5, 1.3), columnspacing = .4, ncol = 4,
                        labelspacing = 0.0, handletextpad = 0.0, handlelength = 1, fancybox = True, 
                        shadow = True)
        
        col_dtype = mask[feat].dtype.kind
        self._decorate_plot(ax, col_dtype, log_scale, nbins, axis, tight, x_ax_rotation, theme);
        
        # update iteration control
        self._n += 1
          

    @itr_plot
    def hs(self,
           bins: Union[str, int, List[int], npt.NDArray[np.int_]] = 'doane',
           stat: str = 'count',
           multiple: str = 'layer',
           element: str = 'bars',
           fill: bool = True,
           discrete: bool = False,
           hue_agg: List[str] = ['mean'],
           log_scale: Optional[Union[int, bool, Tuple[int, bool]]] = False,
           color: str = 'lightblue',
           palette: str = 'Paired',
           nbins: Union[int, str] = 'auto',
           axis: str = 'x',
           tight: Optional[bool] = None,
           x_ax_rotation: Optional[int] = None,
           theme: str = 'darkorange'):
        """
        Visualize numeric features distribution using Seaborn's Hist Plot
        
        Parameters
        ----------
        bins: str, number, vector, or a pair of such values
            histogram bins, Generic bin 
            parameter that can be:
            
                - the name of a reference rule, 
                - the number of bins, 
                - the breaks of the bins.

            Passed to :func:`numpy.histogram_bin_edges`.

            Notes
            -----
            `str` can be one of [‘auto’, ‘fd’, ‘doane’, ‘scott’,
            ‘stone’, ‘rice’, ‘sturges’ or ‘sqrt’]
        stat: str
            Aggregate statistic to compute in each histogram bin.

            - **count**: show the number of observations in each bin
            - **frequency**: show the number of observations divided by the bin width
            - **probability** or **proportion**: normalize such that bar heights sum to 1
            - **percent**: normalize such that bar heights sum to 100
            - **density**: normalize such that the total area of the histogram equals 1
        multiple: {"layer", "dodge", "stack", "fill"}
            Approach to resolving multiple elements when semantic mapping creates subsets.
            Only relevant with univariate data.
        element: {"bars", "step", "poly"}
            Visual representation of the histogram statistic.
            Only relevant with univariate data.
        fill: bool
            If True, fill in the space under the histogram.
        discrete: bool
            If True, default to ``binwidth=1`` and draw the bars so that they are
            centered on their corresponding data points. This avoids "gaps" that may
            otherwise appear when using discrete (integer) data.
        hue_agg: list
            list of functions and/or function names, e.g.: [np.sum, 'mean']
            to use for aggregating the data. Only applicable for conditional
            distributions between numeric and categorical variable, otherwise 
            data is sorted ascendingly following the frequency(count) of categorical 
            levels. e.g.:
            pandas.DataFrame.groupby(category)[value].agg(hue_agg).sort_values(hue_agg)
        log_scale: bool or number, or pair of bools or numbers
            Set axis scale(s) to log. A single value sets the data axis for any numeric
            axes in the plot. A pair of values sets each axis independently.
            Numeric values are interpreted as the desired base (default 10).
            When `None` or `False`, seaborn defers to the existing Axes scale.
        color: str
            adjust color of seaborn plots as desired
        palette: str
            adjust color of 'hue' as desired; See seaborn.color_palette('palette_name')
        nbins: int or 'auto'
            For plot decoration, maximum number of axis intervals; one less than max 
            number of ticks. If the string 'auto', the number of bins will be 
            automatically determined based on the length of the axis.
        axis: str
            For plot decoration, one of ['both', 'x', 'y'], axis on which to apply 
            'nbins'.
        tight : bool or None
            For plot decoration, controls expansion of axis limits, if 'True' axis limits 
            are only expanded using the margins; This does *not* set the margins to zero. 
            If 'False', further expand the axis limits using the axis major locator.
        x_ax_rotation: int or None
            For plot decoration, set degree of x_ticks rotation.
        theme: str
            adjust axis and title colors as desired
            
        Note
        ----
        The choice of bins for computing and plotting a histogram can exert
        substantial influence on the insights that one is able to draw from the
        visualization. If the bins are too large, they may erase important features.
        On the other hand, bins that are too small may be dominated by random
        variability, obscuring the shape of the true underlying distribution. The
        default bin size is determined using a reference rule that depends on the
        sample size and variance. This works well in many cases, (i.e., with
        "well-behaved" data) but it fails in others. It is always a good to try
        different bin sizes to be sure that you are not missing something important.
        This function allows you to specify bins in several different ways, such as
        by setting the total number of bins to use, the width of each bin, or the
        specific locations where the bins should break.

        """

        # prepare data        
        mask, feat, hue = self._grouping(self._col, self._target)
        
        # sort
        if hue and mask[feat].dtype.kind != 'O':        
            order = mask.groupby(hue)[feat].agg(hue_agg).sort_values(hue_agg).index
        else:
            order = None
            
        # plot
        ax = self._fig.add_subplot(self._n_rows, self._n_cols, self._n)
        histplot(mask, x = feat, hue = hue, hue_order = order, bins = bins, stat = stat,
                 multiple = multiple, element = element, fill = fill, discrete = discrete,
                 color = color, palette = palette if hue else None, log_scale = log_scale, ax = ax)
        
        # decorate
        if hue:
            move_legend(ax, 'center', bbox_to_anchor = (.5, 1.3), columnspacing = .4, ncol = 4,
                        labelspacing = 0.0, handletextpad = 0.0, handlelength = 1, fancybox = True, 
                        shadow = True)

        col_dtype = mask[feat].dtype.kind
        self._decorate_plot(ax, col_dtype, log_scale, nbins, axis, tight, x_ax_rotation, theme);
        
        # update iteration control
        self._n += 1 
        

    @itr_plot
    def bo(self, 
           hue: Optional[str] = None, 
           fill: bool = True,
           showmeans: bool = True,
           meanprops: Optional[dict] = None,
           medianprops: Optional[dict] = None,
           whis: Union[float, Tuple[float, float]] = 1.5, 
           fliersize: Optional[float] = None,
           hue_agg: List[str] = ['mean'],
           log_scale: Optional[Union[int, bool, Tuple[int, bool]]] = False,
           color: str = 'lightblue',
           palette: str = 'Paired',
           nbins: Union[int, str] = 'auto',
           axis: str = 'x',
           tight: Optional[bool] = None,
           x_ax_rotation: Optional[int] = None,
           theme: str = 'darkorange'):
        """
        Visualize numeric features distribution using Seaborn's Box Plot
        
        Parameters
        ----------
        hue: str
            column name for additional layer of categorization.
        fill: bool
            If True, use a solid patch. Otherwise, draw as line art.
        showmeans: bool
            Show the arithmetic means.
        meanprops: dict
            Specifies the style of the mean.
        medianprops: dict
            Specifies the style of the median.
        whis: float or pair of floats
            Paramater that controls whisker length. If scalar, whiskers are drawn
            to the farthest datapoint within *whis * IQR* from the nearest hinge.
            If a tuple, it is interpreted as percentiles that whiskers represent.
        fliersize: float
            Size of the markers used to indicate outlier observations.
        hue_agg: list
            list of functions and/or function names, e.g.: [np.sum, 'mean']
            to use for aggregating the data. Only applicable for conditional
            distributions between numeric and categorical variable, otherwise 
            data is sorted ascendingly following the frequency(count) of categorical 
            levels. e.g.:
            pandas.DataFrame.groupby(category)[value].agg(hue_agg).sort_values(hue_agg)
        log_scale: bool or number, or pair of bools or numbers
            Set axis scale(s) to log. A single value sets the data axis for any numeric
            axes in the plot. A pair of values sets each axis independently.
            Numeric values are interpreted as the desired base (default 10).
            When `None` or `False`, seaborn defers to the existing Axes scale.
        color: str
            adjust color of seaborn plots as desired
        palette: str
            adjust color of 'hue' as desired; See seaborn.color_palette('palette_name')
        nbins: int or 'auto'
            For plot decoration, maximum number of axis intervals; one less than max 
            number of ticks. If the string 'auto', the number of bins will be 
            automatically determined based on the length of the axis.
        axis: str
            For plot decoration, one of ['both', 'x', 'y'], axis on which to apply 
            'nbins'.
        tight : bool or None
            For plot decoration, controls expansion of axis limits, if 'True' axis limits 
            are only expanded using the margins; This does *not* set the margins to zero. 
            If 'False', further expand the axis limits using the axis major locator.
        x_ax_rotation: int or None
            For plot decoration, set degree of x_ticks rotation.
        theme: str
            adjust axis and title colors as desired

        """
        
        # prepare data        
        mask, feat, hue_ = self._grouping(self._col, self._target)
            
        # sort
        if hue_ and mask[feat].dtype.kind != 'O':        
            order = mask.groupby(hue_)[feat].agg(hue_agg).sort_values(hue_agg).index
        else:
            order = None
        
        # plot
        ax = self._fig.add_subplot(self._n_rows, self._n_cols, self._n)
        
        mean_props = dict(linewidth = 2, markeredgecolor = 'black', markerfacecolor = 'firebrick') if not meanprops else meanprops
        median_props = dict(linewidth = 1.5, color = 'black') if not medianprops else medianprops
        
        boxplot(mask, x = feat, y = hue_, order = order, hue = hue if hue else None, fill = fill, showmeans = showmeans,
                meanline = showmeans, meanprops = mean_props, medianprops = median_props, whis = whis, fliersize = fliersize, 
                color = color, palette = palette if hue else None, log_scale = log_scale, ax = ax)

        # decorate
        if hue:
            move_legend(ax, 'center', bbox_to_anchor = (.5, 1.3), columnspacing = .4, ncol = 4,
                        labelspacing = 0.0, handletextpad = 0.0, handlelength = 1, fancybox = True, 
                        shadow = True)
        
        # decorate
        col_dtype = mask[feat].dtype.kind
        self._decorate_plot(ax, col_dtype, log_scale, nbins, axis, tight, x_ax_rotation, theme);
        
        # update iteration control
        self._n += 1 


    @itr_plot
    def vi(self, 
           hue: Optional[str] = None, 
           fill: bool = False,
           inner: Optional[str] = 'quart', 
           split: bool = False, 
           cut: float = 2,
           bw_method: Union[str, float] = 'scott',
           bw_adjust: float = 1,
           density_norm: str = 'area',
           hue_agg: List[str] = ['mean'],
           log_scale: Optional[Union[int, bool, Tuple[int, bool]]] = False,
           color: str = 'lightblue',
           palette: str = 'Paired',
           nbins: Union[int, str] = 'auto',
           axis: str = 'x',
           tight: Optional[bool] = None,
           x_ax_rotation: Optional[int] = None,
           theme: str = 'darkorange'):
        """
        Visualize numeric features distribution using Seaborn's Violin Plot
        
        Parameters
        ----------
        hue: str
            column name for additional layer of categorization.
        fill: bool
            If True, use a solid patch. Otherwise, draw as line art. 
        inner: {"box", "quart", "point", "stick", None}
            Representation of the data in the violin interior. 
            One of the following:

                - **box**: draw a miniature box-and-whisker plot
                - **quart**: show the quartiles of the data
                - **point** or **stick**: show each observation
        split: bool
            Show an un-mirrored distribution, alternating sides when using `hue`.
        cut: float
            Distance, in units of bandwidth, to extend the density past extreme
            data points. Set to 0 to limit the violin within the data range.
        bw_method: {"scott", "silverman", float}
            Either the name of a reference rule or the scale factor to use when
            computing the kernel bandwidth. The actual kernel size will be
            determined by multiplying the scale factor by the standard deviation of
            the data within each group.
        bw_adjust: float
            Factor that scales the bandwidth to use more or less smoothing.
        density_norm: {"area", "count", "width"}
            Method that normalizes each density to determine the violin's width.
            If `area`, each violin will have the same area. If `count`, the width
            will be proportional to the number of observations. If `width`, each
            violin will have the same width.       
        hue_agg: list
            list of functions and/or function names, e.g.: [np.sum, 'mean']
            to use for aggregating the data. Only applicable for conditional
            distributions between numeric and categorical variable, otherwise 
            data is sorted ascendingly following the frequency(count) of categorical 
            levels. e.g.:
            pandas.DataFrame.groupby(category)[value].agg(hue_agg).sort_values(hue_agg)
        log_scale: bool or number, or pair of bools or numbers
            Set axis scale(s) to log. A single value sets the data axis for any numeric
            axes in the plot. A pair of values sets each axis independently.
            Numeric values are interpreted as the desired base (default 10).
            When `None` or `False`, seaborn defers to the existing Axes scale.
        color: str
            adjust color of seaborn plots as desired  
        palette: str
            adjust color of 'hue' as desired; See seaborn.color_palette('palette_name')
        nbins: int or 'auto'
            For plot decoration, maximum number of axis intervals; one less than max 
            number of ticks. If the string 'auto', the number of bins will be 
            automatically determined based on the length of the axis.
        axis: str
            For plot decoration, one of ['both', 'x', 'y'], axis on which to apply 
            'nbins'.
        tight: bool or None
            For plot decoration, controls expansion of axis limits, if 'True' axis limits 
            are only expanded using the margins; This does *not* set the margins to zero. 
            If 'False', further expand the axis limits using the axis major locator.
        x_ax_rotation: int or None
            For plot decoration, set degree of x_ticks rotation.
        theme: str
            adjust axis and title colors as desired

        """

        # prepare data
        mask, feat, hue_ = self._grouping(self._col, self._target)
            
        # sort
        if hue_ and mask[feat].dtype.kind != 'O':        
            order = mask.groupby(hue_)[feat].agg(hue_agg).sort_values(hue_agg).index
        else:
            order = None
        
        # plot
        ax = self._fig.add_subplot(self._n_rows, self._n_cols, self._n)
        violinplot(mask, x = feat, y = hue_, order = order, hue = hue if hue else None, inner = inner, 
                   fill = fill, split = split, cut = cut, bw_method = bw_method,
                   bw_adjust = bw_adjust, density_norm = density_norm, color = color, 
                   palette = palette if hue else None, log_scale = log_scale, ax = ax)
        
        # decorate
        if hue:
            move_legend(ax, 'center', bbox_to_anchor = (.5, 1.3), columnspacing = .4, ncol = 4,
                        labelspacing = 0.0, handletextpad = 0.0, handlelength = 1, fancybox = True, 
                        shadow = True)
        
        col_dtype = mask[feat].dtype.kind
        self._decorate_plot(ax, col_dtype, log_scale, nbins, axis, tight, x_ax_rotation, theme);
        
        # update iteration control
        self._n += 1 


    @itr_plot
    def kd(self,
           cut: float = 0,
           bw_method: Union[str, float] = 'scott',
           bw_adjust: float = 1,
           warn_singular: bool = False,
           hue_agg: List[str] = ['mean'],
           log_scale: Optional[Union[int, bool, Tuple[int, bool]]] = False,
           color: str = 'lightblue',
           palette: str = 'Paired',
           nbins: Union[int, str] = 'auto',
           axis: str = 'x',
           tight: Optional[bool] = None,
           x_ax_rotation: Optional[int] = None,
           theme: str = 'darkorange'):
        """
        Visualize numeric features distribution using Seaborn's KDE Plot
        
        Parameters
        ----------
        cut: float
            Factor, for KDE plot, that determines how far to reach past 
            extreme data points. Set to 0, truncate the plot at the data limits.
        bw_method: string, scalar, or callable
            The method used to calculate the estimator bandwidth. This can be
            'scott', 'silverman', a scalar constant or a callable. If a scalar,
            this will be used directly as `kde.factor`. If a callable, it should
            take a `gaussian_kde` instance as only parameter and return a scalar.
            See :class:`scipy.stats.gaussian_kde` for more details.
        bw_adjust: float
            Factor that multiplicatively scales the value chosen using
            ``bw_method``. Increasing will make the curve smoother. See Notes.
        warn_singular: bool
            If True, issue a warning when trying to estimate the density of data
            with zero variance
        hue_agg: list
            list of functions and/or function names, e.g.: [np.sum, 'mean']
            to use for aggregating the data. Only applicable for conditional
            distributions between numeric and categorical variable, otherwise 
            data is sorted ascendingly following the frequency(count) of categorical 
            levels. Example:
            pandas.DataFrame.groupby(category)[value].agg(hue_agg).sort_values(hue_agg)
        log_scale: bool or number, or pair of bools or numbers
            Set axis scale(s) to log. A single value sets the data axis for any numeric
            axes in the plot. A pair of values sets each axis independently.
            Numeric values are interpreted as the desired base (default 10).
            When `None` or `False`, seaborn defers to the existing Axes scale.
        color: str
            adjust color of seaborn plots as desired
        palette: str
            adjust color of 'hue' as desired; See seaborn.color_palette('palette_name')
        nbins: int or 'auto'
            For plot decoration, maximum number of axis intervals; one less than max 
            number of ticks. If the string 'auto', the number of bins will be 
            automatically determined based on the length of the axis.
        axis: str
            For plot decoration, one of ['both', 'x', 'y'], axis on which to apply 
            'nbins'.
        tight: bool or None
            For plot decoration, controls expansion of axis limits, if 'True' axis limits 
            are only expanded using the margins; This does *not* set the margins to zero. 
            If 'False', further expand the axis limits using the axis major locator.
        x_ax_rotation: int or None
            For plot decoration, set degree of x_ticks rotation.
        theme: str
            adjust axis and title colors as desired
            
        Notes
        -----
        The *bandwidth*, or standard deviation of the smoothing kernel, is an
        important parameter. Misspecification of the bandwidth can produce a
        distorted representation of the data. Much like the choice of bin width in a
        histogram, an over-smoothed curve can erase true features of a
        distribution, while an under-smoothed curve can create false features out of
        random variability. The rule-of-thumb that sets the default bandwidth works
        best when the true distribution is smooth, unimodal, and roughly bell-shaped.
        It is always a good idea to check the default behavior by using ``bw_adjust``
        to increase or decrease the amount of smoothing.

        Because the smoothing algorithm uses a Gaussian kernel, the estimated density
        curve can extend to values that do not make sense for a particular dataset.
        For example, the curve may be drawn over negative values when smoothing data
        that are naturally positive. The ``cut`` and ``clip`` parameters can be used
        to control the extent of the curve, but datasets that have many observations
        close to a natural boundary may be better served by a different visualization
        method.

        Similar considerations apply when a dataset is naturally discrete or "spiky"
        (containing many repeated observations of the same value). Kernel density
        estimation will always produce a smooth curve, which would be misleading
        in these situations.

        The units on the density axis are a common source of confusion. While kernel
        density estimation produces a probability distribution, the height of the curve
        at each point gives a density, not a probability. A probability can be obtained
        only by integrating the density across a range. The curve is normalized so
        that the integral over all possible values is 1, meaning that the scale of
        the density axis depends on the data values.

        """
        
        # prepare data
        mask, feat, hue = self._grouping(self._col, self._target)
        
        # sort
        if hue and mask[feat].dtype.kind != 'O':        
            order = mask.groupby(hue)[feat].agg(hue_agg).sort_values(hue_agg).index
        else:
            order = None

        # plot
        ax = self._fig.add_subplot(self._n_rows, self._n_cols, self._n)
        kdeplot(mask, x = feat, hue = hue, hue_order = order, cut = cut, bw_method = bw_method, 
                bw_adjust = bw_adjust, warn_singular = warn_singular, color = color, palette = palette if hue else None, 
                log_scale = log_scale, ax = ax)
        
        # decorate
        if hue:
            move_legend(ax, 'center', bbox_to_anchor = (.5, 1.3), columnspacing = .4, ncol = 4,
                        labelspacing = 0.0, handletextpad = 0.0, handlelength = 1, fancybox = True, 
                        shadow = True)

        col_dtype = mask[feat].dtype.kind
        self._decorate_plot(ax, col_dtype, log_scale, nbins, axis, tight, x_ax_rotation, theme);
        
        # update iteration control
        self._n += 1
        

    def best_fit(self, 
                 cols: Optional[SEQUENCE_LIKE] = None,
                 method: str = 'parametric',
                 distr: Union[str, List[str]] = 'popular',
                 stats: str = 'RSS',
                 alpha: float = 0.05,
                 verbose: Union[str, int] = 30,
                 **kwargs) -> dict:
        """
        Find the best fit distribution for parametric, non-parametric, and discrete 
        distributions using DistFit module
        
        Parameters
        ---------- 
        cols: sequence (lists, tuples, NumPy arrays or Pandas Base Index) or None
            column names of features to analyze. If `None`, all columns at class
            initialization will be used.
        method: str
            specify how the best fit distribution is determined, 
            One of ['parametric', 'quantile', 'percentile', 'discrete'].

            - For the parametric approach, the distfit library can determine the best 
              fit across 89 theoretical distributions. 

            - For the non-parametric approach (assume that the data does not follow a 
              specific probability distribution), either the quantile or percentile 
              method is used; where confidence intervals of distribution boundaries are 
              computed based on either quantiles or percentiles. e.g.: 
              ci_upper = np.quantile(X, 1 - alpha), ci_lower = np.quantile(X, alpha) 
              where 'X' is feature values and 'alpha' is Significance alpha (i.e: 0.05)

            - In case the dataset contains discrete values, the best fit is then derived 
              using the binomial distribution.
        distr: str or list of str
            the (set) of distribution to test. str can be "popular", 
            name of distribution or list of specific theoretical 
            distribution names, for example:

                - 'popular':[norm, expon, pareto, dweibull, t, genextreme, 
                  gamma, lognorm, beta, uniform, loggamma]
                - 'full'
                - 'norm', 't', 'k': Test for one specific distribution.
                - ['norm', 't', 'k', ...]: Test for a list of distributions.

            If ``method`` = 'discrete', then binomial distribution is used.
        stats: str
            specify the scoring statistics for the goodness of fit test, 
            One of ['RSS', 'wasserstein', 'ks', 'energy'].
        alpha: float
            Significance alpha
        verbose: str or int
            set the verbose messages using string or integer:

            - 0, 60, None, 'silent', 'off', 'no']: No message.
            - 10, 'debug': Messages from debug level and higher.
            - 20, 'info': Messages from info level and higher.
            - 30, 'warning': Messages from warning level and higher.
            - 50, 'critical': Messages from critical level and higher.
        
        Attributes
        ----------
        z_best_fit_results: dict,
            where keys are column(s) name(s) and values are fitted model(s)
        z_feats_out_: numpy array,
            excluded columns having null values, if any.

        Note
        ----
        - Columns having null values will not be analyzed
        - For full list of parameters see `<https://erdogant.github.io/distfit>`__.

        """
        
        # Input check
        if cols is not None:
            if not isinstance(cols, (list, tuple, np.ndarray, pd.Index)):
                raise TypeError("'cols' parameter accepts a sequence, e.g: Lists, Tuples, NumPy Arrays or Pandas Base Index. "
                                f"However, '{type(cols)}' was received!")
            # assign columns to analyze
            self._bf_cols = np.array(cols)
        else:
            self._bf_cols = np.array(self._cols)

        if np.any([self._ori_df[col].dtype.kind not in 'ifc' for col in self._bf_cols]):
            raise TypeError("please only use columns having numeric data type")
        if stats not in ['RSS', 'wasserstein', 'ks', 'energy']:
            raise ValueError("'stats' parameter must be one of the following arguments: 'RSS', 'wasserstein', 'ks', or 'energy', "
                             f"however, '{stats}' was received!")

        # exclude columns with null values
        null_cols = self._bf_cols[self._ori_df[self._bf_cols].isnull().sum() != 0]
        n_ori, n_out = len(self._bf_cols), len(null_cols)
        self._bf_cols = self._bf_cols[~np.isin(self._bf_cols, null_cols)]
        
        if n_out == n_ori:
            raise ValueError("All columns have null(missing) values, can't fit!")
        else:
            # highlight exclusion
            if n_out:
                self.z_feats_out_ = null_cols # attributes
                _z_log.info(f"{n_out} out of {n_ori} columns having null values will not be analyzed")
        
            # fit dists
            fit_results = {} # best fit model(s) container

            for col in tqdm(self._bf_cols, desc = f'Finding Best Fits....', disable = self._hide_p_bar):

                dfit = distfit(method = method, distr = distr, stats = stats, alpha = alpha, todf = True, 
                               random_state = self._random_state, verbose = verbose, **kwargs)

                results = dfit.fit_transform(self._ori_df[col]) # using original dataframe ignoring `frac`

                fit_results[col] = dfit # update best fit container

            self.z_best_fit_results_ = fit_results # attributes
            
            
    @itr_plot
    def best_vis(self):
        """
        Visualize best fit model results `distfit module`. 
        Calls `best_fit` method if models were not already fit.
        """
        
        ax = self._fig.add_subplot(self._n_rows, self._n_cols, self._n)  

        self.z_best_fit_results_[self._col].plot(emp_properties = {'color': 'red', 'linewidth' : 1}, 
                                                 pdf_properties = {'color': 'green', 'linewidth' : 1}, 
                                                 cii_properties = {'color' : 'darkorange', 'linewidth': 1, 'size': 10}, 
                                                 fontsize = 13, grid = False, figsize = self._figsize, title = f'{self._col}', 
                                                 ax = ax)
        
        # decorate
        col_dtype = self.z_df_[self._col].dtype.kind
        self._decorate_plot(ax, dtype = col_dtype)
        plt.legend(ncol = 3, loc = 8, bbox_to_anchor = [0.5, 1.2], columnspacing = 1.0, labelspacing = 0.0, 
                   handletextpad = 0.0, handlelength = 1.5, fancybox = True, shadow = True);
                
        self._n += 1 # update iteration control