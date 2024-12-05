import platform
import os


def wifi():
    if platform.system() == 'Windows':
        wifi_cmd = ('netsh wlan show profiles ')
        with os.popen(wifi_cmd) as f:
            wifi_name_list = []
            for line in f:
                if '所有用户配置文件 :' in line:
                    # print(line)
                    line = line.strip()
                    wifi_name = line.split(':')[1]
                    wifi_name_list.append(wifi_name)
            print(wifi_name_list)
        for i in wifi_name_list:
            get = ('netsh wlan show profiles name={} key=clear').format(i)
            with os.popen(get) as r:
                print(r.read())
            r.close()
    else:
        pass
