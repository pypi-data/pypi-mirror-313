import platform
import datetime
import socket
import os
import hashlib


def get_mac_address() -> str:
    """
    获取mac地址，只有联网才能生效
    """
    import netifaces
    try:
        default_gate_way, default_nic_name = netifaces.gateways()['default'][netifaces.AF_INET]  # 获取默认网关和网卡名称
        default_nic_mac_addr = netifaces.ifaddresses(default_nic_name)[netifaces.AF_LINK][0]['addr']  # 默认网卡的mac地址
        return default_nic_mac_addr
    except:
        return ''


def get_net_info():
    import netifaces
    default_gate_way, default_nic_name = netifaces.gateways()['default'][netifaces.AF_INET]  # 获取默认网关和网卡名称
    default_nic_mac_addr = netifaces.ifaddresses(default_nic_name)[netifaces.AF_LINK][0]['addr']  # 默认网卡的mac地址
    default_ip_addr = netifaces.ifaddresses(default_nic_name)[netifaces.AF_INET][0]['addr']  # 本地ip
    default_ip_netmask = netifaces.ifaddresses(default_nic_name)[netifaces.AF_INET][0]['netmask']  # 子网掩码
    default_ip_broadcast = netifaces.ifaddresses(default_nic_name)[netifaces.AF_INET][0]['netmask']
    return {'mac': default_nic_mac_addr, 'local_ip': default_ip_addr, 'netmask': default_ip_netmask, 'broadcast': default_ip_broadcast}


def platform_info() -> dict:
    """
    获取当前环境的信息
    """
    platform_processor = platform.processor()
    platform_architecture = platform.architecture()

    hostname = socket.gethostname()

    res = dict()

    res["node"] = platform.node()  # 计算机的网络名称/主机名

    res["local_datetime"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    res["platform"] = platform.platform()  # 操作系统名称及版本号
    res["system"] = platform.system()  # 操作系统名称
    res["version"] = platform.version()  # 操作系统详细版本
    res["release"] = platform.release()  # 操作系统大版本

    res["platform_machine"] = platform.machine()  # 计算机类型/平台架构
    res["platform_processor"] = platform_processor  # 计算机处理器信息/处理器名称
    res["platform_architecture"] = platform_architecture  # 操作系统的位数

    res["hostname"] = hostname
    res["mac"] = get_mac_address()

    res["cpu_count"] = os.cpu_count()

    import locale
    res["encoding"] = locale.getpreferredencoding()  # 获取系统编码类型

    return res


def equipment_calibration(detail=False):
    import wmi
    c = wmi.WMI()

    # 硬盘序列号
    equipment_information_pre = ''
    equipment_information_list = []
    for physical_disk in c.Win32_DiskDrive():
        equipment_information_pre = equipment_information_pre + physical_disk.SerialNumber
        equipment_information_list.append(physical_disk.SerialNumber)

    # CPU序列号
    cpu_information_list = []
    for cpu in c.Win32_Processor():
        equipment_information_pre = equipment_information_pre + cpu.ProcessorId.strip()
        cpu_information_list.append(cpu.ProcessorId.strip())

    # 主板序列号
    main_board_information_list = []
    for board_id in c.Win32_BaseBoard():
        equipment_information_pre = equipment_information_pre + board_id.SerialNumber
        main_board_information_list.append(board_id.SerialNumber)

    equipment_information = hashlib.md5(equipment_information_pre.encode(encoding='UTF-8')).hexdigest()

    if detail:
        return {
            'hard_disk': equipment_information_list,
            'cpu': cpu_information_list,
            'main_board': main_board_information_list,
            'equipment_code': equipment_information
        }
    else:
        return equipment_information