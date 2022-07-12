#-*- codeing=utf-8 -*-
#@Time:2022/6/15 10:23
#@Author:王钰娜
#@File : predictTest.py
#@Software:PyCharm

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import datasets,linear_model

def get_data(filename):
    data = pd.read_excel(io=filename, sheet_name=0, header=0)
    # 去空
    data.dropna(axis=0, how='any', inplace=True)  # axis=0表示index行  "any"表示这一行或列中只要有元素缺失，就删除这一行或列

    x_parameter=[]
    y_parameter=[]
    for single_square_feet,single_price_value in zip(data['销售额'],data['利润']):
        x_parameter.append([float(single_square_feet)])
        y_parameter.append(float(single_price_value))
    return x_parameter,y_parameter

def linear_model_main(x_parameter,y_parameter,predict_value):
    regr = linear_model.LinearRegression()
    regr.fit(x_parameter,y_parameter)
    predict_outcome = regr.predict(predict_value)
    predictions={}
    predictions['intercept']=regr.intercept_
    predictions['coefficient']=regr.coef_
    predictions['predicted_value']=predict_outcome
    return predictions

def show_linear_line(x_parameter,y_parameter):
    regr=linear_model.LinearRegression()
    regr.fit(x_parameter,y_parameter)
    plt.scatter(x_parameter,y_parameter,color='blue')
    plt.plot(x_parameter,regr.predict(x_parameter),color='red',linewidth=4)
    plt.xticks()
    plt.yticks()
    plt.show()

if __name__ == '__main__':

    x,y=get_data('../超市销售分析.xls')
    predictvalue=129.696
    predictvalue = np.array(predictvalue).reshape(1, -1)    #转为二维数组
    result=linear_model_main(x,y,predictvalue)
    print('intercept value', result['intercept'])
    print('coefficient value', result['coefficient'])
    print('predicted value', result['predicted_value'])

    show_linear_line(x,y)