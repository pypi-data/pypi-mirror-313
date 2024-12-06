import os
import configparser

configPath = '/home'

def reSetConfigPath(path):
    global configPath
    configPath = path
   
# keys传入多个key,section传入对应的type
def readConfig(*keys,section):
    # windows环境文件放E盘根目录
    # linux环境文件放home根目录
    if 'nt' == os.name:
        configPath = 'E:'
    else:
        configPath = '/root/.crawlab'
    # 使用 os.path.expanduser 获取当前用户的 home 目录
    home_dir = os.path.expanduser(configPath)

    # 构建完整路径到 .ini 文件
    ini_file_path = os.path.join(home_dir, 'uic_config.ini')

    # 初始化 ConfigParser
    config = configparser.ConfigParser()
    result = {}
    # 读取配置文件
    if os.path.exists(ini_file_path):
        config.read(ini_file_path)
        for key in keys:
            # 假设 [Credentials] 是 section 名称
            try:
                val = config.get(section, key)
                result[key] = val
            except configparser.NoSectionError as e:
                print("Error reading the file for key:",key, e)
    else:
        print(f"The file {ini_file_path} does not exist.")
    return result
# 设定main函数,程序起点
if __name__ == '__main__':
    try:
        ossConfig = readConfig('end_point','bucket_name',section='ossConfig')
        print('osscofnig',ossConfig)
        
    except Exception as err:
        print(f'任务执行失败',err)