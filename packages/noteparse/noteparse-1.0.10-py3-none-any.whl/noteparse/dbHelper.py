import pymysql
from datetime import datetime
import traceback


db_config = {
    'host': '10.220.6.138',
    'port': 3306,
    'user': 'root',
    'password': '*Ab123456',
    'db': 'unvbasicx_khgz'
}

# 创建数据库连接
def create_connection():
    try:
        print(datetime.now(),'开启数据库链接')
        # 连接数据库
        connection = pymysql.connect(host=db_config.get('host', ''), port=db_config.get('port', ''),
                        user=db_config.get('user', ''), password=db_config.get('password', ''),
                        db=db_config.get('db', ''))
        print(datetime.now(),'数据库链接成功')
        
    except pymysql.MySQLError as e:
        print(datetime.now(),'数据库链接失败',e)
    return connection

# # 创建数据库连接
# def create_connection(host,port,user,password,db):
#     try:
#         print(datetime.now(),'开启数据库链接')
#         # 连接数据库
#         connection = pymysql.connect(host=host, port=port,
#                         user=user, password=password,
#                         db=db)
#         print(datetime.now(),'数据库链接成功')
        
#     except pymysql.MySQLError as e:
#         print(datetime.now(),'数据库链接失败',e)
#     return connection

# 确保在程序退出时关闭数据库连接
def close_connection(connection):
    if connection and connection.open:
        print(datetime.now(),'关闭SQL连接')
        connection.close()

connection = create_connection()

# 通过城市名称查询城市信息
def queryCityInfo(cityName):
    query = f'''
    (SELECT 
        a.areaid,
        a.area,
        c.cityid,
        c.city,
        p.provinceid,
        p.province
    FROM 
        unvbasicx_khgz.areas a
    JOIN 
        unvbasicx_khgz.cities c ON a.cityid = c.cityid
    JOIN 
        unvbasicx_khgz.provinces p ON c.provinceid = p.provinceid
    WHERE 
        a.area like '%{cityName}%')
    UNION ALL
    (SELECT 
        '' AS areaid,
        '' AS area,
        c.cityid,
        c.city,
        p.provinceid,
        p.province
    FROM 
        unvbasicx_khgz.cities c
    JOIN 
        unvbasicx_khgz.provinces p ON c.provinceid = p.provinceid
    WHERE 
        c.city like '%{cityName}%'
        AND NOT EXISTS (
            SELECT 1 FROM unvbasicx_khgz.areas WHERE area like '%{cityName}%'
        )
    )
    UNION ALL
    (SELECT 
        '' AS areaid,
        '' AS area,
        '' AS cityid,
        '' AS city,
        p.provinceid,
        p.province
    FROM 
        unvbasicx_khgz.provinces p
    WHERE 
        p.province like '%{cityName}%'
        AND NOT EXISTS (
            SELECT 1 FROM unvbasicx_khgz.cities WHERE city like '%{cityName}%'
        )
        AND NOT EXISTS (
            SELECT 1 FROM unvbasicx_khgz.areas WHERE area like '%{cityName}%'
        )
    )
    LIMIT 1
    '''
    if connection == None:
        create_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()  # 获取所有查询结果
            return result
    except Exception as e:
        print(datetime.now(),'通过城市名查询城市信息异常',e)
        traceback.print_exc()