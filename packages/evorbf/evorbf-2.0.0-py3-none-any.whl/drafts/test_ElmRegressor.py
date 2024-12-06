#!/usr/bin/env python
# Created by "Thieu" at 11:25, 17/08/2023 ----------%                                                                               
#       Email: nguyenthieu2102@gmail.com            %                                                    
#       Github: https://github.com/thieu1995        %                         
# --------------------------------------------------%

import numpy as np
from evorbf import RbfRegressor

np.random.seed(42)


def test_ElmRegressor_class():
    X = np.random.uniform(low=0.0, high=1.0, size=(100, 5))
    noise = np.random.normal(loc=0.0, scale=0.1, size=(100, 5))
    y = 2 * X + 1 + noise

    model = RbfRegressor(hidden_size=10, act_name="elu")
    model.fit(X, y)

    pred = model.predict(X)
    assert RbfRegressor.SUPPORTED_REG_METRICS == model.SUPPORTED_REG_METRICS
    assert len(pred) == X.shape[0]
