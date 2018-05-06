# -*- coding: utf-8 -*-
"""
Created on Fri May  4 09:41:40 2018

@author: Administrator
"""




import math
import requests 
from bs4 import BeautifulSoup
import re
import pandas as pd

class LouPan(object):
    def __init__(self, xiaoqu, price, total,area,house_type,location):
        # self.district = district
        # self.area = area
        self.xiaoqu = xiaoqu
        #self.address = address
        self.area = area
        self.price = price
        self.total = total
        self.house_type = house_type
        self.location = location

    def text(self):
        return self.xiaoqu + "," + \
                self.price + "," + \
                self.total + "," + \
                self.area + "," + \
                self.house_type + "," + \
                self.location
def collect_city_loupan(city_name, fmt="csv"):
    """
    将指定城市的新房楼盘数据存储下来，默认存为csv文件
    :param city_name: 城市
    :param fmt: 保存文件格式
    :return: None
    """
    global total_num, today_path
    csv_file = r'C:\Users\Administrator\Desktop\lianjia\abc.csv'
    with open(csv_file, "w",encoding = 'utf-8') as f:
        # 开始获得需要的板块数据
        loupans = get_loupan_info(city_name)
        total_num = len(loupans)
        if fmt == "csv":
            for loupan in loupans:
                f.write(loupan.text() + "\n")
    print("Finish crawl: " + city_name + ", save data to : " + csv_file)


def get_loupan_info(city_name):
    """
    爬取页面获取城市新房楼盘信息
    :param city_name: 城市
    :return: 新房楼盘信息列表
    """
    loupan_list = list()
    page = 'http://{0}.fang.lianjia.com/loupan/'.format(city_name)
    print(page)

    response = requests.get(page, timeout=10)
    html = response.content
    soup = BeautifulSoup(html, "lxml")

    # 获得总的页数
    try:
        page_box = soup.find_all('div', class_='page-box')[0]
        matches = re.search('.*data-total-count="(\d+)".*', str(page_box))
        total_page = math.ceil(int(matches.group(1)) / 10)
    except Exception as e:
        print("\tWarning: only find one page for {0}".format(city_name))
        print("\t" + e.message)
        total_page = 1

    # 从第一页开始,一直遍历到最后一页
    for i in range(1,total_page + 1):
        page = 'http://{0}.fang.lianjia.com/loupan/pg{1}'.format(city_name, i)
        print(page)
        response = requests.get(page, timeout=10)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        # 获得有小区信息的panel
        house_elements = soup.find_all('li', class_="resblock-list")
        for house_elem in house_elements:
            price = house_elem.find('span', class_="number")
            total = house_elem.find('div', class_="second")
            xiaoqu = house_elem.find('a', class_='name')
            house_type = house_elem.find('a', class_="resblock-room")
            area = house_elem.find('div', class_="resblock-area")
            location = house_elem.find('div', class_="resblock-location")
            # 继续清理数据
            try:
                price = price.text.strip()
            except Exception as e:
                price = '0'
                
            xiaoqu = xiaoqu.text.replace("\n", "")
            house_type = house_type.text.strip().replace("\n", "")
            location = location.text.strip().replace("\n", "")
            area = area.text.strip()
            try:
                total = total.text.strip().replace(u'总价', '')
                total = total.replace(u'/套起', '')
            except Exception as e:
                total = '0'

            print("{0} {1} {2} {3} {4} {5}".format(
                xiaoqu, price, total,house_type,area,location))

            # 作为对象保存
            loupan = LouPan(xiaoqu, price, total,house_type,area,location)
            loupan_list.append(loupan)
    return loupan_list

if __name__ == "__main__":

    pass