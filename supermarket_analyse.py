#-*- codeing=utf-8 -*-
#@Time:2022/6/14 1:54
#@Author:王钰娜
#@File : supermarket_analyse.py
#@Software:PyCharm
import pandas as pd
import numpy as np
from pyecharts.charts import Bar,Pie,Map,TreeMap,HeatMap,Line,Grid
from pyecharts import options as opts
from pyecharts.faker import Faker
from RFMCustomer import RFMCustomer
class Analyse(object):

    csv_path=''
    newRows=''
    def __init__(self):
        self. excel_path = '超市销售分析.xls'
        self.newRows = pd.read_excel(io=self.excel_path, sheet_name=0, header=0)
        # 去空
        self.newRows.dropna(axis=0, how='any', inplace=True)  # axis=0表示index行  "any"表示这一行或列中只要有元素缺失，就删除这一行或列
        # 统计空值
        print(self.newRows.isnull().sum())
        print("--------------------------------------")



    # 堆叠柱状图显示各地区总体的销售额，利润，成本

    def make_area_Bar(self):
        to_drop = ['行 ID', '订单 ID', '订单日期', '发货日期', '邮寄方式', '客户 ID', '客户名称', '细分', '城市', '省/自治区', '国家',
                   '产品 ID', '类别','子类别','产品名称','数量','折扣']
        res = self.newRows.drop(to_drop, axis=1)
        # 数据统计
        area_dict={}
        for i in res.itertuples():  # 将DataFrame迭代为元祖。
            if i[1] not in area_dict.keys():
                area_dict[i[1]]=[i[2],i[3]]     #新增{'华东'：[129.66,-60.704]}    #地区：销售额，利润
            else:
                list=area_dict[i[1]]
                list[0]+=i[2]   #销售额
                list[1]+=i[3]   #利润
                area_dict[i[1]]=list

        for k,v in area_dict.items():

            list=v
            list.append(list[0]-list[1])    #计算成本
            area_dict[k]=list


        print("========六大地区的销售额，利润，成本==============")
        print(area_dict)

        area = ['华东','西南','中南','西北','东北','华北']

        #按照area顺序添加销售额,利润，成本
        sale=[]
        profit=[]
        cost=[]
        for k,v in area_dict.items():
            sale.append(v[0])
            profit.append(v[1])
            cost.append(v[2])
        c=Bar()
        c.add_xaxis(area)
        c.add_yaxis("销售额",sale)
        c.add_yaxis("利润", profit, stack="stack1")
        c.add_yaxis("成本", cost, stack="stack1")


        c.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        c.set_global_opts(title_opts=opts.TitleOpts(title="各地区总体的销售额,利润,成本"))
        c.render("各地区总体的销售额,利润,成本.html")

        return c
    #各地区总体的利润率
    def make_area_pie(self):
        to_drop = ['行 ID', '订单 ID', '订单日期', '发货日期', '邮寄方式', '客户 ID', '客户名称', '细分', '城市', '省/自治区', '国家',
                   '产品 ID', '类别', '子类别', '产品名称', '数量', '折扣']
        res = self.newRows.drop(to_drop, axis=1)
        # 数据统计
        area_dict = {}
        for i in res.itertuples():  # 将DataFrame迭代为元祖。
            if i[1] not in area_dict.keys():
                area_dict[i[1]] = [i[2], i[3]]  # 新增{'华东'：[129.66,-60.704]}    #地区：销售额，利润
            else:
                list = area_dict[i[1]]
                list[0] += i[2]  # 销售额
                list[1] += i[3]  # 利润
                area_dict[i[1]] = list

        for k, v in area_dict.items():
            list = v
            list.append(list[0] - list[1])  # 计算成本
            area_dict[k] = list


        data_dict={}
        for k, v in area_dict.items():
            list = v
            rate=list[1]/list[2]*100    #计算利润率
            str="%.2f" % rate   #保存两位小数
            data_dict[k]=str

        print("========六大地区的利润率==============")
        print(data_dict)

        data_list=[]
        for i in data_dict.items():
            data_list.append(i)


        c=Pie()
        c.add("", data_list,  center=["40%", "55%"],)
        c.set_global_opts(
            title_opts=opts.TitleOpts(title="各地区利润率"),
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"),
        )
        c.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}%（{d}%）"))   #{a}（系列名称），{b}（数据名称），{c}（数值数组）, {d}（无）。如下图：
        # 生成html
        c.render("各地区利润率.html")
        return c

    #以省展示利润亏损情况
    def make_china_map(self):
        to_drop = ['行 ID', '订单 ID', '订单日期', '发货日期', '邮寄方式', '地区','客户 ID', '客户名称', '细分', '城市',  '国家',
                   '产品 ID', '类别', '子类别', '产品名称', '数量', '折扣']
        res = self.newRows.drop(to_drop, axis=1)
        provice_dict={}
        for i in res.itertuples():
            if i[1] not in provice_dict.keys():
                provice_dict[i[1]]=i[3]
            else:
                provice_dict[i[1]] += i[3]
        print("========以省展示利润情况==============")
        print(provice_dict)

        provice_list=[]
        for k,v in provice_dict.items():
            provice_list.append((k,v))

        #绘制地图
        c=Map()
        c.add("中国地图",provice_list,"china")
        c.set_global_opts(
        title_opts=opts.TitleOpts(title="各省利润情况"),
        visualmap_opts=opts.VisualMapOpts(max_=400000,min_=-200000),
    )
        c.render("各省利润情况.html")

        return c

    #各市利润情况
    def make_city_map(self):
        to_drop = ['行 ID', '订单 ID', '订单日期', '发货日期', '邮寄方式', '地区', '客户 ID', '客户名称', '细分', '省/自治区', '国家',
                   '产品 ID', '类别', '子类别', '产品名称', '数量', '折扣']
        res = self.newRows.drop(to_drop, axis=1)
        city_dict = {}
        for i in res.itertuples():
            if i[1] not in city_dict.keys():
                city_dict[i[1]]=i[3]
            else:
                city_dict[i[1]] += i[3]

        print("========各市的利润情况==============")
        print(city_dict)

        city_list = []
        for k, v in city_dict.items():
            city_list.append((k, v))

        # 绘制地图
        c = Map()
        c.add("中国地图", city_list, "china-cities",)
        c.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        c.set_global_opts(
            title_opts=opts.TitleOpts(title="各市利润情况"),
            visualmap_opts=opts.VisualMapOpts(max_=8000, min_=-5000),
        )
        c.render("各市利润情况.html")

        return c

    #统计利润亏损的省/自治区
    def make_province_bar(self):
        to_drop = ['行 ID', '订单 ID', '订单日期', '发货日期', '邮寄方式', '地区', '客户 ID', '客户名称', '细分', '城市', '国家',
                   '产品 ID', '类别', '子类别', '产品名称', '数量', '折扣']
        res = self.newRows.drop(to_drop, axis=1)
        provice_dict = {}
        for i in res.itertuples():
            if i[1] not in provice_dict.keys():
                provice_dict[i[1]] = i[3]
            else:
                provice_dict[i[1]] += i[3]

        lowrate_provice_dict={}
        for k,v in provice_dict.items():
            if v<0:
                lowrate_provice_dict[k]=v
        print("========展示负利润省/自治区"+str(len(lowrate_provice_dict))+"==============")
        d_order = sorted(lowrate_provice_dict.items(), key=lambda x: x[1],reverse=False)  # 按字典集合中，每一个元组的第二个元素排列。 # x相当于字典集合中遍历出来的一个元组。
        print(d_order)
        x = []
        y = []
        for item in d_order:
            x.append(item[0])
            y.append(item[1])

        c=Bar()
        c.add_xaxis(x)
        c.add_yaxis("利润",y,color=Faker.rand_color())

        c.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        c.set_global_opts(title_opts=opts.TitleOpts(title="负利润省/自治区的利润情况"))
        c.render("负利润省的利润情况.html")

        return c

    #统计利润亏损的市
    def make_city_bar(self):
        to_drop = ['行 ID', '订单 ID', '订单日期', '发货日期', '邮寄方式', '地区', '客户 ID', '客户名称', '细分', '省/自治区', '国家',
                   '产品 ID', '类别', '子类别', '产品名称', '数量', '折扣']
        res = self.newRows.drop(to_drop, axis=1)
        city_dict = {}
        for i in res.itertuples():
            if i[1] not in city_dict.keys():
                city_dict[i[1]] = i[3]
            else:
                city_dict[i[1]] += i[3]

        lowrate_city_dict={}
        for k,v in city_dict.items():
            if v<0:
                lowrate_city_dict[k]=v
        print("========展示负利润城市，共"+str(len(lowrate_city_dict))+"==============")

        d_order = sorted(lowrate_city_dict.items(), key=lambda x: x[1], reverse=False)  # 按字典集合中，每一个元组的第二个元素排列。 # x相当于字典集合中遍历出来的一个元组。
        print(d_order)
        x=[]
        y=[]
        for item in d_order:
            x.append(item[0])
            y.append(item[1])

        c=Bar()
        c.add_xaxis(x)
        c.add_yaxis("利润",y,color=Faker.rand_color())

        c.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        c.set_global_opts(title_opts=opts.TitleOpts(title="负利润城市的利润情况"))
        c.render("负利润城市的利润情况.html")

        return c

    # 各省/自治区销售额情况 矩形树图
    def make_province_treemap(self):

        to_drop = ['行 ID', '订单 ID', '订单日期', '发货日期', '邮寄方式', '地区', '客户 ID', '客户名称', '细分', '国家',
                   '产品 ID', '类别', '子类别', '产品名称', '利润','数量', '折扣']
        res = self.newRows.drop(to_drop, axis=1)
        #数据统计
        provice_dict={}
        for i in res.itertuples():
            if i[2] not in provice_dict.keys():
                dict = {}
                dict[i[1]] = i[3]
                list=[]
                list.append(dict)
                provice_dict[i[2]]=list
            else:
                list=provice_dict[i[2]]
                dict = {}
                dict[i[1]] = i[3]
                list.append(dict)
        print(provice_dict)
        new_provice_dict={}
        for k0,v0 in provice_dict.items():
            temp = {}
            for item in v0:

                for k,v in item.items():
                    key=k
                    value=v
                if key not in temp.keys():
                    temp[key]=value
                else:
                    temp[key]+=value
            list=[]
            list.append(temp)
            new_provice_dict[k0]=list
        print("=======new_provice_dict========")
        print(new_provice_dict)

        new_provice_list=[]
        for k, v in new_provice_dict.items():


            new_city_dict=v[0]
            new_city_list=[]
            for k1,v1 in new_city_dict.items():
                new_city_list.append((k1,v1))

            new_provice_list.append((k, new_city_list))



        #统计省的总销售额
        p_dict={}
        for k,v in new_provice_dict.items():
            dict=v[0]
            count=0
            for v1 in dict.values():
                count+=v1
            p_dict[k]=count

        print("=========p_dict=========")
        print(p_dict)

        p_list=[]
        for k,v in p_dict.items():
            p_list.append((k,v))

        c=TreeMap()
        children_zhejiang=[] #浙江
        for j in new_provice_list[0][1]:
                children_zhejiang.append({"value": j[1], "name": j[0]})
        children_sichuan=[] #四川
        for j in new_provice_list[1][1]:
                children_sichuan.append({"value": j[1], "name": j[0]})
        children_jiangsu=[] #江苏
        for j in new_provice_list[2][1]:
                children_jiangsu.append({"value": j[1], "name": j[0]})
        children_guangdong=[]      #广东
        for j in new_provice_list[3][1]:
                children_guangdong.append({"value": j[1], "name": j[0]})
        children_jiangxi=[]      #江西
        for j in new_provice_list[4][1]:
                children_jiangxi.append({"value": j[1], "name": j[0]})
        children_shanxi=[]      #陕西
        for j in new_provice_list[5][1]:
                children_shanxi.append({"value": j[1], "name": j[0]})
        children_heilongjiang=[]      #黑龙江
        for j in new_provice_list[6][1]:
                children_heilongjiang.append({"value": j[1], "name": j[0]})

        children_shandong=[]      #山东
        for j in new_provice_list[7][1]:
                children_shandong.append({"value": j[1], "name": j[0]})

        children_shanghai=[]      #上海
        for j in new_provice_list[8][1]:
                children_shanghai.append({"value": j[1], "name": j[0]})
        children_hebei=[]      #河北
        for j in new_provice_list[9][1]:
                children_hebei.append({"value": j[1], "name": j[0]})
        children_fujian=[]      #福建
        for j in new_provice_list[10][1]:
                children_fujian.append({"value": j[1], "name": j[0]})
        children_anhui=[]      #安徽
        for j in new_provice_list[11][1]:
                children_anhui.append({"value": j[1], "name": j[0]})
        children_gansu=[]      #甘肃
        for j in new_provice_list[12][1]:
                children_gansu.append({"value": j[1], "name": j[0]})
        children_jilin=[]      #吉林
        for j in new_provice_list[13][1]:
                children_jilin.append({"value": j[1], "name": j[0]})
        children_liaoning=[]      #辽宁
        for j in new_provice_list[14][1]:
                children_liaoning.append({"value": j[1], "name": j[0]})
        children_hubei=[]      #湖北
        for j in new_provice_list[15][1]:
                children_hubei.append({"value": j[1], "name": j[0]})
        children_henan=[]      #河南
        for j in new_provice_list[16][1]:
                children_henan.append({"value": j[1], "name": j[0]})
        children_hunan=[]      #湖南
        for j in new_provice_list[17][1]:
                children_hunan.append({"value": j[1], "name": j[0]})
        children_beijing=[]      #北京
        for j in new_provice_list[18][1]:
                children_beijing.append({"value": j[1], "name": j[0]})
        children_chongqi=[]      #重庆
        for j in new_provice_list[19][1]:
                children_chongqi.append({"value": j[1], "name": j[0]})
        children_qinghai=[]      #青海
        for j in new_provice_list[20][1]:
                children_qinghai.append({"value": j[1], "name": j[0]})
        children_guangxi = []  # 广西
        for j in new_provice_list[21][1]:
            children_guangxi.append({"value": j[1], "name": j[0]})
        children_tianjin=[]      #天津
        for j in new_provice_list[22][1]:
                children_tianjin.append({"value": j[1], "name": j[0]})
        children_yunnan=[]      #云南
        for j in new_provice_list[23][1]:
                children_yunnan.append({"value": j[1], "name": j[0]})
        children_guizhou=[]      #贵州
        for j in new_provice_list[24][1]:
                children_guizhou.append({"value": j[1], "name": j[0]})
        children_shanxi=[]      #山西
        for j in new_provice_list[25][1]:
                children_shanxi.append({"value": j[1], "name": j[0]})
        children_neimenggu=[]      #内蒙古
        for j in new_provice_list[26][1]:
                children_neimenggu.append({"value": j[1], "name": j[0]})
        children_ningxia=[]      #宁夏
        for j in new_provice_list[27][1]:
                children_ningxia.append({"value": j[1], "name": j[0]})
        children_hainan=[]      #海南
        for j in new_provice_list[28][1]:
                children_hainan.append({"value": j[1], "name": j[0]})
        children_xinjiang=[]      #新疆
        for j in new_provice_list[29][1]:
                children_xinjiang.append({"value": j[1], "name": j[0]})
        children_xizang=[]      #西藏
        for j in new_provice_list[30][1]:
                children_xizang.append({"value": j[1], "name": j[0]})

        data=[
            {
                "value": p_list[0][1],
                "name":  p_list[0][0],  #浙江
                "children": children_zhejiang,
            },
            {
                "value": p_list[1][1],
                "name": p_list[1][0],  # 四川
                "children": children_sichuan,
            },
            {
                "value": p_list[2][1],
                "name": p_list[2][0],  # 江苏
                "children": children_jiangsu,
            },
            {
                "value": p_list[3][1],
                "name": p_list[3][0],  # 广东
                "children": children_guangdong,
            },
            {
                "value": p_list[4][1],
                "name": p_list[4][0],  # 江西
                "children": children_jiangxi,
            },
            {
                "value": p_list[5][1],
                "name": p_list[5][0],  # 陕西
                "children": children_shanxi,
            },
            {
                "value": p_list[6][1],
                "name": p_list[6][0],  # 黑龙江
                "children": children_heilongjiang,
            },            {
                "value": p_list[7][1],
                "name": p_list[7][0],  # 山东
                "children": children_shandong,
            },            {
                "value": p_list[8][1],
                "name": p_list[8][0],  # 上海
                "children": children_shanghai,
            },
            {
                "value": p_list[9][1],
                "name": p_list[9][0],  # 河北
                "children": children_hebei,
            },            {
                "value": p_list[10][1],
                "name": p_list[10][0],  # 福建
                "children": children_fujian,
            },            {
                "value": p_list[11][1],
                "name": p_list[11][0],  # 安徽
                "children": children_anhui,
            },            {
                "value": p_list[12][1],
                "name": p_list[12][0],  # 甘肃
                "children": children_gansu,
            },
            {
                "value": p_list[13][1],
                "name": p_list[13][0],  # 吉林
                "children": children_jilin,
            },
            {
                "value": p_list[14][1],
                "name": p_list[14][0],  # 辽宁
                "children": children_liaoning,
            },
            {
                "value": p_list[15][1],
                "name": p_list[15][0],  # 湖北
                "children": children_hubei,
            },
            {
                "value": p_list[16][1],
                "name": p_list[16][0],  # 河南
                "children": children_henan,
            },
            {
                "value": p_list[17][1],
                "name": p_list[17][0],  # 湖南
                "children": children_hunan,
            },
            {
                "value": p_list[18][1],
                "name": p_list[18][0],  # 北京
                "children": children_beijing,
            },
            {
                "value": p_list[19][1],
                "name": p_list[19][0],  # 重庆
                "children": children_chongqi,
            },
            {
                "value": p_list[20][1],
                "name": p_list[20][0],  # 青海
                "children": children_qinghai,
            },

            {
                "value": p_list[21][1],
                "name": p_list[21][0],  # 广西
                "children": children_guangxi,
            },
            {
                "value": p_list[22][1],
                "name": p_list[22][0],  # 天津
                "children": children_tianjin,
            },
            {
                "value": p_list[23][1],
                "name": p_list[23][0],  # 云南
                "children": children_yunnan,
            },
            {
                "value": p_list[24][1],
                "name": p_list[24][0],  # 贵州
                "children": children_guizhou,
            },
            {
                "value": p_list[25][1],
                "name": p_list[25][0],  # 山西
                "children": children_shanxi,
            },
            {
                "value": p_list[26][1],
                "name": p_list[26][0],  # 内蒙古
                "children": children_neimenggu,
            },
            {
                "value": p_list[27][1],
                "name": p_list[27][0],  # 宁夏
                "children": children_ningxia,
            },
            {
                "value": p_list[28][1],
                "name": p_list[28][0],  # 海南
                "children": children_hainan,
            },
            {
                "value": p_list[29][1],
                "name": p_list[29][0],  # 新疆
                "children": children_xinjiang,
            },
            {
                "value": p_list[30][1],
                "name": p_list[30][0],  # 西藏
                "children": children_xizang,
            },

        ]
        c.add("各省市销售额",data)
        c.set_global_opts(title_opts=opts.TitleOpts(title="各省市销售额"))
        c.render("各省市销售额-矩形树图.html")


        return c

    # 子类别-利润值柱形图
    def make_type_bar(self):
        to_drop = ['行 ID', '订单 ID', '订单日期', '发货日期', '邮寄方式', '地区', '客户 ID', '客户名称', '细分', '城市','省/自治区','国家',
                   '产品 ID', '类别', '销售额', '产品名称', '数量', '折扣']
        res = self.newRows.drop(to_drop, axis=1)
        # 数据统计
        type_dict = {}
        for i in res.itertuples():
            if i[1] not in type_dict.keys():
                type_dict[i[1]]=i[2]
            else:
                type_dict[i[1]] += i[2]
        print("============按子类别划分的得到利润值===========")

        d_order = sorted(type_dict.items(), key=lambda x: x[1],reverse=False)  # 按字典集合中，每一个元组的第二个元素排列。 # x相当于字典集合中遍历出来的一个元组。
        print(d_order)

        x = []
        y = []
        for item in d_order:
            x.append(item[0])
            y.append(item[1])
        c=Bar()
        c.add_xaxis(x)
        c.add_yaxis("利润值",y,color=Faker.rand_color())
        c.reversal_axis()
        c.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        c.set_global_opts(title_opts=opts.TitleOpts(title="子类别-利润值"))
        c.render("子类别-利润值.html")

        return c

    #类别-环形图
    def make_type_roll(self):
        to_drop = ['行 ID', '订单 ID', '订单日期', '发货日期', '邮寄方式', '地区', '客户 ID', '客户名称', '细分', '城市', '省/自治区', '国家',
                   '产品 ID', '子类别', '利润', '产品名称', '数量', '折扣']
        res = self.newRows.drop(to_drop, axis=1)
        # 数据统计
        type_dict = {}
        for i in res.itertuples():
            if i[1] not in type_dict.keys():
                type_dict[i[1]]=i[2]
            else:
                type_dict[i[1]]+=i[2]
        print("======按类别统计销售额==============")
        print(type_dict)

        x=[]
        for k,v in type_dict.items():
            x.append((k,v))

        c=Pie()
        c.add("",x,radius=["40%", "75%"],)
        c.set_global_opts(
            title_opts=opts.TitleOpts(title="按类别统计销售额"),
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"),
        )
        c.set_series_opts(
            label_opts=opts.LabelOpts(formatter="{b}: {c}（{d}%）"))  # {a}（系列名称），{b}（数据名称），{c}（数值数组）, {d}（无）。如下图：
        # 生成html
        c.render("按类别统计销售额.html")
        return c


    #每个类别中的子类别排名前10
    def make_typetop10_bar(self):
        to_drop = ['行 ID', '订单 ID', '订单日期', '发货日期', '邮寄方式', '地区', '客户 ID', '客户名称', '细分', '城市', '省/自治区', '国家',
                   '产品 ID', '利润', '销售额', '折扣']
        res = self.newRows.drop(to_drop, axis=1)
        # 数据统计
        furniture_dict = {} #家具
        OfficeSupplies_dict={}  #办公用品
        technology_dict={}  #技术

        for i in res.itertuples():
            str=i[3]
            temp=str.split(",")[0]  #商品名称去掉颜色
            if i[1] == '家具':
                if temp not in furniture_dict.keys():
                    furniture_dict[temp]=i[4]
                else:
                    furniture_dict[temp] += i[4]
            if i[1] == '办公用品':
                if temp not in OfficeSupplies_dict.keys():
                    OfficeSupplies_dict[temp]=i[4]
                else:
                    OfficeSupplies_dict[temp] += i[4]
            if i[1]=='技术':
                if temp not in technology_dict.keys():
                    technology_dict[temp] = i[4]
                else:
                    technology_dict[temp] += i[4]

        d_furniture = sorted(furniture_dict.items(), key=lambda x: x[1],
                         reverse=False)  # 按字典集合中，每一个元组的第二个元素排列。 # x相当于字典集合中遍历出来的一个元组。
        print("==========家具类购买数量前10===========")
        print(d_furniture)
        self.x1=[]
        self.y1=[]

        for item in d_furniture[:10]:
                self.x1.append(item[0])
                self.y1.append(item[1])

        d_OfficeSupplies= sorted(OfficeSupplies_dict.items(), key=lambda x: x[1],
                             reverse=False)  # 按字典集合中，每一个元组的第二个元素排列。 # x相当于字典集合中遍历出来的一个元组。
        print("==========办公用品类购买数量前10===========")
        print(d_OfficeSupplies)
        self.x2 = []
        self.y2 = []

        for item in d_OfficeSupplies[:10]:
            self.x2.append(item[0])
            self.y2.append(item[1])

        d_technology = sorted(technology_dict.items(), key=lambda x: x[1],
                                  reverse=False)  # 按字典集合中，每一个元组的第二个元素排列。 # x相当于字典集合中遍历出来的一个元组。
        print("==========技术类购买数量前10===========")
        print(d_technology)
        self.x3 = []
        self.y3 = []

        for item in d_technology[:10]:
            self.x3.append(item[0])
            self.y3.append(item[1])

        a = Bar()  # 家具
        a.add_xaxis(self.x1)
        a.add_yaxis("销售额", self.y1, color=Faker.rand_color())
        a.reversal_axis()
        a.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        a.set_global_opts(
            title_opts=opts.TitleOpts(title="家具类别销量热榜top10"),
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"),
        )
        a.render("家具类别销量热榜top10.html")
        return a

    def make_bar1(self):
        a=Bar() #家具
        a.add_xaxis(self.x1)
        a.add_yaxis("销售数量",self.y1,color=Faker.rand_color())
        a.reversal_axis()
        a.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        a.set_global_opts(
                title_opts=opts.TitleOpts(title="家具类别销量热榜top10"),
                legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"),
            )
        a.render("家具类别销量热榜top10.html")
        return a

    def make_bar2(self):
        b=Bar() #办公用品
        b.add_xaxis(self.x2)
        b.add_yaxis("销售额",self.y2,color=Faker.rand_color())
        b.reversal_axis()
        b.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        b.set_global_opts(
                title_opts=opts.TitleOpts(title="办公用品类别销量热榜top10"),
                legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"),
            )
        b.render("办公用品类别销量热榜top10.html")
        return b

    def make_bar3(self):
        c=Bar() #技术
        c.add_xaxis(self.x3)
        c.add_yaxis("销售额",self.y3,color=Faker.rand_color())
        c.reversal_axis()
        c.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        c.set_global_opts(
                title_opts=opts.TitleOpts(title="技术类别用品销量热榜top10"),

                legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"),
            )
        c.render("技术类别用品销量热榜top10.html")

        return c

    #销售额、数量、折扣、利润、时间、商品类别的相关性
    def make_Heatmap(self):
        to_drop = ['行 ID', '订单 ID', '发货日期', '邮寄方式', '客户 ID', '客户名称', '细分', '城市', '省/自治区', '国家',
                   '产品 ID', '子类别', '产品名称', '地区']

        res = self.newRows.drop(to_drop, axis=1)
        # 转换 datetime 类型
        res['订单日期'] = pd.to_datetime(res['订单日期'])
        ## 增加年份列和月份列
        res['年份'] = res['订单日期'].dt.year
        res['月份'] = res['订单日期'].dt.month

        #转换类别
        dummy_data = pd.get_dummies(res['类别'], prefix="类别",dummy_na=False,drop_first=False)  # dummy_na是否考虑缺失值，drop_first是否做某一项为全0的哑变量转换，默认False
        temp2 = res.join(dummy_data)

        # 导入数据可视化所需要的库
        import matplotlib.pyplot as plt  # Matplotlib – Python画图工具库
        import seaborn as sns  # Seaborn – 统计学数据可视化工具库
        # 对所有的标签和特征两两显示其相关性的热力图(heatmap)
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        plt.rcParams['axes.unicode_minus'] = False
        sns.heatmap(temp2.corr(), annot=True)   #True，就在热力图的每个单元上显示数值
        plt.savefig("热力图.png", dpi=300)
        plt.show()

    #年度销售额，销售额增长率
    def make_saleyear_BarAndLine(self):
        to_drop = ['行 ID', '订单 ID', '发货日期', '邮寄方式', '客户 ID', '客户名称', '细分', '城市', '省/自治区', '国家',
                   '产品 ID', '类别','子类别', '产品名称', '地区','数量','折扣','利润']

        res = self.newRows.drop(to_drop, axis=1)
        # 转换 datetime 类型
        res['订单日期'] = pd.to_datetime(res['订单日期'])
        ## 增加年份列和月份列
        res['年份'] = res['订单日期'].dt.year
        res['月份'] = res['订单日期'].dt.month

        year=res['年份'].unique()
        year=sorted(year,reverse=False)
        # 创建销售额透视表
        sales = pd.pivot_table(res,  index='月份', columns='年份', aggfunc=[np.sum])    #aggfunc参数可以设置我们对数据聚合时进行的函数操作。
        sales.columns = year
        sales.index = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']

        print(type(sales.sum()))
        sum=sales.sum().tolist()
        #年度销售额，增长率
        rise_12 = (sum[1] - sum[0]) / sum[0]
        rise_13 = (sum[2] - sum[1]) / sum[1]
        rise_14 = (sum[3] - sum[2]) / sum[2]
        rise_rate = [0, rise_12, rise_13, rise_14]

        sales_sum = pd.DataFrame({'Sales_sum': sales.sum()})
        sales_sum['rise_rate'] = rise_rate
        sales_sum.index = pd.Series(['2011年', '2012年', '2013年', '2014年'])


        x=sales_sum.index.tolist()

        y1=sales_sum.Sales_sum.tolist()
        y2=sales_sum.rise_rate.tolist()
        print(x,y1,y2)


        bar = (
            Bar()
                .extend_axis(
                yaxis=opts.AxisOpts(
                    name="销售额",
                    type_="value",
                )
            )
                .add_xaxis(xaxis_data=x)
                .add_yaxis("销售额",y1,label_opts=opts.LabelOpts(is_show=False),color=Faker.rand_color())

                .set_global_opts(
                title_opts=opts.TitleOpts(title="年度销售额及增长率"),
                tooltip_opts=opts.TooltipOpts(
                    is_show=True, trigger="axis", axis_pointer_type="cross"
                ),
                xaxis_opts=opts.AxisOpts(
                    type_="category",
                    axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow"),
                ),
                yaxis_opts=opts.AxisOpts(
                    name="销售额",
                    type_="value",
                    axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                ),
            )
        )

        line = (
            Line()

                .add_xaxis(xaxis_data=x)
                .add_yaxis(
                series_name="增长率",
                yaxis_index=1,
                y_axis=y2,
                label_opts=opts.LabelOpts(is_show=True),
                color=Faker.rand_color()
            )
        )

        bar.overlap(line).render("年度销售额及增长率.html")

        return bar

    #月度销售额
    def make_salemonth_BarAndLine(self):
        to_drop = ['行 ID', '订单 ID', '发货日期', '邮寄方式', '客户 ID', '客户名称', '细分', '城市', '省/自治区', '国家',
                   '产品 ID', '类别', '子类别', '产品名称', '地区', '数量', '折扣', '利润']

        res = self.newRows.drop(to_drop, axis=1)
        # 转换 datetime 类型
        res['订单日期'] = pd.to_datetime(res['订单日期'])
        ## 增加年份列和月份列
        res['年份'] = res['订单日期'].dt.year
        res['月份'] = res['订单日期'].dt.month

        # year = res['年份'].unique()
        # year = sorted(year, reverse=False)
        # 创建销售额透视表
        sales = pd.pivot_table(res, index='月份', columns='年份', aggfunc=[np.sum])  # aggfunc参数可以设置我们对数据聚合时进行的函数操作。
        sales.columns = ['2011年','2012年','2013年','2014年']
        sales.index = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']

        print(sales)
        x = sales.index.tolist()
        y_2011=sales['2011年']
        y_2012 = sales['2012年']
        y_2013 = sales['2013年']
        y_2014 = sales['2014年']

        c=Line()
        c.add_xaxis(x)
        c.add_yaxis("2011年",y_2011, )
        c.add_yaxis("2012年", y_2012,)
        c.add_yaxis("2013年", y_2013, )
        c.add_yaxis("2014年", y_2014,)

        c.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        c.set_global_opts(
            title_opts=opts.TitleOpts(title="月度销售额"),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        yaxis_opts=opts.AxisOpts(
            name='销售额',
            name_textstyle_opts=opts.TextStyleOpts(
                font_family='Times New Roman',
                font_size=14,
                color='black',
                font_weight='bolder',
            ),
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
        xaxis_opts=opts.AxisOpts(name='月份',name_location='middle',
                name_textstyle_opts=opts.TextStyleOpts(
                font_family='Times New Roman',
                font_size=14,
                color='black',
                font_weight='bolder',
            ),type_="category", boundary_gap=False),)
        c.render("月度销售额.html")

        return c

    # 年度利润及增长率
    def make_profityear_BarAndLine(self):
        to_drop = ['行 ID', '订单 ID', '发货日期', '邮寄方式', '客户 ID', '客户名称', '细分', '城市', '省/自治区', '国家',
                   '产品 ID', '类别', '子类别', '产品名称', '地区', '数量', '折扣', '销售额']

        res = self.newRows.drop(to_drop, axis=1)
        # 转换 datetime 类型
        res['订单日期'] = pd.to_datetime(res['订单日期'])
        ## 增加年份列和月份列
        res['年份'] = res['订单日期'].dt.year
        res['月份'] = res['订单日期'].dt.month

        year = res['年份'].unique()
        year = sorted(year, reverse=False)
        # 创建销售额透视表
        sales = pd.pivot_table(res, index='月份', columns='年份', aggfunc=[np.sum])  # aggfunc参数可以设置我们对数据聚合时进行的函数操作。
        sales.columns = year
        sales.index = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']

        print(type(sales.sum()))
        sum = sales.sum().tolist()
        # 年度销售额，增长率
        rise_12 = (sum[1] - sum[0]) / sum[0]
        rise_13 = (sum[2] - sum[1]) / sum[1]
        rise_14 = (sum[3] - sum[2]) / sum[2]
        rise_rate = [0, rise_12, rise_13, rise_14]

        sales_sum = pd.DataFrame({'Sales_sum': sales.sum()})
        sales_sum['rise_rate'] = rise_rate
        sales_sum.index = pd.Series(['2011年', '2012年', '2013年', '2014年'])

        x = sales_sum.index.tolist()

        y1 = sales_sum.Sales_sum.tolist()
        y2 = sales_sum.rise_rate.tolist()
        print(x, y1, y2)

        bar = (
            Bar()
                .extend_axis(
                yaxis=opts.AxisOpts(
                    name="增长率",
                    type_="value",
                )
            )
                .add_xaxis(xaxis_data=x)
                .add_yaxis("利润", y1, label_opts=opts.LabelOpts(is_show=False), color=Faker.rand_color())

                .set_global_opts(
                title_opts=opts.TitleOpts(title="年度利润及增长率"),
                tooltip_opts=opts.TooltipOpts(
                    is_show=True, trigger="axis", axis_pointer_type="cross"
                ),
                xaxis_opts=opts.AxisOpts(
                    type_="category",
                    axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow"),
                ),
                yaxis_opts=opts.AxisOpts(
                    name="利润",
                    type_="value",
                    axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                ),
            )
        )

        line = (
            Line()

                .add_xaxis(xaxis_data=x)
                .add_yaxis(
                series_name="增长率",
                yaxis_index=1,
                y_axis=y2,
                label_opts=opts.LabelOpts(is_show=True),
                color=Faker.rand_color()
            )
        )

        bar.overlap(line).render("年度利润及增长率.html")

        return bar


    # 月度利润
    def make_profitmonth_BarAndLine(self):
        to_drop = ['行 ID', '订单 ID', '发货日期', '邮寄方式', '客户 ID', '客户名称', '细分', '城市', '省/自治区', '国家',
                   '产品 ID', '类别', '子类别', '产品名称', '地区', '数量', '折扣', '销售额']

        res = self.newRows.drop(to_drop, axis=1)
        # 转换 datetime 类型
        res['订单日期'] = pd.to_datetime(res['订单日期'])
        ## 增加年份列和月份列
        res['年份'] = res['订单日期'].dt.year
        res['月份'] = res['订单日期'].dt.month

        # year = res['年份'].unique()
        # year = sorted(year, reverse=False)
        # 创建销售额透视表
        sales = pd.pivot_table(res, index='月份', columns='年份', aggfunc=[np.sum])  # aggfunc参数可以设置我们对数据聚合时进行的函数操作。
        sales.columns = ['2011年', '2012年', '2013年', '2014年']
        sales.index = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']

        print(sales)
        x = sales.index.tolist()
        y_2011 = sales['2011年']
        y_2012 = sales['2012年']
        y_2013 = sales['2013年']
        y_2014 = sales['2014年']

        c = Line()
        c.add_xaxis(x)
        c.add_yaxis("2011年", y_2011, )
        c.add_yaxis("2012年", y_2012, )
        c.add_yaxis("2013年", y_2013, )
        c.add_yaxis("2014年", y_2014, )

        c.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        c.set_global_opts(
            title_opts=opts.TitleOpts(title="月度利润"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            yaxis_opts=opts.AxisOpts(
                name='利润',
                name_textstyle_opts=opts.TextStyleOpts(
                    font_family='Times New Roman',
                    font_size=14,
                    color='black',
                    font_weight='bolder',
                ),
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            xaxis_opts=opts.AxisOpts(name='月份', name_location='middle',
                                     name_textstyle_opts=opts.TextStyleOpts(
                                         font_family='Times New Roman',
                                         font_size=14,
                                         color='black',
                                         font_weight='bolder',
                                     ), type_="category", boundary_gap=False), )
        c.render("月度利润.html")

        return c

    ##客户类别销售，利润情况
    def customer_sale(self):
        to_drop = ['行 ID', '订单 ID', '发货日期', '邮寄方式', '客户 ID', '客户名称', '城市', '省/自治区', '国家',
                   '产品 ID', '类别', '子类别', '产品名称', '地区', '数量', '折扣']

        res = self.newRows.drop(to_drop, axis=1)
        customer_sale_dict = {}  # 销售额
        customer_profit_dict = {}  # 利润
        for i in res.itertuples():
            if i[2] not in customer_sale_dict.keys() and i[2] not in customer_profit_dict.keys():
                customer_sale_dict[i[2]]=i[3]
                customer_profit_dict[i[2]] = i[4]
            else:
                customer_sale_dict[i[2]] += i[3]
                customer_profit_dict[i[2]] += i[4]

        print("=================按消费者划分得到的销售额与利润================")
        print(customer_sale_dict)
        print(customer_profit_dict)

        y1=[]   #销售额
        for value in customer_sale_dict.values():
            y1.append(value)

        y2 = [] #利润
        for value in customer_profit_dict.values():
            y2.append(value)


        c=Bar()
        c.add_xaxis(['公司','消费者','小型企业'])
        c.add_yaxis("销售额",y1,color=Faker.rand_color())
        c.add_yaxis("利润", y2, color=Faker.rand_color())
        c.set_series_opts(label_opts=opts.LabelOpts(is_show=True))
        c.set_global_opts(
            title_opts=opts.TitleOpts(title="客户-销售额-利润"),
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"),
        )
        c.render("客户-销售额，利润.html")

        return c

    # 客户-商品子类别，销售额
    def customer_type(self):
        to_drop = ['行 ID', '订单 ID', '发货日期', '邮寄方式', '客户 ID', '客户名称', '城市', '省/自治区', '国家',
                   '产品 ID', '类别', '产品名称', '地区', '数量', '折扣','利润']

        res = self.newRows.drop(to_drop, axis=1)
        type_sale_dict = {}  # 销售额
        for i in res.itertuples():
            dict = {}
            if i[3] not in type_sale_dict.keys():
                dict[i[2]]=i[4]
                type_sale_dict[i[3]]=dict
            else:
                dict=type_sale_dict[i[3]]
                if i[2] not in dict.keys():
                    dict[i[2]]=i[4]
                else:
                    if i[2] == '公司':
                        dict['公司']+=i[4]
                    if i[2] == '消费者':
                        dict['消费者']+=i[4]
                    if i[2] == '小型企业':
                        dict['小型企业']+=i[4]
        print("========商品子类别-客户，销售额==========")
        print(type_sale_dict)

        x1=[]   #商品类别
        y1 = []  #公司销售额
        y2=[]   #消费者销售额
        y3=[]   #小型公司销售额

        for key,value in type_sale_dict.items():
            x1.append(key)
            for k,v in value.items():
               if k == '公司':
                   y1.append(v)
               if k == '消费者':
                   y2.append(v)
               if k == '小型企业':
                   y3.append(v)

        c=Bar()
        c.add_xaxis(x1)
        c.add_yaxis("公司销售额",y1)
        c.add_yaxis("消费者销售额", y2)
        c.add_yaxis("小型企业销售额", y3)

        c.reversal_axis()
        c.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        c.set_global_opts(
            title_opts=opts.TitleOpts(title="商品子类别-客户，销售额"),
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"),
        )
        c.render("商品子类别-客户，销售额.html")

        return c

    # 客户-商品子类别，利润
    def customer_profit_type(self):
        to_drop = ['行 ID', '订单 ID', '发货日期', '邮寄方式', '客户 ID', '客户名称', '城市', '省/自治区', '国家',
                   '产品 ID', '类别', '产品名称', '地区', '数量', '折扣','销售额']

        res = self.newRows.drop(to_drop, axis=1)
        type_sale_dict = {}  # 利润
        for i in res.itertuples():
            dict = {}
            if i[3] not in type_sale_dict.keys():
                dict[i[2]]=i[4]
                type_sale_dict[i[3]]=dict
            else:
                dict=type_sale_dict[i[3]]
                if i[2] not in dict.keys():
                    dict[i[2]]=i[4]
                else:
                    if i[2] == '公司':
                        dict['公司']+=i[4]
                    if i[2] == '消费者':
                        dict['消费者']+=i[4]
                    if i[2] == '小型企业':
                        dict['小型企业']+=i[4]
        print("========商品子类别-客户，利润==========")
        print(type_sale_dict)

        x1=[]   #商品类别
        y1 = []  #公司利润
        y2=[]   #消费者销售额
        y3=[]   #小型公司销售额

        for key,value in type_sale_dict.items():
            x1.append(key)
            for k,v in value.items():
               if k == '公司':
                   y1.append(v)
               if k == '消费者':
                   y2.append(v)
               if k == '小型企业':
                   y3.append(v)

        c=Bar()
        c.add_xaxis(x1)
        c.add_yaxis("公司利润",y1)
        c.add_yaxis("消费者利润", y2)
        c.add_yaxis("小型企业利润", y3)

        c.reversal_axis()
        c.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        c.set_global_opts(
            title_opts=opts.TitleOpts(title="商品子类别-客户，利润"),
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"),
        )
        c.render("商品子类别，客户，利润.html")

        return c


if __name__ == '__main__':
    a=Analyse()
    #各地区总体的销售额和利润及利润率
    #a.make_area_Bar()
    # a.make_area_pie()

    #各省/自治区销售额情况
    #a.make_province_treemap()
    #各省市的利润情况，
    # a.make_china_map()
    # a.make_city_map()

    #有哪些省市利润存在亏损
    # a.make_province_bar()
    # a.make_city_bar()

    #子类别-利润值柱形图
    #a.make_type_bar()
    #类别-环形图
    #a.make_type_roll()
    # 每个类别中的子类别排名前10
    #a.make_typetop10_bar()

    #相关性-热力图
    a.make_Heatmap()

    #年度销售额，增长率
    #a.make_saleyear_BarAndLine()
    #月度销售额，增长率
    #a.make_salemonth_BarAndLine()
    # 年度利润，增长率
    #a.make_profityear_BarAndLine()
    #月度利润
    #a.make_profitmonth_BarAndLine()

    #客户类别销售，利润情况
    #a.customer_sale()
    #客户-商品类别，销售额
    #a.customer_type()
    #客户，商品类别，利润
    #a.customer_profit_type()

    #RFM模型
    # c=RFMCustomer()
    # c.make_bar()    #8大用户的消费金额，以及消费金额占比
    # c.make_pie()    #8大用户对应的占比

