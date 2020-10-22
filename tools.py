# -*- coding:utf-8  -*-
"""
time: 2020-10-11 10:06 
"""
import csv

with open("11.csv", "r") as f:
    reader = csv.reader(f)

    shop_sale_count = dict()  # 店铺销售额统计
    single_goods_quantity_count = dict()  # 单品销售数量统计
    city_quantity_count = dict()  # 城市销售量统计

    rows = list(reader)
    total_sales = int(float(rows[-1][-1]))
    print(total_sales)

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

    # 柱状图
    shops = list(shop_sale_count.keys())
    shop_count = [int(i) for i in shop_sale_count.values()]

    goods = list(single_goods_quantity_count.keys())
    goods_count = list(single_goods_quantity_count.values())

    # 饼图
    city_data = [{"name": k, "value": city_quantity_count[k]} for k in city_quantity_count.keys()]
