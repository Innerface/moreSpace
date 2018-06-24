# Author: YuYuE (1019303381@qq.com) 2018.06.22
import pandas as pd
import numpy as np
import re
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import KFold
from sklearn import cross_validation
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectKBest, f_classif
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier


def DataPrecondition(file_path='./train.csv'):
    data = pd.read_csv(file_path)
    # 将数据集中所有的样本特征属性打印出来，每一列的相关数据信息
    # 数据预处理， 填充缺失值以及将特征中含有字符的转换为数值型
    # 将年龄这一列的数据缺失值进行填充
    data["Age"] = data["Age"].fillna(data["Age"].median())
    data["Fare"] = data["Fare"].fillna(data["Fare"].median())
    # print(data.describe())
    # 打印这一列特征中的特征值都有哪些
    # print(data["Sex"].unique())
    # 将性别中的男女设置为0 1 值 把机器学习不能处理的自字符值转换成能处理的数值
    # loc定位到哪一行，将titanic['Sex'] == 'male'的样本Sex值改为0
    data.loc[data["Sex"] == "male", "Sex"] = 0
    data.loc[data["Sex"] == "female", "Sex"] = 1
    # print(data["Sex"].unique)
    # print(data["Embarked"].unique())
    # 通过统计三个登船地点人数最多的填充缺失值
    data["Embarked"] = data["Embarked"].fillna("S")
    # 将登船地点同样转换成数值
    data.loc[data["Embarked"] == "S", "Embarked"] = 0
    data.loc[data["Embarked"] == "C", "Embarked"] = 1
    data.loc[data["Embarked"] == "Q", "Embarked"] = 2
    # 提取的第一个特征
    data["FamilySize"] = data["SibSp"] + data["Parch"]
    # 提取的第二个特征 根据名字长度
    data["NameLength"] = data["Name"].apply(lambda x: len(x))
    return data


def FieldSearch(data):
    field_search = re.search(' ([A-Za-z]+)\.', data)
    if field_search:
        return field_search.group(1)
    return ""


def TransferIntoDigital(data, new_field, field='Name'):
    fields = data[field].apply(FieldSearch)
    # transfer name to digit
    name_map = {"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Dr": 5, "Rev": 6, "Major": 7, "Col": 7, "Mlle": 8,
                "Mme": 8, "Don": 9, "Lady": 10, "Countess": 10, "Jonkheer": 10, "Sir": 9, "Capt": 7, "Ms": 2
                }
    for i, title in enumerate(fields):
        for k, v in name_map.items():
            if title == k:
                fields[i] = v
    data[new_field] = fields
    return data


def LinearRegressionTrain(data, predictors=None, target_field='Survived'):
    if predictors is None:
        # 人为的先选取部分有用特征
        predictors = ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked"]
    # 将线性回归方法导进来
    alg = LinearRegression()
    # 将m个样本分成三份 n_folds 代表的是交叉验证划分几层（几份）
    kf = KFold(data.shape[0], n_folds=3, random_state=1)  # 该行代码做的是交叉验证
    predictions = []
    for train, test in kf:
        # 将训练数据拿出来，对原始数据取到建立好的特征 然后取出用于训练的那一部分
        train_predictors = (data[predictors].iloc[train, :])
        # 获取到数据集中交叉分类好的标签，即是否活了下来
        train_target = data[target_field].iloc[train]
        # 将数据放进去做训练
        alg.fit(train_predictors, train_target)
        # 训练完后，使用测试集进行测试误差
        test_predictions = alg.predict(data[predictors].iloc[test, :])
        predictions.append(test_predictions)
    # 使用线性回归得到的结果是在区间[0,1]上的某个值，需要将该值转换成0或1
    predictions = np.concatenate(predictions, axis=0)
    predictions[predictions > .5] = 1
    predictions[predictions <= .5] = 0
    predictions.dtype = "float64"
    data[target_field] = data[target_field].astype(float)
    test_total = len(predictions)
    correction_count = sum(predictions == data[target_field])
    accuracy = correction_count / test_total
    return accuracy


def LogisticRegressionTrain(data, predictors=None, target_field='Survived'):
    if predictors is None:
        # 人为的先选取部分有用特征
        predictors = ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked"]
    alg = LogisticRegression(random_state=1)
    # 使用逻辑回归做交叉验证
    score = cross_validation.cross_val_score(alg, data[predictors], data[target_field], cv=3)
    return score.mean()


def FeatureSelect(data, predictors=None, target_field='Survived', num=5):
    feature_selected = []
    if predictors is None:
        predictors = ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked", "FamilySize", "Title", "NameLength"]
    selector = SelectKBest(f_classif, k=5)
    selector.fit(titanic[predictors], data[target_field])
    scores = -np.log10(selector.pvalues_)
    # plt.bar(range(len(predictors)), scores)
    # plt.xticks(range(len(predictors)), predictors, rotation="vertical")
    # plt.show()
    feature = dict(zip(predictors, scores))
    feature = sorted(feature.items(), key=lambda item: item[1], reverse=True)
    feature = feature[:num]
    for predictor, _ in feature:
        feature_selected.append(predictor)
    return feature_selected


def RandomForestClassifierTrain(data, predictors=None, target_field='Survived', n_folds=3):
    alg = RandomForestClassifier(random_state=1, n_estimators=50, min_samples_split=8, min_samples_leaf=4)
    kf = cross_validation.KFold(data.shape[0], n_folds=n_folds, random_state=1)
    scores = cross_validation.cross_val_score(alg, data[predictors], data[target_field], cv=kf)
    return scores.mean()


def GradientBoostingClassifierTrain(data, predictors=None, target_field='Survived'):
    if predictors is None:
        predictors = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked', 'FamilySize', 'NameLength', 'Title']
    algorithms = [
        [GradientBoostingClassifier(random_state=1, n_estimators=50, max_depth=6),
         predictors],
        [LogisticRegression(random_state=1),
         predictors]
    ]
    kf = KFold(data.shape[0], n_folds=3, random_state=1)
    predictions = []
    for train, test in kf:
        train_target = data[target_field].iloc[train]
        full_test_predictions = []
        for alg, predictors in algorithms:
            alg.fit(data[predictors].iloc[train, :], train_target)
            test_prediction = alg.predict_proba(data[predictors].iloc[test, :].astype(float))[:, 1]
            # print(test_prediction)
            full_test_predictions.append(test_prediction)
        # print(full_test_predictions)
        test_predictions = (full_test_predictions[0] + full_test_predictions[1]) / 2
        test_predictions[test_predictions > .5] = 1
        test_predictions[test_predictions <= .5] = 0
        predictions.append(test_predictions)
    predictions = np.concatenate(predictions, axis=0)
    accury = sum(predictions == data[target_field]) / len(predictions)  # 测试准确率
    return accury


def GenerateSubmission(data, predictions):
    data["Survived"] = predictions
    predictors = ["PassengerId", "Survived"]
    df = pd.DataFrame(data=data[predictors], columns=["PassengerId", "Survived"])
    df.to_csv('./submission_v3.csv', index=False)


if __name__ == "__main__":
    titanic = DataPrecondition('./titanic/train.csv')
    titanic = TransferIntoDigital(titanic, 'Title', 'Name')
    result = LinearRegressionTrain(titanic)
    print(result)
    result = LogisticRegressionTrain(titanic)
    print(result)
    predictors_ = FeatureSelect(titanic)
    print(predictors_)
    result = RandomForestClassifierTrain(titanic, predictors_)
    print(result)
    result = GradientBoostingClassifierTrain(titanic)
    print(result)
