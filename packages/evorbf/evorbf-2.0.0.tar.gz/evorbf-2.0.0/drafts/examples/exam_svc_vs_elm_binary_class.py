#!/usr/bin/env python
# Created by "Thieu" at 22:32, 16/08/2023 ----------%                                                                               
#       Email: nguyenthieu2102@gmail.com            %                                                    
#       Github: https://github.com/thieu1995        %                         
# --------------------------------------------------%

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC
from permetrics import ClassificationMetric
from evorbf import MhaRbfClassifier


X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

ss_train = StandardScaler()
X_train = ss_train.fit_transform(X_train)
X_test = ss_train.transform(X_test)

# Support Vector Machines
model = LinearSVC()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
cm = ClassificationMetric(y_test, y_pred)
print("Results of LinearSVC on Breast Cancer dataset!")
print(cm.get_metrics_by_list_names(["AS", "RS", "PS", "F1S"]))

###################################################################################################

opt_paras = {"name": "GA", "epoch": 100, "pop_size": 30}
model = MhaRbfClassifier(hidden_size=10, act_name="elu", obj_name="BSL", optimizer="BaseGA", optimizer_paras=opt_paras, verbose=False)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
cm = ClassificationMetric(y_test, y_pred)
print("Results of MhaRbfClassifier on Breast Cancer dataset!")
print(cm.get_metrics_by_list_names(["AS", "RS", "PS", "F1S"]))

print("Try my AS metric with score function")
print(model.score(X_test, y_test, method="AS"))

print("Try my multiple metrics with scores function")
print(model.scores(X_test, y_test, list_metrics=["AS", "PS", "F1S", "CEL", "BSL"]))
