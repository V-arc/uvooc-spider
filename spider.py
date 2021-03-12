import os
import re
import time

import requests

start_url = r'https://pan.uvooc.com/Learn/CV/'
start_path = r'UVOOC爬虫\CV'
if_cover_file = False  # 是否覆盖下载

host = "https://pan.uvooc.com"

li_folder_pattern = re.compile(
    r'<li class="mdui-list-item mdui-ripple">.*?</li>', re.S)
li_file_pattern = re.compile(
    r'<li class="mdui-list-item file mdui-ripple">.*?</li>', re.S)
li_url_pattern = re.compile(r'<a href="(.*?)"', re.S)
li_span_pattern = re.compile(r'<span>(.*?)</span>', re.S)


def download(url, path, filename):
    # 判断是否需要覆盖
    file_path = os.path.join(path, filename)
    if((not if_cover_file) and os.path.exists(file_path)):
        print(file_path, "已存在")
        return
    # 目录不存在则创建目录
    if not os.path.exists(path):
        os.makedirs(path)
    print(path + filename, "下载中")
    # 下载文件到指定目录
    r = requests.get(url)
    with open(file_path, "wb") as f:
        f.write(r.content)
    print("下载完成，等待3秒")
    time.sleep(3)


def get_folders_from_urlhtml(father_url_html):
    result_list = []
    li_list = li_folder_pattern.findall(father_url_html)
    for li in li_list:
        # 跳过父目录
        if(".." in li):
            continue
        temp = []
        temp.append(li_url_pattern.search(li).group(1))
        temp.append(li_span_pattern.search(li).group(1))
        result_list.append(temp)
    return result_list


def get_files_from_urlhtml(father_url_html):
    result_list = []
    li_list = li_file_pattern.findall(father_url_html)
    for li in li_list:
        temp = []
        temp.append(li_url_pattern.search(li).group(1))
        temp.append(li_span_pattern.search(li).group(1))
        result_list.append(temp)
    return result_list


def deal_url(url, now_path):
    r = requests.get(url)
    r.encoding = "utf-8"
    html = r.text
    folders = get_folders_from_urlhtml(html)
    files = get_files_from_urlhtml(html)
    for folder in folders:
        deal_url(host + folder[0], os.path.join(now_path, folder[1]))
    for file in files:
        download(host + file[0], now_path, file[1])


if(__name__ == "__main__"):
    deal_url(start_url, start_path)
    print("全部下载完成")
