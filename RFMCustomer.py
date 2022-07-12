#-*- codeing=utf-8 -*-
#@Time:2022/6/16 2:47
#@Author:王钰娜
#@File : RFMCustomer.py
#@Software:PyCharm

"""
RFM模型
该模型通过R(Recency)表示客户购买时间有多远，F(Frequency)表示客户在固定时间内购买次数，M(Monetary)表示客户在固定时间内购买的金额。

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pyecharts.charts import Grid, Pie, Bar
from pyecharts import options as opts
from pyecharts.globals import ThemeType
class RFMCustomer:
    def __init__(self):
        #filename='F:\桌面\数据可视化\计卓班  数据可视化技术  大作业\计卓班  数据可视化技术  大作业\电商行业-超市销售数据分析7.0版本\超市销售分析.xls'
        filename='超市销售分析.xls'
        data = pd.read_excel(io=filename, sheet_name=0, header=0)
        # 去空
        data.dropna(axis=0, how='any', inplace=True)  # axis=0表示index行  "any"表示这一行或列中只要有元素缺失，就删除这一行或列
        #定义用户类别
        def transform_label(x):
            if x == 111:
                label = '重要价值客户'
            elif x == 110:
                label = '潜力客户'
            elif x == 101:
                label = '重要发展客户'
            elif x == 100:
                label = '新客户'
            elif x == 11:
                label = '重要唤回客户'
            elif x == 10:
                label = '一般客户'
            elif x == 1:
                label = '重要挽留客户'
            elif x == 0:
                label = '流失客户'
            return label

        df=data
        df = df[['订单 ID','订单日期','客户 ID','销售额']]

        r = df.groupby('客户 ID')['订单日期'].max().reset_index()
        r['R'] = (pd.to_datetime('2015-1-1') - r['订单日期']).dt.days   #因为数据集的数据都是2011年-2014年的，所以我们设置2015-1-1即刚好能研究2014年之前的数据
        r = r[['客户 ID','R']]    #R值：最近一次消费（Recency）

        #每一条记录代表一种商品，有些订单有多种商品，原始数据会把订单展开成多行，将其算成一次购买记录，即频次算1次
        dup_f = df.groupby(['客户 ID','订单 ID'])['订单日期'].count().reset_index()
        f = dup_f.groupby('客户 ID')['订单日期'].count().reset_index()
        f.columns = ['客户 ID','F']   #F值：消费频率（Frequency）

        sum_m = df.groupby('客户 ID')['销售额'].sum().reset_index()
        com_m = pd.merge(sum_m,f,left_on = '客户 ID',right_on = '客户 ID',how = 'inner')

        #计算用户平均支付金额
        com_m['M'] = com_m['销售额'] / com_m['F']  #M值：消费金额（Monetary）

        rfm = pd.merge(r,com_m,left_on = '客户 ID',right_on = '客户 ID',how = 'inner')
        rfm = rfm[['客户 ID','R','F','M']]
        #就要对这些次数进行分级，相应的频次对应相应的等级，划分出用户价值。RFM模型分级一般分3到5级，我这里采用5分法。
        #quantile是分位数函数
        #给RFM的每个值进行打分评级
        rfm['R-SCORE'] = pd.cut(rfm['R'],bins = rfm['R'].quantile(q=np.linspace(0,1,num=6),interpolation='nearest'),
                                labels = [5,4,3,2,1],right = False).astype(float)
        rfm['F-SCORE'] = pd.cut(rfm['F'],bins = rfm['F'].quantile(q=np.linspace(0,1,num=6),interpolation='nearest'),
                                labels = [1,2,3,4,5],right = False).astype(float)
        rfm['M-SCORE'] = pd.cut(rfm['M'],bins = rfm['M'].quantile(q=np.linspace(0,1,num=6),interpolation='nearest'),
                                labels = [1,2,3,4,5],right = False).astype(float)

        #R值打分是从5到1，而其他值是从1到5呢
        #因为R值是距今的天数，所以值越大，离现在越久，所以分数越低，价值越低，因此标签是倒过来的；而其他的指标，值越大，越有价值，比如消费额度越高越好，所以是顺序进行打分。

        rfm['R>mean'] = (rfm['R-SCORE'] > rfm['R-SCORE'].mean()) * 1    #当前行的R-SCORE是否大于R-SCORE，是的话置1
        rfm['F>mean'] = (rfm['F-SCORE'] > rfm['F-SCORE'].mean()) * 1
        rfm['M>mean'] = (rfm['M-SCORE'] > rfm['M-SCORE'].mean()) * 1

        #对RFM总分进行统计分级
        #因为在不同业务中，每个指标的重要性是不一样的，有的阶段，频率很重要，有的阶段，销售额很重要。
        #这里倾向于R，最近一次消费时间间隔
        rfm['Score'] = (rfm['R>mean'] * 100) + (rfm['F>mean'] * 10) + (rfm['M>mean'] * 1)

        #根据rfm总分对每个用户进行贴标签，然后分层运营
        rfm['客户类型'] = rfm['Score'].apply(transform_label)


        #统计不同类型客户的消费金额以及金额占比
        count = rfm['客户类型'].value_counts().reset_index()
        count.columns = ['客户类型','人数']
        count['人数占比'] = count['人数'] / count['人数'].sum()

        rfm['购买总金额'] = rfm['F'] * rfm['M']
        mon = rfm.groupby('客户类型')['购买总金额'].sum().reset_index()
        mon.columns = ['客户类型','消费金额']
        mon['金额占比'] = mon['消费金额'] / mon['消费金额'].sum()
        self.result = pd.merge(count,mon,left_on = '客户类型',right_on = '客户类型')

        print( self.result)
        print("====================================")

    # 顾客分层结构分析
    #
    #     各类顾客对销售额的贡献
    from pyecharts.charts import Grid, Pie, Bar
    from pyecharts import options as opts
    from pyecharts.globals import ThemeType

    def make_pie(self):

        # 这里为了美观和交互性，使用pyecharts做南丁格尔玫瑰图，需要将numpy.int转化成python原生态int
        customer_category_sum = []
        for i in self.result['人数'].values:
            customer_category_sum.append(int(i))
        customer_list = [list(z) for z in zip(self.result['客户类型'], customer_category_sum)]

        # 绘制饼图
        pie = (
            Pie(init_opts=opts.InitOpts(theme=ThemeType.MACARONS,bg_color='white'))
            .add('',customer_list,
             radius=['30%','75%'],
             rosetype='radius',
             label_opts=opts.LabelOpts(is_show=True))
            .set_global_opts(title_opts=opts.TitleOpts(title='顾客分层结构',pos_left='center'),
                             toolbox_opts=opts.ToolboxOpts(is_show=True),
                             legend_opts=opts.LegendOpts(orient='vertical',pos_right='0%',pos_top='30%'))
            .set_series_opts(label_opts=opts.LabelOpts(formatter='{b}:{d}%')))
        pie.render("顾客分层结构.html")

        return pie

    def make_bar(self):
        ##金额占比累加
        self.result.sort_values(by=['消费金额'],ascending=False,inplace=True)
        sales_rate=[]; a=0
        for i in self.result.金额占比:
            a +=i
            sales_rate.append(a)
        self.result['金额占比累加'] = sales_rate
        print(self.result)


        # 建立左侧纵坐标画板
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        plt.rcParams['axes.unicode_minus'] = False
        #绘制带子图
        fig, ax1 = plt.subplots(figsize=(16, 10))   #ax：子图对象    在Figure对象中可以包含一个或者多个Axes对象。每个Axes(ax)对象都是一个拥有自己坐标系统的绘图区域
        # 画柱状图图
        s = plt.bar(self.result.客户类型, self.result.消费金额, alpha=0.5, label='消费金额',width=0.7)
        # 显示左侧纵坐标
        ax1.set_ylabel('消费金额', fontsize=10)
        plt.yticks(range(0, 6000000, 500000),   #50万为单位增长
                   ['0', '50W', '100W', '150W', '200W', '250W', '300W', '350W', '400W', '450W', '500W', '550W'])
        plt.tick_params(labelsize=10)
        # 显示文字
        for x1, y1 in zip(self.result.客户类型, self.result.消费金额):
            plt.text(x1, y1, str(int(y1 / 10000)) + 'W', ha='center', fontsize=10)

        ax2 = ax1.twinx()   #twinx()一个图两个不同的y轴
        # # 画折线图
        line = ax2.plot(self.result.客户类型, self.result.金额占比累加, linewidth=3, marker='o', c='y', ms=10)
        # # 折线图显示标识
        for a, b in zip(self.result.客户类型, self.result.金额占比累加):
            ax2.text(a, b, "%.0f" % (100 * b) + '%', ha='center', fontsize=10)
        ax2.set_ylabel('金额占比累加', fontsize=12, rotation=270)
        plt.ylim(0, 1.05)
        plt.tick_params(labelsize=10)
        ax2.set_title("各类型顾客消费额及其累加占比", fontsize=12)
        plt.savefig("各类型顾客消费额及其累加占比.png", dpi=300)
        plt.show()

if __name__ == '__main__':
        a=RFMCustomer()
        a.make_pie()
        a.make_bar()