# SupermarketAnalysis
超市数据可视化分析

使用超市数据进行可视化分析，数据集：超市销售分析.xls,分为三个工作簿，订单，退货，销售人员。这里只用了订单工作簿,数据集属性如下
<br/>
**| 行 ID | 订单 ID | 订单日期 | 发货日期  | 邮寄方式  | 客户 ID | 客户名称 | 细分 | 城市 | 省/自治区 | 国家 | 地区 | 产品 | ID	类别 | 子类别 | 产品名称 | 销售额 | 数量 | 折扣 | 利润 |**

<br/>
项目中包含的python文件为：
<br/>
supermarket_analyse.py 生成各个图表
RFMCustomer.py 生成RFM模型，以及绘制顾客分层结构玫瑰图与各类型顾客消费额及其累加占比柱形折线图
<br/>
predictTree.py 生成决策树预测
<br/>
predictLine.py 生成线性回归预测
<br/>
Merge.py 生成大屏临时html
<br/>
生成最终大屏.py 拖拽形成的最终大屏html
<br/>

<br/>



