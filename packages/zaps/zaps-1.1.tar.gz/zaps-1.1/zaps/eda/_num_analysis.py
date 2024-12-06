import pandas as pd

import numpy as np

import time

from statsmodels.formula.api import ols, mnlogit

from statsmodels.nonparametric.smoothers_lowess import lowess

from scipy import stats

from tqdm.auto import tqdm

from matplotlib import pyplot as plt

from seaborn import regplot, scatterplot, histplot

from plotly.graph_objs import Heatmap, Figure, layout

from plotly.express import scatter, scatter_3d, colors, get_trendline_results

from typing import Optional, Union, Tuple, List

from itertools import product

from textwrap import wrap

from .._utils import SEQUENCE_LIKE, itr_plot, PlotMixin

from .._logr import _z_log

###################################################################

class NumAna(PlotMixin):
    """
    Collection of Numeric features analysis that includes: 
    
    - Regression
    - Correlation 
    - visualizations
    
    Parameters
    ----------
    df: pandas dataframe
        data source
    cols: sequence (lists, tuples, NumPy arrays or Pandas Base Index)
        column names of numeric features
    target: str
        target column name, categorical target will be encode as integer.
    degree: int
        If ``degree`` is greater than 1, ``fit`` is ignored and polynomial 
        regression is applied to the nth ``degree``.
    fit: str or None
        type of regression to fit. One of `ols`, `logit` or `lws`. If `ols`
        then Ordinary Least Squares regression is applied. If `logit` then
        logistic regression will be fitted, if `lws` then Locally Weighted 
        Scatterplot Smoothing non-parametric regression is applied. If `None` 
        it's either Ordinary Least Squares or logistic regression based on 
        type of ``target``.
    method: str
        Only applicable when ``fit`` = `logit`. The following solvers from 
        `scipy.optimize` are accepted:

            - **newton** for Newton-Raphson, ‘nm’ for Nelder-Mead
            - **bfgs** for Broyden-Fletcher-Goldfarb-Shanno (BFGS)
            - **lbfgs** for limited-memory BFGS with optional box constraints
            - **powell** for modified Powell’s method
            - **cg** for conjugate gradient
            - **ncg** for Newton-conjugate gradient
            - **basinhopping** for global basin-hopping solver
            - **minimize** for generic wrapper of scipy minimize 
              (BFGS by default)

        Note 
        ----
        Each solver has several optional unique arguments. See ``**kwargs`` 
        parameter below (or scipy.optimize) for the available arguments that 
        each solver supports.
    lowess_frac: float
        Between 0 and 1. The fraction of the data used when estimating each 
        y-value for lowess fit.
    it: int
        The number of residual-based reweightings to perform for lowess fit.
    delta: float
        Distance within which to use linear-interpolation instead of weighted 
        regression for lowess fit. `'delta'` can be used to save computations. 
        
        For each `x_i`, regressions are skipped for points closer than ``delta``. 
        The next regression is fit for the farthest point within delta of `x_i` and 
        all points in between are estimated by linearly interpolating between the 
        two regression fits.

        Judicious choice of delta can cut computation time considerably
        for large data (N > 5000). A good choice is ``delta`` = 0.01 * range(x).
    nans_d: dict or None
        dictionary where keys are column names and values are missing(nan) 
        replacements. To perform multiple imputation for several numeric columns.
    frac: float or None
        fraction of dataframe to use as a sample 
        for analysis:

            - 0 < ``frac`` < 1 returns a random sample with size ``frac``. 
            - ``frac`` = 1 returns shuffled dataframe.
            - ``frac`` > 1 up-sample the dataframe, sampling of the same row more 
              than once.
    random_state: int
        for reproducibility, controls the random number generator for ``frac``
        parameter.
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
    theme: str
        adjust axis and title colors as desired
    
    Keyword Args
    ------------
    warn_convergence: bool, optional
        If True, checks the model for the converged flag. If the
        converged flag is False, a ConvergenceWarning is issued.
        All other kwargs are passed to the chosen solver.

        newton
            tol: float
                Relative error in params acceptable for convergence.
        nm -- Nelder Mead
            xtol: float
                Relative error in params acceptable for convergence
            ftol: float
                Relative error in loglike(params) acceptable for
                convergence
            maxfun: int
                Maximum number of function evaluations to make.
        bfgs
            gtol: float
                Stop when norm of gradient is less than gtol.
            norm: float
                Order of norm (np.inf is max, -np.inf is min)
            epsilon
                If fprime is approximated, use this value for the step
                size. Only relevant if LikelihoodModel.score is None.
        lbfgs
            m: int
                This many terms are used for the Hessian approximation.
            factr: float
                A stop condition that is a variant of relative error.
            pgtol: float
                A stop condition that uses the projected gradient.
            epsilon
                If fprime is approximated, use this value for the step
                size. Only relevant if LikelihoodModel.score is None.
            maxfun: int
                Maximum number of function evaluations to make.
            bounds: sequence
                (min, max) pairs for each element in x,
                defining the bounds on that parameter.
                Use None for one of min or max when there is no bound
                in that direction.
        cg
            gtol: float
                Stop when norm of gradient is less than gtol.
            norm: float
                Order of norm (np.inf is max, -np.inf is min)
            epsilon: float
                If fprime is approximated, use this value for the step
                size. Can be scalar or vector.  Only relevant if
                Likelihoodmodel.score is None.
        ncg
            fhess_p: callable f'(x,*args)
                Function which computes the Hessian of f times an arbitrary
                vector, p.  Should only be supplied if
                LikelihoodModel.hessian is None.
            avextol: float
                Stop when the average relative error in the minimizer
                falls below this amount.
            epsilon: float or ndarray
                If fhess is approximated, use this value for the step size.
                Only relevant if Likelihoodmodel.hessian is None.
        powell
            xtol: float
                Line-search error tolerance
            ftol: float
                Relative error in loglike(params) for acceptable for
                convergence.
            maxfun: int
                Maximum number of function evaluations to make.
            start_direc: ndarray
                Initial direction set.
        basinhopping
            niter: int
                The number of basin hopping iterations.
            niter_success: int
                Stop the run if the global minimum candidate remains the
                same for this number of iterations.
            T: float
                The "temperature" parameter for the accept or reject
                criterion. Higher "temperatures" mean that larger jumps
                in function value will be accepted. For best results
                `T` should be comparable to the separation (in function
                value) between local minima.
            stepsize: float
                Initial step size for use in the random displacement.
            interval: int
                The interval for how often to update the `stepsize`.
            minimizer: dict
                Extra keyword arguments to be passed to the minimizer
                `scipy.optimize.minimize()`, for example 'method' - the
                minimization method (e.g. 'L-BFGS-B'), or 'tol' - the
                tolerance for termination. Other arguments are mapped 
                from explicit argument of `fit`:

                - `args` <- `fargs`
                - `jac` <- `score`
                - `hess` <- `hess`
        minimize
            min_method: str, optional
                Name of minimization method to use.
                Any method specific arguments can be passed directly.
                For a list of methods and their arguments, see
                documentation of `scipy.optimize.minimize`.
                If no method is specified, then BFGS is used.

    Attributes
    ----------
    z_inf_out : numpy array
        excluded columns having `inf` values, if any.
    z_nans: numpy array
        numeric column names where imputation of `nan` values took place.
    z_df: pandas dataframe
        preprocessed dataframe that was used internally

    """

    def __init__(self, 
                 df: pd.DataFrame,
                 cols: SEQUENCE_LIKE,
                 target: str,
                 degree: int = 1,
                 fit: Optional[str] = None,
                 method: str = 'newton',
                 lowess_frac: float = 2/3,
                 it: int = 3,
                 delta: float = 0.0,
                 nans_d: Optional[dict] = None,
                 frac: Optional[float] = None,
                 random_state: int = 45,
                 figsize: Optional[Tuple[int, int]] = None,
                 n_rows: Optional[int] = None,
                 n_cols: Optional[int] = None,
                 silent: bool = False,
                 hide_p_bar: bool = False,
                 theme: str = 'darkorange',
                 **kwargs):
        
        # input checks
        if not isinstance(cols, (list, tuple, np.ndarray, pd.Index)):
            raise TypeError("'cols' parameter accepts a sequence e.g: Lists, Tuples, NumPy Arrays or Pandas Base Index. "
                            f"However, '{type(cols)}' was received!")
        if not isinstance(target, str):
            raise TypeError("Please pass target column name as string")
        if np.any(~np.isin(np.r_[cols, [target]], df.columns)):
            raise KeyError("Missing columns! Please ensure that all columns to analyze are included in the DataFrame")
        if np.any([df[col].dtype.kind not in 'ifc' for col in cols]):
            raise ValueError("All 'cols' must be numeric please refer to parameter description")
        if fit and fit not in ['ols', 'logit', 'lws']:
            raise ValueError("'fit' parameter accepts the following arguments: 'ols', 'logit' or 'lws', "
                             f"however, '{fit}' was received!")
        if nans_d:
            if not isinstance(nans_d, dict):
                raise TypeError("Please pass 'nans_d' parameter as a dictionary. Example: {'column name': imputation value}")
            if np.any(~np.isin(np.array(list(nans_d.keys())), df.columns)):
                raise KeyError("Missing columns! Please ensure that all columns to impute are included in the DataFrame")

        if frac:
            replace = True if frac > 1 else False
            self.z_df_ = df.sample(frac = frac, replace = replace, random_state = random_state).copy()
        else:
            self.z_df_ = df.copy() # avoid editing original dataframe

        # handling infs and nans
        self._cols = np.array(cols)
        self._slash_n_impute(nans_d) # attributes
            
        # check and assign correct fits
        str_target = self.z_df_[target].dtype.kind in 'bO'
        cat_target = ((self.z_df_[target].dtype.kind in 'i' and self.z_df_[target].nunique() <= 20) or str_target)

        if degree > 1:
            _z_log.info("Polynomial Least Squares fit will be applied")
            self._fit = None
        elif not fit: # assign generic fits
            if cat_target:
                self._fit = 'logit'
                _z_log.info("logistic fit will be applied")
            else:
                self._fit = 'ols'
                _z_log.info("Ordinary Least Squares fit will be applied")
        elif fit == 'logit' and not cat_target: # switch to regression
            self._fit = 'ols'
            _z_log.info(f"Logistic fit will not be applied rather OLS instead! `{target}` is of high cardinality.")
        else:
            self._fit = fit
            if fit == 'ols' and cat_target:
                _z_log.warning(f"OLS fit will be applied on `{target}` that appears to be categorical.")

        # encoding categorical target as integer
        if str_target: # checking for string only because OLS is allowed on categorical target
            nums, labels = self.z_df_[target].factorize()
            # assign new values
            self.z_df_[target] = nums
            # used to capture last class label when added to plot text
            # discrete values are assigned following order of appearance not alphabetically
            # so last label = highest discrete value
            # left unsorted to match same order when capturing fitted model parameters
            # as these are sorted ascendingly
            # TODO: prompt user for sorting?
            self._lbl = labels

        if self._fit == 'logit':
            if not hasattr(self, '_lbl'): # discrete target
                # unlike earlier this needs sorting to match fitted model parameters
                self._lbl = np.sort(self.z_df_[target].unique())
            self._binary_t = len(self._lbl) == 2

        self._target = target
        self._degree = degree
        self._method = method
        self._lowess_frac = lowess_frac
        self._it = it
        self._delta = delta
        self._hide_p_bar = hide_p_bar
        self._figsize = figsize
        self._n_rows = n_rows
        self._n_cols = n_cols
        self._silent = silent
        self._theme = theme
        self._kwargs = kwargs


    def corr(self,
             disp_corr: str = 'pearson',
             quant: float = .75,
             thresh: Optional[float] = None,
             alpha: Optional[float] = None,
             plot: bool = False,
             ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """ 
        Calculate Pearson (linear) and Spearman (monotonic) correlation 
        and generate heat-map visualizations;

        Visualizations `Plotly Module`:
            - v1: Feature ``cols`` vs Target correlation either overall or 
              for significant results only (P-value <= 0.05).
            - v2: Feature correlation for a selection of highly correlated 
              features with target.

        Note
        ---- 
        to check correlation for categorical features, encode categories as 
        integers first (e.g.: LabelEncoder, OrdinalEncoder, ...).

        Parameters
        ----------
        disp_corr: str
            One of ['Pearson', 'Spearman'], correlation method to 
            be used in:

            - calculating correlation between features
            - sorting v1
        quant: float
            proportion of features to be used in calculating feature 
            correlation and display in v2; default is top 25% (> q3) 
            of features that are highly correlated with ``target``
        thresh: float or None
            minimum correlation strength between features to display 
            in v2; if not `None`, only display correlation >= ``thresh``
        alpha: float or None
            Significance alpha for rejecting null hypothesis (e.g.:0.05).
            if not `None`, V1 display features with significant results 
            only (corr coef p-value <= ``alpha``)
        plot: Bool
            whether to run visualizations or not

        Returns
        -------
        corr_df: pandas dataframe
            correlation coefficient and p-value for each feature vs ``target``
        feat_corr_df: pandas dataframe
            correlation coefficient of highly correlated features, only 
            ``quant`` features are included

        """

        # input checks
        self._input_validation(disp_corr = disp_corr)

        corr = [] # result container

        for col in tqdm(self._cols, desc = f'Calculating Corr....', disable = self._hide_p_bar):
            r_pea, p_pea = stats.pearsonr(self.z_df_[self._target], self.z_df_[col])
            r_spr, p_spr = stats.spearmanr(self.z_df_[self._target], self.z_df_[col])
            corr.append((col, r_pea, p_pea, r_spr, p_spr))

        # Feature vs Target Correlation Dataframe
        corr_df = pd.DataFrame([c[1:] for c in corr], columns = ['pearson', 'p_val_pear', 'spearman', 'p_val_spr'], 
                           index = np.array(corr)[:,:1].ravel()).sort_values(disp_corr, ascending = False)

        # highly correlated features (>= q?)
        abs_mask = corr_df[disp_corr].abs()
        feat_corr_df = self.z_df_[corr_df.index[abs_mask >= abs_mask.quantile(quant)]].corr(disp_corr)

        if plot:
            if alpha:
                # plotting correlations' statistically significant results
                # null hypothesis: two sets of data are uncorrelated/have no ordinal correlation
                # reject Null if P Val <= significance threshold(alpha)
                plot_data = corr_df[(corr_df.p_val_pear <= alpha) | 
                                    (corr_df.p_val_spr <= alpha)].sort_values(disp_corr, ascending = False)
            else:
                plot_data = corr_df.sort_values(disp_corr, ascending = False)
            
            corr_n_cols = len(plot_data)

            # plotting feature correlation
            if thresh:
                corr_plot = feat_corr_df[abs(feat_corr_df) >= thresh]
                # if True then all are nans except diagonals
                # because this is a square matrix
                all_nans = len(corr_plot)**2 - corr_plot.isna().sum().sum() == len(corr_plot)
                if all_nans: # skip plotting as none > thresh
                    feat_corr_n_cols = 1
                else:
                    feat_hm_title = f'{disp_corr} correlation heatmap (>={thresh:.0%}) of top {1 - quant:.0%} features'
                    feat_corr_n_cols = len(corr_plot)
            else:
                corr_plot = feat_corr_df
                feat_hm_title = f'{disp_corr} correlation heatmap of top {1 - quant:.0%} features'
                feat_corr_n_cols = len(corr_plot)

            if corr_n_cols:
                self._n = 0 # control iterations and slicing indices
                lim = 30 # limit plotting to 30 features per map
                title = f'Correlation Heatmap - {self._target}'

                for _ in tqdm(range(int(np.ceil(corr_n_cols / lim))), 
                              desc = f'Plotting Target Correlation Heat Maps....', 
                              disable = self._hide_p_bar):

                    self._heat_plot(plot_data, lim, title)

                    if corr_n_cols > self._n:
                        if not self._silent:
                            _z_log.info(f"{corr_n_cols - self._n} out of {corr_n_cols} features remaining, to continue press "
                                        "'Enter' or input any value to exit.")
                            time.sleep(2)
                            if input().strip().lower().replace(' ',''):
                                break
                        else:
                            _z_log.info(f"{corr_n_cols - self._n} out of {corr_n_cols} features remaining.")

            else:
                _z_log.info("No Significant Correlation Was Noted!")
                
            if feat_corr_n_cols > 1:
                self._n = 0
                lim = 15
                
                for _ in tqdm(range(int(np.ceil(feat_corr_n_cols / lim))), desc = f'Plotting Feature Correlation Heat Maps....', 
                              disable = self._hide_p_bar):

                    self._heat_plot(corr_plot, lim, feat_hm_title, feat_corr = True)

                    if feat_corr_n_cols > self._n:
                        if not self._silent:
                            _z_log.info(f"{feat_corr_n_cols - self._n} out of {feat_corr_n_cols} features remaining, "
                                        "to continue plotting press 'Enter' or input any value to exit.")
                            time.sleep(2)
                            if input().strip().lower().replace(' ',''):
                                break
                        else:
                            _z_log.info(f"{feat_corr_n_cols - self._n} out of {feat_corr_n_cols} features remaining.")

            else:
                _z_log.info(f"No high correlation among top {1 - quant:.0%} features that are highly correlated with `target`")

        return corr_df.T.copy(), feat_corr_df


    def fit_models(self):
        """
        Univariate model fitting:

            - Polynomial regression
            - Ordinary Least Squares regression
            - Locally Weighted Scatterplot Smoothing non-parametric regression
            - Logistic regression
        
        Attributes
        ----------
        z_fit_results_: dict
            where keys are ``cols`` and values are fitted regression model(s).

        z_fit_out_: numpy array
            excluded ``cols``, if any, causing regression fit errors.

        """

        # input checks
        self._input_validation()

        # attributes
        self.z_fit_results_ = {} # fitted models
        fit_out = [] # features not fitted

        for col in tqdm(self._cols, desc = f'Fitting Models....', disable = self._hide_p_bar):

            try:

                # fit models
                if self._degree > 1: 
                    # Least-squares fit of a polynomial of nth degree
                    model = np.polynomial.polynomial.polyfit(self.z_df_[col], self.z_df_[self._target], self._degree)

                elif self._fit == 'ols':
                    # Ordinary Least Squares Regression
                    # Q("{}")' controls column names having numbers and spaces
                    # adds constant automatically
                    model = ols(formula = f'Q("{self._target}")~Q("{col}")', data = self.z_df_).fit()

                elif self._fit == 'logit':
                    # logistic Regression
                    # binary or multiclass
                    model = mnlogit(formula = f'Q("{self._target}")~Q("{col}")', data = self.z_df_).fit(disp = 0, 
                                                                                                      method = self._method,
                                                                                                      **self._kwargs)
                    
                else:
                    # Locally Weighted Scatterplot Smoothing non-parametric regression
                    model = lowess(self.z_df_[self._target], self.z_df_[col], frac = self._lowess_frac, it = self._it, 
                                   delta = self._delta).T
                    
                self.z_fit_results_[col] = model

            except:

                fit_out.append(col)

        if fit_out:

            _z_log.info(f"{len(fit_out)} out of {len(self._cols)} features were not fit! "
                        "Please ensure that data to fit matches model requirements.")

            self.z_fit_out_ = np.asarray(fit_out) # attributes

        return self


    @itr_plot(n_cols = 6, figsize = (24, 11))
    def vis_fit(self,
                olrs_idx: Optional[Tuple[pd.core.indexes.base.Index, list]] = None,
                olrs_mapping: Optional[dict] = None,
                x_jitter: Optional[float] = None,
                y_jitter: Optional[float] = None,
                scatter_kws: dict = {'alpha': 0.3},
                tc_color: str = 'orange',
                olrs_color: str = 'red',
                nbins: Union[int, str] = 'auto',
                axis: str = 'x',
                tight: Optional[bool] = None,
                x_ax_rotation: Optional[int] = None,
                ):
        """
        Scatter plot visualization of univariate regression fits `Seaborn Module`
        
        Parameters
        ----------
        olrs_idx: pandas index, list or None, 
            Index of outlier data points
        olrs_mapping: dict or None
            column names as keys and outlier data points indices as values 
            (pandas index or list) to highlight during plotting. Outliers 
            from each column are plotted against their respective plot
        {x, y}_jitter: float or None
            adds random noise to the observations on {x, y}_axis.
            applicable to main scatter plot of `x` and `y`.
        scatter_kws : dict or None
            Additional keyword arguments passed to `plt.scatter` and 
            `plt.plot`. Applide to main scatter plot of `x` and `y`.
        tc_color: str
            Color of OLS trendline or Sigmoid/lOWESS Curve
        olrs_color: str
            Color of outlier data points
        nbins: int or 'auto'
            For plot decoration, maximum number of axis intervals; 1 - max 
            number of ticks. If the string 'auto', the number of bins will be 
            automatically determined based on the length of the axis.
        axis: str
            For plot decoration, one of ['both', 'x', 'y'], axis on which to apply 
            ``nbins``.
        tight : bool or None
            For plot decoration, controls expansion of axis limits, if `True` axis limits 
            are only expanded using the margins; This does *not* set the margins to zero. 
            If `False`, further expand the axis limits using the axis major locator.
        x_ax_rotation: int or None
            For plot decoration, set degree of x_ticks rotation.

        """

        # prepare plots
        ax = self._fig.add_subplot(self._n_rows, self._n_cols, self._n)

        model = self.z_fit_results_[self._col]

        x, grid = self._plot_data(self.z_df_, self._col)

        if self._degree > 1:

            # fit plot
            y_pred = np.polynomial.polynomial.polyval(grid, model)[:,-1]

            # plot text
            text = "$" + self._func_text(model, poly = True, text_wrap = True) + "$"

            plt.title(text, color = self._theme)
        
        elif self._fit == 'ols':
            
            # fit plot
            paras = model.params.values
            y_pred = grid.dot(paras) # model.fittedvalues

            # plot text
            text = "$" + self._func_text(paras) + "$" + '\n' + \
                   f'$r^2$ = {model.rsquared:.4f}'

            plt.title(text, color = self._theme)

        elif self._fit == 'logit':

            # fit plot
            y_pred = self._logistic_pred(grid, model)

            # plot text
            null_ll = model.llnull
            full_ll = model.llf

            # likelihood function is the probability that the data were generated by the model parameters
            # the model's goal is to find values for the parameters (coefficients) that maximize value of 
            # the likelihood function. The pseudo-R-squared(McFadden’s) measures model's performance, 
            # higher values indicate a better fit, similar to R^2 available under least squares regression. 
            # It is computed based on the ratio of the maximized log-likelihood function as follows:
            # 1 - (Log-Likelihood / LL-Null) where
            # Log-Likelihood(full model): maximized log-likelihood function using all parameters
            # LL-Null(null model): maximized log-likelihood function when only an intercept is included
            pr = 1 - (full_ll / null_ll) # model.prsquared

            # This is the p-value from a likelihood-ratio test of the full versus null model.
            # significance (p-value <.05) indicates favoring full(including feature) versus null(intercept only) model.
            # For example in a binary classification this means that the feature does have an effect on observing a positive 
            # class label this effect is measured by the size(value) of model coefficients(parameters), 
            # which refers to the change in the log-odds of observing positive class for each unit change in the feature value
            ll_stat = -2 * (null_ll - full_ll) # likelihood ratio Chi-Squared test statistic

            # calculate p-value of test statistic using n degrees of freedom
            llrp = stats.chi2.sf(ll_stat, model.df_model) # model.llr_pvalue

            if self._binary_t:
                # model params
                paras = model.params.values.ravel()

            else:
                # displaying results of last class label
                # compared to the base(reference) class
                # i.e.: the change in log-odds of last class
                # as a result of unit change in that feature
                # TODO: what about other class labels?
                paras = model.params.values[:,-1]

            text = "$" + self._func_text(paras) + "$" + '\n' + \
                   f'P$r^2$ = {pr:.4f}' + ' | ' + f'llrp = {llrp:.4f}'

            plt.title(text, color = self._theme)

        else: # lowes
            # fit plot
            x, y_pred = model

        # Main scatter plot
        regplot(data = self.z_df_, x = self._col, y = self._target, fit_reg = False, x_jitter = x_jitter, 
                y_jitter = y_jitter, scatter_kws = scatter_kws, ax = ax)
        
        # fit plot
        plt.plot(x, y_pred, c = tc_color)
        
        # Overlay Outliers
        if hasattr(self, '_lrs') and self._col in self._lrs: # single check for both mapping or idx
            idx = np.array(self._lrs[self._col])[np.isin(self._lrs[self._col], self.z_df_.index)]
            if len(idx): # edge case: using `frac` and full index
                outliers_df = self.z_df_.loc[idx]
                scatterplot(data = outliers_df, x = self._col, y = self._target, color = olrs_color, ax = ax)
        
        # decorate
        col_dtype = self.z_df_[self._col].dtype.kind
        self._decorate_plot(ax, dtype = col_dtype, nbins = nbins, axis = axis, tight = tight, 
                            x_ax_rotation = x_ax_rotation, theme = self._theme);

        self._n += 1
    

    @itr_plot(n_cols = 6, figsize = (24, 11))
    def vis_ols_fit(self):
        """ 
        Histograms and Scatter plots for Assessing OLS residuals' 
        normality and homoscedasticity assumptions
        """

        # fitted model
        model = self.z_fit_results_[self._col]

        # Residuals Normality assumption
        ax = self._fig.add_subplot(self._n_rows, self._n_cols, self._n)
        histplot(model.resid, bins = 'doane', ax = ax) 
        plt.title(f'{self._col}', color = self._theme)
        plt.xlabel('Residuals')
        self._decorate_plot(ax, theme = self._theme);

        # Residuals homoscedasticity assumption
        ax_ = self._fig.add_subplot(self._n_rows, self._n_cols, self._n + 1)
        scatterplot(x = model.fittedvalues, y = model.resid, ax = ax_) # predictions vs residuals
        plt.axhline(0, alpha = 0.5, color = 'r')
        plt.title(f'Residual Plot - {self._col}', color = self._theme)
        plt.xlabel('Predictions')
        plt.ylabel('Residuals')
        self._decorate_plot(ax_, theme = self._theme);

        self._n += 2 # update iteration control
    
    
    def vis_multi(self,
                  col: str,
                  olrs_idx: Optional[Tuple[pd.core.indexes.base.Index, list]] = None,
                  color: Optional[Union[str, int, pd.Series]]= None,
                  size: Optional[Union[str, int, pd.Series]] = None,
                  size_max: int = 15,
                  symbol: Optional[Union[str, int, pd.Series]] = None,
                  symbol_sequence: Optional[List[str]] = None,
                  symbol_map: Optional[dict] = None,
                  hover_name: Optional[Union[str, int, pd.Series]] = None,
                  hover_data: Optional[Union[str, list[str, int], pd.Series, dict]] = None,
                  custom_data: Optional[Union[str, list[str, int], pd.Series]] = None,
                  text: Optional[Union[str, int, pd.Series]] = None,
                  facet_row: Optional[Union[str, int, pd.Series]] = None,
                  facet_col: Optional[Union[str, int, pd.Series]] = None,
                  facet_col_wrap: int = 0,
                  facet_row_spacing: Optional[float] = None,
                  facet_col_spacing: Optional[float] = None,
                  error_x: Optional[Union[str, int, pd.Series]] = None,
                  error_x_minus: Optional[Union[str, int, pd.Series]] = None,
                  error_y: Optional[Union[str, int, pd.Series]] = None,
                  error_y_minus: Optional[Union[str, int, pd.Series]] = None,
                  labels: Optional[dict] = None,
                  color_discrete_sequence: Optional[List[str]] = None,
                  color_continuous_scale: Optional[List[str]] = None,
                  opacity: Optional[float] = None,
                  marginal_x: Optional[str] = None,
                  marginal_y: Optional[str] = None,
                  category_orders: Optional[dict] = None,
                  trendline: Optional[str] = None,
                  trendline_options: Optional[dict] = None, 
                  trendline_color_override: Optional[str] = None,
                  trendline_scope: str = 'trace',
                  log_x: bool = False,
                  log_y: bool = False,
                  range_x: Optional[List[float]] = None,
                  range_y: Optional[List[float]] = None,
                  title: Optional[str] = None,
                  template: Optional[Union[str, dict]] = None,
                  width: Optional[int] = None,
                  height: Optional[int] = None,
                  theme: str = 'darkorange'):
        """
        Interactive multivariate scatter plot 
        visualization and trend analysis `Plotly Module`
        
        Parameters
        ----------
        col: str
            Name of column that goes to `x` axis
        olrs_idx: pandas index, list or None
            Index of outlier data points
        color: str or int or Series or array-like
            Either a name of a column in `data_frame`, or a pandas Series or
            array_like object. Values from this column or array_like are used to
            assign color to marks.
        size: str or int or Series or array-like
            Either a name of a column in `data_frame`, or a pandas Series or
            array_like object. Values from this column or array_like are used to
            assign mark sizes. 
        size_max: int (default `20`)
            Set the maximum mark size when using `size`.
        symbol: str or int or Series or array-like
            Either a name of a column in `data_frame`, or a pandas Series or
            array_like object. Values from this column or array_like are used to
            assign symbols to marks.
        symbol_sequence: list of str
            Strings should define valid plotly.js symbols. When `symbol` is set,
            values in that column are assigned symbols by cycling through
            `symbol_sequence` in the order described in `category_orders`, unless
            the value of `symbol` is a key in `symbol_map`.
        symbol_map: dict with str keys and str values (default `{}`)
            String values should define plotly.js symbols Used to override
            `symbol_sequence` to assign a specific symbols to marks corresponding
            with specific values. Keys in `symbol_map` should be values in the
            column denoted by `symbol`. Alternatively, if the values of `symbol`
            are valid symbol names, the string `'identity'` may be passed to cause
            them to be used directly.
        hover_name: str or int or Series or array-like
            Either a name of a column in `data_frame`, or a pandas Series or
            array_like object. Values from this column or array_like appear in bold
            in the hover tooltip.
        hover_data: str, or list of str or int, or Series or array-like, or dict
            Either a name or list of names of columns in `data_frame`, or pandas
            Series, or array_like objects or a dict with column names as keys, with
            values True (for default formatting) False (in order to remove this
            column from hover information), or a formatting string, for example
            `':.3f'` or `'|%a'` or list-like data to appear in the hover tooltip or
            tuples with a bool or formatting string as first element, and list-like
            data to appear in hover as second element Values from these columns
            appear as extra data in the hover tooltip.
        custom_data: str, or list of str or int, or Series or array-like
            Either name or list of names of columns in `data_frame`, or pandas
            Series, or array_like objects Values from these columns are extra data,
            to be used in widgets or Dash callbacks for example. This data is not
            user-visible but is included in events emitted by the figure (lasso
            selection etc.)
        text: str or int or Series or array-like
            Either a name of a column in `data_frame`, or a pandas Series or
            array_like object. Values from this column or array_like appear in the
            figure as text labels.
        facet_row: str or int or Series or array-like
            Either a name of a column in `data_frame`, or a pandas Series or
            array_like object. Values from this column or array_like are used to
            assign marks to facetted subplots in the vertical direction.
        facet_col: str or int or Series or array-like
            Either a name of a column in `data_frame`, or a pandas Series or
            array_like object. Values from this column or array_like are used to
            assign marks to facetted subplots in the horizontal direction.
        facet_col_wrap: int
            Maximum number of facet columns. Wraps the column variable at this
            width, so that the column facets span multiple rows. Ignored if 0, and
            forced to 0 if `facet_row` or a `marginal` is set.
        facet_row_spacing: float between 0 and 1
            Spacing between facet rows, in paper units. Default is 0.03 or 0.0.7
            when facet_col_wrap is used.
        facet_col_spacing: float between 0 and 1
            Spacing between facet columns, in paper units Default is 0.02.
        error_x: str or int or Series or array-like
            Either a name of a column in `data_frame`, or a pandas Series or
            array_like object. Values from this column or array_like are used to
            size x-axis error bars. If `error_x_minus` is `None`, error bars will
            be symmetrical, otherwise `error_x` is used for the positive direction
            only.
        error_x_minus: str or int or Series or array-like
            Either a name of a column in `data_frame`, or a pandas Series or
            array_like object. Values from this column or array_like are used to
            size x-axis error bars in the negative direction. Ignored if `error_x`
            is `None`.
        error_y: str or int or Series or array-like
            Either a name of a column in `data_frame`, or a pandas Series or
            array_like object. Values from this column or array_like are used to
            size y-axis error bars. If `error_y_minus` is `None`, error bars will
            be symmetrical, otherwise `error_y` is used for the positive direction
            only.
        error_y_minus: str or int or Series or array-like
            Either a name of a column in `data_frame`, or a pandas Series or
            array_like object. Values from this column or array_like are used to
            size y-axis error bars in the negative direction. Ignored if `error_y`
            is `None`.
        labels: dict with str keys and str values (default `{}`)
            By default, column names are used in the figure for axis titles, legend
            entries and hovers. This parameter allows this to be overridden. The
            keys of this dict should correspond to column names, and the values
            should correspond to the desired label to be displayed.
        color_discrete_sequence: list of str
            Strings should define valid CSS-colors. When `color` is set and the
            values in the corresponding column are not numeric, values in that
            column are assigned colors by cycling through `color_discrete_sequence`
            in the order described in `category_orders`, unless the value of
            `color` is a key in `color_discrete_map`. Various useful color
            sequences are available in the `plotly.express.colors` submodules,
            specifically `plotly.express.colors.qualitative`.
        color_continuous_scale: list of str
            Strings should define valid CSS-colors This list is used to build a
            continuous color scale when the column denoted by `color` contains
            numeric data. Various useful color scales are available in the
            `plotly.express.colors` submodules, specifically
            `plotly.express.colors.sequential`, `plotly.express.colors.diverging`
            and `plotly.express.colors.cyclical`.
        opacity: float
            Value between 0 and 1. Sets the opacity for markers.
        marginal_x: str
            One of `'rug'`, `'box'`, `'violin'`, or `'histogram'`. If set, a
            horizontal subplot is drawn above the main plot, visualizing the
            x-distribution.
        marginal_y: str
            One of `'rug'`, `'box'`, `'violin'`, or `'histogram'`. If set, a
            vertical subplot is drawn to the right of the main plot, visualizing
            the y-distribution.
        category_orders: dict with str keys and list of str values (default `{}`)
            By default, in Python 3.6+, the order of categorical values in axes,
            legends and facets depends on the order in which these values are first
            encountered in `data_frame` (and no order is guaranteed by default in
            Python below 3.6). This parameter is used to force a specific ordering
            of values per column. The keys of this dict should correspond to column
            names, and the values should be lists of strings corresponding to the
            specific display order desired.
        trendline: str or None
            One of `'ols'`, `'lowess'`, `'rolling'`, `'expanding'` or `'ewm'`. If
            `'ols'`, an Ordinary Least Squares regression line will be drawn for
            each discrete-color/symbol group. If `'lowess`', a Locally Weighted
            Scatterplot Smoothing line will be drawn for each discrete-color/symbol
            group. If `'rolling`', a Rolling (e.g. rolling average, rolling median)
            line will be drawn for each discrete-color/symbol group. If
            `'expanding`', an Expanding (e.g. expanding average, expanding sum)
            line will be drawn for each discrete-color/symbol group. If `'ewm`', an
            Exponentially Weighted Moment (e.g. exponentially-weighted moving
            average) line will be drawn for each discrete-color/symbol group. See
            the docstrings for the functions in
            `plotly.express.trendline_functions` for more details on these
            functions and how to configure them with the `trendline_options`
            argument.
        trendline_options: dict or None
            Options passed as the first argument to the function from
            `plotly.express.trendline_functions` named in the `trendline`
            argument. Valid keys for the `trendline_options` dict are as
            follows:

            ols
                add_constant: bool, default 'True'
                    if `False`, the trendline passes through the origin 
                    but if `True` a y-intercept is fitted.

                log_x and log_y: bool, default 'False'
                    if `True` the OLS is computed with respect to the base 
                    10 logarithm of the input. Note that this means no zeros 
                    can be present in the input.

            lowess
                frac: float, default '0.6666666'
                    Between 0 and 1. The fraction of the data used when 
                    estimating each y-value.

            rolling
                function: function, str, list or dict, default 'mean'
                    Function to use for aggregating the data. If a function, 
                    must either work when passed a Series/Dataframe or when 
                    passed to Series/Dataframe.apply. Accepted combinations 
                    are:

                    - function
                    - string function name
                    - list of functions and/or 
                      function names, e.g. [np.sum, 'mean']
                    - dict of axis labels -> functions, 
                      function names or list of such.

                function_args: dict
                    function arguments. For examples please refer to 'win_type' 
                    argument documentation below.   

                window: int, timedelta, str, offset, or BaseIndexer subclass
                    - Size of the moving window.

                    - If an integer, the fixed number of observations used for
                      each window.

                    - If a timedelta, str, or offset, the time period of each 
                      window. Each window will be a variable sized based on the 
                      observations included in the time-period. This is only valid 
                      for datetimelike indexes.

                    - If a BaseIndexer subclass, the window boundaries based on the 
                      defined ``get_window_bounds`` method. Additional rolling
                      keyword arguments, namely ``min_periods``, ``center``, 
                      ``closed`` and ``step`` will be passed to ``get_window_bounds``.

                min_periods: int, default None
                    Minimum number of observations in window required to have a value,
                    otherwise, result is ``np.nan``.

                center: bool, default False
                    - If False, set the window labels as the right edge of the window index.

                    - If True, set the window labels as the center of the window index.

                win_type: str, default None
                    - If ``None``, all points are evenly weighted.

                    - If a string, it must be a valid `scipy.signal window function
                      <https://docs.scipy.org/doc/scipy/reference/signal.windows.html#module-scipy.signal.windows>`__. 

                    - e.g.: [`barthann`, `bartlett`, `blackman`, `blackmanharris`, 
                      `bohman`, `boxcar`, `chebwin`, `cosine`, `exponential`, `flattop`, 
                      `gaussian`, `general_gaussian`, `hamming`, `hann`, `kaiser`, 
                      `nuttall`, `parzen`,  `triang`, `tukey`]

                    - Certain Scipy window types require additional parameters to be 
                      passed in the aggregation function. The additional parameters 
                      must match the keywords specified in the Scipy window type method 
                      signature.

                    - `window` and `rolling` are pandas subclasses utilizing window 
                      functions from `scipy` module.

                    - If `win_type` is not `None` a `window` subclass is returned, 
                      otherwise a `rolling` subclass is returned. This affects the
                      way `function` argument behaves, see examples below.

                on: str, optional
                    - For a DataFrame, a column label or Index level on which
                      to calculate the rolling window, rather than the DataFrame's index.

                    - Provided integer column is ignored and excluded from result since
                      an integer index is not used to calculate the rolling window.

                closed: str, default None
                    - If ``'right'``, the first point in the window is excluded from 
                      calculations.

                    - If ``'left'``, the last point in the window is excluded from 
                      calculations.

                    - If ``'both'``, the no points in the window are excluded from 
                      calculations.

                    - If ``'neither'``, the first and last points in the window are 
                      excluded from calculations.

                    - Default ``None`` (``'right'``).

                step: int, default None
                    Evaluate the window at every ``step`` result, equivalent to slicing as
                    ``[::step]``. ``window`` must be an integer. Using a step argument 
                    other than None or 1 will produce a result with a different shape than 
                    the input.

            expanding
                function and function_args
                    same as in `rolling`

                min_periods: int, default 1
                    Minimum number of observations in window required to have a value;
                    otherwise, result is ``np.nan``.
            ewm
                function and function_args
                    same as in `rolling`

                com: float, optional
                    Specify decay in terms of center of mass

                span: float, optional
                    Specify decay in terms of span

                halflife: float, str, timedelta, optional
                    - Specify decay in terms of half-life

                    - If ``times`` is specified, a timedelta convertible unit over which an
                      observation decays to half its value. Only applicable to ``mean()``,
                      and halflife value will not apply to the other functions.

                alpha: float, optional
                    Specify smoothing factor

                min_periods: int, default 0
                    Minimum number of observations in window required to have a value;
                    otherwise, result is ``np.nan``.

                adjust: bool, default True
                    Divide by decaying adjustment factor in beginning periods to account
                    for imbalance in relative weightings (viewing EWMA as a moving
                    average).

                ignore_na: bool, default False
                    Ignore missing values when calculating weights.

                times : np.ndarray, Series, default None
                    - Only applicable to ``mean()``.

                    - Times corresponding to the observations. Must be monotonically 
                      increasing and ``datetime64[ns]`` dtype.

                    - If 1-D array like, a sequence with the same shape as the observations.
        trendline_color_override: str or None
            Valid CSS color. If provided, and if ``trendline`` is set, all trendlines
            will be drawn in this color rather than in the same color as the traces
            from which they draw their inputs.
        trendline_scope: str (one of `'trace'` or `'overall'`, default `'trace'`)
            If `'trace'`, then one trendline is drawn per trace (i.e. per color,
            symbol, facet, animation frame etc) and if `'overall'` then one
            trendline is computed for the entire dataset, and replicated across all
            facets.
        log_x: boolean (default `False`)
            If `True`, the x-axis is log-scaled in cartesian coordinates.
        log_y: boolean (default `False`)
            If `True`, the y-axis is log-scaled in cartesian coordinates.
        range_x: list of two numbers
            If provided, overrides auto-scaling on the x-axis in cartesian
            coordinates.
        range_y: list of two numbers
            If provided, overrides auto-scaling on the y-axis in cartesian
            coordinates.
        title: str
            The figure title.
        template: str or dict or plotly.graph_objects.layout.Template instance
            The figure template name (must be a key in plotly.io.templates) or
            definition.
        width: int (default `None`)
            The figure width in pixels.
        height: int (default `None`)
            The figure height in pixels.
        theme: str,
            adjust axis and title colors as desired
        

        Attributes
        ----------
        z_plotly_ols_fit: pandas dataframe
            fitted Ordinary Least Squares model(s)
        z_plotly_fit: pandas dataframe
            fitted Logistic or Polynomial model(s)
        z_plotly_fit_out: pandas dataframe
            groups where fitting models fails, only applicable 
            for Logistic or Polynomial fits if ``facet`` is assigned


        Rolling Examples
        ----------------
        >>> # Custom Function
        >>> # pandas
        >>> series.rolling('win_type' = None).aggregate(**opts)
        >>> # trendline_options - lambda is the euclidean distance  
        >>> tl_opts = dict(
        >>>                 function = 'aggregate', 
        >>>                 function_args = dict(
        >>>                                      func = lambda x: np.sqrt(x.dot(x))
        >>>                                      ),
        >>>                  win_type = None)

        >>> # Rolling object
        >>> # pandas
        >>> series.rolling('win_type' = None).sum(**opts)
        >>> # trendline_options
        >>> tl_opts = dict(
        >>>                function = 'sum', 
        >>>                function_args = None,
        >>>                win_type = None)
           
        >>> # Window object
        >>> # pandas
        >>> series.rolling('win_type' = 'gaussian').sum(**opts)
        >>> # trendline_options - 'std' is parameter required by  
        >>> # 'gaussian' window function, not the aggregation function 'sum'
        >>> tl_opts = dict(
        >>>                function = 'sum', 
        >>>                function_args = dict(std = 2),
        >>>                win_type = 'gaussian')

        """

        # force order on facet grid if not already
        self._facets = [f for f in [facet_row, facet_col] if f]

        if any(self._facets):
            # ensure complete mapping incase only
            # single facet order was set by user
            # otherwise, override default values
            category_orders = {
                f'{f}': self.z_df_[f].unique() for f in self._facets} | (category_orders if category_orders else {}) 

        # Check active arguments and column type 
        # for proper formatting of hover templates
        args = [col, self._target, color, symbol, size, *self._facets] # all columns arguments
        active_args, numeric, categorical = self._plotly_args(args)
        
        if not hover_data:    
            # Apply proper formatting, hide facets and display index
            # for main scatter plot
            hover_data = {k:':,.3f' for k in numeric} | \
                         {k: False for k in self._facets} | {'index': (':,.0f', self.z_df_.index)}

        # set colors if not already
        if not color_discrete_sequence:
            color_discrete_sequence = colors.qualitative.Dark24
        if not color_continuous_scale:
            color_continuous_scale = colors.sequential.Viridis # ignored if `color` is binary feature
        
        # Main scatter plot using copy of dataFrame, accounting for fraction - if any
        fig = scatter(self.z_df_, x = col, y = self._target, color = color, size = size, size_max = size_max, 
                      symbol = symbol, symbol_sequence = symbol_sequence, symbol_map = symbol_map, 
                      hover_name = hover_name, hover_data = hover_data, custom_data = custom_data, 
                      text = text, facet_row = facet_row, facet_col = facet_col, facet_col_wrap = facet_col_wrap,
                      facet_row_spacing = facet_row_spacing, facet_col_spacing = facet_col_spacing, 
                      error_x = error_x, error_x_minus = error_x_minus, error_y = error_y, 
                      error_y_minus = error_y_minus, labels = labels,
                      color_discrete_sequence = color_discrete_sequence, color_continuous_scale = color_continuous_scale, 
                      opacity = opacity, marginal_x = marginal_x, marginal_y = marginal_y, category_orders = category_orders, 
                      trendline = trendline, trendline_options = trendline_options, 
                      trendline_color_override = trendline_color_override, trendline_scope = trendline_scope, 
                      log_x = log_x, log_y = log_y, range_x = range_x, range_y = range_y, title = title,
                      template = template, width = width, height = height
                      )

        if trendline == 'ols':
            self.z_plotly_ols_fit_ = get_trendline_results(fig) # attributes

        # mapping position on facet grid, if any
        if facet_col_wrap and (any([marginal_x, marginal_y]) or facet_row or not facet_col):
            facet_col_wrap = 0 # Ignore facet column wrapping to match plotly logic
            
        row_map, col_map = self._facet_map(category_orders, facet_row, facet_col, facet_col_wrap)

        # fit identifier for hovertemplate
        if self._degree > 1:
            fit = f'Polynomial(degree = {self._degree})'
            fit_cols = [f'x^{i}' for i in range(self._degree + 1)] # columns of fit results dataframe: polynomial coefs
        elif self._fit == 'logit':
            fit = 'logistic'
            fit_cols = ['fit'] # fitted models
        else:
            fit = None

        # overlay fits
        if fit:
            # log transformation takes place only during fitting
            # this is controlled by designated keys in 
            # `trendline_options` attribute.
            # Plot axis are displayed in original input values
            # unless `log_x` or log_y` attributes are activated
            # which in-turn updates `fig` x/y-axis
            log_x = log_y = False
            col_ = col
            target_ = self._target

            if trendline_options:
                log_x = trendline_options.get("log_x", False)
                log_y = trendline_options.get("log_y", False)

                if log_y and fit != 'logistic':
                    if np.any(self.z_df_[self._target] <= 0):
                        log_y = False
                        _z_log.info(f"Log_y transformation was not applied, {self._target} includes non-positive values")
                    else:
                        self.z_df_[f'{self._target}_'] = np.log10(self.z_df_[self._target])
                        target_ = f'{self._target}_'

                if log_x:
                    if np.any(self.z_df_[col] <= 0):
                        log_x = False
                        _z_log.info(f"Log_x transformation was not applied, {col} includes non-positive values")
                    else:
                        self.z_df_[f'{col}_'] = np.log10(self.z_df_[col])
                        col_ = f'{col}_'

            self._models = [] # fit dataframe container
            self._fit_fail = [] # failed fits container
            
            # fit data is grouped by: color(if categorical) + symbol + facets
            # plotly grouping order is color -> symbol -> facet row -> facet col
            groupers = [color, symbol] if color in categorical else [symbol]
            full_gs = groupers + self._facets
            self._g_map = {col: self.z_df_[col].unique() for col in full_gs if col}

            if self._g_map and trendline_scope != 'overall':
                # update columns of results dataframe
                if self._facets:
                    fit_cols = list(self._g_map.keys()) + fit_cols

                # nested loops for all combinations in grouping map
                for comb in product(*[self._g_map[col] for col in self._g_map.keys()], repeat = 1):
                    mask = self.z_df_[(self.z_df_[self._g_map.keys()] == comb).all(1)]

                    if len(mask.dropna()) > 1 and mask[self._target].nunique() > 1:
                        # location on facet_grid
                        if facet_col_wrap:
                            row_idx = row_map[mask[facet_col].unique()[0]]
                        else:
                            row_idx = row_map[mask[facet_row].unique()[0]] if row_map else 1
                        col_idx = col_map[mask[facet_col].unique()[0]] if col_map else 1

                        # plot data
                        x, y_pred, hovertemplate, name = self._fit_models(col_, target_, mask, fit, self._degree, row_idx, 
                                                                          col_idx, comb, groupers, log_x, log_y)
                        # plot
                        if name: # None if fit fails
                            fig.add_scatter(x = x, y = y_pred, hovertemplate = hovertemplate, showlegend = False, 
                                            name = name, row = row_idx, col = col_idx)

            else:
                # check pre-fit
                # only applicable for 
                # overall non-transformed fits
                model = self.z_fit_results_.get(f'{col_}') if hasattr(self, 'z_fit_results_') else False

                # plot data
                x, y_pred, hovertemplate, name = self._fit_models(col_, target_, self.z_df_, fit, self._degree, 
                                                                  log_x = log_x, log_y = log_y, model = model)
                # plot
                if name:
                    fig.add_scatter(x = x, y = y_pred, hovertemplate = hovertemplate, showlegend = False, 
                                    name = name, row = 'all', col = 'all')

            # attributes
            self.z_plotly_fit_ = pd.DataFrame(self._models, columns = fit_cols)

            if self._fit_fail:
                self.z_plotly_fit_out_ = pd.DataFrame(self._fit_fail)

        # overlay outliers
        if olrs_idx is not None:
            idx = np.array(olrs_idx)[np.isin(olrs_idx, self.z_df_.index)]
            if len(idx):
                # Editing Outliers Scatter hover template
                # Meta define values(column names) to be accessed within the hovertemplate
                meta = active_args[~np.isin(active_args, self._facets)] # only active cols ignoring facets

                # outlier dataframe
                outliers_df = self.z_df_.loc[idx].copy()

                # location on facet_grid, if any
                if facet_col_wrap:
                    outliers_df['row_idx'] = outliers_df[facet_col].map(row_map)
                else:
                    outliers_df['row_idx'] = outliers_df[facet_row].map(row_map) if row_map else 1
                outliers_df['col_idx'] = outliers_df[facet_col].map(col_map) if col_map else 1

                # unique facet grid coordinates
                cord_list = sorted(list(set(zip(outliers_df['row_idx'].values, outliers_df['col_idx'].values))))
                
                # plot
                for idx in cord_list:
                    temp_df = outliers_df[(outliers_df['row_idx'] == idx[0]) & (outliers_df['col_idx'] == idx[1])]

                    # fetching all active arguments from outlier dataframe
                    # for each column displayed in hovertemplate
                    customdata = np.stack([temp_df[_] for _ in meta], axis = -1)

                    # workaround as hovertemplate contradicts python format string (% & f)
                    hovertemplate = \
                    '<br>'.join(['%{meta[i]}: %{customdata[i]:,.3f}'.replace('i', f'{i}') if _ in numeric
                                 else '%{meta[i]}: %{customdata[i]}'.replace('i', f'{i}') 
                                 for i, _ in enumerate(meta)]) + '<br>''Index: %{text}<extra></extra>'

                    # overlay outliers in each respective facet position
                    fig.add_scatter(x = temp_df[col], y = temp_df[self._target],
                                    meta = meta, customdata = customdata, mode = 'markers', 
                                    marker = dict(size = 10, color = 'red', line = dict(color = 'orange', width = 2)),
                                    hovertemplate = hovertemplate, text = temp_df.index, showlegend = False, 
                                    name = 'outliers', row = idx[0], col = idx[1],
                                    )
        
        if not title:
            title = f"'{self._target}' interactive scatter plot"

        # Decorate
        fig.update_layout(dict(paper_bgcolor = 'rgba(0,0,0,0)', plot_bgcolor = 'rgba(0,0,0,0)', 
                               hoverlabel = dict(bgcolor = 'brown', font = dict(family = 'Rockwell', 
                                                                                size = 16, color = 'moccasin')),
                               legend = dict(orientation = 'h', xanchor = 'right', x = 1,
                                             title_font_family = 'Arial', font = dict(family = 'Rockwell',
                                                                                      size = 14, color = 'lemonchiffon'),
                                             bgcolor = 'dimgrey', bordercolor =  'Black', borderwidth = 2),
                               title = dict(text = title, x = 0.5, y = .99, xref = 'paper', 
                                            font = dict(family = 'Arial', size = 20, color = theme))
                              ))
        
        fig.update_xaxes(showgrid = False, color = theme, title_standoff = 10)
        fig.update_yaxes(showgrid = False, color = theme)
        # check if traces exists other than trendlines 
        # if they are the last trace then no other 
        # traces exists as they get plotted first
        if len(fig.data) > 1 and 'trendline' not in fig.data[-1]['hovertemplate']: # other traces exists 
            fig.update_traces(selector = -1, showlegend = True) # only show last trace in legend
        fig.for_each_annotation(lambda x: x.update(text = x.text.split('=')[-1], bgcolor = 'dimgrey', 
                                                   font = dict(family = 'Rockwell', size = 16, color = 'oldlace')))
        # return fig
        # fig.write_image('figure.png', scale=4)
        fig.show();
        

    def vis_multi_d(self,
                    x: str,
                    y: str,
                    z: Optional[str] = None,
                    olrs_idx: Optional[Tuple[pd.core.indexes.base.Index, list]] = None,
                    color: Optional[Union[str, int, pd.Series]]= None,
                    symbol: Optional[Union[str, int, pd.Series]] = None,
                    symbol_sequence: Optional[List[str]] = None,
                    symbol_map: Optional[dict] = None,
                    size: Optional[Union[str, int, pd.Series]] = None,
                    size_max: int = 20,
                    text: Optional[Union[str, int, pd.Series]] = None,
                    hover_name: Optional[Union[str, int, pd.Series]] = None,
                    hover_data: Optional[Union[str, list[str, int], pd.Series, dict]] = None,
                    custom_data: Optional[Union[str, list[str, int], pd.Series]] = None,
                    error_x: Optional[Union[str, int, pd.Series]] = None,
                    error_x_minus: Optional[Union[str, int, pd.Series]] = None,
                    error_y: Optional[Union[str, int, pd.Series]] = None,
                    error_y_minus: Optional[Union[str, int, pd.Series]] = None,
                    error_z: Optional[Union[str, int, pd.Series]] = None,
                    error_z_minus: Optional[Union[str, int, pd.Series]] = None,
                    animation_frame: Optional[Union[str, int, pd.Series]] = None,
                    animation_group: Optional[Union[str, int, pd.Series]] = None,
                    category_orders: Optional[dict] = None,
                    labels: Optional[dict] = None,
                    color_discrete_sequence: Optional[List[str]] = None,
                    color_continuous_scale: Optional[List[str]] = None, 
                    opacity: Optional[float] = None,
                    log_x: bool = False,
                    log_y: bool = False,
                    log_z: bool = False,
                    range_x: Optional[List[float]] = None,
                    range_y: Optional[List[float]] = None,
                    range_z: Optional[List[float]] = None,
                    title: Optional[str] = None,
                    template: Optional[Union[str, dict]] = None,
                    width: Optional[int] = None,
                    height: Optional[int] = None,
                    theme: str = 'darkorange'):
        """
        Interactive 3D multivariate scatter plot visualization `Plotly Module`
        
        Parameters
        ----------
        x: str
            Name of column that goes to `x` axis
        y: str
            Name of column that goes to `y` axis
        z: str or None
            Name of column that goes to `z` axis. If `None`, 
            z-axis is the ``target`` variable
        olrs_idx: pandas index, list or None
            Index of outlier data points
        color: str or int or Series or array-like
            Either a name of a column in `data_frame`, or a pandas Series or
            array_like object. Values from this column or array_like are used to
            assign color to marks.
        symbol: str or int or Series or array-like
            Either a name of a column in `data_frame`, or a pandas Series or
            array_like object. Values from this column or array_like are used to
            assign symbols to marks.
        symbol_sequence: list of str
            Strings should define valid plotly.js symbols. When ``symbol`` is set,
            values in that column are assigned symbols by cycling through
            ``symbol_sequence`` in the order described in ``category_orders``, unless
            the value of ``symbol`` is a key in ``symbol_map``.
        symbol_map: dict with str keys and str values (default `{}`)
            String values should define plotly.js symbols Used to override
            ``symbol_sequence`` to assign a specific symbols to marks corresponding
            with specific values. Keys in ``symbol_map`` should be values in the
            column denoted by ``symbol``. Alternatively, if the values of ``symbol``
            are valid symbol names, the string `'identity'` may be passed to cause
            them to be used directly. 
        size: str or int or Series or array-like
            Either a name of a column in `data_frame`, or a pandas Series or
            array_like object. Values from this column or array_like are used to
            assign mark sizes.
        size_max: int (default `20`)
            Set the maximum mark size when using ``size``.
        text: str or int or Series or array-like
            Either a name of a column in `data_frame`, or a pandas Series or
            array_like object. Values from this column or array_like appear in the
            figure as text labels.
        hover_name: str or int or Series or array-like
            Either a name of a column in `data_frame`, or a pandas Series or
            array_like object. Values from this column or array_like appear in bold
            in the hover tooltip.
        hover_data: str, or list of str or int, or Series or array-like, or dict
            Either a name or list of names of columns in `data_frame`, or pandas
            Series, or array_like objects or a dict with column names as keys, with
            values `True` (for default formatting) `False` (in order to remove this
            column from hover information), or a formatting string, for example
            `':.3f'` or `'|%a'` or list-like data to appear in the hover tooltip or
            tuples with a bool or formatting string as first element, and list-like
            data to appear in hover as second element Values from these columns
            appear as extra data in the hover tooltip.
        custom_data: str, or list of str or int, or Series or array-like
            Either name or list of names of columns in `data_frame`, or pandas
            Series, or array_like objects Values from these columns are extra data,
            to be used in widgets or Dash callbacks for example. This data is not
            user-visible but is included in events emitted by the figure (lasso
            selection etc.)
        error_x: str or int or Series or array-like
            Either a name of a column in `data_frame`, or a pandas Series or
            array_like object. Values from this column or array_like are used to
            size x-axis error bars. If ``error_x_minus`` is `None`, error bars will
            be symmetrical, otherwise `error_x` is used for the positive direction
            only.
        error_x_minus: str or int or Series or array-like
            Either a name of a column in `data_frame`, or a pandas Series or
            array_like object. Values from this column or array_like are used to
            size x-axis error bars in the negative direction. Ignored if ``error_x``
            is `None`.
        error_y: str or int or Series or array-like
            Either a name of a column in `data_frame`, or a pandas Series or
            array_like object. Values from this column or array_like are used to
            size y-axis error bars. If ``error_y_minus`` is `None`, error bars will
            be symmetrical, otherwise ``error_y`` is used for the positive direction
            only.
        error_y_minus: str or int or Series or array-like
            Either a name of a column in `data_frame`, or a pandas Series or
            array_like object. Values from this column or array_like are used to
            size y-axis error bars in the negative direction. Ignored if ``error_y``
            is `None`.
        error_z: str or int or Series or array-like
            Either a name of a column in `data_frame`, or a pandas Series or
            array_like object. Values from this column or array_like are used to
            size z-axis error bars. If ``error_z_minus`` is `None`, error bars will
            be symmetrical, otherwise ``error_z`` is used for the positive direction
            only.
        error_z_minus: str or int or Series or array-like
            Either a name of a column in `data_frame`, or a pandas Series or
            array_like object. Values from this column or array_like are used to
            size z-axis error bars in the negative direction. Ignored if ``error_z``
            is `None`.
        animation_frame: str or int or Series or array-like
            Either a name of a column in `data_frame`, or a pandas Series or
            array_like object. Values from this column or array_like are used to
            assign marks to animation frames.
        animation_group: str or int or Series or array-like
            Either a name of a column in `data_frame`, or a pandas Series or
            array_like object. Values from this column or array_like are used to
            provide object-constancy across animation frames: rows with matching
            ``animation_group`` will be treated as if they describe the same object
            in each frame.
        category_orders: dict with str keys and list of str values (default `{}`)
            By default, in Python 3.6+, the order of categorical values in axes,
            legends and facets depends on the order in which these values are first
            encountered in `data_frame` (and no order is guaranteed by default in
            Python below 3.6). This parameter is used to force a specific ordering
            of values per column. The keys of this dict should correspond to column
            names, and the values should be lists of strings corresponding to the
            specific display order desired.
        labels: dict with str keys and str values (default `{}`)
            By default, column names are used in the figure for axis titles, legend
            entries and hovers. This parameter allows this to be overridden. The
            keys of this dict should correspond to column names, and the values
            should correspond to the desired label to be displayed.
        color_discrete_sequence: list of str
            Strings should define valid CSS-colors. When ``color`` is set and the
            values in the corresponding column are not numeric, values in that
            column are assigned colors by cycling through ``color_discrete_sequence``
            in the order described in ``category_orders``, unless the value of
            ``color`` is a key in ``color_discrete_map``. Various useful color
            sequences are available in the `plotly.express.colors` submodules,
            specifically `plotly.express.colors.qualitative`.
        color_continuous_scale: list of str
            Strings should define valid CSS-colors This list is used to build a
            continuous color scale when the column denoted by `color` contains
            numeric data. Various useful color scales are available in the
            `plotly.express.colors` submodules, specifically
            `plotly.express.colors.sequential`, `plotly.express.colors.diverging`
            and `plotly.express.colors.cyclical`.
        opacity: float or None,
            Value between 0 and 1. Sets the opacity for markers.
        log_x: boolean (default `False`)
            If `True`, the x-axis is log-scaled in cartesian coordinates.
        log_y: boolean (default `False`)
            If `True`, the y-axis is log-scaled in cartesian coordinates.
        log_z: boolean (default `False`)
            If `True`, the z-axis is log-scaled in cartesian coordinates.
        range_x: list of two numbers
            If provided, overrides auto-scaling on the x-axis in cartesian
            coordinates.
        range_y: list of two numbers
            If provided, overrides auto-scaling on the y-axis in cartesian
            coordinates.
        range_z: list of two numbers
            If provided, overrides auto-scaling on the z-axis in cartesian
            coordinates.
        title: str
            The figure title.
        template: str or dict or plotly.graph_objects.layout.Template instance
            The figure template name (must be a key in plotly.io.templates) or
            definition.
        width: int (default `None`)
            The figure width in pixels.
        height: int (default `None`)
            The figure height in pixels.
        theme: str
            adjust axis and title colors as desired
        
        """
        # Setting target variable to z-axis
        if not z and self._target not in [x, y, z]:
            z = self._target
             
        # Editing Main Scatter hover template
        args = [x, y, z, color, symbol, size] # all column arguments ignoring facets
        active_args, numeric, categorical = self._plotly_args(args)
        
        if not hover_data:
            # Apply proper formatting and display index
            # for main scatter plot
            hover_data = {k:':,.3f' for k in numeric} | {'index': (':,.0f', self.z_df_.index)}

        # set colors if not already
        c_disc = color_discrete_sequence if color_discrete_sequence else colors.qualitative.Bold_r
        c_cont = color_continuous_scale if color_continuous_scale else colors.sequential.YlOrRd

        # XD scatter plot
        fig = scatter_3d(self.z_df_, x = x, y = y, z = z, color = color, symbol = symbol,
                         symbol_sequence = symbol_sequence, symbol_map = symbol_map,
                         size = size, size_max = size_max, text = text, hover_name = hover_name, 
                         hover_data = hover_data, custom_data = custom_data, error_x = error_x, 
                         error_x_minus = error_x_minus, error_y = error_y, error_y_minus = error_y_minus,
                         error_z = error_z, error_z_minus = error_z_minus, animation_frame = animation_frame, 
                         animation_group = animation_group, category_orders = category_orders, labels = labels,
                         color_discrete_sequence = c_disc, color_continuous_scale = c_cont,
                         opacity = opacity, log_x = log_x, log_y = log_y, log_z = log_z, range_x = range_x, 
                         range_y = range_y, range_z = range_z, title = title, template = template, width = width,
                         height = height)
        
        # overlay outliers
        if olrs_idx is not None:
            idx = np.array(olrs_idx)[np.isin(olrs_idx, self.z_df_.index)]
            if len(idx): # edge case: using `frac` and full index
                # Editing Outliers Scatter hover template
                meta = active_args

                # fetching all active arguments from outlier dataframe
                outliers_df = self.z_df_.loc[idx].copy()
                customdata = np.stack([outliers_df[_] for _ in meta], axis = -1)
                
                # workaround as hovertemplate contradicts python format string (% & f)
                # <extra></extra> remove trace name
                hovertemplate = \
                '<br>'.join(['%{meta[i]}: %{customdata[i]:,.0f}'.replace('i', f'{i}') if _ in numeric
                             else '%{meta[i]}: %{customdata[i]}'.replace('i', f'{i}') 
                             for i, _ in enumerate(meta)]) + '<br>''Index: %{text}<extra></extra>'
                
                fig.add_scatter3d(x = outliers_df[x], y = outliers_df[y], z = outliers_df[z], 
                                  meta = meta, customdata = customdata, mode = 'markers', 
                                  marker = dict(size = 10, color = 'yellow', line = dict(color = 'red', width = 4)), 
                                  hovertemplate = hovertemplate, text = outliers_df.index, name = 'outliers'
                                 )
            
        if not title:
            title = f'3D Visualization of {self._target}'

        fig.update_layout(dict(paper_bgcolor = 'rgba(0,0,0,0)', plot_bgcolor = 'rgba(0,0,0,0)',
                               # 3d scene decoration
                               scene = dict(
                                   aspectratio = dict(x = 1.5, y = 1.5, z = 1), # axes ratio
                                   # axes decoration
                                   xaxis = dict(backgroundcolor = 'darkred', showgrid = False, 
                                                color = 'darkred'),   
                                   yaxis = dict(backgroundcolor = 'darkslateblue', showgrid = False, 
                                                color = 'darkslateblue'),
                                   zaxis = dict(backgroundcolor = 'darkolivegreen', showgrid = False, 
                                                color = 'darkolivegreen')),
                               hoverlabel = dict(bgcolor = 'brown',
                                                 font = dict(family = 'Rockwell', size = 16, color = 'moccasin')),
                               legend = dict(orientation = 'h', xanchor = 'right', x = 1, 
                                             title_font_family = 'Arial', font = dict(family = 'Rockwell',
                                                                                      size = 14, color = 'lemonchiffon'),
                                             bgcolor = 'dimgrey', bordercolor =  'Black', borderwidth = 2),
                               title = dict(text = title, x = 0.5, y = .99, xref = 'paper', 
                                            font = dict(family = 'Arial', size = 20, color = theme))))

        fig.update_traces(marker = dict(line = dict(width = 2))) # scatter markers decoration
        fig.show();


    def _input_validation(self, disp_corr: Optional[str] = None):
        """ validate inputs before execution """

        if not len(self._cols):
            raise AttributeError("No feature to analyze! Please ensure that input columns are valid") 

        if disp_corr and disp_corr not in ['pearson', 'spearman']:
            raise ValueError("'disp_corr' parameter must be one of the following arguments: 'pearson' or 'spearman', "
                             f"however, '{disp_corr}' was received!")


    def _heat_plot(self, plot_data, lim, title, feat_corr = False):
        """ Correlation heatmaps"""

        # limit features per map
        mask = plot_data[self._n: self._n + lim].T
        data = mask.values.round(2)
        x = mask.columns

        # heat map data and annotations
        if not feat_corr:
            z = data[::2,:] # coef values
            y = mask.index[::2] # corr text
            customdata = data[1::2,:] # pvals
            hovtemp = '<br>'.join(['txt vs %{x}'.replace('txt', f'{self._target}'),
                                   'pval = %{customdata:.3f}<extra></extra>'])
        else:
            z = np.where(np.isnan(data), '', data) # hide values < thresh
            y = mask.index
            customdata = None
            hovtemp = '<br>'.join(['%{y} vs %{x}<extra></extra>'])

        annotations = [layout.Annotation(text = str(z[idx][col_idx]), x = x[col_idx], y = y[idx], 
                                         bgcolor = 'black', bordercolor = 'purple',
                                         showarrow = False, font = dict(family = 'Arial', size = 11, color = 'oldlace')) 
                       for idx, col in enumerate(z) for col_idx, v in enumerate(col)]

        # Heatmaps
        fig = Figure(
            data=[Heatmap(z = z, x = x, y = y ,zmin = -1, zmax = 1, customdata = customdata,
                          hovertemplate = hovtemp, colorscale = 'icefire', showscale = False
                          )])

        # Decorate
        fig.update_layout(
            dict(paper_bgcolor = 'rgba(0,0,0,0)', plot_bgcolor = 'rgba(0,0,0,0)', 
                 hoverlabel = dict(bgcolor = 'darkred'), annotations = annotations,
                 title = dict(text = title, x = 0.5, xref = 'paper', 
                              font = dict(family = 'Arial', size = 20, color = self._theme))
                ))
        fig.update_xaxes(showgrid = False, color = self._theme)
        fig.update_yaxes(showgrid = False, color = self._theme)
        fig.show();

        self._n += lim # update iteration control and slicing indices


    def _plot_data(self, df, col) -> Tuple[np.ndarray, np.ndarray]:
        """ Data used to plot generated predictions """

        lim = np.linspace(df[col].min(), df[col].max(), 100)
        grid = np.c_[np.ones(len(lim)), lim]
        x = grid[:,1]

        return x, grid


    def _logistic_pred(self, grid, model) -> Tuple[np.ndarray]:
        """ Generate predictions from fitted logistic regression model """

        # Use a constant logit of zero for the first class in multiclass
        # because the reference class is never predicted directly
        logits = np.c_[np.zeros(len(grid)), grid.dot(model.params)] 

        # class probability
        # using softmax function
        y_pred = np.exp(logits) / (np.sum(np.exp(logits), axis = 1, keepdims = 1)) # softmax = sigmoid for binary class
        y_pred = y_pred[:,-1] # positive class label for binary or last label for multiclass 

        return y_pred


    def _func_text(self, params, poly = False, text_wrap = False)-> str:
        """ format regression equation and model parameters text """

        # generic mapping for proper display
        replace_map = {"+ -":"- "}
        
        if not poly:

            coef_list = [f"{coef:,.3f}" for coef in params]

            equation = "f(x) = " + " + ".join(coef_list) + "x"

        else:

            coef_list = [f"{coef:,.3f}x<sup>{i}</sup>" for i, coef in enumerate(params)]

            if text_wrap: # seaborn plot title

                text = "P(x) = " + " + ".join(coef_list)

                equation = "$ \n $".join(wrap(text, 70))
                
                replace_map =  replace_map | {"<sup>":"^", "</sup>":"", "x^0":"", 
                                              "x^1":"x", "+$ \n $-": "-$ \n $"}

            else: # plotly hovertemplate
            
                equation = "P(x) = " + " + ".join(coef_list)
                
                replace_map = replace_map | {"x<sup>0</sup>":"", "x<sup>1</sup>":"x"}
                
        for k, v in replace_map.items():
            equation = equation.replace(k, v)

        return equation


    def _plotly_args(self, args) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """ Identify numeric and categorical features for proper formatting """

        active_args = np.array(list({arg for arg in args if arg})) # active arguments, no need to preserve order

        # column dtypes of active arguments
        numeric = np.array([col for col in active_args if self.z_df_[col].dtype.kind in 'ifc'])
        categorical = active_args[~np.isin(active_args, numeric)]

        return active_args, numeric, categorical


    def _facet_map(self, category_orders, facet_row, facet_col, facet_col_wrap = None) -> Optional[Tuple[dict, dict]]:
        """ Map category orders to their corresponding row and column positions within plotly facet grid """

        if facet_col and facet_row:
            n_rows_ = range(1, len(category_orders[facet_row]) + 1)
            n_cols_ = range(1, len(category_orders[facet_col]) + 1)
            row_map = dict(zip(np.flip(category_orders[facet_row]), n_rows_))
            col_map = dict(zip(category_orders[facet_col], n_cols_))
            
        elif facet_col:
            if facet_col_wrap: # Wraps the column variable at this width, Ignored if `facet_row` is set.
                n_rows_ = int(np.ceil(len(category_orders[facet_col]) / facet_col_wrap))
                row_map = {}
                col_map = {}
                c_idx = r_idx = 1
                for _ in range(len(category_orders[facet_col])):
                    row_map[np.flip(category_orders[facet_col])[_]] = r_idx
                    col_map[category_orders[facet_col][_]] = c_idx
                    c_idx += 1
                    if len(category_orders[facet_col][1+_:]) == facet_col_wrap: # remaining categories goes to new row
                        r_idx += 1
                    if c_idx > facet_col_wrap: # max columns reached, new row needed ?
                        c_idx = 1
                        if r_idx < n_rows_:
                            r_idx += 1
            else:
                n_cols_ = range(1, len(category_orders[facet_col]) + 1)
                row_map = None
                col_map = dict(zip(category_orders[facet_col], n_cols_))

        elif facet_row:
            n_rows_ = range(1, len(category_orders[facet_row]) + 1)
            row_map = dict(zip(np.flip(category_orders[facet_row]), n_rows_))
            col_map = None
            
        else:
            row_map = col_map = None

        return row_map, col_map


    def _fit_models(self, col, target, fit_data, fit, degree, row_idx = None, col_idx = None, 
                    comb = None, groupers = None, log_x = False, log_y = False, model = False) -> Optional[Tuple[np.ndarray, str]]:
        """ Generate fit data for Logistic and Polynomial fits in plotly scatter plots """

        # plot data
        x, grid = self._plot_data(fit_data, col)

        # generic return values
        y_pred = hovertemplate = name = None

        # indications of groups for each fit
        gs = [f'{groupers[i]}: {comb[i]}' for i, _ in enumerate(groupers) if _] if groupers else []

        try:
            if fit == 'logistic':
                if not model:
                    model = mnlogit(formula = f'Q("{target}")~Q("{col}")', data = fit_data).fit(disp = 0, method = self._method,
                                                                                                **self._kwargs)
                y_pred = self._logistic_pred(grid, model)
                pr = model.prsquared
                llrp = model.llr_pvalue

                if self._binary_t:
                    paras = model.params.values.ravel()
                    y_hover = 'P(y = 1): %{y:,.0%}<b>(probability)</b><extra></extra>' # <extra></extra> remove trace name
                    name = f'{target} Logistic Fit'
                else:
                    paras = model.params.values[:,-1]
                    y_hover = 'P(y = c): %{y:,.0%}<b>(probability)</b><extra></extra>'.replace('c', f'{self._lbl[-1]}')
                    name = f'{target} Logistic Fit: {self._lbl[-1]} vs {self._lbl[0]}(base)'

                # decorate
                hover_text = [f'pR<sup>2</sup> = {pr:,.3f}',
                              f'llrp = {llrp:,.4f}</b><br>',
                              *gs,
                              'col: %{x:,.3f}'.replace('col', f'{col}'),
                              y_hover]

            else:
                if not np.any(model):
                    model = np.polynomial.polynomial.polyfit(fit_data[col], fit_data[target], degree)
                paras = model
                y_pred = np.polynomial.polynomial.polyval(grid, model)[:,-1]
                name = 'Polynomial Fit'
                hover_text = [*gs,
                              'col: %{x:,.3f}'.replace('col', f'{col}'),
                              'c: %{y:,.3f}<b>(trend)</b><extra></extra>'.replace('c', target)]
                
            if log_x:
                x = np.power(10, x)
            if log_y:
                y_pred = np.power(10, y_pred)

            # decorate
            text = self._func_text(paras, poly = True if degree > 1 else False)

            hovertemplate = '<br>'.join([f'<b>Fit: {fit}</b>',
                                         f'{text}</b><br>'.replace('<br>', '') if fit == 'logistic' else f'{text}</b><br>',
                                         *hover_text
                                         ])

            # update fit container
            # unpack categories tuple and
            # poly fit output of array dtype
            if self._facets and comb:
                self._models.append((*comb, *model) if np.ndim(model) else (*comb, model))
            else:
                self._models.append(model)

        except:
            if comb:
                self._fit_fail.append(dict(zip(self._g_map.keys(), comb)) | {'row': row_idx, 'col':col_idx})
            else:
                _z_log.info(f"{fit} was not applied! Please ensure that data to fit matches model requirements")

        return x, y_pred, hovertemplate, name