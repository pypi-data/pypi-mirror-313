import numpy as np
import logging
from pytest import mark, raises, num_cols, cat_cols, cont_tar, binary_tar
from zaps.eda import NumAna

# adjust logging, default level is INFO
logger = logging.getLogger('[zaps]')
logger.setLevel(logging.WARNING)

#####################################################
# ALL plots are visually tested in Jupyter Notebook #
#####################################################

@mark.parametrize(
    "params, err_msg",
    [
        ({"cols": "", "target": cont_tar},
            "cols' parameter accepts a sequence e.g: Lists, Tuples, NumPy Arrays or Pandas Base Index. "
            "However, '<class 'str'>' was received!"),
        ({"cols": num_cols, "target": []}, 
            "Please pass target column name as string"),
        ({"cols": cat_cols, "target": cont_tar},
            "All 'cols' must be numeric please refer to parameter description"),
        ({"cols": num_cols, "target": cont_tar, "fit": "ol"},
            "'fit' parameter accepts the following arguments: 'ols', 'logit' or 'lws', however, 'ol' was received!"),
        ({"cols": num_cols, "target": cont_tar, "nans_d": [1, 2]}, 
            "Please pass 'nans_d' parameter as a dictionary. Example: {'column name': imputation value}"),
        ({"cols": num_cols, "target": cont_tar, "nans_d": {"feat_0": 1}}, 
            "Missing columns! Please ensure that all columns to impute are included in the DataFrame"),
        ({"cols": [num_cols[0]], "target": cont_tar}, 
            "No feature to analyze! Please ensure that input columns are valid"),
        ({"cols": num_cols, "target": cont_tar}, 
            "'disp_corr' parameter must be one of the following arguments: 'pearson' or 'spearman', however, 'pear' was received!"),
    ],
)
def test_init_and_corr_params_validation(X, params, err_msg):
    """Test that correct errors for invalid inputs are raised"""

    with raises((TypeError, ValueError, AttributeError, KeyError), match = err_msg):
        NumAna(X, **params).corr(disp_corr = 'pear')


def test_corr_output_and_logging(X, caplog):
    """
    Test that correct results are generated and 
    correct logs are captured at correct level
    """
    
    # setup
    caplog.set_level(logging.DEBUG, logger = '[zaps]')
    alpha, thresh, q, disp_corr = 0.05, 0.1, 0.25, 'spearman'

    # fit
    n_a = NumAna(X, ['feat_2', 'feat_3', 'feat_4'], cont_tar)
    corr_mtrx, feat_corr_mtrx = n_a.corr(disp_corr = disp_corr, quant = q, 
                                         thresh = thresh, plot = True, alpha = alpha)

    # test results
    quant = corr_mtrx.T[disp_corr].abs().quantile(q)
    expected_top_feats = corr_mtrx.T.index[corr_mtrx.T[disp_corr] >= quant]
    expected_sorting = ['feat_3','feat_4','feat_2']

    assert all(corr_mtrx.columns == expected_sorting) # sorting
    assert not np.any(corr_mtrx.iloc[[1,3]].values <= alpha) # significance with target
    assert np.all(feat_corr_mtrx.columns == expected_top_feats) # selection of top corr
    assert feat_corr_mtrx[abs(feat_corr_mtrx) >= thresh].isna().sum().sum() == len(feat_corr_mtrx) # significance among top

    # test logging
    log_tuples =[ 
             ("[zaps]", logging.INFO, "No Significant Correlation Was Noted!"),
             ("[zaps]", logging.INFO, r"No high correlation among top 75% features that are highly correlated with `target`")]
    
    assert np.all(np.isin(log_tuples, caplog.record_tuples))


@mark.parametrize(
    "params, log_tuples",
    [
        ({"cols": ['feat_3', 'feat_4'], "target": binary_tar}, 
            [("[zaps]", logging.INFO, "logistic fit will be applied")]
            ),
        ({"cols": ['feat_2'], "target": "feat_5", "degree": 2, "fit": "ols"}, # test categorical target transformed, fit ignored
            [("[zaps]", logging.INFO, "Polynomial Least Squares fit will be applied")]
            ),
        ({"cols": ['feat_3'], "target": cont_tar, "nans_d": {'feat_2': .5}},
            [("[zaps]", logging.INFO, "No imputation took place as no columns having missing values were found!"),
             ("[zaps]", logging.INFO, "Ordinary Least Squares fit will be applied")]
            ),
        ({"cols": ['feat_3'], "target": cont_tar, "fit": "logit"},
            [("[zaps]", logging.INFO, "Logistic fit will not be applied rather OLS instead! `t_1` is of high cardinality.")]
            ),
        ({"cols": ['feat_3'], "target": binary_tar, "fit": "ols"},
            [("[zaps]", logging.WARNING, "OLS fit will be applied on `t_2` that appears to be categorical.")]
            ),
    ],
)
def test_fit_models_and_generic_logging(X, params, log_tuples, caplog):
    """
    Test the following:
        - Correct logs are captured at correct level
        - Models are fitted and assigned to designated attribute
    """

    # setup
    caplog.set_level(logging.DEBUG, logger = '[zaps]')

    # fit
    n_a = NumAna(X, **params).fit_models()

    # test
    assert np.any(n_a.z_fit_results_[params["cols"][0]])
    assert np.all(np.isin(log_tuples, caplog.record_tuples))