#-*- codeing=utf-8 -*-
#@Time:2022/6/15 10:40
#@Author:王钰娜
#@File : predictLine.py
#@Software:PyCharm

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

filename='超市销售分析.xls'
data = pd.read_excel(io=filename, sheet_name=0, header=0)
# 去空
data.dropna(axis=0, how='any', inplace=True)  # axis=0表示index行  "any"表示这一行或列中只要有元素缺失，就删除这一行或列

predict_value=129.696
predict_value = np.array(predict_value).reshape(1, -1)    #转为二维数组

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

#输出各数据大小
# # 特征
# print('原始数据特征:',examX.shape ,
#       '\n训练数据特征：',x_train.shape,
#       '\n测试数据特征： ',x_test.shape )
# # 标签
# print('\n原始数据标签:',examY.shape ,
#       '\n训练数据标签：',y_train.shape,
#       '\n测试数据标签： ',y_test.shape )


'''线性回归'''
'''
Reshape your data either using array.reshape(-1, 1) if your data has a single feature 
or array.reshape(1, -1) if it contains a single sample.
期望的是2D的数组，而x_train和y_train均为Series
如果只有一个特征，需要reshape(-1, 1)；
如果包含一个样本，需要reshape(1, -1)。
'''

# 将训练数据特征x_train转换为2D array XX行*1列
X_train=x_train.values.reshape(-1,1)

# 导入线性回归
from sklearn.linear_model import LinearRegression

# 创建模型：线性回归
model=LinearRegression()

# 训练模型
model.fit(X_train,y_train)

'''
回归函数：y=a+bx
截距intercept: a
回归系数coef : b
'''
a=model.intercept_
b=model.coef_
predict_outcome = model.predict(predict_value)
print("销售额为:"+str(predict_value)+",利润预测值为:"+str(predict_outcome))
print('最佳拟合线的截距：a=',a,'最佳拟合线的回归系数:b=',b)

# 将测试数据特征x_test 转换为2D array  XX行*1列
X_test=x_test.values.reshape(-1,1)

# 返回决定系数R²
print("R²="+str(model.score(X_test,y_test)))

'''绘制训练&测试散点图及最佳拟合线'''

# 1.绘制训练数据散点图
plt.scatter(X_train,y_train,color='b',label='train data')

# 2.绘制最佳拟合线
# 训练数据的预测值
y_train_pred=model.predict(X_train)
# 绘制最佳拟合线
plt.plot(X_train,y_train_pred,color='y',linewidth=2,label='best line')

# 3.绘制测试数据的散点图
plt.scatter(X_test,y_test,color='r',label='test data')

# 4.添加图例和标签
plt.legend(loc=2)
plt.xlabel("销售额")
plt.ylabel("利润")

# 5.显示图像
plt.savefig("销售额-利润线性回归预测",dpi=300)
plt.show()


