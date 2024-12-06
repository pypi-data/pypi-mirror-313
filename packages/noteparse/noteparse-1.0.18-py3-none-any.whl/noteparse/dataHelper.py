# -*- coding: UTF-8 -*-
"""
@File    ：dataHelper.py
@Author  ：VerSion/08398
@Date    ：2023/12/07 14:29 
@Corp    ：Uniview
"""
import json
import os
import time

import pymysql
import requests

db_config = {
    'host': '10.220.6.138',
    'port': 3306,
    'user': 'root',
    'password': '*Ab123456',
    'db': 'unvbasicx_khgz'
}


def write_log(announce_list, province_key):
    print('正在写入日志...')
    # 记录日志
    try:
        # 获取当前脚本所在的目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 创建log文件夹
        log_folder = os.path.join(current_dir, 'log')
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)
        # 获取当前时间
        current_time = time.strftime("%Y-%m-%d", time.localtime())
        # 导出JSON到文件
        file_name = f"{current_time}_{province_key}.json"
        file_path = os.path.join(log_folder, file_name)
        announce_dict = [item.__json__() for item in announce_list]
        with open(file_path, 'a', encoding='utf-8') as file:
            json.dump(announce_dict, file, ensure_ascii=False)
        print(f"JSON已成功导出到文件: {file_path}")
    except Exception as log_ex:
        print('日志写入异常：' + str(log_ex))
        raise Exception('日志写入异常：' + str(log_ex))
    return file_path


def upload_datas(announce_list, province_key):
    upload_msg = ''
    # 上传数据
    try:
        upload_url = 'http://10.220.6.138/api/khgz/project'
        headers = {
            'Content-Type': 'application/json'
        }

        upload_response = requests.post(upload_url, headers=headers,
                                        data=json.dumps([item.__json__() for item in announce_list],
                                                        ensure_ascii=False).encode('utf-8'))

        if upload_response.status_code == 200:
            upload_result = json.loads(upload_response.text)
            if upload_result['ok']:
                upload_msg = f'\033[1;33;42m数据上传成功\033[0m'
            else:
                upload_msg = f'\033[1;31;40m数据上传失败，详细信息：{upload_result["msg"]}\033[0m'
        else:
            upload_msg = f'数据上传失败，错误码：{upload_response.status_code}'
    except Exception as upload_ex:
        upload_msg = '数据上传异常：' + str(upload_ex)
        raise Exception('数据上传异常：' + str(upload_ex))
    finally:
        # 获取当前脚本所在的目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 创建log文件夹
        log_folder = os.path.join(current_dir, 'log')
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)
        # 获取当前时间
        current_time = time.strftime("%Y-%m-%d", time.localtime())
        # 导出JSON到文件
        file_name = f"{current_time}_数据上传.json"
        file_path = os.path.join(log_folder, file_name)
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(f'\n[{province_key}]数据上传日志 => ' + upload_msg)
            print(upload_msg)


def excute_sql(sql_str):
    # 连接数据库
    conn = pymysql.connect(host=db_config.get('host', ''), port=db_config.get('port', ''),
                           user=db_config.get('user', ''), password=db_config.get('password', ''),
                           db=db_config.get('db', ''))
    # 创建游标对象
    with conn.cursor() as cursor:
        # 执行SQL语句
        cursor.execute(sql_str)
    # 提交更改
    conn.commit()


def execute_sql_query(sql_query):
    # 建立数据库连接
    conn = pymysql.connect(host=db_config.get('host', ''), port=db_config.get('port', ''),
                           user=db_config.get('user', ''), password=db_config.get('password', ''),
                           db=db_config.get('db', ''))
    # 创建游标对象
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        # 执行 SQL 查询
        cursor.execute(sql_query)
        # 获取查询结果
        result = cursor.fetchall()

        return result

    except Exception as e:
        # 如果发生异常，回滚事务
        conn.rollback()
        raise Exception('数据库查询异常：' + str(e))

    finally:
        # 关闭游标和连接
        cursor.close()
        conn.close()


def insert_engineering_datas(engineering_list):
    print('正在写入数据...')
    template_sql = "INSERT INTO tbl_engineering_project (project_name, project_number, publish_date, version_type, project_stage, province_id, city_id, area_id, origin_location, address, construction_period, investment_amount, total_investment, engineering_type, client_type, industry, building_area, land_occupation_area,decoration_situation, foreign_investment, topic, project_scale, installed_capacity, industry_level, project_overview, construction_desc, procures_equipment, client_infos, designer_infos, epcs_infos, contractor_infos, subcontractor_infos, project_link,special_name, data_source, data_source_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    data = []
    for item in engineering_list:
        data.append((item.project_name,
                     item.project_number,
                     item.publish_date,
                     item.version_type,
                     item.project_stage,
                     item.province_id,
                     item.city_id,
                     item.area_id,
                     item.origin_location,
                     item.address,
                     item.construction_period,
                     item.investment_amount,
                     item.total_investment,
                     item.engineering_type,
                     item.client_type,
                     item.industry,
                     item.building_area,
                     item.land_occupation_area,
                     item.decoration_situation,
                     item.foreign_investment,
                     item.topic,
                     item.project_scale,
                     item.installed_capacity,
                     item.industry_level,
                     item.project_overview,
                     item.construction_desc,
                     item.procures_equipment,
                     item.client_infos,
                     item.designer_infos,
                     item.epcs_infos,
                     item.contractor_infos,
                     item.subcontractor_infos,
                     item.project_link,
                     item.special_name,
                     item.data_source,
                     item.data_source_id))

    err_msg = ''
    try:
        # 连接数据库
        conn = pymysql.connect(host='10.220.6.138', port=3306, user='root', password='*Ab123456', db='unvbasicx_khgz')
        # 创建游标对象
        with conn.cursor() as cursor:
            # 执行SQL语句
            cursor.executemany(template_sql, data)
        # 提交更改
        conn.commit()

        err_msg = f'写入数据成功！本次写入 {len(engineering_list)} 条数据。'
        print(f'写入数据成功！本次写入 {len(engineering_list)} 条数据。')
    except Exception as sql_ex:
        err_msg = '数据写入数据库异常：' + str(sql_ex)
        raise Exception('数据写入数据库异常：' + str(sql_ex))
    finally:
        # 获取当前脚本所在的目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 创建log文件夹
        log_folder = os.path.join(current_dir, 'log')
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)
        # 获取当前时间
        current_time = time.strftime("%Y-%m-%d", time.localtime())
        # 导出JSON到文件
        file_name = f"{current_time}_数据上传.json"
        file_path = os.path.join(log_folder, file_name)
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(json.dumps([item.__json__() for item in engineering_list]) + '\r\n')
            file.write(err_msg + '\r\n')
            file.write('################################################################\r\n')


def redis_set(key, value, expire=30, time_type=1):
    """
    在redis中设置数据
    :param key: 键
    :param value: 值
    :param expire: 超时时间
    :param time_type: 时间类型（1-分钟,2-小时,3-天）
    :return:
    """
    # 如果没有传入key，则抛出异常
    if key is None or len(key) == 0:
        raise Exception('未传入键')
    try:
        upload_url = 'http://10.220.6.63:8090/api/khgz/redis/saveCache'
        headers = {
            'Content-Type': 'application/json'
        }
        payload = {
            "key": key,
            "value": value,
            "timeout": expire,
            "type": time_type
        }
        redis_response = requests.post(upload_url, headers=headers, data=json.dumps(payload).encode('utf-8'))
        if redis_response.status_code == 200:
            redis_result = json.loads(redis_response.text)
            if redis_result['ok']:
                print(f'Redis设置成功')
            else:
                raise Exception(f'Redis设置失败，详细信息：{redis_result["msg"]}')
        else:
            raise Exception('接口调用失败，错误码：' + str(redis_response.status_code))
    except Exception as redis_ex:
        print('Redis设置异常：' + str(redis_ex))
        raise Exception('Redis设置异常：' + str(redis_ex))


def redis_get(key):
    """
    从redis中获取数据
    :param key: 键
    :return:
    """
    # 如果没有传入key，则抛出异常
    if key is None or len(key) == 0:
        raise Exception('未传入键')
    try:
        upload_url = 'http://10.220.6.138/api/khgz/redis/getCache'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        redis_response = requests.get(upload_url, headers=headers, params={"key": key})
        if redis_response.status_code == 200:
            redis_result = json.loads(redis_response.text)
            if redis_result['ok']:
                return str(redis_result['data'])
            else:
                raise Exception(f'Redis获取失败，详细信息：{redis_result["msg"]}')
        else:
            raise Exception('接口调用失败，错误码：' + str(redis_response.status_code))

    except Exception as redis_ex:
        print('Redis获取异常：' + str(redis_ex))
        raise Exception('Redis获取异常：' + str(redis_ex))
