# -*- coding:utf-8  -*-
"""
time: 2020-10-11 10:05
"""
import csv
import json

from flask import Flask, render_template

from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pyecharts.charts import Bar, Pie

# 导出的csv文件路径，注意路径中全部改成 “/” 斜杠
csv_path = "C:/Users/YZ/Desktop/11.csv"

app = Flask(__name__, static_folder="templates")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/data")
def data():
    res = {
        "total_sales": None,
        "shop": None,
        "city": None,
        "goods": None
    }

    with open(csv_path, "r", encoding="utf8") as f:
        reader = csv.reader(f)

        shop_sale_count = dict()  # 店铺销售额统计
        single_goods_quantity_count = dict()  # 单品销售数量统计
        city_quantity_count = dict()  # 城市销售量统计

        rows = list(reader)
        res['total_sales'] = int(float(rows[-1][-1]))

        for row in rows[1:-1]:

            if row[0] not in single_goods_quantity_count:
                single_goods_quantity_count.update({row[0]: int(row[4])})
            else:
                single_goods_quantity_count[row[0]] += int(row[4])

            if row[2] not in shop_sale_count:
                shop_sale_count.update({row[2]: float(row[5])})
            else:
                shop_sale_count[row[2]] += float(row[5])

            if row[3] not in city_quantity_count:
                city_quantity_count.update({row[3]: int(row[4])})
            else:
                city_quantity_count[row[3]] += int(row[4])

        # 排序
        shop_sale_count = sort_dict_by_value(shop_sale_count)
        single_goods_quantity_count = sort_dict_by_value(single_goods_quantity_count, reverse=True)
        city_quantity_count = sort_dict_by_value(city_quantity_count)

        # 柱状图-商铺
        shops = list(shop_sale_count.keys())
        shop_count = [int(i) for i in shop_sale_count.values()]
        c = (
            Bar(init_opts=opts.InitOpts())
                .add_xaxis(shops)
                .add_yaxis("", shop_count, itemstyle_opts=opts.ItemStyleOpts(color="rgb(81, 220, 190)"), )
                .set_global_opts(
                title_opts=opts.TitleOpts(title="商铺销量", title_textstyle_opts=opts.TextStyleOpts(color="white")),
                xaxis_opts=opts.AxisOpts(axislabel_opts={"interval": 0, "rotate": -20, "color": "white"}),
                yaxis_opts=opts.AxisOpts(axislabel_opts={"color": "white"})
            )
        )
        res["shop"] = json.loads(c.dump_options_with_quotes())

        # 柱状图-单品销量
        goods = list(single_goods_quantity_count.keys())
        goods = [i.split("-")[-1] for i in goods if "-" in i]
        goods = [j.replace("2020v1", "") for j in goods]
        goods = [k.replace("2020V1", "") for k in goods]
        goods_count = list(single_goods_quantity_count.values())
        c = (
            Bar()
                .add_xaxis(goods)
                .add_yaxis("", goods_count, itemstyle_opts=opts.ItemStyleOpts(color="rgb(43, 167, 255)"))
                # .reversal_axis()
                .set_global_opts(
                title_opts=opts.TitleOpts(title="单品销量", title_textstyle_opts=opts.TextStyleOpts(color="white")),
                xaxis_opts=opts.AxisOpts(axislabel_opts={"color": "white", "interval": 0, "rotate": -45, }),
                yaxis_opts=opts.AxisOpts(axislabel_opts={"color": "white"}))
        )
        res["goods"] = json.loads(c.dump_options_with_quotes())

        # 饼图-城市销量
        city_data = list(tuple(city_quantity_count.items()))
        c = (
            Pie().add(data_pair=city_data, series_name="城市销量", radius=("50%", "70%"), )
                .set_global_opts(title_opts=opts.TitleOpts(title="城市销量", title_textstyle_opts=opts.TextStyleOpts(color="white")),
                                 legend_opts=opts.LegendOpts(is_show=False))
        )
        res["city"] = json.loads(c.dump_options_with_quotes())

    return json.dumps(res)


def sort_dict_by_value(dic: dict, reverse=True) -> dict:
    t = tuple(dic.items())
    return dict(sorted(t, key=lambda kv: kv[1], reverse=reverse))


if __name__ == "__main__":
    app.run()
