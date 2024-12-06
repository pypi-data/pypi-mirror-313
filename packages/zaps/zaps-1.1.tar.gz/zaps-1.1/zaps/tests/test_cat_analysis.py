import numpy as np
import logging
from pytest import mark, raises, num_cols, cat_cols, cont_tar, binary_tar, multi_tar
from zaps.eda import CatAna

# adjust logging, default level is INFO
logger = logging.getLogger('[zaps]')
logger.setLevel(logging.WARNING)

################################################
# Inherited methods are tested at parent class #
################################################

@mark.parametrize(
    "params, err_msg",
    [
        ({"target": cont_tar, "cat_cols": False}, 
            "'t_1' target have significant rare levels! If it is truly categorical, "
            "Consider adjusting 'top_n' and 'rare_thresh' parameters"),
        ({"target": cont_tar, "nans_d": [1, 2]}, 
            "Please pass 'nans_d' parameter as a dictionary. Example: {'column name': imputation value}"),
        ({"target": cont_tar, "nans_d": {"feat_0": 1}}, 
            "Missing columns! Please ensure that all columns to impute are included in the DataFrame"),
    ],
)
def test_additional_init_params_validation(X, params, err_msg):
    """Test that correct errors for invalid initialization inputs are raised"""

    with raises((TypeError, AttributeError, KeyError), match = err_msg):
        CatAna(X, cat_cols, **params)


@mark.parametrize(
    "params, err_msg, log_tuples",
    [
        ({"cols": cat_cols, "target": 'feat_6'},
            "`cols` and `target` are both Categorical, consider using Chi2 test of independence instead", 
            []),
        ({"cols": cat_cols, "target": binary_tar, "cat_cols": False},
            "Some columns are categorical, Please ensure 'cat_cols' parameter is set to 'True'", 
            []),
        ({"cols": num_cols, "target": cont_tar, "cat_cols": False, "rare_thresh": 0},
            "`cols` and `target` are both Numeric, consider using regression and correlation tests instead",
            [("[zaps]", logging.WARNING, "Conditional distributions given 't_1' are analyzed for top 25 frequent "
              "categories while grouping 275 rare lvls. This behavior is controlled by 'rare_thresh' and `top_n` parameters")]
            ),
    ],
)
def test_anova_params_validation_and_partial_logging(X, params, err_msg, log_tuples, caplog):
    """
    Test that correct errors for invalid ANOVA inputs are raised and
    related logs are captured at correct level
    """

    with raises((TypeError), match = err_msg):
        CatAna(X, **params).ana_owva()

    # confirm logging despite failure
    # only for third case to prevent stuffing
    # logging is tested separately anyways with working examples
    try: assert np.all(np.isin(log_tuples, caplog.record_tuples))
    except: raise(AssertionError(f"{log_tuples} not found in caplog.record_tuples"))


def test_cat_num_anova_and_post_hoc_output_with_input_validation(X):
    """
    Test that correct results and attribute are generated and 
    correct errors for invalid PostHoc inputs are raised
    """

    c_a = CatAna(X, cat_cols, cont_tar, rare_thresh = 0.01)

    # ANOVA
    anova_df = c_a.ana_owva()

    # rare and missing grouping
    f_6_mis = X[X.feat_6.isna()].index
    f_6_rar = X[~X.feat_6.isin(c_a.z_freq_lvls_map_)].index

    # ANOVA results
    # `feat_6` provide several test cases 
    lvls = X.feat_6.value_counts(dropna = False)
    results = anova_df.feat_6
    expected_stats = [1.0290, 0.428, 46.653, 0.005, 0.900, 0.114]
    expected_bool = [True, False, True, True]

    assert 'missing' in c_a.z_df_.iloc[f_6_mis]['feat_6'].unique()
    assert 'rare' in c_a.z_df_.iloc[f_6_rar]['feat_6'].unique()
    assert np.allclose([results.f_stat_ANOVA, results.p_val_f, results.h_stat_Kruskal, 
                        results.p_val_h, results.p_val_lev, results.p_val_flg], expected_stats, atol = 1e-03)
    assert [results.eq_mean, results.eq_median, results.eq_var_lev, results.eq_var_flg] == expected_bool
    assert results.max_sample_size == lvls.max()
    assert results.min_sample_size == lvls.min()
    assert results.n_frequent_lvls == len(lvls)
    assert np.isclose(results.m_i_score, 0.03845, atol = 1e-04)

    # Conditional aggregation
    assert all(c_a.zefct_df_[c_a.zefct_df_.feature == 'feat_6'].sort_values('lvl').t_1.values == \
               c_a.z_df_.groupby(['feat_6'])['t_1'].mean().values)

    # Post-Hoc results
    # `feat_5` provide several test cases 
    post_hoc = c_a.ana_post(multi_tst_corrc = 'bonf', disp_res = False)

    phoc_results = post_hoc[post_hoc.feature == 'feat_5']
    expected_t_p_vals = [0.0316, 0.2053, 0.0457, 0.4218, 0.4488, 0.6361]
    expected_adj_t_p_vals = [0.1896, 1, 0.2742, 1, 1, 1]
    expected_mw_stat = [4746, 1732, 3197, 1622, 2939, 1088]
    expected_mw_p_val = [0.2663, 0.3357, 0.668 , 0.9051, 0.6606, 0.7723]

    assert sorted(list(set(np.r_[phoc_results.group_one.unique(), phoc_results.group_two.unique()]))) == \
           sorted(c_a.z_df_.feat_5.unique())
    assert np.allclose(phoc_results['p_val_t'].values, expected_t_p_vals)
    assert np.allclose(phoc_results['adj_p_val_t'].values, expected_adj_t_p_vals)
    assert np.allclose(phoc_results['mw_stat'].values, expected_mw_stat)
    assert np.allclose(phoc_results['p_val_mw'].values, expected_mw_p_val)
    assert not all(phoc_results['reject_t_bonf'])
    assert np.isclose(1 - np.power((1 - 0.05), 1/len(phoc_results)), phoc_results['FWER_Sidak'].iloc[0])
    assert np.isclose(0.05 / len(phoc_results), phoc_results['FWER_Bonf'].iloc[0])
    assert "feat_3" in c_a.xludd_phoc_feats_

    with raises(ValueError, match = "'equal_var' parameter must be one of the following arguments: "
                                    "'levene' or 'fligner' however, 'lev' was received!"):
        c_a.ana_post(equal_var = 'lev', disp_res = False)


def test_num_cat_anova_and_post_hoc_output_with_input_validation(X):
    """Testing additional features and PostHoc error handling while swapping inputs"""
    
    # Using string binary target
    X['t_2_'] = X.t_2.map({0 : 'no', 1 : 'yes'})

    c_a = CatAna(X, num_cols, 't_2_', cat_cols = None, rare_thresh = 0.15, top_n = 25)

    # ANOVA
    anova_df = c_a.ana_owva()

    assert 'feat_1' in c_a.z_inf_out_
    assert 'feat_2' in c_a.z_nans_
    assert anova_df.feat_2.imputed
    assert c_a.z_df_.feat_2.iloc[-1] == X.feat_2.mean()

    # Post-Hoc
    with raises(TypeError, match = "Post Hoc Analysis only applicable for categorical features having more than 2 levels"):
        c_a.ana_post()

    with raises(AttributeError, match = "Please run ANOVA first!"):
        CatAna(X, num_cols, binary_tar).ana_post()


def test_cat_cat_chi2_output(X):
    """Test that correct results and attribute are generated"""

    c_a = CatAna(X, cat_cols, multi_tar)

    # Chi2 results
    # `feat_4` provide several test cases 
    chi_2_df = c_a.ana_chi2()
    expected_stats = [34.645, 0.0738]
    expected_proba = c_a.zefct_df_[c_a.zefct_df_.feature == 'feat_4']['t_3_4'].values
    lbls = np.sort(c_a.z_df_[multi_tar].unique())
    c_a.z_df_['temp'] = np.where(c_a.z_df_[multi_tar].isin(lbls[:-1]), 0, 1) # for reporting last label only
    cond_proba = c_a.z_df_.groupby('feat_4')['temp'].mean().sort_values(ascending = False).values
    print([chi_2_df['feat_4'].chi2, chi_2_df['feat_4'].p_val])
    assert np.allclose([chi_2_df['feat_4'].chi2, chi_2_df['feat_4'].p_val], expected_stats, atol= 1e-03)
    assert (chi_2_df['feat_4'].p_val < 0.05) == chi_2_df['feat_4'].dependent
    assert c_a.z_crss_tabs_['feat_4'].values.min() == chi_2_df['feat_4'].min_sample_size
    assert all(cond_proba == expected_proba)
    assert c_a.zefct_df_['prior'].iloc[0] == c_a.z_df_['temp'].mean()


@mark.filterwarnings("ignore::RuntimeWarning:scipy")
@mark.parametrize(
    "df, params, log_tuples",
    [
        ("X", {"cols": [cont_tar], "target": cont_tar, 'rare_thresh': 0, "top_n": 1}, 
            [("[zaps]", logging.INFO, "Columns are assumed to be Categorical. If not correct, "
              "please manually set 'cat_cols' parameter"),
             ("[zaps]", logging.INFO, "'rare_thresh' and 'top_n' parameters are not properly configured! "
              "All categorical levels will be analysed. 't_1' feature has 300 levels!"),
             ("[zaps]", logging.INFO, "target column 't_1' has been removed from input columns"),
             ("[zaps]", logging.INFO, "no columns to analyze! Please check input columns")]
            ),
        ("X", {"cols": num_cols, "target": binary_tar, "nans_d": None},
            [("[zaps]", logging.INFO, "Columns are assumed to be Numeric. If not correct, please manually set 'cat_cols' parameter"),
             ("[zaps]", logging.DEBUG, "data type of 't_2' changed from 'i' to 'O'"),
             ("[zaps]", logging.INFO, "Some columns contain 'inf' values and will be excluded."),
             ("[zaps]", logging.INFO, "Mean imputation took place for 1 out of 1 columns having missing values")]
            ),
        ("X", {"cols": num_cols, "target": binary_tar, "nans_d": {'feat_2': 1}},
            [("[zaps]", logging.INFO, "Imputation took place for 1 out of 1 columns having missing values")]
            ),
        ("X", {"cols": cat_cols, "target": cont_tar, "rare_thresh": .1},
            [("[zaps]", logging.WARNING, "1 out of 4 Features Will Not Be Analyzed Being Dominated By Rare Levels. "
              "This behavior is controlled by 'rare_thresh' parameter")]
            ),
        ("X_", {"cols": ['a','b'], "target": 'c'},
            [("[zaps]", logging.WARNING, "Check the groups in features having 'inf' and 'nan' results.")]
            )
    ],
)
def test_anova_logging(df, params, log_tuples, caplog, request):
    """Test that correct logs are captured at correct level"""

    # setup
    caplog.set_level(logging.DEBUG, logger = '[zaps]')
    df = request.getfixturevalue(df)
    
    # fit
    CatAna(df, **params).ana_owva()

    # test
    assert np.all(np.isin(log_tuples, caplog.record_tuples))


def test_post_hoc_logging(X, caplog):
    """Test that correct logs are captured at correct level"""

    # setup
    caplog.set_level(logging.INFO, logger = '[zaps]')
    log_tuple = [("[zaps]", logging.INFO, "1 Feature(s) Having Only 2 Frequent Levels Were Excluded From Post Hoc Analysis")]

    # fit
    c_a_ = CatAna(X, cat_cols, cont_tar)
    _ = c_a_.ana_owva()
    __ = c_a_.ana_post(disp_res = False)
    
    # test
    assert np.all(np.isin(log_tuple, caplog.record_tuples))


@mark.parametrize(
    "params, log_tuples",
    [
        ({"cols": cat_cols, "target": cont_tar, "cat_cols": False, "rare_thresh": .001},
            [("[zaps]", logging.INFO, "Chi2 test of independence is best suited for two categorical variables.")]
            ),
        ({"cols": cat_cols, "target": multi_tar, "cat_cols": False},
            [("[zaps]", logging.INFO, "'cat_cols' is set to 'False', rare and missing categorical levels are not preprocessed.")]
            )
    ],
)
def test_chi2_logging(X, params, log_tuples, caplog):
    """Test that correct logs are captured at correct level"""

    # setup
    caplog.set_level(logging.INFO, logger = '[zaps]')

    # fit
    CatAna(X, **params).ana_chi2()

    # test
    assert np.all(np.isin(log_tuples, caplog.record_tuples))