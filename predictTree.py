#-*- codeing=utf-8 -*-
#@Time:2022/6/15 16:42
#@Author:王钰娜
#@File : predictTree.py
#@Software:PyCharm

import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn import tree
from sklearn.model_selection import train_test_split


#filename='F:\桌面\数据可视化\计卓班  数据可视化技术  大作业\计卓班  数据可视化技术  大作业\电商行业-超市销售数据分析7.0版本\超市销售分析.xls'
filename='超市销售分析.xls'
data = pd.read_excel(io=filename, sheet_name=0, header=0)
# 去空
data.dropna(axis=0, how='any', inplace=True)  # axis=0表示index行  "any"表示这一行或列中只要有元素缺失，就删除这一行或列
to_drop=['行 ID', '订单 ID','订单日期','发货日期', '邮寄方式', '客户 ID', '客户名称', '细分', '城市', '省/自治区', '国家',
                   '产品 ID','类别', '子类别','产品名称','地区','折扣','数量']
data=data.drop(to_drop, axis=1)

'''提取特征和标签数据'''
# 特征features
examX=data['销售额']
# 标签labes
examY=data['利润']

'''建立训练数据和测试数据'''
from sklearn.model_selection import train_test_split

#建立训练数据和测试数据
# 变量依次为：数量数据特征、测试数据特征、训练数据标签、测试数据标签
x_train, x_test, y_train, y_test=train_test_split(examX,examY,train_size=0.25)

# 将训练数据特征x_train转换为2D array XX行*1列
X_train=x_train.values.reshape(-1,1)
# 将测试数据特征x_test 转换为2D array  XX行*1列
X_test=x_test.values.reshape(-1,1)
# 将训练数据特征y_train转换为2D array XX行*1列
Y_train=y_train.values.reshape(-1,1)
# 将测试数据特征y_test 转换为2D array  XX行*1列
Y_test=y_test.values.reshape(-1,1)

#划分成训练集，验证集，验证集，不过这里我们数据量不够大，没必要
#此段代码中，test_size = 0.25,表示把数据集划分为两份，训练集和测试集之比为4:1（二八原则）
#关于train_test_split()，随机划分训练集和测试集的函数，可参考博客：https://blog.csdn.net/qq_38410428/article/details/94054920
#train_x, test_x, train_y, test_y = train_test_split(X_train, Y_train, test_size = 0.25)
#训练决策树
clf = tree.DecisionTreeClassifier(criterion='gini')
model = clf.fit(X_train,y_train.astype('int'))

# #如果划分了，训练集、验证集和测试集，加上此步骤，看训练好的决策树在测试集上的准确率
# res = model.predict(X_test)
# print(res)    #模型结果输出
# print(Y_test)    #实际值
# print((sum(res==Y_test)/len(res)))    #准确率
print("==========================")
score = model.score(X_test,y_test.astype('int'))
print("R²="+str(score))
print("==========================")
predict_value=129.696
A = ([[predict_value]]) #销售额
predict_result = clf.predict(A)
print('销售额为：'+str(predict_value)+' 利润值预测结果：'+str(predict_result))