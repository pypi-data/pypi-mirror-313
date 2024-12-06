#!/usr/bin/env python
# Created by "Thieu" at 22:28, 14/08/2023 ----------%
#       Email: nguyenthieu2102@gmail.com            %                                                    
#       Github: https://github.com/thieu1995        %                         
# --------------------------------------------------%

import numpy as np
from evorbf import get_dataset, MhaRbfRegressor


data = get_dataset("diabetes")
data.split_train_test(test_size=0.2, random_state=2)
print(data.X_train.shape, data.X_test.shape)

data.X_train, scaler_X = data.scale(data.X_train, method="MinMaxScaler", feature_range=(0, 1))
data.X_test = scaler_X.transform(data.X_test)

data.y_train, scaler_y = data.scale(data.y_train, method="MinMaxScaler", feature_range=(0, 1))
data.y_test = scaler_y.transform(np.reshape(data.y_test, (-1, 1)))

opt_paras = {"name": "GA", "epoch": 100, "pop_size": 30}
model = MhaRbfRegressor(hidden_size=10, act_name="elu", obj_name="MSE", optimizer="BaseGA", optimizer_paras=opt_paras)
model.fit(data.X_train, data.y_train)

y_pred = model.predict(data.X_test)

print(model.score(data.X_test, data.y_test, method="RMSE"))
print(model.scores(data.X_test, data.y_test, list_metrics=("RMSE", "R2")))
print(model.evaluate(data.y_test, y_pred, list_metrics=("R2", "MAPE", "NSE")))
