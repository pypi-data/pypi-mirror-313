from yplib.chart_html import *
from yplib.index import *


def to_html(html_list, name=None):
    name = 'html' if name is None else name
    to_txt(data_list=html_list,
           file_name=str(name),
           file_name_is_date=True,
           file_path='html',
           fixed_name=False,
           suffix='.html')


# text_list = [{
#     name: '王小虎',
#     text: '上海市普陀区金沙江路 1518 弄'
# }, {
#     name: '王小虎',
#     text: '上海市普陀区金沙江路 1517 弄'
# }, {
#     name: '王小虎',
#     text: '上海市普陀区金沙江路 1516 弄'
# }]
def to_text_html(text_list, title=None, return_file=True):
    title = 'text' if title is None else title
    h_d = text_list_html(text_list, title)
    if return_file:
        to_html(h_d, title)
    else:
        return h_d


# table的 html 模板代码
# table_list = [{
#     date: '2016-05-02',
#     name: '王小虎',
#     address: '上海市普陀区金沙江路 1518 弄'
# }, {
#     date: '2016-05-04',
#     name: '王小虎',
#     address: '上海市普陀区金沙江路 1517 弄'
# }, {
#     date: '2016-05-03',
#     name: '王小虎',
#     address: '上海市普陀区金沙江路 1516 弄'
# }]
# title = {
#     date: '日期',
#     name: '名称',
#     address: '地址'
# }
# 以下另外另外一种 api
# table_list : table = [
#       ['x轴的数据', 'line1', 'line2', 'line3'],
#       ['2020-01-01', 120, 132, 101],
#       ['2020-01-02', 100, 102, 131],
#       ['2020-01-03', 123, 165, 157],
#       ['2020-01-04', 126, 109, 189],
#       ['2020-01-05', 150, 156, 128],
#       ['2020-01-06', 178, 134, 140],
#       ['2020-01-07', 157, 148, 161],
#  ]
def to_table_html(table, title=None, name=None, return_file=True):
    header = []
    table_list = []
    # 是一种两个 list 的形式的 api
    is_list = False
    if isinstance(table[0], list) or isinstance(table[0], tuple) or isinstance(table[0], set):
        is_list = True
    if is_list:
        first_line = table[0]
        for o_obj in first_line:
            header.append(str(o_obj) + ": '" + str(o_obj) + "'")
        for o_line in table[1:]:
            l = []
            for i in range(len(o_line)):
                l.append(str(first_line[i]) + ': "' + str(o_line[i]) + '"')
            table_list.append('{' + ', '.join(l) + '}')
    else:
        if title is None:
            title = {}
            for k in table[0]:
                title[k] = k
        for obj_one in table:
            l = []
            for k in obj_one:
                l.append(str(k) + ': "' + str(obj_one[k]) + '"')
            table_list.append('{' + ', '.join(l) + '}')
        for k in title:
            header.append(str(k) + ": '" + str(title[k]) + "'")
    name = 'table' if name is None else name
    h_d = table_list_html(table_list, header, name)
    if return_file:
        to_html(h_d, name)
    else:
        return h_d


# 将 html 中的占位符 替换成数据
# 并且 导出 生成后的 html 文件
def insert_data_to_chart(html_data,
                         name=None,
                         x_list=None,
                         y_list=None,
                         legend=None,
                         series=None,
                         smooth=0,
                         return_file=True):
    p_list = [
        'chart_name', 'name', 'x_list', 'y_list', 'legend', 'series', 'smooth'
    ]
    p_data_list = [
        name, name, x_list, y_list, legend, series, smooth
    ]
    h_r = []
    for html_line in html_data:
        for index in range(len(p_list)):
            one_p = p_list[index]
            one_data = p_data_list[index]
            if one_data is None:
                continue
            one_p = f'-{one_p}-'
            if one_p in html_line:
                html_line = html_line.replace(one_p, str(one_data))
        h_r.append(html_line)
    if return_file:
        to_html(h_r, name)
    else:
        return h_r


# 将数据整理成折线图
# 情况1:
# x轴数据 : x_list = [
#       ['x轴的数据', 'line1', 'line2', 'line3'],
#       ['2020-01-01', 120, 132, 101],
#       ['2020-01-02', 100, 102, 131],
#       ['2020-01-03', 123, 165, 157],
#       ['2020-01-04', 126, 109, 189],
#       ['2020-01-05', 150, 156, 128],
#       ['2020-01-06', 178, 134, 140],
#       ['2020-01-07', 157, 148, 161],
#  ]
#  --- 以上这种情况,当 y_list 为空的时候,就说明有可能是这种情况
#  --- 以上这种情况,数据与 excel 中的数据对齐
# 情况2:
# x轴数据 : x_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
# y轴数据 : y_list = [
#     [120, 132, 101, 134, 90, 230, 210],
# 	  [220, 182, 191, 234, 290, 330, 310],
# 	  [150, 232, 201, 154, 190, 330, 410],
# 	  [320, 332, 301, 334, 390, 330, 320],
# 	  [820, 932, 901, 934, 1290, 1330, 1320]
# ]
# 情况3--标准情况下的数据:
# x轴数据 : x_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
# y轴数据 : y_list = [
#             {
#                 name: 'Email',
#                 hide: True,
#                 smooth: True,
#                 data: [120, 132, 101, 134, 90, 230, 210],
#             },
#             {
#                 name: 'Union Ads',
#                 hide: 1,
#                 smooth: 1,
#                 data: [220, 182, 191, 234, 290, 330, 310],
#             },
#             {
#                 name: 'Video Ads',
#                 data: [150, 232, 201, 154, 190, 330, 410],
#             },
#             {
#                 name: 'Direct',
#                 data: [320, 332, 301, 334, 390, 330, 320],
#             },
#             {
#                 name: 'Search Engine',
#                 data: [820, 932, 901, 934, 1290, 1330, 1320],
#             },
#         ]
#  name : 文件名称,折线图的名称
#  name_raw : 用原始的名字,不用带上属性 line_stack
def to_chart(x_list,
             y_list=None,
             name=None,
             name_raw=False,
             return_file=True):
    # 当 y_list 没有的话, 需要整理出 y_list 的数据
    if y_list is None:
        data_list = x_list
        x_list = []
        y_list = []
        for index in range(len(data_list)):
            line_one = data_list[index]
            # 第一行数据
            if index == 0:
                for y in range(1, len(line_one)):
                    y_list.append({'name': line_one[y], 'data': []})
            # 第二行开始的数据
            if index > 0:
                x_list.append(line_one[0])
                for y in range(1, len(line_one)):
                    y_list[y - 1]['data'].append(line_one[y])
    name_list = []
    name_hide = {}
    for y_index in range(len(y_list)):
        y_one = y_list[y_index]
        name_one = y_one['name'] if 'name' in y_one else str(y_index + 1) + '_' + random_letter(3)
        name_list.append(str(name_one))
        if 'hide' in y_one and y_one['hide']:
            name_hide[name_one] = 0
    legend = 'data: ' + str(name_list) + ',\n            selected: ' + str(name_hide)
    # {
    #     name: 'Email',
    #     type: 'line',
    #     smooth: 1,
    #     data: [120, 132, 101, 134, 90, 230, 210],
    # }
    # [120, 132, 101, 134, 90, 230, 210],
    series = []
    for y_index in range(len(y_list)):
        y_o = {}
        y_one = y_list[y_index]
        y_o['name'] = name_list[y_index]
        y_o['data'] = y_one['data'] if 'data' in y_one else y_one
        y_o['type'] = 'line'
        if 'smooth' in y_one and y_one['smooth']:
            y_o['smooth'] = 1
        # 只有一条线,就不显示 name 了
        if len(y_list) == 1:
            del y_o['name']
        series.append(y_o)

    if not name_raw:
        # name = 'line_stack' if name is None else name + '_line_stack'
        name = 'line_stack' if name is None else name
    return insert_data_to_chart(html_data=line_stack_html(),
                                name=name,
                                x_list=x_list,
                                legend=legend,
                                series=series,
                                return_file=return_file)


# 即使用 table 也使用 chart
# 情况1:
# x轴数据 : x_list = [
#       ['x轴的数据', 'line1', 'line2', 'line3'],
#       ['2020-01-01', 120, 132, 101],
#       ['2020-01-02', 100, 102, 131],
#       ['2020-01-03', 123, 165, 157],
#       ['2020-01-04', 126, 109, 189],
#       ['2020-01-05', 150, 156, 128],
#       ['2020-01-06', 178, 134, 140],
#       ['2020-01-07', 157, 148, 161],
#  ]
#  --- 以上这种情况,当 y_list 为空的时候,就说明有可能是这种情况
#  --- 以上这种情况,数据与 excel 中的数据对齐
# 情况2:
# x轴数据 : x_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
# y轴数据 : y_list = [
#     [120, 132, 101, 134, 90, 230, 210],
# 	  [220, 182, 191, 234, 290, 330, 310],
# 	  [150, 232, 201, 154, 190, 330, 410],
# 	  [320, 332, 301, 334, 390, 330, 320],
# 	  [820, 932, 901, 934, 1290, 1330, 1320]
# ]
def to_chart_table(x_list=[],
                   y_list=None,
                   name=None,
                   name_raw=False):
    html_chart = to_chart(x_list, y_list, name, name_raw, False)
    if y_list is not None:
        x_list.extend(y_list)
    html_table = to_table_html(x_list, None, name, False)
    html_chart.extend(html_table)
    to_html(html_chart, name)


# 生成 chart , table , text 的操作
def to_chart_table_text(x_list=[],
                        y_list=None,
                        text_list=None,
                        name=None,
                        name_raw=False):
    html_chart = to_chart(x_list, y_list, name, name_raw, False)
    if y_list is not None:
        x_list.extend(y_list)
    html_table = to_table_html(x_list, None, name, False)
    html_chart.extend(html_table)
    if text_list is not None:
        # 生成 text 的操作
        text_html = to_text_html(text_list, name, False)
        html_chart.extend(text_html)
    to_html(html_chart, name)


# 将数据整理成折线图
# 一条折线
# 数据 : data_list = [
#             ['2020-01-01', 132],
#             ['2021-01-01', 181],
#             ['2022-01-01', 147]
#         ]
# x_index : x 轴数据的下标
# y_index : y 轴数据的下标
# 或者
# 数据 : data = [
#        {name: "Search Engine", value: 1048 },
#        {name: "Direct", value: 735 },
#        {name: "Email", value:580 },
#        {name: "Union Ads", value:484 },
#        {name: "Video Ads", value:300 }
#       }]
#  x_key : 当元素为对象的时候, x 的 key
#  y_key : 当元素为对象的时候, y 的 key
# is_area : 是否使用 area 图
# smooth : 曲线是否平滑
def to_chart_one(data_list,
                 name=None,
                 x_index=0,
                 x_key='name',
                 y_index=1,
                 y_key='value',
                 is_area=False,
                 smooth=False):
    x_list = []
    y_list = []
    name = 'line' if name is None else name + '_line'
    name = name + '_smooth' if smooth else name
    name = name + '_area' if is_area else name
    sm = 1 if smooth else 0
    for d_one in data_list:
        if isinstance(d_one, list):
            x = d_one[x_index]
            y = d_one[y_index]
        else:
            x = d_one[x_key]
            y = d_one[y_key]
        x_list.append(x)
        y_list.append(y)
    if is_area:
        insert_data_to_chart(html_data=line_area_html(),
                             name=name,
                             x_list=x_list,
                             y_list=y_list,
                             smooth=sm)
    else:
        to_chart(x_list=x_list,
                 y_list=[{'name': name, 'data': y_list, 'smooth': sm}],
                 name=name,
                 name_raw=True)


# 将数据整理成饼状图
# 数据 : data = [
#         { value: 1048, name: "Search Engine" },
#         { value: 735, name: "Direct" },
#         { value: 580, name: "Email" },
#         { value: 484, name: "Union Ads" },
#         { value: 300, name: "Video Ads" }
#       ]
#  name_key : 当元素为对象的时候, x 的 key
#  value_key : 当元素为对象的时候, y 的 key
# 或者
# 数据 : data = [
#         [ "Search Engine", 1048 ],
#         [ "Direct", 735 ],
#         [ "Email",580 ],
#         [ "Union Ads",484 ],
#         [ "Video Ads",300 ]
#       ]
#  name_index : 当元素为数组的时候, name 的下标
#  value_index : 当元素为数组的时候, value 的下标
def to_chart_pie(data_list,
                 name=None,
                 name_index=0,
                 name_key='name',
                 value_index=1,
                 value_key='value'):
    x_list = []
    name = 'pie' if name is None else name + '_pie'
    for one_data in data_list:
        if isinstance(one_data, list):
            x = one_data[name_index]
            y = one_data[value_index]
        else:
            x = one_data[name_key]
            y = one_data[value_key]
        x_list.append({'name': x, 'value': y})
    insert_data_to_chart(html_data=pie_html(),
                         name=name,
                         x_list=x_list)


# 将数据整理成柱状图
# 数据 : data = [
#         { value: 1048, name: "Search Engine" },
#         { value: 735, name: "Direct" },
#         { value: 580, name: "Email" },
#         { value: 484, name: "Union Ads" },
#         { value: 300, name: "Video Ads" }
#       ]
#  name_key : 当元素为对象的时候, x 的 key
#  value_key : 当元素为对象的时候, y 的 key
# 或者
# 数据 : data = [
#         [ "Search Engine", 1048 ],
#         [ "Direct", 735 ],
#         [ "Email",580 ],
#         [ "Union Ads",484 ],
#         [ "Video Ads",300 ]
#       ]
#  name_index : 当元素为数组的时候, name 的下标
#  value_index : 当元素为数组的时候, value 的下标
def to_chart_bar(data_list,
                 name=None,
                 name_index=0,
                 name_key='name',
                 value_index=1,
                 value_key='value'):
    x_list = []
    y_list = []
    name = 'bar' if name is None else name + '_bar'
    for one_data in data_list:
        if isinstance(one_data, list):
            x = one_data[name_index]
            y = one_data[value_index]
        else:
            x = one_data[name_key]
            y = one_data[value_key]
        x_list.append(x)
        y_list.append(y)
    insert_data_to_chart(html_data=bar_html(),
                         name=name,
                         x_list=x_list,
                         y_list=y_list)
