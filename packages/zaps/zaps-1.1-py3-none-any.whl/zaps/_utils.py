import numpy as np

import pandas as pd

from matplotlib import pyplot as plt

import matplotlib.ticker as tkr

from tqdm.auto import tqdm

from functools import wraps, partial

from typing import Optional, Union, Tuple, List, Callable

import numpy.typing as npt

import time

from ._logr import _z_log

############################################################################
# typing for input columns
SEQUENCE_LIKE = Union[List[str], Tuple[str], npt.NDArray[np.str_], pd.Index]
############################################################################

def itr_plot(method: Optional[Callable] = None,
             suptitle: Optional[str] = None, 
             desc: Optional[str] = None, 
             n_rows: int = 3,
             n_cols: int = 4,
             figsize: Tuple[int, int] = (20, 12)):
    """
    Class method decorator for iterative plotting, can be called using 
    either @itr_plot or @itr_plot(); however, the former uses default parameters.
    
    Parameters
    ----------
    method: callable,
        class method to decorate
    suptitle: str,
        figure subtitle
    desc: str,
        text to display in progress bar (tqdm module)
    n_rows: int,
        number of rows in matplotlib subplot figure
    n_cols: int,
        number of columns in matplotlib subplot figure
    figsize: tuple, 
        dimensions of matplotlib figure (width, height)

    """

    # gain access to an outer function's scope(decorator) from an inner method(decorated)
    # returning partial function allowing editing itr_plot() params (e.g: n_rows, n_cols...)
    if not method:
        return partial(itr_plot, suptitle = suptitle, desc = desc, n_rows = n_rows, n_cols = n_cols, figsize = figsize)
    
    @wraps(method) # preserve information(doc string) of the original method
    def wrapper(self, *args, **kwargs): # *args, **kwargs allows an arbitrary number of method's positional & keyword arguments
        """ 
        Decorated method is replaced by this wrapper. When decorated is called, wrapper is what actually gets called.
        """

        suptitle_, desc_ = suptitle, desc

        # input checks
        if method.__name__ == 'cp':
            if not self._cat_cols:
                raise TypeError("'cat_cols' is set to 'False', if columns are truly categorical "
                                "please set it to 'True' or use categorical columns instead")
                
            # check if target is truly categorical
            if self._target and self.z_df_[self._target].nunique() > 20:     
                raise AttributeError(f"The x variable '{self._target}' have significant frequent levels! If it is "
                                     "truly categorical, Consider adjusting 'top_n' and 'rare_thresh' parameters "
                                     "otherwise change the feature or plot type")
                
        elif method.__name__ == 'kd':
            if self._cat_cols and not self._target: # Categorical distributions
                raise TypeError("'cat_cols' is set to 'True', if plotting conditional distributions, set a numeric 'target'. "
                                "Otherwise use numeric/datetime columns instead")
            
        elif method.__name__ == 'skew_plot':
            
            # prepare plot data
            cols = kwargs.get('cols')
            
            if cols is not None:
                # input checks
                if not isinstance(cols, (list, tuple, np.ndarray, pd.core.indexes.base.Index)):
                    raise TypeError("'cols' parameter accepts a sequence e.g: Lists, Tuples, NumPy Arrays or Pandas Base Index. "
                                    f"However, '{type(cols)}' was received!")
                if np.any(~np.isin(cols, self._df.columns)):
                    raise KeyError("Missing columns! Please ensure that all columns to plot are included in the DataFrame")
                if np.any([self._df[col].dtype.kind not in 'ifc' for col in cols]): # discrete cats will also raise this error
                    raise TypeError("Only numeric feature(s) are accepted")

                self._plot_cols = np.array(cols)

            else: # use initialization features
                try:
                    stats_df = self.z_univ_stat_df_
                except:
                    self.peek(disp_res = False)
                    stats_df = self.z_univ_stat_df_

                self._plot_cols = stats_df.T[abs(stats_df.T.skw) > self.skw_thresh].sort_values('skw', ascending = False).index
    
            # set progress bar description
            desc_ = 'Preparing Probability Plots....'
            
            # set figure subtitle - seaborn
            suptitle_ = 'Goodness of Fit: Skewed Features'
            
        elif method.__name__ == 'best_vis':
            # prepare plot data
            try:
                self.z_best_fit_results_ # should always call `best_fit()` first
            except:
                raise AttributeError("This instance of 'Dist' class is not fitted yet. " 
                                     "Call 'best_fit' method with appropriate arguments first!")
            
            if not self.z_best_fit_results_[list(self.z_best_fit_results_.keys())[0]].method == 'discrete':
                
                # prepare plot data
                self._plot_cols = np.array(list(self.z_best_fit_results_.keys()))

                # set progress bar description
                desc_ = 'Plotting Best Fitting Distribution....'
                
            else: # skip plotting if method is 'discrete' because it outputs two plots per each feature/column
                raise Exception("please visualize each distribution from the models directly using model.plot()")
        
        elif method.__name__ in ['vis_fit', 'vis_ols_fit']:
            
            # input checks
            if method.__name__ == 'vis_fit':

                idx, mapping = kwargs.get('olrs_idx'), kwargs.get('olrs_mapping')

                if idx is not None:
                    if not isinstance(idx, (list, pd.Index)):
                        raise TypeError("'olrs_idx' parameter can either be a List or Pandas Base Index. "
                                        f"However, '{type(idx)}' was received!")
                    # convert to dict for single check when plotting each column latter
                    self._lrs = {col: idx for col in self._cols}

                if mapping is not None:
                    if not isinstance(mapping, dict):
                        raise TypeError("please pass 'olrs_mapping' parameter as dictionary where "
                                        "keys are column names and values are outlier data points indices (list or pandas index)")
                    self._lrs = mapping

            elif self._fit != 'ols': # now we in `vis_ols_fit`
                raise TypeError("can only assess the results of Ordinary Least Squares regression fit")

            # prepare plot data
            try:
                self.z_fit_results_
            except:
                self.fit_models()

            self._plot_cols = np.array(list(self.z_fit_results_.keys()))

            desc_ = f'Plotting Regression Fits....' if method.__name__ == 'vis_fit' else f'Plotting OLS Fit Results....'

            # set figure subtitle - seaborn
            if hasattr(self, '_fit'):
                if self._fit == 'logit' and not self._binary_t:
                    suptitle_ = f"Logistic Fit '{self._target}': {self._lbl[-1]} vs {self._lbl[0]}(base)"
                elif self._fit == 'lws':
                    suptitle_ = 'LOWESS Smoothing'
                elif self._degree > 1:
                    suptitle_ = f'Polynomial Fit: degree = {self._degree}'
            else:
                suptitle_ = None
            
        # assign plotting columns
        # for other methods where
        # no change was introduced
        try:
            self._plot_cols
        except:
            self._plot_cols = self._cols
        
        if len(self._plot_cols): # plot, if any
            
            # prepare figure
            if not self._n_rows: # when class' = None
                self._n_rows = n_rows # use decorator's
            
            if not self._n_cols:
                self._n_cols = n_cols if n_cols <= len(self._plot_cols) else len(self._plot_cols)

            if not self._figsize:
                self._figsize = figsize

            self._fig = plt.figure(figsize = self._figsize)

            if suptitle_:
                self._fig.suptitle(suptitle_, y = 1.05, fontsize = 20)

            # iterative plotting
            self._n = 1 # count iterations and control index of subplots
            tot_cols = len(self._plot_cols)

            if not desc_: # progress bar text
                desc_ = 'Plotting Feature Distribution....' 
            
            for col in tqdm(self._plot_cols, desc = desc_, disable = self._hide_p_bar):
                
                self._col = col # to be used inside method
                
                method(self, *args, **kwargs) # decorated(original) method
        
                if len(self._fig.get_axes()) == self._n_rows * self._n_cols:

                    self._n = 1 # reset counter         
                    plt.show(close = True); # show then close existing figure
                    cols_to_plot = tot_cols - (np.argwhere(self._plot_cols == col)[0][0] + 1) # remaining columns

                    if cols_to_plot:

                        if not self._silent:
                            _z_log.info(f"{cols_to_plot} out of {tot_cols} features remaining, to "
                                        "continue plotting press 'Enter' or input any value to exit.")
                            time.sleep(2)
                            if not input().strip().lower().replace(' ',''):
                                self._fig = plt.figure(figsize = self._figsize); # new figure
                            else:
                                break
                        else:
                            _z_log.info(f"{cols_to_plot} out of {tot_cols} features remaining.")
                            self._fig = plt.figure(figsize = self._figsize);
                            time.sleep(2)
                            
                elif len(self._fig.get_axes()) == 0: # nothing plotted
                    plt.close(); # close existing figure
                    
            del self._fig # delete figure
            
        else:
            _z_log.info('Nothing to plot! Please ensure that input columns matches plotting criteria')
    
    return wrapper


class PlotMixin:
    """
    Mixin class for all plots in Zaps.

    This mixin provide several functionality that can extend 
    beyond plotting:

        - Handling infs and NaNs in numeric columns.
        - Handling high cardinality categorical columns.
        - Prepare data for plotting.
        - Styling plots.
    """

    def _slash_n_impute(self, nans_d: Optional[dict] = None):
        """ excluding infs and imputing NaNs in numeric columns """

        # remove `inf` columns, if any
        inf_mask = np.isinf(self.z_df_[self._cols]).any()
        if inf_mask.any():
            self.z_inf_out_ = self._cols[inf_mask] # attributes
            _z_log.info("Some columns contain 'inf' values and will be excluded.")
            self._cols = self._cols[~np.isin(self._cols, self.z_inf_out_)]

        # simple mean imputation for missing values
        nans = self._cols[self.z_df_[self._cols].isnull().sum() != 0]
        if any(nans): # imputation
            self.z_nans_ = nans # attributes
            if not nans_d:
                self.z_df_.fillna({col: self.z_df_[col].mean() for col in self.z_nans_}, inplace = True)
                _z_log.info(f"Mean imputation took place for {len(self.z_nans_)} out of {len(self._cols)} columns " 
                            "having missing values")
            else:
                self.z_df_.fillna(nans_d, inplace = True)
                _z_log.info(f"Imputation took place for {len(nans_d)} out of {len(self._cols)} columns " 
                            "having missing values")
        elif nans_d and not any(nans):
            _z_log.info(f"No imputation took place as no columns having missing values were found!")


    def _capt_freq_cats(self, col: str):
        """ Capturing frequent categories for a given DataFrame column """

        lvls = self.z_df_[col].value_counts(normalize = True, dropna = False)
        max_lvls = len(lvls) if self._top_n < 2 else self._top_n
        freq_lvls = lvls.iloc[:max_lvls][lvls.iloc[:max_lvls] >= self._rare_thresh].index

        return freq_lvls


    def _preprocess(self):
        """ Identify `rare` and `missing` values in categorical columns at class initialization """

        if self._cat_cols is None:
            # decide on nature of target and columns
            # assume categorical columns if columns
            # are of 'Bool' or 'Object' data type or
            # `target` is not categorical
            if np.any([self.z_df_[col].dtype.kind in 'bO' for col in self._cols]):
                self._cat_cols = True
            elif self._target:
                self._cat_cols = not ((self.z_df_[self._target].dtype.kind in 'i' and self.z_df_[self._target].nunique() <= 20) or \
                                       self.z_df_[self._target].dtype.kind in 'bO') # `category` dtype is also 'O'

            _z_log.info(f"Columns are assumed to be {'Categorical' if self._cat_cols else 'Numeric'}. "
                        "If not correct, please manually set 'cat_cols' parameter")
            
        if self._cat_cols: # works either: cat cols vs num target or individual cat dists
            
            self.z_freq_lvls_map_ = {} # frequent categorical levels container
            
            for col in tqdm(self._cols, desc = 'Capturing Frequent Levels....', disable = self._hide_p_bar):
                # limit categorization and plotting to top n categories and frequent levels
                freq_lvls = self._capt_freq_cats(col)

                # attributes
                if len(freq_lvls) > 1:
                    self.z_freq_lvls_map_[col] = freq_lvls
            
            # features not analyzed
            cols_ =  np.array(list(self._cols))
            self._cols = np.array(list(self.z_freq_lvls_map_.keys())) # filtered subset
            xludd_feats = cols_[~np.isin(cols_, self._cols)]

            if any(xludd_feats):
                _z_log.warning(f"{len(xludd_feats):,.0f} out of {len(cols_)} Features Will Not Be Analyzed Being "
                               "Dominated By Rare Levels. This behavior is controlled by 'rare_thresh' parameter")
                self.xludd_feats_ = xludd_feats # attributes

            if self._rare_thresh == 0 and self._top_n < 2:
                max_n_lvls = [len(v) for v in self.z_freq_lvls_map_.values()] # accounts for missing values
                high_card_col = self._cols[np.argmax(max_n_lvls)]

                _z_log.info("'rare_thresh' and 'top_n' parameters are not properly configured! All categorical levels "
                            f"will be analysed. '{high_card_col}' feature has {np.max(max_n_lvls):,.0f} levels!")
            
        elif self._target: # num cols vs cat target(discrete or string)
            # limit categorization and plotting to top n categories and frequent levels
            freq_lvls = self._capt_freq_cats(self._target)
            
            if len(freq_lvls) > 1:

                # attributes
                self.z_freq_lvls_map_ = freq_lvls
                
                # handle nan values as 'missing' category
                temp_col = self.z_df_[self._target] # preserve dtype and category names
                n_lvls = len(temp_col.value_counts(dropna = False))
                
                if np.any(temp_col.isna()):
                    self.z_df_[self._target] = np.where(temp_col.isna(), 'missing', temp_col)

                # group rare levels in a separate category
                self.z_df_[self._target] = np.where(~temp_col.isin(freq_lvls), 'rare', self.z_df_[self._target])
                
                # for violin and box plots if discrete categories and no rare or missing
                # categories goes to the y-axis and it needs to be a string
                self.z_df_[self._target] = self.z_df_[self._target].astype(str)

                # highlight dtype change
                ori_dt, new_dt = temp_col.dtype.kind, self.z_df_[self._target].dtype.kind
                
                if ori_dt != new_dt:
                    _z_log.debug(f"data type of '{self._target}' changed from '{ori_dt}' to '{new_dt}'")
                
                # report grouping, if any
                n_grbd_lvls = n_lvls - len(self.z_freq_lvls_map_)
                
                if n_grbd_lvls:
                    _z_log.warning(f"Conditional distributions given '{self._target}' are analyzed for top " 
                                   f"{len(self.z_freq_lvls_map_)} frequent categories while grouping {n_grbd_lvls} rare lvls. "
                                   "This behavior is controlled by 'rare_thresh' and `top_n` parameters")
                    
            else:
                raise AttributeError(f"'{self._target}' target have significant rare levels! If it is truly categorical, "
                                      "Consider adjusting 'top_n' and 'rare_thresh' parameters")
         

    def _grouping(self, col: str, target: str) -> Tuple[pd.DataFrame, str, str]:
        """
        Column wise preparation before execution 
        
        Parameters
        ----------
        col: str,
            feature column name
        target: str,
            target column name
            
        Returns:
        --------
        mask: pandas dataframe
            filtered dataframe by the frequent categories, if any.
        feat: str,
            column name of main feature to plot
        hue: str,
            column name to use when categorizing `feat`,
            only applicable for conditional distributions
        """

        if self._cat_cols:

            freq_lvls = self.z_freq_lvls_map_[col]
            # use original column to preserve dtype while allowing for fraction
            # this is important to avoid overwriting column data if plotting method
            # was called several times with different parameters
            temp_col = self._ori_df.iloc[self.z_df_.index][col]

            if np.any(temp_col.isna()):
                # handle nan values as `missing` category
                self.z_df_[col] = np.where(temp_col.isna(), 'missing', temp_col)
        
            self.z_df_[col] = np.where(~temp_col.isin(freq_lvls), 'rare', self.z_df_[col])

            # capturing all categories as string 
            # for plots(violin, box) and ANOVA
            self.z_df_[col] = self.z_df_[col].astype(str) 
            
            if target: # cat feats vs num target
                feat, hue = target, col
            else: # cat feats (string or discrete)
                feat, hue = col, None
        elif target: # num feats vs cat target
            feat, hue = col, target
        else: # num feats
            feat, hue = col, None
        
        return self.z_df_.copy(), feat, hue # TODO: avoid .copy() overhead


    def _decorate_plot(self,
                       ax: plt.axes, 
                       dtype: str = 'i', 
                       log: bool = False,
                       nbins: Union[int, str] = 'auto', 
                       axis: str = 'x', 
                       tight: Optional[bool] = None, 
                       x_ax_rotation: Optional[int] = None, 
                       theme: str = 'darkorange'):
        """
        Set matplotlib axis format and color

        Parameters
        ----------
        ax: matplotlib Axes
            Axes object to edit ticks.
        dtype: str,
            column dtype, output of (pd.DataFrame[col].dtype.kind), 
            to guide numeric formatting of x-axis
        log: Bool,
            triggers formatting x-axis for log scale.
        nbins = int or 'auto',
            Maximum number of axis intervals; one less than max number of ticks. 
            If the string 'auto', the number of bins will be automatically determined 
            based on the length of the axis. Ignored if `log` is 'True'.
        axis: str,
            One of ['both', 'x', 'y'], axis on which to apply `nbins`.
        tight: bool or None
            controls expansion of axis limits, if 'True' axis limits are 
            only expanded using the margins; This does *not* set the margins to zero. 
            If 'False', further expand the axis limits using the axis major locator.
        x_ax_rotation: int or None,
            set degree of x_ticks rotation
        theme: str,
            adjust axis colors as desired
        """

        if dtype in 'ifc': # adjust numeric format
            # dynamic tick formatting that 
            # fits most cases. No reliance 
            # on axis data because, weirdly,
            # the behavior of tick labels 
            # is not consistent
            # TODO: dynamic float format instead of fixed 3 points
            ax.xaxis.set_major_formatter(lambda x, p: f'{x:,.3f}' if x != 0 and dtype == 'f' and int(str(abs(x)).split('.')[1]) > 0 \
                                         else (f'{x:,.0f}' if np.any(np.isclose(x, [0,1])) or len(str(abs(x)).split('.')[0]) <= 4 \
                                               else f'{x/1_000:,.0f}K'))

            if log:
                ax.xaxis.set_major_locator(tkr.LogLocator(base = 10.0, subs = (1.0, 3.0)))
                ax.xaxis.set_minor_locator(tkr.NullLocator()) # no minor ticks
            else: # Setting the number of x-ticks
                ax.xaxis.set_major_locator(tkr.MaxNLocator(nbins = nbins, integer = dtype =='i'))

        # x-ticks rotation
        ax.xaxis.set_tick_params(rotation = x_ax_rotation)

        # color both axis and all ticks
        ax.tick_params(axis = 'both', which = 'both', colors = theme)


class PipeLineMixin:
    """
    Mixin class for all transformers in Zaps, so they can be used
    with other transformers that return Numpy arrays within 
    Scikit-learn Pipeline.

    This mixin defines the following functionality:
    
        - Create a copy of input data if it is a DataFrame.
        - Convert input data to DataFrame if it is a numpy array.
    """

    def _array_to_df(self,
                     data: Union[np.generic, np.ndarray, pd.DataFrame], 
                     idx: Optional[Union[list, pd.RangeIndex]] = None,
                     labels: Optional[Union[list, pd.Index]] = None,
                     dtypes: Optional[Union[str, dict, np.dtype]] = None) -> pd.DataFrame:

        """
        Convert Numpy ndarray to Pandas DataFrame. If already a DataFrame, return
        a copy.

        Parameters
        ----------
        data: np.ndarray or pd.DataFrame, 
            array to convert

        idx: lists, Pandas Range Index or None,
            values for the dataframe's index. If None, will default to RangeIndex,

        labels: lists, Pandas Base Index or None,
            labels to use as column names when converting `data` to a DataFrame. 
            If `None`, generic names will be generated.

        dtypes: str, dict, np.dtype, Python Type or None,
            data types for output columns. If None, the types are inferred from 
            the data. If not `dict` then the entire output DataFrame will be 
            casted to the same type, otherwise, `dict` mapping {col: dtype} will 
            be used to cast one or more of the output DataFrame's columns to 
            column-specific types where mapping `col` is a column label and `dtype` 
            is a `numpy.dtype` or `Python type`

        Returns
        -------
        df: pd.DataFrame,
            `data` in the a dataframe form
        """

        # input checks
        if not isinstance(data, (np.generic, np.ndarray, pd.DataFrame)):
            raise TypeError("'data' parameter accepts NumPy Arrays or Pandas DataFrame. "
                            f"However, '{type(data)}' was received!")

        n_rows, n_cols = data.shape[0], 1 if data.ndim == 1 else data.shape[1]

        if idx is not None:
            if not isinstance(idx, (list, pd.RangeIndex)):
                raise TypeError("'idx' parameter accepts a List or Pandas Range Index. "
                                f"However, '{type(idx)}' was received!")
            rows_in = len(idx)
            if rows_in != n_rows:
                raise ValueError("Index mismatch! Ensure length of `index` matches length of `data` "
                                 f"expected {n_rows}, However, {rows_in} was received.")
        if labels is not None:
            if not isinstance(labels, (list, pd.Index)):
                raise TypeError("'labels' parameter accepts a List or Pandas Base Index. "
                                f"However, '{type(labels)}' was received!")
            lbls_in = len(labels)
            if lbls_in != n_cols:
                raise ValueError(f"Labels mismatch! expected {n_cols} labels, However, {lbls_in} was received.")

        # process input data
        if isinstance(data, pd.DataFrame):
            df = data.copy()
            self._from_array = False
        else:
            if labels is None:
                labels = [f'feat_{n}' for n in range(1, n_cols + 1)]

            df = pd.DataFrame(data, columns = labels, index = idx)
            self._from_array = True

            if dtypes:
                if isinstance(dtypes, dict) and np.any(~np.isin(list(dtypes.keys()), df.columns)):
                    _z_log.info("Invalid columns used in `dtypes` mapping, data types will be auto inferred.")
                else:
                    df = df.astype(dtypes)

        return df