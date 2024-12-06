Quickstart
==========


Analysing and highlighting data problems
----------------------------------------

.. code-block:: python

   import pandas as pd
   from zaps.eda import UniStat, Dist, Olrs, NumAna, CatAna

   # loading sample dataset
   df = pd.read_csv('...')

   # univariate stats - highlighting skewed numeric features and rare categories and  
   u_s = UniStat(df)

   num_cols, cat_cols, dup_df = u_s.peek()

   # visualizing data problems
   u_s.stats_plot()

   # skewed features goodness of fit: Normal distribution
   u_s.skew_plot()


Visualizing distributions
-------------------------

.. code-block:: python

   # plotting numeric distributions with no user input
   dsts = Dist(df = df, cols = num_cols, silent = True)

   # Histograms iterative plotting 
   dsts.hs()

   # analysing best fitting distribution
   dsts.best_fit(
   		 cols = num_cols,
                 distr = ['norm', 'expon', 'lognorm', 'uniform']
                )

   # visualize best fitting distribution
   dsts.best_vis()


Identifying and handling outliers
---------------------------------

.. code-block:: python

   # outliers: identifying and capping using different methods
   lrs = Olrs(num_cols, 
   	      mapping = {'column_name': ('iqr', 1.5)},
   	      method = 'q',
              hide_p_bar = True
             )

   trans_df = lrs.fit_transform(df)


Numeric features analysis
-------------------------

.. code-block:: python
   
   # numeric analysis - fitting regression models and displaying results
   n_a = NumAna(df, num_cols, 'numeric_target_column_name', 
   		hide_p_bar = True).fit_models()

   # target and feature correlation - with filtered display
   corr_df, feat_corr = n_a.corr(plot = True, thresh = .5)

   # visualizing trend lines and overlaying outliers on a selected subset
   n_a.vis_fit(olrs_mapping = lrs.z_olrs_)

   # assess fit results visually - OLS
   n_a.vis_ols_fit()

   # check fit results
   n_a.z_fit_results_['column_name'].summary()

   # interactive multivariate analysis
   n_a.vis_multi(col = 'column_name1', color = 'column_name2', symbol = 'column_name3', 
   		trendline = 'ols', olrs_idx = lrs.z_olrs_idx_)


Categorical features analysis
-----------------------------

.. code-block:: python
   
   # categorical analysis - cats vs num
   c_a = CatAna(df, cat_cols, 'numeric_target_column_name', hide_p_bar = True)

   # ANOVA with assumptions and mutual info scores
   anova = c_a.ana_owva()

   # Post-hoc displaying groups that could be merged
   post_hoc = c_a.ana_post(multi_tst_corrc = 'bonf')
   

.. code-block:: python
   
   # categorical analysis - cats vs cat
   c_a = CatAna(df, cat_cols, 'categorical_target_column_name', hide_p_bar = True)

   # chi2 test of independence
   chi2 = c_a.ana_chi2()


Preprocessing Pipeline
----------------------

.. code-block:: python

   # sklearn pipline integration
   from sklearn.preprocessing import PolynomialFeatures
   from sklearn.pipeline import Pipeline

   # setup
   feats = ['column_name1', 'column_name2']

   lrs = Olrs(cols = feats, hide_p_bar = True)
   poly = PolynomialFeatures(interaction_only = True, 
   			     include_bias = False).set_output(transform = "pandas")

   # pipline
   pl = Pipeline([
   		  ('pf', poly),
    		  ('olrs', lrs),
    		])
    
   pl.fit_transform(df[feats])
