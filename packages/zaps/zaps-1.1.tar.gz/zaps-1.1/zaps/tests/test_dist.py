import numpy as np
import logging
from pytest import mark, raises, num_cols
from zaps.eda import Dist

# adjust logging, default level is INFO
logger = logging.getLogger('[zaps]')
logger.setLevel(logging.WARNING)

#####################################################
# ALL plots are visually tested in Jupyter Notebook #
#####################################################

@mark.parametrize(
    "params, fit_params, err_msg",
    [
        ({"cols": num_cols, "target": ['']}, {},
            "please pass 'target' column name as string"),
        ({"cols": num_cols, "target": 'feat_0'}, {},
            "Missing columns! Please ensure that all columns to analyze are included in the DataFrame"),
        ({"cols": num_cols}, {"cols": {}},
            "'cols' parameter accepts a sequence, e.g: Lists, Tuples, NumPy Arrays or Pandas Base Index. "
            "However, '<class 'dict'>' was received!"),
        ({"cols": num_cols}, {"cols": ['feat_5', 'feat_6']},
            "please only use columns having numeric data type"),
        ({"cols": num_cols}, {"stats": 'rss'},
            "'stats' parameter must be one of the following arguments: 'RSS', 'wasserstein', 'ks', or 'energy', "
            "however, 'rss' was received!"),
        ({"cols": num_cols[1:2]}, {},
            r"All columns have null\(missing\) values, can't fit!")
    ],
)
def test_init_params_validation(X, params, fit_params, err_msg):
    """Test that correct errors for invalid inputs are raised"""

    with raises((TypeError, ValueError, KeyError), match = err_msg):
        Dist(X, **params, hide_p_bar = True).best_fit(**fit_params)


@mark.parametrize(
    "params, fit_params, log_tuples",
    [
        ({"cols": ["feat_2", "feat_3"]}, {"distr" : ['expon']},
            [("[zaps]", logging.INFO, "1 out of 2 columns having null values will not be analyzed")]
            ),
    ],
)
def test_logging(X, params, fit_params, log_tuples, caplog):
    """Test that correct logs are captured at correct level"""

    # setup
    caplog.set_level(logging.DEBUG, logger = '[zaps]')

    # fit
    Dist(X, **params, hide_p_bar = True).best_fit(**fit_params)

    # test
    assert np.all(np.isin(log_tuples, caplog.record_tuples))