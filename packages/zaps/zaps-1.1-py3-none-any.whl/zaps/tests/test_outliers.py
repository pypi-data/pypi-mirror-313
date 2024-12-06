import numpy as np
import logging
from pytest import mark, raises, cols
from zaps.eda import Olrs
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures

# adjust logging, default level is INFO
logger = logging.getLogger('[zaps]')
logger.setLevel(logging.WARNING)

#####################################################

@mark.parametrize(
    "data, params, fit_params, err_msg",
    [
        (None, {"cols": ""}, {},
            "cols' parameter accepts a sequence e.g: Lists, Tuples, NumPy Arrays or Pandas Base Index. "
                       "However, '<class 'str'>' was received!"),
        (None, {"mapping": [1,2]}, {},
            r"please pass 'mapping' parameter as dictionary where keys are column names and values are tuples \('method', distance\)"),
        (None, {"mapping": {"feat_1": ['gaus', 3]}}, {},
            r"'mapping' values must be tuples of \('method', distance\)"),
        (None, {"mapping": {"feat_1": ('gau', 3)}}, {},
            r"all 'method' values in 'mapping' parameter must be one of the following arguments: \['gaus', 'iqr', 'mad', 'q'\]."),
        (None, {"mapping": {"feat_1": ('q', .3)}}, {},
            "Invalid Mapping. Only acceptable distance values are between 0 and 0.2 when using 'q' method."),
        (None, {"method": 'gau'}, {},
            r"'method' parameter must be one of the following arguments: \['gaus', 'iqr', 'mad', 'q'\], however, 'gau' was received!"),
        (None, {"distance": 0}, {},
            "distance takes only positive numbers"),
        (None, {"method": 'q', "distance": .3}, {},
            "Only acceptable distance values are between 0 and 0.2 when using 'q' method."),
        (None, {"tail": 'mid'}, {},
            r"'tail' parameter must be one of the following arguments: \['both', 'right', 'left'\], however, 'mid' was received!"),
        (" ", {}, {},
            "'data' parameter accepts NumPy Arrays or Pandas DataFrame. However, '<class 'str'>' was received!"),
        (None, {}, {"labels": ""},
            "'labels' parameter accepts a List or Pandas Base Index. However, '<class 'str'>' was received!"),
        (None, {}, {"labels": ["feat_0"]},
            "Labels mismatch! expected 9 labels, However, 1 was received."),
    ],
)
def test_init_and_fit_params_validation(data, X, params, fit_params, err_msg):
    """Test that correct errors for invalid inputs are raised during initialization and fitting"""

    X = X if not data else data
    with raises((TypeError, ValueError), match = err_msg):
        Olrs(**params, hide_p_bar = True).fit(X, **fit_params, disp_res = False)


def test_transform_params_validation_and_sklearn_pipeline_integration(X):
    """
    Test the following:
        1 - correct errors are raised for invalid transformation 
        2 - proper integration with Sklearn Pipeline and internal data checks
    """

    # transformers
    lrs = Olrs(hide_p_bar = True)
    poly = PolynomialFeatures(degree = 3)

    # test params
    feats = X.columns[2:4]
    labels_error = [f'f{x}' for x in range(9)]
    labels_pipeline = [f'x{x}' for x in range(1, 11)]

    # test data
    data = poly.fit_transform(X[feats])
    X_ = X.drop(['feat_2'], axis = 1)

    with raises(AttributeError, match = 'Please fit training data first!'):
        lrs.transform(X)

    with raises(KeyError, match = 'Missing columns! Please ensure that the DataFrame includes all columns to transform'):
        lrs.fit(X).transform(X_)

    with raises(ValueError, match = f'Labels mismatch! expected {10} labels, However, {9} was received.'):
        lrs.fit_transform(data, labels = labels_error)

    # Sklearn Pipeline
    # takes in a `DataFrame` and retrun `Ndarray`
    # before `olrs` step.
    pl = Pipeline([
        ('pf', poly),
        ('olrs', Olrs(cols = feats, hide_p_bar = True)),
        ])

    output_df = pl.fit_transform(X[feats], olrs__labels = labels_pipeline)

    # test if `cols` parameter is ignored and
    # internal conversion took place 
    # from `Ndarray` back to `DataFrame`
    # using custom `labels`
    assert pl[-1].z_thrsh_df_.columns.to_list() == labels_pipeline


def test_output(X):
    """Test that correct results and attribute are generated"""

    # different mapping to test all calculations and distance override
    mapping = {'feat_3': ('q', .1), 'feat_4': ('gaus', 3), 't_1': ('mad', 3 * 1.4826), 't_2': ('iqr', 1.5)}

    # fit
    lrs = Olrs(cols, mapping, method = 'iqr', distance = .5, hide_p_bar = True).fit(X, disp_res = False)

    # transform both tails
    test_df = lrs.transform(X, mark = True)

    # for fit tests: calculations, correct mapping, distance override, and feature filtering
    lower = lrs.z_thrsh_df_[lrs.z_thrsh_df_.columns[:-2]].loc['lower'].values.astype(float)
    upper = lrs.z_thrsh_df_[lrs.z_thrsh_df_.columns[:-2]].loc['upper'].values.astype(float)
    numeric_only = X.select_dtypes(['number'])

    # for transform tests: allocation, marking
    t_1_olyrs = test_df[(test_df['t_1'] < -1.652155) | (test_df['t_1'] > 3.614265)]
    t_3_olyrs = test_df[(test_df['t_3'] < 0.5) | (test_df['t_3'] > 2.5)]
    shared_idx = t_1_olyrs.index.isin(t_3_olyrs.index).astype(int).sum()
    unique_idx = list(set(np.r_[t_1_olyrs.index, t_3_olyrs.index]))
    expected_lower = np.array([-0.030, 0.0, -1.519, -1.652])
    expected_upper = np.array([0.996, 1.0, 6.099, 3.614])

    # fit tests
    assert np.allclose(lower, expected_lower, atol = 1e-3)
    assert np.allclose(upper, expected_upper, atol = 1e-3)
    assert 'feat_1' in lrs.z_inf_out_
    assert all(numeric_only.columns[np.isinf(numeric_only).sum() == 0] == lrs.z_thrsh_df_.columns)

    # transform tests
    assert np.allclose(t_1_olyrs[t_1_olyrs.t_1 > 3.614265]['t_1_b_winso'], 3.614265)
    assert all(t_3_olyrs[t_3_olyrs.t_3 < 0.5]['t_3_b_winso'] == 0.5)
    assert all(t_3_olyrs[t_3_olyrs.t_3 > 2.5]['t_3_b_winso'] == 2.5)

    # marking
    assert t_1_olyrs.shape[0] + t_3_olyrs.shape[0] - shared_idx == test_df.olyr.sum()
    assert test_df.iloc[unique_idx].olyr.sum() == test_df.olyr.sum() # no other marking took place but for outliers

    # index attribute
    assert all(lrs.z_olrs_['t_1'] == t_1_olyrs.index)
    assert all(lrs.z_olrs_['t_3'] == t_3_olyrs.index)
    assert lrs.z_unique_olrs_idx_ == unique_idx

    # test different tails
    lower = lrs.z_thrsh_df_.t_3.lower
    upper = lrs.z_thrsh_df_.t_3.upper
    
    # left tail only test
    lrs.tail = 'left'

    test_df = lrs.transform(X, mark = True)
    mask = test_df[test_df['t_3'] < lower] # t_3 has outliers at both ends

    # allocation
    assert all(mask['t_3_l_winso'] == lower)
    assert all(test_df[~test_df.index.isin(mask.index)]['t_3_l_winso'] != upper) # no other allocation took place

    # marking
    assert mask.shape[0] == test_df.olyr.sum() # only t_3 has outlier at this end

    # index attribute
    assert lrs.z_unique_olrs_idx_ == list(lrs.z_olrs_['t_3']) == mask.index.to_list()

    # right tail only test
    lrs.tail = 'right'
    
    test_df = lrs.transform(X, mark = True)
    mask = test_df[test_df['t_3'] > upper]

    # allocation
    assert all(mask['t_3_r_winso'] == upper)
    assert all(test_df[~test_df.index.isin(mask.index)]['t_3_r_winso'] != lower)

    # marking
    assert mask.shape[0] == mask.olyr.sum()

    # index attribute
    assert all(lrs.z_olrs_['t_3'] == mask.index)
    assert lrs.z_unique_olrs_idx_ == test_df[(test_df['t_1'] > 3.614265) | (test_df['t_3'] > 2.5)].index.to_list()


@mark.parametrize(
    "params, log_tuples",
    [
        ({"cols": ['feat_2'], "mapping": {'feat_1': ('gaus', 3)}}, 
            [("[zaps]", logging.INFO, "Some columns contain 'inf' values and will be excluded."),
             ("[zaps]", logging.INFO, "Some columns contain `null` values, these values will be ignored."),
             ("[zaps]", logging.INFO, "No transformation took place; capping threshold (lower, upper) not breached.")]
            ),
        ({"cols": ['feat_0'], "mapping": {'feat_6': ('gaus', 3)}},
            [("[zaps]", logging.INFO, "Missing and/or None Numeric columns. `cols` parameter will be ignored"),
             ("[zaps]", logging.INFO, "Missing and/or None Numeric columns. `mapping` parameter will be ignored")]
            ),
    ],
)
def test_logging(X, params, log_tuples, caplog):
    """Test that correct logs are captured at correct level"""

    # setup
    caplog.set_level(logging.DEBUG, logger = '[zaps]')

    # fit
    Olrs(**params, hide_p_bar = True).fit_transform(X, disp_res = False) # fit_transform to test merging and feature filtering

    # test
    assert np.all(np.isin(log_tuples, caplog.record_tuples))