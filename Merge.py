#-*- codeing=utf-8 -*-
#@Time:2022/6/16 9:40
#@Author:王钰娜
#@File : Merge.py
#@Software:PyCharm

from supermarket_analyse import Analyse
from RFMCustomer import RFMCustomer
from pyecharts.charts import Page,Bar
import pyecharts.options as opts
from pyecharts.components import Table
def pic_bar():
	pic = Bar(init_opts=opts.InitOpts(width="800px", height="600px"))
	pic.set_global_opts(

		graphic_opts=[
			opts.GraphicImage(
				graphic_item=opts.GraphicItem(
					id_="logo", right=20, top=8, z=-10, bounding="raw",
				),
				graphic_imagestyle_opts=opts.GraphicImageStyleOpts(
					image='各类型顾客消费额及其累加占比.png',
					width=800,
					height=600,
				),
			)
		], )

	return pic
def pic_reli():
	pic=Bar(init_opts=opts.InitOpts(width="800px",height="600px"))
	pic.set_global_opts(

	graphic_opts = [
					   opts.GraphicImage(
						   graphic_item=opts.GraphicItem(
							   id_="logo", right=20, top=8, z=-10, bounding="raw",
						   ),
						   graphic_imagestyle_opts=opts.GraphicImageStyleOpts(
							   image='热力图.png',
							   width=800,
							   height=600,
							   ),
					   )
				   ],)

	return pic
def text_line(text):
		table = Table()
		table.add(headers=[text], rows=[])
		#table.render(text+'.html')
		print('生成完毕:'+text+'.html')
		return table
a = Analyse()
c = RFMCustomer()
page = Page(layout=Page.DraggablePageLayout, page_title="超市数据分析")

# 在页面中添加图表
page.add(
		a.make_area_Bar(),  # 堆叠柱状图显示各地区总体的销售额，利润，成本
		a.make_area_pie(),  # 各地区总体的利润率 占比
		#
		a.make_china_map(),  #以省展示利润亏损情况
		a.make_city_map(),   #各市利润情况
		a.make_province_bar(),  #统计利润亏损的省/自治区
		a.make_city_bar(),   #统计利润亏损的市
		a.make_province_treemap(),   # 各省/自治区销售额情况 矩形树图
		#
		#
		a.make_type_bar(),   # 子类别-利润值柱形图
		a.make_type_roll(),	 #类别-环形图
)
page.add(
		a.make_typetop10_bar(),#每个类别中的子类别排名前10，因为要构建3个柱形图则要有3个返回值，因为每个函数都要有返回值，所以make_type_10_bar()虽然是处理数据得到三个图表的x[],y[]，但为了要返回值，则让这个函数返回家具类图表
		#a.make_bar1()
		a.make_bar2(),	# #办公用品类
		a.make_bar3(),	##技术
		#
		#a.make_Heatmap(),	#销售额、数量、折扣、利润、时间、商品类别的相关性
		#
		a.make_saleyear_BarAndLine(),	#年度销售额，销售额增长率
		a.make_salemonth_BarAndLine(),	# 月度销售额
		a.make_profityear_BarAndLine(),	# 年度利润及增长率
		a.make_profitmonth_BarAndLine(),# 月度利润
		#
		a.customer_sale(),	##客户类别销售，利润情况
		a.customer_type(),	# 客户-商品子类别，销售额
		a.customer_profit_type()# 客户-商品子类别，利润
	)
page.add(
		# 生成几个文本
		text_line("地区分析"),
		text_line("商品类别分析"),
		text_line("客户分析"),

		#添加热力图
		pic_reli(),	#销售额、数量、折扣、利润、时间、商品类别的相关性



	)
page.add(
	#RFM模型
	c.make_pie(),	#顾客分层结构
	# c.make_bar()

	pic_bar()	#添加各类型顾客消费额及其累加占比
	)
page.render('大屏_临时.html')  # 执行完毕后,打开临时html并排版,排版完点击Save Config，把json文件放到本目录下
print('生成完毕:大屏_临时.html')