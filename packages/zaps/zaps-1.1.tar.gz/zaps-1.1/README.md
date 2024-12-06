<picture align="center">
<img alt="zaps Logo"  src="https://drive.google.com/uc?id=1QxZ0ZEadn1_1HNItsOTN6kqILWQbsLP0">
</picture>

-----------------

# ZAPS: Pythonic Exploratory Data Analysis Framework

ZAPS is a lightweight, low-code Python wrapper designed to simplify and accelerate the exploratory data analysis (EDA) process. Built on top of industry-standard libraries, it provides an intuitive and efficient framework for data inspection, visualization, and preparation. 

With ZAPS, you can quickly and easily perform a wide range of EDA tasks, without the need for complex code or extensive programming expertise; allowing you to focus on insights and decision-making rather than tedious data manipulation, all for unlocking deeper understanding and actionable insights from your data.

[![!python-versions](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11-blue)](https://pypi.org/project/zaps/)
[![Pypi](https://img.shields.io/pypi/v/zaps)](https://pypi.org/project/zaps/)
[![License](https://img.shields.io/badge/license-MIT-green.svg?color=orange)](https://github.com/AmMoPy/zaps/blob/main/LICENSE.txt)
[![Documentation Status](https://readthedocs.org/projects/zaps/badge/?version=stable)](https://zaps.readthedocs.io/)

[![zaps_demo](https://drive.google.com/uc?id=1l6G9bmOe663uvV54bNxBAi54XaoI2lhT)](https://youtu.be/XIAk670WAWM)

## Table of Contents

- [Main Features](#main-features)
- [Installation](#installation)
- [Dependencies](#dependencies)
- [Quickstart](#quickstart)
- [Tutorials](#tutorials)
- [License](#license)
- [API Documentation](#api-documentation)
- [Contributing to ZAPS](#contributing-to-zaps)

## Main Features

- Combined capabilities of multiple modules in a concise single interface
- Highlighting potential underlying problems and summarizing input data
- Rich tabular reports and highly customizable interactive visualizations
- Statistical modeling with commonly used algorithms and metrics
- Flexible alternation between numeric and categorical data
- User friendly error handling and informative workflow 
- Easy integration with Scikit-learn Pipeline

## Installation

ZAPS is tested and supported on 64-bit systems with:

- Python 3.9 or latter
- Debian 12
- Windows 8.1 or later

You can install ZAPS with Python's pip package manager:

```python
# install zaps
pip install zaps
```

## Dependencies

- [Numpy](https://numpy.org)
- [Pandas](https://pandas.pydata.org)
- [Seaborn](https://seaborn.pydata.org)
- [Matplotlib](https://matplotlib.org)
- [Plotly](https://plotly.com)
- [Statsmodels](https://www.statsmodels.org)
- [Scipy](https://scipy.org)
- [Scikit-learn](https://scikit-learn.org)
- [Distfit](https://erdogant.github.io/distfit)

## Quickstart

#### Analysing and highlighting data problems

```python
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
```

#### Visualizing distributions

```python
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
```

#### Identifying and handling outliers

```python
# outliers: identifying and capping using different methods
lrs = Olrs(num_cols,
		   mapping = {'column_name': ('iqr', 1.5)},
		   method = 'q',
           hide_p_bar = True
           )

trans_df = lrs.fit_transform(df)
```

#### Numeric features analysis

```python
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
```

#### Categorical features analysis

```python
# categorical analysis - cats vs num
c_a = CatAna(df, cat_cols, 'numeric_target_column_name', hide_p_bar = True)

# ANOVA with assumptions and mutual info scores
anova = c_a.ana_owva()

# Post-hoc displaying groups that could be merged
post_hoc = c_a.ana_post(multi_tst_corrc = 'bonf')
```

```python
# categorical analysis - cats vs cat
c_a = CatAna(df, cat_cols, 'categorical_target_column_name', hide_p_bar = True)

# chi2 test of independence
chi2 = c_a.ana_chi2()
```

#### Preprocessing Pipeline

```python
# sklearn pipline integration
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline

# setup
feats = ['column_name1', 'column_name2']

lrs = Olrs(cols = feats, hide_p_bar = True)
poly = PolynomialFeatures(interaction_only = True, include_bias = False).set_output(transform = "pandas")

# pipline
pl = Pipeline([
    ('pf', poly),
    ('olrs', lrs),
    ])
    
pl.fit_transform(df[feats])
```

## Tutorials

[ZAPS in Colab](https://colab.research.google.com/drive/1TWAz1kTRLatXOr1MWVf_oMEdnMXJFNoM?usp=sharing)

## License

[MIT](LICENSE.txt)

## API Documentation

The official documentation is hosted at [Read The Docs](https://zaps.readthedocs.io/).

## Contributing to ZAPS

All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.

-----------------

[TOC](#table-of-contents)