import pandas as pd

import numpy as np

from packaging.version import parse

from scipy import stats

from tqdm.auto import tqdm

from matplotlib import pyplot as plt

from plotly.graph_objs import Bar, Figure

from typing import Optional, Union, Tuple

from IPython.display import display

from .._utils import SEQUENCE_LIKE, itr_plot, PlotMixin

from .._logr import _z_log

###################################################################

class UniStat(PlotMixin):
    '''
    Calculate and visualize Univariate statistics for all features, identifying 
    feature problems (e.g.: missing values, skew, rare categories,...)
    
    Parameters
    ----------
    df: pandas dataframe
        data source
    col_drop: sequence (lists, tuples, NumPy arrays or Pandas Base Index) or None
        column(s) name(s) to exclude when analysing duplicates
    card_thresh: int
        threshold for considering categorical feature to be of high cardinality
    rare_thresh: float
        threshold below which categorical levels are considered to be rare 
        (e.g.: 1% or 5%). If 0 then all levels are considered during the analysis.
    skw_thresh: int
        threshold for highlighting and plotting skewed numeric distributions, assuming 
        normal theoretical distribution. Features are considered to be skewed if outside
        bounds of ``skw_thresh``: abs(skew score) > ``skw_thresh``
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
        triggers hiding progress bar (tqdm module); Default `False`
    theme: str
        adjust axis and title colors as desired
    color: str
        adjust color of Plotly Bar as desired
    
    Note
    ----
    Data types will be inferred automatically, however, to get optimal separation of categorical
    and numeric ``cols`` its better to ensure that correct data types are applied before using 
    this class.

    '''
    
    def __init__(self,
                 df: pd.DataFrame,
                 col_drop: Optional[SEQUENCE_LIKE] = None,
                 card_thresh: int = 10,
                 rare_thresh: float = 0.05,
                 skw_thresh: int = 1,
                 figsize: Optional[Tuple[int, int]] = None,
                 n_rows: Optional[int] = None,
                 n_cols: Optional[int] = None,
                 silent: bool = False,
                 hide_p_bar: bool = False,
                 theme: str = 'darkorange',
                 color: str = 'lightblue'):

        # input check
        if col_drop is not None:
            if not isinstance(col_drop, (list, tuple, np.ndarray, pd.Index)):
                raise TypeError("'col_drop' parameter accepts a sequence e.g: Lists, Tuples, NumPy Arrays or Pandas Base Index. "
                                f"However, '{type(col_drop)}' was received!")
            if np.any(~np.isin(col_drop, df.columns)):
                raise KeyError("Missing columns! Please ensure that column name passed to 'col_drop' parameter "
                               "is included in the DataFrame")
        if (card_thresh or rare_thresh) < 0:
            raise ValueError("cardinality and/or rare threshold(s) can't be less than 0")

        _z_log.info("Missing values in categorical columns will be considered as an additional 'missing' level "
                    "when calculating cardinality and rare levels percent")
        
        self._df = df.copy()
        self._col_drop = col_drop
        self._card_thresh = card_thresh
        self.rare_thresh = rare_thresh
        self.skw_thresh = skw_thresh
        self._figsize = figsize
        self._n_rows = n_rows
        self._n_cols = n_cols
        self._silent = silent
        self._hide_p_bar = hide_p_bar
        self._theme = theme 
        self._color = color
    

    @property # could've been exposed, just an example of property usage
    def card_thresh(self):
        """get cardinality threshold"""
        return self._card_thresh


    @card_thresh.setter
    def card_thresh(self, value):
        """set cardinality threshold"""
        if value >= 0:
            self._card_thresh = value
        else:
            print(f"cardinality threshold can't be negative, default value of {self._card_thresh} was not changed")
        

    # delete
    @card_thresh.deleter
    def card_thresh(self):
        """delete cardinality threshold"""
        del self._card_thresh
        

    def peek(self, disp_res: bool = True) -> Tuple[pd.core.indexes.base.Index, pd.DataFrame]:
        '''
        Calculate univariate statistics for Numeric and Categorical features while 
        identifying the following:
        
        - Proportion of missing data
        - Highly skewed features, assuming normal distribution
        - High cardinality categorical features
        - Proportion of rare categorical levels
        
        Parameters
        ----------
        disp_res: Bool
            triggers displaying summary results
        
        Attributes
        ----------
        z_summary: Pandas DataFrame
            info about the dataframe
        z_miss_data: Pandas Series
            Proportion of missing data
        z_hc_data: Pandas Series
            Count of categories/levels of high cardinality categorical columns
        z_rare_cat: Pandas DataFrame
            Count and proportion of rare categories/levels    
        z_univ_stat_df: Pandas DataFrame
            univariate statistics
        
        Returns
        -------
        num_cols: Pandas Index
            Numeric column names
        cat_cols: Pandas Index
            Categorical column names
        dup_df: Pandas DataFrame
            duplicate rows

        '''
        
        # capture all missing values before modification
        null_vals = self._df.isnull().mean().round(4)

        # dynamic progress bar for non iterable execution
        result_list = ['Categorical', 'Numeric', 'Univariate Statistics', 'Missing Data', 'High Cardinality Features', 
                       'Rare Categorical Features', 'Duplicates'] # progress bar text
        
        p_bar = tqdm(range(len(result_list)), desc = '', disable = self._hide_p_bar) # progress bar
        
        for i in p_bar:
            # Categorical Features
            if result_list[i] == 'Categorical':
                p_bar.set_description(f'Capturing {result_list[i]}')
                cats = self._df.select_dtypes(['object', 'bool', 'category']).columns
                # Checking for `ifc` instead of `i`
                # for features that better be
                # treated as categorical
                discats = {col: dtype for col in self._df.columns for dtype in [self._df[col].dtype] \
                           if dtype.kind in 'ifc' and self._df[col].nunique() <= 20} # dict to assign original dtypes latter
                discats_ = list(discats)
                cat_cols = np.r_[discats_, cats]

                # capturing original values and dtypes then
                # unifying display of missing values under `missing`
                # label for both discats and cats as missing values
                # in cats are ignored by pandas.describe
                cat_df = self._df[cat_cols] # preserve original values and dtypes
                cat_nulls = cat_cols[null_vals[cat_cols] > 0]
                for col in cat_nulls:
                    self._df[col] = np.where(self._df[col].isna(), 'missing', self._df[col])

                # for summary stats to be treated
                # as categorical if not having nulls
                self._df[discats_] = self._df[discats_].astype(str)
                            
            # Numeric Features
            elif result_list[i] == 'Numeric':
                p_bar.set_description(f'Capturing {result_list[i]}')
                num_cols = self._df.columns[~self._df.columns.isin(cat_cols)]
                
                # remove `inf` columns, if any
                inf_mask = np.isinf(self._df[num_cols]).any()
                if inf_mask.any():
                    self.z_inf_out_ = num_cols[inf_mask] # attributes
                    _z_log.info("Some columns contain 'inf' values and will be excluded.")
                    num_cols = num_cols[~np.isin(num_cols, self.z_inf_out_)]

                    n_inf = len(self.z_inf_out_)
                else:
                    n_inf = 0

            # Summary Statistics
            elif result_list[i] == 'Univariate Statistics':
                p_bar.set_description(f'Capturing {result_list[i]}')

                # datetime correct dtype
                kwargs = ({} if parse(pd.__version__) > parse('1.5') else {'datetime_is_numeric': True}) 

                # stats
                univ_stat_df = self._df[np.r_[num_cols, cat_cols]].describe(include = 'all', **kwargs)

                # back to original values and dtypes so if peek() called again
                # missing values re-appear after being labeled "missing"
                self._df[cat_cols] = cat_df

                # add dtypes to summary stats, reflecting changes to discats
                univ_stat_df.loc['d_types'] = self._df.dtypes

                # calculate skew, kurt and normality for numeric features only
                # skew: how much a distribution is pushed left or right
                # Rule of Thump between -1 and 1
                univ_stat_df.loc['skw'] = round(self._df[num_cols].skew(skipna = True), 2)

                # kurtosis: how much of the distribution is in the tail
                # kurtosis of normal == 0
                univ_stat_df.loc['krts'] = round(self._df[num_cols].kurt(skipna = True), 2)
                
                # spotting rare levels in categorical features
                rare_count = [(self._df[col].value_counts(dropna = False, normalize = True) < self.rare_thresh).sum() for col in cat_cols]

                univ_stat_df.loc['n_rare_lvls', cat_cols] = rare_count
                univ_stat_df.loc['pct_rare_lvls', cat_cols] = \
                univ_stat_df[cat_cols].loc['n_rare_lvls'] / univ_stat_df[cat_cols].loc['unique'] if any(cat_cols) else np.nan

                # re-arrange index - cosmetics
                re_idx = np.r_[univ_stat_df.index[:2], univ_stat_df.index[-2:], univ_stat_df.index[2:-2]]
                univ_stat_df = univ_stat_df.reindex(re_idx)
            
            # missing data    
            elif result_list[i] == 'Missing Data':
                p_bar.set_description(f'Capturing {result_list[i]}')
                univ_stat_df.loc['pct_missing'] = null_vals
                miss_data = univ_stat_df.T[univ_stat_df.T.pct_missing > 0]['pct_missing'].sort_values()
            
            # Overall Categorical Feature Cardinality
            elif result_list[i] == 'High Cardinality Features':
                p_bar.set_description(f'Capturing {result_list[i]}')
                cat_card = self._df[cat_cols].nunique(dropna = False).sort_values()
                hc_data = cat_card[cat_card > self._card_thresh]
            
            # Rare Categorical Levels
            elif result_list[i] == 'Rare Categorical Features':
                p_bar.set_description(f'Capturing {result_list[i]}')
                rare_cat = univ_stat_df.T[univ_stat_df.T.n_rare_lvls > 0][['unique', 'n_rare_lvls', 'pct_rare_lvls']]\
                .sort_values('pct_rare_lvls') if any(cat_cols) else hc_data # no cat_cols means empty pd.Series as is hc_data
            
            # duplicate samples
            else:
                p_bar.set_description(f'Capturing {result_list[i]}')
                if self._col_drop is not None: # e.g: drop target and check identical features with different target values
                    mask = self._df.drop(np.array(self._col_drop), axis = 1)
                    dup_df = self._df[mask.duplicated(keep = False)].sort_values(list(mask.columns))
                else: # in all columns
                    dup_df = self._df[self._df.duplicated(keep = False)].sort_values(list(self._df.columns))

        # attributes  
        self.z_summary_ = pd.DataFrame([{'rows': self._df.shape[0], 'columns': self._df.shape[1], 'num_feats': len(num_cols), 
                                         'cat_feats': len(cat_cols), 'high_card_cats': len(hc_data), 'rare_lvl_cats': len(rare_cat), 
                                         'n_feats_missing_data': len(miss_data), 'n_inf_feats': n_inf, 'duplicates': len(dup_df)}])

        # display results
        if disp_res:
            display('** Data Summary **', self.z_summary_.T.style.hide(axis = 1).format(thousands = ','),
                    '** Univariate stats - Numeric Features **', univ_stat_df[num_cols]\
                    .sort_values('skw', ascending = False, axis = 1).dropna().style.apply(
                        lambda x: ['background: olive' if abs(x.loc['skw']) > self.skw_thresh else '' for i in x],
                       subset = pd.IndexSlice['skw':'skw']).format(precision = 3, thousands = ',') if any(num_cols) else 'N/A', 
                    '** Univariate stats - Categorical Features **', univ_stat_df[cat_cols]\
                    .sort_values('unique', ascending = False, axis = 1).dropna().style.apply(
                        lambda x: ['background: grey' if x.loc['pct_rare_lvls'] >= .5 else '' for i in x], 
                        subset = pd.IndexSlice['pct_rare_lvls':'pct_rare_lvls']).format(precision = 3, thousands = ',')\
                        if any(cat_cols) else 'N/A')

        # attributes
        self.z_miss_data_ = miss_data
        self.z_hc_data_ = hc_data
        self.z_rare_cat_ = rare_cat
        self.z_univ_stat_df_ = univ_stat_df
         
        return num_cols, cat_cols, dup_df
    

    def stats_plot(self, width: Optional[int] = None, height: Optional[int] = None):
        '''
        Interactive plots visualizing:

        - Proportion of missing data
        - High cardinality categorical features
        - Proportion of rare categorical levels

        Parameters
        ----------
        width: int, default `None`
            The figure width in pixels
        height: int, default `None`
            The figure height in pixels

        '''

        try:
            self.z_miss_data_; self.z_hc_data_; self.z_rare_cat_ # check if plot data is ready
        except:
            self.peek(disp_res = False)
            
        miss_d, hc_d, rare_d = self.z_miss_data_, self.z_hc_data_, self.z_rare_cat_
        
        if any(miss_d): # plot missing data stats 
            # pLot
            fig = Figure(data=[Bar(x = miss_d.index, y = miss_d.values, marker = dict(color = self._color), 
                                   customdata = self._df[miss_d.index].dtypes.values.astype(str), 
                                   hoverlabel = dict(namelength=0), 
                                   hovertemplate = '<br>'.join(['Feat: %{x}', 'Missing Value: %{y:.1%}', 
                                                                'Data Type: %{customdata}']))])
            # Decorate
            fig.update_layout(dict(paper_bgcolor = 'rgba(0,0,0,0)', plot_bgcolor = 'rgba(0,0,0,0)', 
                                   hoverlabel = dict(bgcolor = 'darkred'), 
                                   title = dict(text = 'Quantifying Missing data', x = 0.5, xref = 'paper', 
                                                font = dict(family = 'Arial', size = 20, color = self._theme)),
                                   width = width, height = height))
            fig.update_xaxes(title = 'Features', color = self._theme)
            fig.update_yaxes(showgrid = False, title = 'Percentage of Missing Values', color = self._theme)
            fig.show();

        else:
            _z_log.info('No Missing Values')

        if any(hc_d): # plot high cardinality stats
            # pLot
            fig = Figure(data=[Bar(x = hc_d.index, y = hc_d.values, marker = dict(color = self._color), 
                                   # customdata = customdata, 
                                   hoverlabel = dict(namelength=0),
                                   hovertemplate = '<br>'.join(['Feat: %{x}', 'n_lvls: %{y:.0f}']))])
            # Decorate
            fig.update_layout(dict(paper_bgcolor = 'rgba(0,0,0,0)', plot_bgcolor = 'rgba(0,0,0,0)', 
                                   hoverlabel = dict(bgcolor = 'darkred'), 
                                   title = dict(text = f'High Cardinality Categorical Features (>{self._card_thresh} levels)', 
                                                x = 0.5, xref = 'paper', 
                                                font = dict(family = 'Arial', size = 20, color = self._theme)),
                                   width = width, height = height))
            fig.update_xaxes(title = 'Features', color = self._theme)
            fig.update_yaxes(type = 'log', showgrid = False, title = '(log) Size of Unique Categories', color = self._theme)
            fig.show();

        else:
            _z_log.info(f'No High Cardinality Categorical Features (>{self._card_thresh})')

        if len(rare_d) > 0: # plot rare categorical levels stats
            # plot
            customdata = np.stack(rare_d.values, axis = 0) # hover data

            fig = Figure(data=[Bar(x = rare_d.index, y = rare_d.pct_rare_lvls, 
                                   marker = dict(color = self._color), 
                                   customdata = customdata, hoverlabel = dict(namelength=0),
                                   hovertemplate = '<br>'.join(['Feat: %{x}', 'n_lvls: %{customdata[0]:.0f}',
                                                                'n_rare_lvls: %{customdata[1]:.0f}', 
                                                                'pct_rare_Lvls: %{y:.1%}']))])

            # decorate
            fig.update_layout(dict(paper_bgcolor = 'rgba(0,0,0,0)', plot_bgcolor = 'rgba(0,0,0,0)', 
                                   hoverlabel = dict(bgcolor = 'darkred'),
                                   title = dict(
                                       text = f'Proportion of Rare Categorical Levels (<{self.rare_thresh})',
                                       x = 0.5, xref = 'paper', font = dict(family = 'Arial', size = 20, color = self._theme)),
                                   width = width, height = height))
            fig.update_xaxes(title = 'Features', color = self._theme)
            fig.update_yaxes(showgrid = False, title = '% of Rare Levels', color = self._theme)
            fig.show();
            
        else:
            _z_log.info(f'No Rare Categorical Levels (<{self.rare_thresh})')


    @itr_plot(n_cols = 6, figsize = (24, 11))
    def skew_plot(self, dist: str = 'norm', cols: Optional[SEQUENCE_LIKE] = None):
        '''
        Generate Probability Plots for highly skewed features given a specific 
        distribution (default Normal).
        
        `Probability Plots`: Compare unscaled ordered feature values `Y-axis` vs 
        Scaled theoretical `Expected` Quantiles of Normal Distribution `X-axis`
        representing Z-scores of standard normal distribution `dist.ppf(p)`; 
        where `p` is Order statistics of the uniform distribution and `ppf` is 
        inverse `cdf`, so we basically generating `x` values with uniform `p` and 
        norm `mu` and `sigma`.

        If true, that generated(x) and actual(y) values both comes from same 
        distribution, all values (blue dots) should form a straight line in the plot 
        and lie on the red line. 
        
        Note that the red line is a function of Ordered Values(y) ~ theoretical `x`: 
        `OLS(dist.ppf(p), sort(x))`, this `OLS` best-fit line provide insight as to 
        whether or not the feature can be characterized by the distribution; if the 
        two distributions are linearly related, but not similar, the blue dots will 
        approximately lie on a line, but not necessarily on the line. 
        
        So the degree of similarity between both distributions can be assessed this way, 
        guiding the methods for further data preprocessing.
        
        Parameters
        ----------
        dist: str or stats.distributions instance
            Distribution or distribution function name. The default is `norm` for a
            normal probability plot. Objects that look enough like a `stats.distributions`
            instance (i.e. they have a `ppf` method) are also accepted.
        cols: sequence (lists, tuples, NumPy arrays or Pandas Base Index) or None
            column(s) name(s) to fit distribution, if `None`, then `peek` method is invoked 
            and ``cols`` are those having abs(skew score) > ``skew threshold``.

        '''
        ax = self._fig.add_subplot(self._n_rows, self._n_cols, self._n)
        plot = stats.probplot(self._df[self._col], dist = dist, plot = plt, rvalue = False)
        r_2 = plot[1][2]**2
        text = f'{self._col} \n $r^2$ = {r_2:.2f}' if not np.isnan(r_2) else f'{self._col}'
        plt.title(text, color = self._theme)
        self._decorate_plot(ax, theme = self._theme);
        self._n += 1