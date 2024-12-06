import pandas as pd

import numpy as np

from scipy import stats

from statsmodels.stats.multitest import multipletests

from itertools import combinations

from collections import deque

from sklearn.feature_selection import mutual_info_classif, mutual_info_regression

from tqdm.auto import tqdm

from typing import Optional, Tuple

from IPython.display import display

from ._dist import Dist

from .._utils import SEQUENCE_LIKE

from .._logr import _z_log

###################################################################

class CatAna(Dist):
    '''
    Utilizing both Statsmodels and Scipy modules to perform univariate and
    Multi-variate analysis and visualizations to guide handling multi-level
    categorical features.

    Notes
    -----
    - Categorical features are considered irrespective of their dtype, either string
      or numbers, users of this class are advised to explicitly specify whether the
      columns are categorical using ``cat_cols`` parameter as this will affect both
      grouping and underlying calculations.
    - If not explicitly specified then it is assumed that if features ``cols`` are
      categorical then ``target`` must be numeric and vise versa. This is to dictate
      the direction of categorical grouping of numeric data and method of calculating
      mutual information score `MI`.
    - Categories are preprocessed to highlight `rare` levels; only frequent levels are
      displayed as is while others are grouped into a single level called `rare`. This
      behavior can be controlled by ``top_n`` and ``rare_thresh`` parameters. 
      For severely imbalanced datasets, ensure that ``rare_thresh`` parameter account 
      for the minority class when plotting conditional distributions.
    - Missing values `NaN` in categorical features are not removed by default, rather,
      considered as a separate level called `missing`. If `missing` values happens to 
      be also rare, then they will be labeled as `rare` instead of `missing`.
    - Missing values `NaN` in numeric columns are imputed with mean value of respective
      column, if desired otherwise, use ``nans_d`` parameter or do imputation before 
      using this class.
    - `Scikit-learn` algorithm for Mutual Information score treats discrete features
      differently from continuous features, thus, anything that must have a `float` 
      dtype is not `discrete` and will be flagged as such when calculating `MI` score 
      when ``target`` is continuous. It is advised to specify appropriate dtypes for 
      numeric features before using this class.
    - For Ordinal Categorical Features its better to check correlations and regression
      analysis.
    - Mind the ``frac`` parameter when using the internal preprocessed DataFrame.

    Parameters
    ----------
    df: pandas dataframe
        data source
    cols: sequence (lists, tuples, NumPy arrays or Pandas Base Index)
        column names of features to analyze. Better use homogeneous subsets, example:
        either all categorical or all numeric features; categorical subset can have
        multiple dtypes (object or numeric) depending on the nature of the feature
    target: str
        column name of target variable
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
    nans_d: dict or None
        dictionary where keys are column names and values are missing `nan` 
        replacements. To perform multiple imputation for several numeric ``cols``.
    frac: float or None
        fraction of dataframe to use as a sample 
        for analysis:

            - 0 < ``frac`` < 1 returns a random sample with size ``frac``. 
            - ``frac`` = 1 returns shuffled dataframe.
            - ``frac`` > 1 up-sample the dataframe, sampling of the same row more 
              than once.
    random_state: int
        for reproducibility, controls the random number generator for ``frac`` 
        parameter and when calculating mutual information scores.
    figsize: tuple
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

    Attributes
    ----------
    z_inf_out : numpy array
        excluded columns having `inf` values, if any.
    z_nans: numpy array
        numeric column names where imputation of `nan` values took place.
    z_df: pandas dataframe
        preprocessed dataframe that was used internally
    z_freq_lvls_map: dict
        where keys are column(s) name(s) and values are frequent levels. Only 
        applicable when ``cols`` are categorical
    xludd_feats: numpy array
        categorical column names excluded from the analysis being dominated by 
        rare levels. Only applicable when ``cols`` are categorical

    '''
    
    def __init__(self,
                 df: pd.DataFrame,
                 cols: SEQUENCE_LIKE,
                 target: str,
                 cat_cols: Optional[bool] = None,
                 rare_thresh: float = 0.05,
                 top_n: int = 25,
                 nans_d: Optional[dict] = None,
                 frac: Optional[float] = None,
                 random_state: int = 45,
                 figsize: Optional[Tuple[int, int]] = None,
                 n_rows: Optional[int] = None,
                 n_cols: Optional[int] = None,
                 silent: bool = False,
                 hide_p_bar: bool = False):
        
        # Additional input checks
        if nans_d: 
            if not isinstance(nans_d, dict):
                raise TypeError("Please pass 'nans_d' parameter as a dictionary. Example: {'column name': imputation value}")
            if np.any(~np.isin(np.array(list(nans_d.keys())), df.columns)):
                raise KeyError("Missing columns! Please ensure that all columns to impute are included in the DataFrame")
            
        super().__init__(df, cols, target, cat_cols, rare_thresh, top_n, frac, random_state, figsize, n_cols, n_rows, silent, hide_p_bar)
        
        # remove target from input columns, if any
        self._cols = np.array(self._cols)
        if self._target in self._cols:
            self._cols = self._cols[~(self._cols == self._target)]
            _z_log.info(f"target column '{self._target}' has been removed from input columns")

        # handling infs and nanas 
        # numeric features vs Categorical Target
        if not self._cat_cols and not np.any([self.z_df_[col].dtype.kind in 'bO' for col in self._cols]):

            self._target_lvls = self.z_df_[self._target].unique() # unique categories for ANOVA and PostHoc

            self._slash_n_impute(nans_d) # attributes


    def ana_owva(self, alpha: float = 0.05, disp_res: bool = True) -> pd.DataFrame:
        
        """
        One-way ANOVA & Kruskal-Wallis H (non-parametric equivalent of the One-Way ANOVA)
        for Numeric vs Categorical Features.
        
        null: mean/median of all groups are equal
        
        Parameters
        ----------
        alpha: float
            Significance alpha for rejecting null hypothesis.
            Reject null if p-value < ``alpha``
        disp_res: bool
            triggers displaying ANOVA results DataFrame
        
        Attributes
        ----------
        zefct_df: pandas dataframe
            dataframe showing effect of categorical feature on ``target`` 
            distribution. Only applicable when ``cols`` are categorical
        
        Returns
        -------
        anova_df: pandas dataframe
            dataframe of ANOVA and related assumptions results

        """

        # input check
        if self._cat_cols and (self.z_df_[self._target].nunique() <= 20 or self.z_df_[self._target].dtype.kind in 'bO'):
            raise TypeError("`cols` and `target` are both Categorical, consider using Chi2 test of independence instead")
        
        if not self._cat_cols:
            if np.any([self.z_df_[col].dtype.kind in 'bO' for col in self._cols]):
                raise TypeError("Some columns are categorical, Please ensure 'cat_cols' parameter is set to 'True'")
            if self.z_df_[self._target].nunique() > 20:
                raise TypeError("`cols` and `target` are both Numeric, consider using regression and correlation tests instead")
        
        if any(self._cols):
            
            summary = {} # ANOVA results container
            var_dict = {} # Mean variation container
            self._p_val = {} # p-value container for equal variances assumption tests in latter post-hoc

            for col in tqdm(self._cols, desc = 'Ongoing ANOVA....', disable = self._hide_p_bar):

                # target always categorical
                mask, feat, target = self._grouping(col, self._target)

                if self._cat_cols: # categorical feats, numeric target
                    n_lvls = mask[target].unique()

                    # Mutual Info Score
                    # These numbers are not percentages rather an indication of relative importance
                    # Features of high importance have high Score
                    m_i = mutual_info_regression(mask[target].factorize()[0][:, np.newaxis], mask[feat],
                                                 discrete_features = True,
                                                 random_state = self._random_state)[0].round(4)

                    # Mean variation within groups(conditional) compared to global(prior)
                    # variations within different groups of a single feature can indicate significance to prediction results
                    # the closer to global the less significant
                    var_dict[col] = mask.groupby(target)[feat].mean().to_frame()

                else: # numeric feats, categorical target
                    n_lvls = self._target_lvls

                    # Mutual Info Score
                    m_i = mutual_info_classif(mask[[feat]], mask[target],
                                              discrete_features = False if mask[feat].dtype.kind == 'f' else True,
                                              random_state = self._random_state)[0].round(4)

                # groups/lvls
                groups = [mask[feat][mask[target] == g] for g in n_lvls] # (cat cols, num target) --> feat = target, target = col

                # One-way ANOVA
                # Assume normal distribution of the residuals
                # null: mean of all groups are equal
                f, p_f = stats.f_oneway(*groups)

                # Kruskal-Wallis H (non-parametric equivalent of the One-Way ANOVA)
                # Does not assume a normal distribution of the residuals
                # null: median of all groups are equal
                h, p_h = stats.kruskal(*groups)

                # accept reject ANOVA/Kruskal
                eq_mean_anova = p_f > alpha
                eq_median_kruskal = p_h > alpha

                # Test ANOVA Assumptions
                # Checking homogeneity of variance across samples
                # ANOVA assumes Equal Variance

                # assuming data is not normally distributed
                p_v = stats.levene(*groups).pvalue
                # non-parametric(distribution free) when populations are identical
                p_flg = stats.fligner(*groups).pvalue

                # null: all input samples have equal variances
                # Reject Null if P val <= 0.05
                eq_var_lev = p_v > alpha
                eq_var_flg = p_flg > alpha

                # feature stats
                sample_size = [len(_) for _ in groups]
                n_frequent_lvls, max_sample, min_sample = len(n_lvls), np.max(sample_size), np.min(sample_size)

                # update 'equal variance' p-value container
                self._p_val[col] = {'levene': p_v, 'fligner': p_flg}

                # update ANOVA container
                summary[col] = {
                                'f_stat_ANOVA': f, 'p_val_f': p_f, 'eq_mean': eq_mean_anova,
                                'h_stat_Kruskal': h, 'p_val_h': p_h, 'eq_median': eq_median_kruskal,    
                                'p_val_lev': p_v, 'eq_var_lev': eq_var_lev,
                                'p_val_flg': p_flg, 'eq_var_flg': eq_var_flg,
                                'max_sample_size': max_sample,
                                'min_sample_size': min_sample, 
                                'n_frequent_lvls': n_frequent_lvls,
                                'm_i_score': m_i
                                }

            # ANOVA/Krus dataframe
            anova_df = pd.DataFrame(summary)
            if hasattr(self, "z_nans_"):# flag imputations
                anova_df.loc['imputed'] = [col in self.z_nans_ for col in anova_df.columns]
            
            if any(anova_df.loc['f_stat_ANOVA'].values == np.inf) or any(np.isnan(list(anova_df.loc['f_stat_ANOVA'].values))):
                _z_log.warning("Check the groups in features having 'inf' and 'nan' results.")

            if self._cat_cols:
                # columns for post_hoc analysis
                self._pos_hoc_cols = anova_df.columns[~(anova_df.loc['n_frequent_lvls'] == 2)] 
                # attributes
                # conditional vs prior target mean
                self.zefct_df_ = self._var_df(var_dict, self.z_df_, self._target).sort_values('ratio', ascending = False)

            if disp_res:
                display('** One-way ANOVA / Kruskal-Wallis H and their related assumptions assessment **',
                        'Note: `False` means Reject Null; there is at least one group/lvl with '
                        'mean/median differences that are statistically significant',
                        anova_df.style.apply(lambda x: ['background: olive' if not x.eq_mean else '' for i in x],
                                            subset = pd.IndexSlice['eq_mean':'eq_mean'])\
                        .apply(lambda x: ['background: grey' if not x.eq_median else '' for i in x],
                               subset = pd.IndexSlice['eq_median':'eq_median']).format(precision = 3, thousands = ','))

            return anova_df
        else:
             _z_log.info("no columns to analyze! Please check input columns")
                

    def ana_post(self, equal_var: str = 'levene', alternative: str = 'two-sided', alpha: float = 0.05, 
                 multi_tst_corrc: str = 'bonf', disp_res: bool = True) -> pd.DataFrame:
        """
        post-hoc analysis(T-test and Mann–Whitney U test) for categorical features 
        having more than two levels.
                
        Parameters
        ----------
        equal_var: str
            method to apply when checking for equal variance assumption prior to
            calculating the T-test. One of `levene` or `fligner`. `levene` tests
            equal variance assumption assuming data is not normally distributed, 
            `Fligner-Killeen's` test is distribution free when populations are 
            identical
        alternative: str
            defines the alternative
            hypothesis

                * **two-sided**: distributions underlying the samples are unequal
                * **less**: the distribution underlying the first sample is less 
                  than the distribution underlying the second sample
                * **greater**: the distribution underlying the first sample is 
                  greater the distribution underlying the second sample.
        alpha: float
            pre-adjusted alpha(significance level) for rejecting null hypothesis, 
            will also be used in multiple comparison corrections. Reject null if 
            p-value < ``alpha``
        multi_tst_corrc: str
            method used for testing and adjusting pvalues from statsmodels 
            multipletests

                - **bonferroni**: one-step correction
                - **sidak**: one-step correction
                - **holm-sidak**: step down method using Sidak adjustments
                - **holm**: step-down method using Bonferroni adjustments
                - **simes-hochberg**: step-up method (independent)
                - **hommel**: closed method based on Simes tests (non-negative)
                - **fdr_bh**: Benjamini/Hochberg (non-negative)
                - **fdr_by**: Benjamini/Yekutieli (negative)
                - **fdr_tsbh**: two stage fdr correction (non-negative)
                - **fdr_tsbky**: two stage fdr correction (non-negative)
        disp_res: bool
            triggers displaying results DataFrame, only for features having no
            significant results
        
        Attributes
        ----------
        xludd_phoc_feats: numpy array
            column names excluded from the analysis having only two frequent levels.
            Only applicable when ``cols`` are categorical
        
        Returns
        --------
        post_hoc_df: pandas dataframe
            dataframe of Post-Hoc analysis results

        """

        # input check
        try:
            self._p_val
        except:
            raise AttributeError("Please run ANOVA first!")
        if not self._cat_cols and self.z_df_[self._target].nunique() <= 2: # cat target with only two lvls
            raise TypeError("Post Hoc Analysis only applicable for categorical features having more than 2 levels")
        if equal_var not in ['levene', 'fligner']:
            raise ValueError("'equal_var' parameter must be one of the following arguments: 'levene' or 'fligner' "
                             f"however, '{equal_var}' was received!")
            
        if self._cat_cols: # cat features vs num target
            # run post hoc only if more than two levels for columns already analyzed 
            # Note: `missing` and `rare` levels are inclusive
            cols = self._pos_hoc_cols
            
            # attributes
            self.xludd_phoc_feats_ = self._cols[~np.isin(self._cols, cols)]
            
            if self.xludd_phoc_feats_ :
                _z_log.info(f"{len(self.xludd_phoc_feats_):,.0f} Feature(s) Having Only 2 Frequent Levels "
                            "Were Excluded From Post Hoc Analysis")
            
        else: # num features vs cat target
            cols = self._cols
            comb = self._target_lvls # for calculating n-possible combinations
            mask = self.z_df_

        if any(cols):
            
            post_hoc = [] # test results container
            
            for col in tqdm(cols, desc = 'Ongoing Post Hoc Analysis....', disable = self._hide_p_bar):
                
                temp_post_hoc = [] # column wise test container

                mask, feat, target = self._grouping(col, self._target)
 
                if self._cat_cols:
                    comb = mask[target].unique()

                equal_var_ = True if self._p_val[col][equal_var] > 0.05 else False
                
                # post-hoc  
                # null: 2 independent samples have identical distributions
                for i in combinations(comb, 2):
                    # t-test based on equal variance analysis
                    # Welch's t-test is used assuming no-qual variance
                    t, p_t = stats.ttest_ind(mask[feat][mask[target] == i[0]], 
                                             mask[feat][mask[target] == i[1]], 
                                             equal_var = equal_var_, alternative = alternative,
                                             random_state = self._random_state)

                    # Mann–Whitney U test (Nonparametric version of two-sided t-test)
                    mw, p_mw = stats.mannwhitneyu(mask[feat][mask[target] == i[0]], 
                                                  mask[feat][mask[target] == i[1]],
                                                  alternative = alternative)
                    
                    # update temp test container
                    if self._cat_cols:
                        temp_post_hoc.append([target, i[0], i[1], round(t,2), round(p_t,4), round(mw,2), round(p_mw,4)])
                    else: # numeric feats vs target column. Groups(combs) are that of target's
                        temp_post_hoc.append([feat, i[0], i[1], round(t,2), round(p_t,4), round(mw,2), round(p_mw,4)])

                # there are two ways for adjusting the statistical inference of multiple comparisons. 
                # first, adjusting P-values directly by adjusting the observed P value for each hypothesis/group
                # while keeping the significance level (alpha, i.e: 0.05) unchanged; comparing adjusted P-values to original alpha 
                # second, adjusting alpha while leaving observed P-values as is; comparing adjusted alpha to the observed P-values
                # `multipletests` provide a range of results including: adjusted P-vals, adjusted alpha(FWER) and accept/reject text
                # example of bonferroni adjustment of observed P-values: np.minimum(array of unadjusted P-values * N groups, 1)
                # example of bonferroni adjustment of alpha: alpha / N groups
                pv_t = np.array(temp_post_hoc)[:, 4:5].ravel().astype(float) # unadjusted T-TEST P-values

                mul_ts_t = multipletests(pv_t, alpha = alpha, method = multi_tst_corrc) # includes adjusted P-values

                # update temp test container
                deque(map(list.append, temp_post_hoc, np.repeat(mul_ts_t[2], len(mul_ts_t[0]))), 0) # adjusted FWER(alpha) Sidak
                deque(map(list.append, temp_post_hoc, np.repeat(mul_ts_t[3], len(mul_ts_t[0]))), 0) # adjusted FWER(alpha) Bonferroni
                deque(map(list.append, temp_post_hoc, mul_ts_t[1]), 0) # corrected P-values of multiple tests
                deque(map(list.append, temp_post_hoc, mul_ts_t[0]), 0) # accept/reject text of T-TEST's null

                # update tests container
                post_hoc.extend(temp_post_hoc)

            # post-hoc dataframe
            post_hoc_df = pd.DataFrame(post_hoc, columns = ['feature', 'group_one', 'group_two', 
                                                            't_stat', 'p_val_t', 'mw_stat', 'p_val_mw', 
                                                            'FWER_Sidak', 'FWER_Bonf', 'adj_p_val_t', 
                                                            f'reject_t_{multi_tst_corrc}'])
            # re-arrange columns
            o_cols = post_hoc_df.columns

            post_hoc_df = post_hoc_df[np.r_[o_cols[:5], o_cols[9:], o_cols[5:9]]]

            if disp_res:
                false_mask = post_hoc_df[post_hoc_df[f'reject_t_{multi_tst_corrc}'] == False]
                if false_mask.shape[0]:
                    display(f'** Post-hoc results using `{multi_tst_corrc}` correction for groups/lvls having no '
                            'significant results **',
                            'Note: `False` means Accept Null; difference in conditional distribution given these groups/lvls '
                            'is not statistically significantl',
                            false_mask.T.style\
                            .apply(lambda x: ['background: olive' if not x.iloc[-1] else '' for i in x],
                                   subset = pd.IndexSlice[f'reject_t_{multi_tst_corrc}':f'reject_t_{multi_tst_corrc}'])\
                            .format(precision = 3, thousands = ',').hide(axis = 1))
                else:
                    display('** Conditional distribution of all groups/lvls has statistically significant differences **')

            return post_hoc_df
        else:
             _z_log.info("no columns to analyze! Please check input columns")
                

    def ana_chi2(self, alpha: float = 0.05, disp_res: bool = True) -> pd.DataFrame:
        """
        Chi2 test of independence between two categorical variables, best suited for 
        nominal data.

        null: categorical variables are independent

        Notes
        -----
        - An often quoted guideline for the validity of this calculation is that
          the test should be used only if the observed and expected frequencies
          in each cell are at least 5.

        - This is a test for the independence of different categories of a
          population. The test is only meaningful when the dimension of
          `observed` is two or more.  Applying the test to a one-dimensional
          table will always result in `expected` equal to `observed` and a
          chi-square statistic equal to 0.

        - This function does not handle masked arrays, because the calculation
          does not make sense with missing values.
        
        Parameters
        ----------
        alpha: float
            Significance alpha for rejecting null hypothesis.
            Reject null if p-value < ``alpha``
        disp_res: bool
            triggers displaying results DataFrame
        
        Attributes
        ----------
        zefct_df: pandas dataframe
            dataframe showing effect of categorical feature on target distribution.
            Only applicable when ``cols`` are categorical
        z_crss_tabs: dict
            where keys are analyzed columns and values are their corresponding 
            cross_tabs. Only applicable when ``cols`` are categorical
        
        Returns
        -------
        chi2_df: pandas dataframe
            dataframe of chi2 analysis results

        """

        # input check - triggers grouping which can be bypassed by 'rare_thresh' and 'top_n'
        if not self._cat_cols:
            if self.z_df_[self._target].nunique() > 20:
                _z_log.info("Chi2 test of independence is best suited for two categorical variables.")
            else:
                _z_log.info("'cat_cols' is set to 'False', rare and missing categorical levels are not preprocessed.")
        
        # sorting discrete labels to report on posterior vs prior changes
        # string class labels follows order of appearance
        if self.z_df_[self._target].dtype.kind not in 'bO':
            self._lbl = np.sort(self.z_df_[self._target].unique())
        else:
            self._lbl = self.z_df_[self._target].unique()

        if any(self._cols):
            
            var_dict = {} # Mean variation container
            chi2_res = {} # chi2 results container
            self.z_crss_tabs_ = {} # cross_tabs container
            
            for col in tqdm(self._cols, desc = 'Ongoing Independence Test(Chi2)....', disable = self._hide_p_bar):

                mask, feat, target = self._grouping(col, self._target)

                # calculate chi2 statistic and p-value from contingency table
                crss_tab = pd.crosstab(mask[feat], mask[target])
                chi2, p_chi2 = stats.chi2_contingency(crss_tab)[:2]

                # null: both categories are independent
                acc_rej = p_chi2 <= alpha

                # `min_smpl` captures the smallest sample size
                # across all crosstab cells; rule of thumb is that
                # chi2 test should be used only if the observed and  
                # expected frequencies in each cell are at least 5.
                chi2_res[col] = {'chi2': chi2, 'p_val': p_chi2, 'dependent': acc_rej, 'min_sample_size': min(crss_tab.min())}

                # attributes
                self.z_crss_tabs_[col] = crss_tab

                # Mean variation within groups(conditional) compared to global(prior)
                # the closer to global the less significant
                # treat multiclass as binary
                # TODO: better handling of multiclass to display more results
                if self._cat_cols: # why here? so it wont mess with `comb` dtype calls from `ana_post`
                    var_dict[col] = (crss_tab / crss_tab.sum()).iloc[-1].to_frame()

            # chi2 dataframe
            chi2_df = pd.DataFrame(chi2_res)

            # attributes
            if var_dict and not hasattr(self, 'zefct_df_'):
                # P(Class|feature)
                self.zefct_df_ = self._var_df(var_dict, self.z_df_, self._target).sort_values('ratio', ascending = False)

            if disp_res:
                # Display Results
                # Note when using subset: Only label-based slicing is supported, any valid indexer to .loc will work
                display('** Chi2 test of independence results **', 
                        'Note: `True` means Reject Null; categorical variables are dependent **',
                        chi2_df.style.apply(lambda x: ['background: olive' if x.dependent else '' for i in x],
                                            subset = pd.IndexSlice['dependent':'dependent']).format(precision = 3, thousands = ','))

            return chi2_df
        
        else:
            _z_log.info("No columns to analyze! Please check input columns")


    def _var_df(self, var_dict: dict, 
                df: pd.DataFrame, 
                target: str) -> pd.DataFrame:
        """
        Construct a DataFrame highligting Conditional and Prior ``target`` mean
        differences for each categorical feature.
        
        Parameters
        ----------
        var_dict: dictionary
            where keys are categorical column names and values are
            DataFrames of conditional ``target`` distribution. Example:
            {col:df.groupby(col)[target].mean().to_frame()}
        df: pandas dataframe,
            data source
        target: str
            target column name
            
        Returns
        -------
        var_df: pandas dataframe
            dataframe showing effect of categorical feature on ``target`` distribution

        """

        if df[target].nunique() > 20 and df[target].dtype.kind in 'ifc': # regression target
            last_lbl = ''
            prior = df[target].mean()
            target_lvl = target
        else:
            last_lbl = self._lbl[-1]
            prior = df[target].value_counts(dropna = False, normalize = True).loc[last_lbl]
            target_lvl = f'{target}_{last_lbl}'

        var_df = pd.concat(var_dict).reset_index().rename(columns = {'level_0': 'feature', 'level_1': 'lvl',
                                                                     last_lbl: target_lvl,
                                                                        })

        # global mean
        var_df['prior'] = prior

        # Example: for binary classification:
        # +ve = prior < posteriori (group wise), this means that this group is 
        # More likely to be a positive example(1) and vise versa. The magnitude
        # (size of difference) is more important that the sign (+/-)
        var_df['diff'] = var_df[target_lvl] - var_df['prior']

        # Example: for binary classification:
        # 1 means prior = posteriori (group wise) implying no impact on prediction. 
        # If > 1 (1.5 for example) then this group is 1.5 times more likely to be a positive example 
        # (aka this group is 50% more likely to be a positive example, its 50% higher than global mean)";
        # If < 1 (0.75 for example) then this group is 25% less likely to be a positive example and so on
        var_df['ratio'] = var_df[target_lvl] / var_df['prior']

        return var_df