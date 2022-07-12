import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn import tree
from sklearn.model_selection import train_test_split


'''
获取数据内容。pandas.read_csv(“data.csv”)默认情况下，会把数据内容的第一行默认为字段名标题。
为了解决这个问题，我们添加“header=None”，告诉函数，我们读取的原始文件数据没有列索引
'''
filename='F:\桌面\数据可视化\计卓班  数据可视化技术  大作业\计卓班  数据可视化技术  大作业\电商行业-超市销售数据分析7.0版本\超市销售分析.xls'
data = pd.read_excel(io=filename, sheet_name=0, header=0)
# 去空
data.dropna(axis=0, how='any', inplace=True)  # axis=0表示index行  "any"表示这一行或列中只要有元素缺失，就删除这一行或列
to_drop=['行 ID', '订单 ID','订单日期','发货日期', '邮寄方式', '客户 ID', '客户名称', '细分', '城市', '省/自治区', '国家',
                   '产品 ID','类别', '子类别','产品名称','地区','折扣','数量']
data=data.drop(to_drop, axis=1)


#sparse=False意思是不产生稀疏矩阵
vec=DictVectorizer(sparse=False)
#先用 pandas 对每行生成字典，然后进行向量化
feature = data[['销售额']]
target = data[['利润']]
X_train = vec.fit_transform(feature.to_dict(orient='record'))

#使用feature_names_all接收特征列名,便于后面使用
feature_names_all = vec.get_feature_names()

#打印各个变量
# print('show feature\n',feature)
# print('show vector\n',X_train)
# print('show vector name\n',vec.get_feature_names())

Y_train = vec.fit_transform(target.to_dict(orient='record'))
# print('show vector name\n',vec.get_feature_names())
# print('show target\n',target)


#划分成训练集，验证集，验证集，不过这里我们数据量不够大，没必要
#此段代码中，test_size = 0.25,表示把数据集划分为两份，训练集和测试集之比为4:1（二八原则）
#关于train_test_split()，随机划分训练集和测试集的函数，可参考博客：https://blog.csdn.net/qq_38410428/article/details/94054920
train_x, test_x, train_y, test_y = train_test_split(X_train, Y_train, test_size = 0.5)
#训练决策树
clf = tree.DecisionTreeClassifier(criterion='gini')
model = clf.fit(X_train,Y_train.astype('int'))



#res = model.predict(test_x)
# print(res)    #模型结果输出
# print(Y_test)    #实际值
#print((sum(res==test_x)/len(res)))    #准确率
print("==========================")
score=model.score(test_x,test_y.astype('int'))
print(score)
A = ([[129.696]])
predict_result = clf.predict(A)
print('预测结果：'+str(predict_result))