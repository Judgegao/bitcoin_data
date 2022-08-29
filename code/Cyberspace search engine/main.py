import csv
import tqdm
import zoomeye.sdk as zoomeye
import json
import os
# 第一步读取文件
# 获得IP地址
# 使用SDK查询信息
# 保存信息
# 过滤信息

INPUT_FILE_NAME = '../csv/firewall_ip.csv'
# OUTPUT_FILE_NAME = 'csv/result.csv'


def read_csv(ip_list, csv_name):
    with open(csv_name) as f:
        f_csv = csv.reader(f)
        # 获取header
        headers = next(f_csv)
        # 循环获取每一行的内容
        for row in f_csv:
            ip_list.append(row[0])


def init_zoomeye():
    zm = zoomeye.ZoomEye()
    zm.username = '********'
    zm.password = '********'
    zm.login()
    return zm


def zoomeye_sdk(ip, zm):
    data = zm.dork_search(ip, resource="host", facets=None)
    return data


def write_file(data, ip, file_name):
    # f = open(file_name, "w")
    # json_data
    json_data = {}
    # key
    ip = ip
    # value
    value = {}
    for service in data:
        # 构造字典类型 {ip:{service:{content},service:{content}}}
        # key
        key = service['portinfo']['service']
        # value
        content = service
        # item service:{content}
        item = {key: content}
        value.update(item)

    json_data = {"ip": ip, "result": value}
    with open("../result_5688/"+file_name, "w") as f:
        json.dump(json_data, f)
    print("写入"+file_name+"文件")


def search_ip(ip_list):
    dir_list = []
    read_result_5688(dir_list)
    # print(len(dir_list))
    zm = init_zoomeye()
    for ip in tqdm.tqdm(ip_list):
        print("正在处理的IP为", ip)
        if ip not in dir_list:
            data = zoomeye_sdk(ip, zm)
            for i in data:
                print(i)
                print("----------------")
            #write_file(data, ip, ip+".json")
            print(data)
        else:
            print(ip+"存在文件中")


def read_result_5688(dir_list):
    path = "../result_5688/"
    files = os.listdir(path)
    for filename in files:
        dir_list.append(os.path.splitext(filename)[0])


def main():
    # 用来保存待查找的IP
    ip_list = []

    csv_name = INPUT_FILE_NAME
    read_csv(ip_list, csv_name)
    print("准备查找的列表为："+str(ip_list))
    # print(dir_list)
    search_ip(ip_list)


if __name__ == '__main__':
    main()