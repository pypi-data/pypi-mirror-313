import numpy as np
import logging
from pytest import mark, raises
from zaps.eda import UniStat

# adjust logging, default level is INFO
logger = logging.getLogger('[zaps]')
logger.setLevel(logging.WARNING)

#####################################################
# ALL plots are visually tested in Jupyter Notebook #
#####################################################

@mark.parametrize(
    "params, plot_params, err_msg",
    [
        ({"col_drop" : ""}, {},
            "'col_drop' parameter accepts a sequence e.g: Lists, Tuples, NumPy Arrays or Pandas Base Index. "
            "However, '<class 'str'>' was received!"),
        ({"col_drop" : ["t"]}, {},
            "Missing columns! Please ensure that column name passed to 'col_drop' parameter "
                               "is included in the DataFrame"),
        ({"card_thresh" : -1}, {},
            r"cardinality and/or rare threshold\(s\) can't be less than 0"),
        ({}, {"cols" : ""},
            "'cols' parameter accepts a sequence e.g: Lists, Tuples, NumPy Arrays or Pandas Base Index. "
            "However, '<class 'str'>' was received!"),
        ({}, {"cols" : ["t"]},
            "Missing columns! Please ensure that all columns to plot are included in the DataFrame"),
        ({}, {"cols" : ["feat_6"]},
            r"Only numeric feature\(s\) are accepted"),
    ],
)
def test_init_and_corr_params_validation(X, params, plot_params, err_msg):
    """Test that correct errors for invalid inputs are raised"""

    with raises((TypeError, ValueError, KeyError), match = err_msg):
        UniStat(X, **params).skew_plot(**plot_params)


def test_peek_output(X):
    """ Test that correct results are generated """
    
    # setup
    rare_thresh, skw_thresh = 0.05, 1
    X['multi_cat_none'] = np.random.choice(['g', 'h', None], p = [.1, .4, .5], size = len(X)) # to test if NaNs categorized

    # fit
    u_s = UniStat(df = X, col_drop = ['t_1'], rare_thresh = rare_thresh, skw_thresh = skw_thresh, hide_p_bar = True)
    num_feats, cat_feats, dup_df = u_s.peek(disp_res = False)

    # test results
    expected_num_cols = ['feat_2', 't_1']
    expected_cat_cols = ['feat_3', 'feat_4', 'feat_5', 'feat_6', 't_2', 't_3' , 'multi_cat_none']
    expected_hc_col = 'feat_6'
    expected_inf_col = 'feat_1'
    expected_missing_cols = ['feat_2', 'feat_5', 'feat_6', 'multi_cat_none']
    expected_pct_missing = sorted([X[col].isnull().mean().round(4) for col in expected_missing_cols])
    expected_rare_cols = ['feat_4', 'feat_6', 't_3']
    expected_pct_rare = sorted(
        [(X[col].value_counts(dropna = False, normalize = True) < rare_thresh).mean() for col in expected_rare_cols]
        )
    expected_skewed_col = 't_1'

    skewed_cols = u_s.z_univ_stat_df_.columns[u_s.z_univ_stat_df_.loc['skw'].abs() > skw_thresh]

    assert all(np.isin(num_feats, expected_num_cols))
    assert all(np.isin(cat_feats, expected_cat_cols))
    assert u_s.z_hc_data_.index == expected_hc_col
    assert u_s.z_inf_out_ == expected_inf_col
    assert all(np.isin(u_s.z_miss_data_.index, expected_missing_cols))
    assert np.allclose(u_s.z_miss_data_.values.astype(float), expected_pct_missing)
    assert all(np.isin(u_s.z_rare_cat_.index, expected_rare_cols))
    assert np.allclose(u_s.z_rare_cat_.values.astype(float)[:,2], expected_pct_rare)
    assert skewed_cols == expected_skewed_col
    assert u_s.z_univ_stat_df_.loc['top', 'multi_cat_none'] == 'missing'