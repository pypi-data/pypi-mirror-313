import pytest
import numpy as np
import pandas as pd
import string
from scipy import stats

################################################

@pytest.fixture
def X():
   """
   Generic regression and classification data
   """ 
   np.random.seed(45)

   df = pd.DataFrame({
      'feat_1': np.r_[stats.norm.rvs(size = 299), np.inf], # normal
      'feat_2': np.r_[stats.uniform.rvs(size = 299), np.nan], # uniform
      'feat_3': stats.binom.rvs(n = 1, p = .2, size = 300), # discat
      'feat_4': stats.binom.rvs(n = 8, p = .3, size = 300), # multicat + rare
      'feat_5': np.random.choice(['a', 'b', 'c', None], p = [.4, .3, .2, .1], size = 300), # low card cat + missing
      'feat_6': np.random.choice(list(string.ascii_lowercase)[:25] + [None], size = 300), # high card cat + rare + missing
      't_1': stats.lognorm.rvs(size = 300, s = 1, random_state = 40), # skewed regression target
      't_2': stats.binom.rvs(n = 1, p = .3, size = 300, random_state = 40), # binary classification
      't_3': stats.binom.rvs(n = 4, p = .4, size = 300, random_state = 40), # Multiclass classification
      }
   )
   return df


@pytest.fixture
def X_():
   """
   Generic data for testing some warnings
   """ 
   X_ = pd.DataFrame(np.array([[1,2,0], [3,4,1], [5,6,2]]), columns = ['a', 'b', 'c'])
   
   return X_


# shared testing params
def pytest_configure():
   pytest.cols = ['feat_1', 'feat_2', 'feat_3', 'feat_4', 'feat_5', 'feat_6', 't_1', 't_2', 't_3']
   pytest.cat_cols = ['feat_3','feat_4','feat_5','feat_6']
   pytest.num_cols = ['feat_1','feat_2']
   pytest.cont_tar = 't_1'
   pytest.binary_tar = 't_2'
   pytest.multi_tar = 't_3'