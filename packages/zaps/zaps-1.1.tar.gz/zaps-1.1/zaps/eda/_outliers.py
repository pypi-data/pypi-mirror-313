import pandas as pd

import numpy as np

from sklearn.base import BaseEstimator, TransformerMixin

from tqdm.auto import tqdm

from typing import Optional, Union, Tuple

from .._utils import SEQUENCE_LIKE, PipeLineMixin

from .._logr import _z_log

###################################################################

class Olrs(PipeLineMixin, TransformerMixin, BaseEstimator): # Sklearn docs: mixins: left, BaseEstimator: right for proper MRO.
    """
    Identify and handle outlier values, identification is done by calculating a 
    threshold beyond which an observation is considered to be an outlier, 
    using one of the following methods:

    - Gaussian approximation: 
        outliers are captured based on distance from the mean. 
        e.g.: x data point is an outlier if: (mean - 3 * std) > x or x > (mean + 3 * std) 
        where 3 is distance from mean. 
    - Inter-quantile range proximity rule (IQR): 
        outliers are identified based on distance from IQR(Q3-Q1). e.g.: x data point is an 
        outlier if: (q1 - 1.5 * iqr) > x or x > (q3 + 1.5 * iqr) 
        where 1.5 is distance from IQR.
    - Median Absolute Deviation from the median (MAD-median rule): 
        same formula as Gaussian approximation for highlighting outliers, however, replacing 
        mean with median and std with MAD which is suitable for skewed data. See notes below.
    - Quantiles: 
        outliers are identified using a specific quantile values.
        e.g.: x data point is an outlier if: (.05) > x or x > (1 - .05) 
        where [.05, 1-.05] are the 5th and 95th quantile.
            
    Handling is done using Winsorization that is transforming the data by limiting the 
    extreme values `outliers`, to a certain arbitrary value. The arbitrary value are the 
    thresholds from one of the methods mentioned above beyond which outliers are 
    labeled. 
    
    e.g.: if ``distance`` = .1 and ``method`` = `q` then it's 80% winsorization as 
    all data below the 10th quantile is set to the 10th quantile, and data above the 
    90th quantile is set to the 90th quantile, thus 20% of data is reassigned.
        
    Winsorizing is different from trimming because the extreme values are not removed, 
    but are instead replaced by other values.
    
    Notes
    -----
    - default ``distance`` under `mad` method is not scaled. If it is desired to use 
      MAD as a robust replacement for the standard deviation of normal distribution, 
      then multiply the distance by 1.4826 before passing it to ``distance`` parameter. 
      e.g.: (3 * std) becomes ((3 * 1.4826) * MAD)

    - If the data is normally distributed then Gaussian approximation method is best 
      suited for identifying outliers, otherwise, rest of methods works on normal and 
      non-normal data.

    - data passed to `fit` and `transform` methods will be converted to a DataFrame if 
      not one already, default behavior is to bypass ``cols`` and ``mapping`` parameter 
      if any of names not found in the DataFrame and transform all numeric columns instead. 
      So be mindful of names used in ``cols`` and ``mapping`` parameters as column names 
      will be generic in that case.

    Parameters
    ----------
    cols: sequence (lists, tuples, NumPy arrays or Pandas Base Index) or None
        column names of numeric features. If `None` then ``cols`` is ignored 
        and all numeric columns will be inferred and transformed this also applies 
        if any of the ``cols`` not found in the DataFrame or thier data types are not 
        numeric.
    mapping: dict or None
        Dictionary for mapping different outlier labeling method to each column, it must 
        have the following structure: {'column name':(method, distance)} and follows the 
        same logic of ``method`` and ``distance`` parameters. Columns could be independent 
        of ``cols`` parameter and will be merged during fit.
    method: str
        method to label outliers, one of [`gaus`, `qr`, `mad`, `q`]:

        - **gaus**: Gaussian approximation 
        - **iqr**: Inter-quantile range proximity rule (IQR)
        - **mad**: Median Absoulte Deviation from the median
        - **q**: data quantiles
    distance: float or None
        override default distance to label outliers, default is:
        {`gaus`: 3, `iqr`: 1.5, `mad`: 1, `q`: .05}.
        
        Note
        -----
        when ``method`` = `q`:

        - distance indicates the quantiles. Example: if ``distance`` = .05, data 
          will be capped at 5th and 95th percentiles.
        - Outliers will be removed up to a maximum of the 20th percentiles. Thus, 
          'distance' takes values between 0 and 0.2
    tail: str
        specify direction to handle outliers, One of `both`, `right`, `left`.

        - **both** for outliers at both ends of the distribution
        - **right** for outliers at the right end of the distribution 
        - **left** for outliers at the left end of the distribution
    hide_p_bar: Bool
        triggers hiding progress bar (tqdm module); Default `False`

    """

    def __init__(self,
                 cols: Optional[SEQUENCE_LIKE] = None,
                 mapping: Optional[dict] = None,
                 method: str = 'iqr', 
                 distance: Optional[float] = None,
                 tail: str = 'both',
                 hide_p_bar: bool = False):

        # Sklearn docs: no parameter validation in `__init__` rather in `fit`
        self.cols = cols
        self.mapping = mapping
        self.method = method
        self.distance = distance
        self.tail = tail
        self.hide_p_bar = hide_p_bar
        

    def fit(self,
            X: Union[np.generic, np.ndarray, pd.DataFrame],
            y = None,
            labels: Optional[Union[list, pd.Index]] = None,
            disp_res: bool = False):
        """
        Calculate thresholds beyond which values are labeled as outliers
        
        Parameters
        ----------
        X: np.ndarray or pd.DataFrame
            data source to use in outlier threshold calculation, usually the 
            training data. `Ndarray` will be converted to a DataFrame with 
            generic column names.
        y: None
            There is no need of a target in this transformer, yet the pipeline 
            API requires this parameter.
        labels: list, Pandas Base Index or None
            labels to use as column names when converting ``X`` to a DataFrame. 
            If `None`, generic names will be generated
        disp_res: bool
            triggers displaying capping thresholds per each column

        Attributes
        ----------
        z_inf_out : numpy array
            excluded columns having `inf` values, if any.
        z_thrsh_df : Pandas DataFrame
            method used and capping thresholds per feature
        feature_names_in_: numpy array
            Feature names in.
        n_features_in_: numpy array
            Number of feature in

        """
        # Input checks
        t_ = ['both', 'right', 'left']
        m_ = ['gaus', 'iqr', 'mad', 'q']
        self._labels = labels

        X = self._array_to_df(X, labels = self._labels) # confirm input data is a DataFrame

        if self.cols is not None:
            if not isinstance(self.cols, (list, tuple, np.ndarray, pd.Index)):
                raise TypeError("'cols' parameter accepts a sequence e.g: Lists, Tuples, NumPy Arrays or Pandas Base Index. "
                                f"However, '{type(self.cols)}' was received!")
            # if `cols` passed with errors force to none, this trigger transforming all numeric columns
            if np.any(~np.isin(self.cols, X.columns)) or np.any([X[col].dtype.kind not in 'ifc' for col in self.cols]):
                    _z_log.info("Missing and/or None Numeric columns. `cols` parameter will be ignored")
                    self.cols = None
        
        if self.mapping is not None and len(self.mapping): # len to account for {} if multiple `fit` calls on single instance
            if not isinstance(self.mapping, dict):
                raise TypeError("please pass 'mapping' parameter as dictionary where "
                                "keys are column names and values are tuples ('method', distance)")
            dvs = list(self.mapping.values())
            if (np.array([type(v) for v in dvs]) != tuple).any() or (np.array([len(v) for v in dvs]) != 2).any():
                raise TypeError("'mapping' values must be tuples of ('method', distance)")
            if np.any(~np.isin(np.array(dvs)[:,0], m_)):
                raise ValueError("all 'method' values in 'mapping' parameter must be "
                                 f"one of the following arguments: {m_}.")
            qs = np.array([v[1] for v in dvs if 'q' in v])
            if any(qs.ravel().astype(float) > 0.2):
                raise ValueError("Invalid Mapping. Only acceptable distance values are between 0 and 0.2 " 
                                 "when using 'q' method.")
            maped_cols = list(self.mapping)
            if np.any(~np.isin(maped_cols, X.columns)) or np.any([X[col].dtype.kind not in 'ifc' for col in maped_cols]):
                _z_log.info("Missing and/or None Numeric columns. `mapping` parameter will be ignored")
                self.mapping = {}
        else:
            self.mapping = {} # ensure empty dict for merging latter

        if self.method not in m_:
            raise ValueError("'method' parameter must be one of the following arguments: "
                             f"{m_}, however, '{self.method}' was received!")
        if self.distance is not None:
            if self.distance <= 0:
                raise ValueError('distance takes only positive numbers')
            if self.method == 'q' and self.distance > 0.2:
                raise ValueError("Only acceptable distance values are between 0 and 0.2 " 
                                 "when using 'q' method.")
        if self.tail not in t_:
            raise ValueError("'tail' parameter must be one of the following arguments: " 
                             f"{t_}, however, '{self.tail}' was received!")
        if self._from_array or self.cols is None: # select all numeric columns, covers if forced to None or original is ndarray 
            self.cols = X.select_dtypes('number').columns
        
        all_cols = np.array(list(set(np.r_[self.cols, list(self.mapping)]))) # merge all, assuming different columns
        inf_mask = np.isinf(X[all_cols]).any()
        if inf_mask.any():
            self.z_inf_out_ = all_cols[inf_mask] # attributes
            _z_log.info("Some columns contain 'inf' values and will be excluded.")
            # update both inputs
            self.cols = np.array(self.cols)[~np.isin(self.cols, self.z_inf_out_)]
            self.mapping = {col: self.mapping[col] for col in self.mapping if col not in self.z_inf_out_}
        if X[all_cols].isnull().any().any():
            _z_log.info("Some columns contain `null` values, these values will be ignored.")

        # prepare for iterations
        # default distance to label outliers
        param_dict = {'gaus': 3, 'iqr': 1.5, 'mad': 1, 'q': .05}

        # override defaults distance, if any
        if self.distance:
            param_dict[self.method] = self.distance

        # prepare for iteration
        # if different columns mapped they will be merged
        # if same they will be overwritten
        # if no mapping it will be ignored
        self._m_d_map = {col: (self.method, param_dict[self.method]) for col in self.cols} | self.mapping
    
        for col in tqdm(self._m_d_map, desc = f'Spotting Outliers....', disable = self.hide_p_bar):

            # method and distance for each column
            m, dist = self._m_d_map[col][0], self._m_d_map[col][1]

            if m == 'gaus':
                # ddof = 0 divides by N instead of N-1
                col_mean, col_std = X[col].mean(), X[col].std(ddof = 0)
                thresh_min = col_mean - (dist * col_std)
                thresh_max = col_mean + (dist * col_std)
            
            elif m == 'iqr':
                q1, q3 = X[col].quantile(0.25), X[col].quantile(0.75)
                thresh_min = q1 - dist * (q3 - q1)
                thresh_max = q3 + dist * (q3 - q1)
                
            elif m == 'mad':
                col_median = X[col].median()
                mad = (X[col] - col_median).abs().median()

                thresh_min = col_median - (dist * mad)
                thresh_max = col_median + (dist * mad)
                
            elif m == 'q':
                thresh_min, thresh_max = X[col].quantile(dist), X[col].quantile(1 - dist)
            
            # update mapping with boundaries
            self._m_d_map[col] = self._m_d_map[col] + (thresh_min, thresh_max)
            
        # attributes
        self.z_thrsh_df_ = pd.DataFrame(self._m_d_map, index = ('method', 'distance', 'lower', 'upper')) 

        # for `transform` input validation
        # using final feature set after
        # removing invalid inputs, if any
        self.feature_names_in_ = self.z_thrsh_df_.columns
        self.n_features_in_ = self.z_thrsh_df_.shape[1]

        if disp_res:  
            display(self.z_thrsh_df_)
                
        return self
              

    def transform(self,
                  X: pd.DataFrame,
                  mark: bool = False) -> pd.DataFrame:
        """
        Cap outliers.
        
        Parameters
        ----------
        X: np.ndarray or pd.DataFrame
            data to transform, Ndarray will be converted to a DataFrame with 
            generic column names.
        mark: Bool
            whether to flag the capped outliers or not. If `True`, a new binary
            column is added to the dataframe flagging outlier observations

        Attributes
        ----------
        z_olrs: dict
            outlier data points index per feature
        z_unique_olrs_idx: dict,
            unique outlier index across all features

        Returns
        -------
        df_clean : Pandas DataFrame
            transformed features after capping outliers

        """

        # check if fit
        try:
            self.z_thrsh_df_
        except:
            raise AttributeError('Please fit training data first!')

        # Input check
        X = self._array_to_df(X, labels = self._labels)
    
        if np.any(~np.isin(self.z_thrsh_df_.columns, X.columns)):
            raise KeyError("Missing columns! Please ensure that the DataFrame includes all columns to transform")
            
        self.z_olrs_ = {} # outlier index container, column wise
        wins_cols = {} # new columns container
        X_clean = X.copy()
        
        for col in tqdm(self.z_thrsh_df_.columns, desc = f'Capping Outliers....', disable = self.hide_p_bar):
            
            thresh_min, thresh_max = self.z_thrsh_df_[col].lower, self.z_thrsh_df_[col].upper
            
            # handle outliers
            if self.tail == 'both':
                olrs_idx = X_clean[(X_clean[col] < thresh_min) | 
                                   (X_clean[col] > thresh_max)].index
                # winsorize
                if any(olrs_idx):
                    wins_cols[f'{col}_b_winso'] = X_clean[col].clip(lower = thresh_min, upper = thresh_max)
                    self.z_olrs_[col] = olrs_idx
            
            elif self.tail == 'right':
                olrs_idx = X_clean[(X_clean[col] > thresh_max)].index
               
                # winsorize
                if any(olrs_idx):
                    wins_cols[f'{col}_r_winso'] = X_clean[col].clip(upper = thresh_max)
                    self.z_olrs_[col] = olrs_idx
            else:
                olrs_idx = X_clean[(X_clean[col] < thresh_min)].index
                
                # winsorize
                if any(olrs_idx):
                    wins_cols[f'{col}_l_winso'] = X_clean[col].clip(lower = thresh_min)
                    self.z_olrs_[col] = olrs_idx # attributes

        if any(self.z_olrs_):
            # unique outliers indices across all columns
            self.z_unique_olrs_idx_ = sorted(list(set([v for col in self.z_olrs_ for v in self.z_olrs_[col]]))) # attributes

            # add transformed columns to the original dataframe
            X_clean = pd.concat([X_clean, pd.DataFrame(wins_cols)], axis = 1)
            
            if mark:
                X_clean['olyr'] = np.where(np.isin(X_clean.index, self.z_unique_olrs_idx_), 1, 0)
        else:
            _z_log.info("No transformation took place; capping threshold (lower, upper) not breached.")
            
        return X_clean