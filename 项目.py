"""
重庆2021年空气质量分析
"""
import requests
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from bs4 import BeautifulSoup

#数据
def get_data(url):
    r=requests.get(url)
    #print(r)
    #print(r.text) #文本形式返回网页源代码，检查是否一致

    #解析数据
    html = r.text
    soup = BeautifulSoup(html, 'html.parser') #html.parser/lxml为解析器
    #print(soup)
 
    #数据提取和分析
    #检查，找到所需数据项的标签，这里是tr
    tr_list = soup.find_all('tr') 
    #print(tr_list)
    dates, air_quality, PM2_5 = [], [], []
    for data in tr_list[1:]:
        data1 = data.text.split() #获取汉字信息并去除空格
        #print(data1)
        current_date = datetime.datetime.strptime(data1[0], '%Y-%m-%d')
        dates.append(current_date)
        air_quality.append(data1[1])
        data1[4] = int(data1[4])#保存数据时要保存为int形式，否则y轴数值顺序不对
        PM2_5.append(data1[4])
    #print(dates)
    #print(air_quality)
    #print(PM2_5)
    df = pd.DataFrame()
    df['日期'] = dates
    df['空气质量'] = air_quality
    df['PM2.5'] = PM2_5
    #print(df['日期'][0].month)
    #print(df)
    return (df)


#绘制每个月的PM2.5的折线图，横坐标为日期，纵坐标为PM2.5指数
def draw_PM2_5(df):
    plt.style.use('seaborn')
    plt.rcParams['font.sans-serif']='SimHei'#设置中文显示
    #print(df['日期'], df['PM2.5'])
    fig, ax = plt.subplots() #fig表示整张图片，ax表示各个图表
    ax.plot(df['日期'], df['PM2.5'], marker='o')
    ax.set_title(f"重庆2021年{df['日期'][0].month}月PM2.5分布图")
    ax.set_xlabel('日期')
    fig.autofmt_xdate()#绘制倾斜的日期
    ax.set_ylabel('PM2.5')
    #显示数据
    for a, b in zip(df['日期'], df['PM2.5']):
        plt.text(a, b, b, ha = 'center', va = 'bottom', fontsize = 10)
    #ha:水平对齐方式；va:垂直对齐方式
    plt.show()


#绘制每个月空气质量的饼状图
def air_pie(df):
    count1, count2, count3, count4 = 0, 0, 0, 0
    for air in df['空气质量']:
        if (air == '优'):
            count1 += 1
        elif (air == '良'):
            count2 += 1
        elif (air == '轻度污染'):
            count3 += 1
        else:
            count4 += 1
    plt.rcParams['font.sans-serif']='SimHei'#指定字体为‘SimHei’,中文显示
    plt.figure(figsize=(6,6))#将画布设定为正方形，则绘制的饼图是正圆
    label=['优','良','轻度污染', '中度污染']#定义饼图的标签，标签是列表
    explode=[0.01, 0.01, 0.01, 0.01]#设定各项距离圆心n个半径
    values=[count1, count2, count3, count4]
    color = ['limegreen', 'gold', 'orange', 'red']
    plt.pie(values, explode=explode, labels=label, colors = color, autopct='%1.1f%%')#绘制饼图
    #autopct为特定的string，默认是None。指定数值的显示方式。
    plt.title(f"重庆2021年{df['日期'][0].month}月空气质量分布图")#绘制标题
    plt.show()


#4个月空气质量的柱状图，横坐标为空气质量，纵坐标为天数
def count_excellent(df1, df2, df3, df4):
    df = pd.concat([df1, df2, df3, df4])
    #print(df)
    count1, count2, count3, count4 = 0, 0, 0, 0
    for air in df['空气质量']:
        if (air == '优'):
            count1 += 1
        elif (air == '良'):
            count2 += 1
        elif (air == '轻度污染'):
            count3 += 1
        else:
            count4 += 1
    print(count1, count2, count3, count4) 
    plt.rcParams['font.sans-serif']='SimHei'
    x_list = ['优','良','轻度污染','重度污染']  
    y_list = [count1, count2, count3, count4]  
    plt.bar(x_list, y_list)
    #显示数据
    for a, b in zip(x_list, y_list):
        plt.text(a, b, b, ha = 'center', va = 'bottom', fontsize = 10)
    """
    另一种显示数据的方式
    rects = plt.bar(x_list, y_list) 
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2.-0.2, 1.03*height, '%s' % int(height))
    """
    plt.xlabel('空气质量')
    plt.ylabel('天数')
    plt.title("重庆2021年截至4月底空气质量分布图")
    plt.show()


if __name__=="__main__":
    print("------------------------菜单-----------------------")
    print("|   1.查看重庆2021年至4月份各月份PM2.5的折线图     |")
    print("|   2.查看重庆2021年至4月份各月份空气质量的饼状图   |")
    print("|   3.查看重庆2021年至4月份空气质量的柱状图         |")
    df1 = get_data('http://www.tianqihoubao.com/aqi/chongqing-202101.html')
    df2 = get_data('http://www.tianqihoubao.com/aqi/chongqing-202102.html')
    df3 = get_data('http://www.tianqihoubao.com/aqi/chongqing-202103.html')
    df4 = get_data('http://www.tianqihoubao.com/aqi/chongqing-202104.html')
    continues = 'y'
    while (continues == 'y'):
        select = int(input("请输入选项:"))
        if (select == 1):
            month = int(input("请输入待查看的月份（1-4）:"))
            if (month == 1):
                draw_PM2_5(df1)
            elif (month == 2):
                draw_PM2_5(df2)
            elif (month == 3):
                draw_PM2_5(df3)
            elif (month == 4):
                draw_PM2_5(df4)
            else:
                print("输入错误！")
            continues = input("是否继续？（y/n）")
        elif (select == 2):
            month = int(input("请输入待查看的月份（1-4）:"))
            if (month == 1):
                air_pie(df1)
            elif (month == 2):
                air_pie(df2)
            elif (month == 3):
                air_pie(df3)
            elif (month == 4):
                air_pie(df4)
            else:
                print("输入错误！")
            continues = input("是否继续？（y/n）")
        elif (select == 3):
            count_excellent(df1, df2, df3, df4)
            continues = input("是否继续？（y/n）")
        else:
            print("输入错误")
    print("欢迎下次查询！")