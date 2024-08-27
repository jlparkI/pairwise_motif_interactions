"""Contains functionality for the basic 5x CV experiment on the GM
cell line data, including functions needed to load the raw data for
fitting."""
import os
import math
import numpy as np

from exactPolynomial import ExactQuadratic
from exactPolynomial import build_online_dataset


def fit_gm_cv(yvalue_fpath, xvalue_fpath, priority_fpath,
              logfile_path):
    """Fits the input data using 5x CV, with NMLL used to select
    the hyperparameters on each cross-validation iteration."""
    yvalues = np.load(yvalue_fpath).flatten()
    xvalues = np.load(xvalue_fpath)
    priorities = np.load(priority_fpath).flatten()

    print(f"Loaded x with shape {xvalues.shape}, y with shape {yvalues.shape}, and "
          f"priorities with shape {priorities.shape}.", flush=True)

    retained_x = np.ascontiguousarray(xvalues[:,priorities[:250]])
    print(f"Shape of x is now {retained_x.shape} after keeping 250 "
          "highest priority motifs.", flush=True)

    rng = np.random.default_rng(123)
    idx = rng.permutation(retained_x.shape[0])
    ctp = math.ceil(idx.shape[0] / 5)

    for i in range(5):
        test_idx = idx[i*ctp:(i+1)*ctp]
        train_idx = np.concatenate([idx[:i*ctp],
                                    idx[(i+1)*ctp:]])
        print(f"On CV split {i}, {train_idx.shape[0]} train datapoints, "
              f"{test_idx.shape[0]} test datapoints.")

        trainx, trainy = retained_x[train_idx,:], yvalues[train_idx]
        testx, testy = retained_x[test_idx,:], yvalues[test_idx]

        cv_model = ExactQuadratic(interactions_only = True,
                                  regularization = "l2", num_threads = 4)
        train_data = build_online_dataset(trainx, trainy)


