#!/usr/bin/env python3
# coding = utf8
from . import lazyCrypto
from . import lazytime
from . import lazyfile
from . import lazypath
from . import lazymd5
from . import lazyprocess
import subprocess
import threading
import requests
import showlog
import shutil
import queue
import m3u8
import time
import sys
import os
import re
from rich.progress import track


timeout = 10
default_headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0"
}
path_separator = lazypath.path_separator


def m3u8_file_maker(
        m3u8_url
):
    """
    输入m3u8的地址，生成m3u8文件，以供下载，当前不含解密部分
    生成的m3u8文件为可以离线直接下载或播放的文件
    主要是为了解决一些m3u8文件内容地址不完整的情况
    """
    m3u8_obj = m3u8.load(
        uri=m3u8_url,
        headers=default_headers,
        timeout=timeout,
        verify_ssl=False
    )  # 获取内容
    # ---------- 头部处理 ----------
    m3u8_obj_base_uri = m3u8_obj.base_uri
    # print('m3u8_obj_base_uri: %s' % m3u8_obj_base_uri)
    m3u8_base_url_head = re.findall('(.*?//)', m3u8_obj.base_uri, re.S)[0]  # http或https的头
    m3u8_base_url_heart = re.findall('//(.*?)/', m3u8_obj.base_uri, re.S)[0]  # 根域名内容
    m3u8_base_url = m3u8_base_url_head + m3u8_base_url_heart  # 拼接根域名
    # print('m3u8_base_url: %s' % m3u8_base_url)
    m3u8_base_url_body = m3u8_obj_base_uri.replace(m3u8_base_url, '')  # 根域名后面的内容（肚子1）
    # print('m3u8_base_url_body: %s' % m3u8_base_url_body)
    # ---------- 头部处理 ----------

    if m3u8_obj.is_variant is True:
        print('含有码流选择')
        for playlist in m3u8_obj.playlists:
            print(playlist.uri)
            print(playlist.stream_info.bandwidth)
        print('默认选择第1个')
        playlist_0 = m3u8_obj.playlists[0]
        url_new = m3u8_obj.base_uri + playlist_0.uri.replace(m3u8_base_url_body, '')  # 去除相同内容
        print('url_new: %s' % url_new)
        # ---------- 2次跳转处理 ----------
        url_new_body = url_new.replace(m3u8_obj_base_uri, '').replace('index.m3u8', '')  # 根域名后面的内容（肚子2）
        print(url_new_body)
        # ---------- 2次跳转处理 ----------

        m3u8_obj_p0 = m3u8.load(url_new, headers=default_headers, timeout=timeout, verify_ssl=False)

        m3u8_obj_p0_base_uri = m3u8_obj_p0.base_uri
        # print(m3u8_obj_p0_base_uri)  # 根uri
        m3u8_obj_p0_content = m3u8_obj_p0.dumps()
        m3u8_obj_p0_content = m3u8_obj_p0_content.split('\n')
        # print(m3u8_obj_p0_content)
        m3u8_obj_p0_content_pro = list()
        for line in range(len(m3u8_obj_p0_content)):
            each_line = m3u8_obj_p0_content[line]
            if '#' in each_line:
                # 标记行
                m3u8_obj_p0_content_pro.append(each_line)
                if '#EXTINF' in each_line:
                    data_url = m3u8_obj_p0_base_uri + m3u8_obj_p0_content[line + 1].replace(m3u8_base_url_body, '').replace(url_new_body, '')  # 去除相同内容
                    m3u8_obj_p0_content_pro.append(data_url)
            else:
                # 非标记行
                pass
        m3u8_obj_p0_content_pro_m3u8 = '\n'.join(m3u8_obj_p0_content_pro)
        return m3u8_obj_p0_content_pro_m3u8
    else:
        print('不含码流选择')
        # 检查链接是否完整
        m3u8_obj_content = m3u8_obj.dumps()
        m3u8_obj_content_split = m3u8_obj_content.split('\n')
        m3u8_line_list = list()
        for index, line in enumerate(m3u8_obj_content_split):
            if '#' in line:
                # 含有#的行为标记行
                m3u8_line_list.append(line)
                if '#EXTINF' in line:
                    if 'http' in m3u8_obj_content_split[index + 1]:
                        data_url = m3u8_obj_content_split[index + 1]
                    elif m3u8_base_url in m3u8_obj_content_split[index + 1]:
                        data_url = m3u8_obj_content_split[index + 1].replace(m3u8_base_url_body, '')  # 去除相同内容
                    else:
                        if m3u8_base_url_body in m3u8_base_url:
                            data_url = m3u8_base_url + m3u8_obj_content_split[index + 1].replace(m3u8_base_url_body,
                                                                                                 '')  # 去除相同内容
                        else:
                            data_url = m3u8_base_url + m3u8_base_url_body + m3u8_obj_content_split[index + 1].replace(
                                m3u8_base_url_body, '')  # 去除相同内容
                    m3u8_line_list.append(data_url)
            else:
                # 非标记行
                pass
        m3u8_file = '\n'.join(m3u8_line_list)
        return m3u8_file


def m3u8_checker(
        url
):
    """
    url为m3u8地址
    """
    m3u8_obj = m3u8.load(
        uri=url,
        headers=default_headers,
        timeout=timeout,
        verify_ssl=False
    )  # 获取内容
    # ---------- 头部处理 ----------
    m3u8_obj_base_uri = m3u8_obj.base_uri
    print('m3u8_obj_base_uri: %s' % m3u8_obj_base_uri)
    m3u8_base_url_head = re.findall('(.*?//)', m3u8_obj.base_uri, re.S)[0]  # http或https的头
    m3u8_base_url_heart = re.findall('//(.*?)/', m3u8_obj.base_uri, re.S)[0]  # 根域名内容
    m3u8_base_url = m3u8_base_url_head + m3u8_base_url_heart  # 拼接根域名
    print('m3u8_base_url: %s' % m3u8_base_url)
    m3u8_base_url_body = m3u8_obj_base_uri.replace(m3u8_base_url, '')  # 根域名后面的内容（肚子1）
    print('m3u8_base_url_body: %s' % m3u8_base_url_body)
    # ---------- 头部处理 ----------

    if m3u8_obj.is_variant is True:
        print('含有码流选择')
        for playlist in m3u8_obj.playlists:
            print(playlist.uri)
            print(playlist.stream_info.bandwidth)
        print('默认选择第1个')
        playlist_0 = m3u8_obj.playlists[0]
        url_new = m3u8_obj.base_uri + playlist_0.uri.replace(m3u8_base_url_body, '')  # 去除相同内容
        print('url_new: %s' % url_new)
        # ---------- 2次跳转处理 ----------
        url_new_body = url_new.replace(m3u8_obj_base_uri, '').replace('index.m3u8', '')  # 根域名后面的内容（肚子2）
        print(url_new_body)
        # ---------- 2次跳转处理 ----------

        m3u8_obj_p0 = m3u8.load(
            uri=url_new,
            headers=default_headers,
            timeout=timeout,
            verify_ssl=False
        )

        m3u8_obj_p0_base_uri = m3u8_obj_p0.base_uri
        print(m3u8_obj_p0_base_uri)  # 根uri
        m3u8_obj_p0_content = m3u8_obj_p0.dumps()
        m3u8_obj_p0_content = m3u8_obj_p0_content.split('\n')
        # print(m3u8_obj_p0_content)
        m3u8_obj_p0_content_pro = list()
        for line in range(len(m3u8_obj_p0_content)):
            each_line = m3u8_obj_p0_content[line]
            if '#' in each_line:
                # 标记行
                m3u8_obj_p0_content_pro.append(each_line)
                if '#EXTINF' in each_line:
                    data_url = m3u8_obj_p0_base_uri + m3u8_obj_p0_content[line + 1].replace(m3u8_base_url_body, '').replace(url_new_body, '')  # 去除相同内容
                    m3u8_obj_p0_content_pro.append(data_url)
            else:
                # 非标记行
                pass
        m3u8_obj_p0_content_pro_m3u8 = '\n'.join(m3u8_obj_p0_content_pro)
        return m3u8_obj_p0_content_pro_m3u8
    else:
        print('不含码流选择')
        return m3u8_obj.dumps()


def download_st_2(
        url_list,
        filename,
        aes_key=None,
        suffix_name="st",
        headers=None,
        save_path="download",
        temp_path='temp'
):
    """
    注意这里分段解码后拼接会出现视频花屏问题，所以不能分段，此模块不适用于需要解码的
    实现文件下载功能，可指定url、文件名、后缀名、请求头、文件保存路径
    :param url_list:
    :param filename:文件名
    :param aes_key: aes解密key
    :param suffix_name:后缀名
    :param headers:请求头
    :param save_path:文件保存路径
    :param temp_path:临时文件路径
    :return:
    """
    if headers is None:
        headers_local = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0"}
    else:
        headers_local = headers

    if save_path is None:
        path_local = str(filename) + "." + str(suffix_name)
    else:
        if not os.path.exists(save_path):
            try:
                os.makedirs(save_path)
            except:
                pass
        path_local = save_path + '/' + str(filename) + "." + str(suffix_name)

    with open(path_local, "ab+") as f:
        url_count = 0
        for each_url in url_list:
            url_count += 1
            showlog.info("正在下载第 [ %s/%s ] 部分..." % (url_count, len(url_list)))
            while True:
                try:
                    print("下载进度：", end="")
                    time_pre = time.time()
                    response = requests.get(
                        url=each_url,
                        headers=headers_local,
                        stream=True
                    )
                    total_length = response.headers.get('content-length')

                    if total_length is None:  # no content length header
                        print("文件为空!")
                    else:
                        dl = 0
                        total_length = int(total_length)
                        char_list = ['\\', '|', '/', '-']
                        index = 0
                        for data in response.iter_content(chunk_size=8192):
                            dl += len(data)
                            if aes_key is None:
                                data_decode = data
                            else:
                                data_decode = lazyCrypto.aes_decode(
                                    data=data,
                                    key=aes_key
                                )
                            f.write(data_decode)
                            f.flush()
                            done = int(40 * dl / total_length)

                            time_now = time.time()
                            sys.stdout.write("\r下载中: %s [%s%s] %.2f%%  %.2fMB / %.2fMB SPEED: %.2fMB/s" % (
                            char_list[index], '=' * done, ' ' * (40 - done), (dl / total_length) * 100, dl / 1000000,
                            total_length / 1000000, (dl / (1024.0 * 1024.0 * 1024.0)) / ((time_now - time_pre) / 1000)))
                            sys.stdout.flush()
                            index = (index + 1) % len(char_list)
                    print("")
                    break
                except:
                    pass
    showlog.info("  ==> 保存位置:", path_local)


def worker(
        each_url,
        q,
        threading_num,
        aes_key=None,
        path_local='temp2.ts'
):
    path_local = 'temp/%s.ts' % threading_num
    for url in each_url:
        while True:
            try:
                response = requests.get(url=url, headers=default_headers, stream=True)
                break
            except:
                time.sleep(1)
        total_length = response.headers.get('content-length')

        if total_length is None:  # no content length header
            print("文件为空!")
        else:
            dl = 0
            total_length = int(total_length)
            char_list = ['\\', '|', '/', '-']

            with open(path_local, "ab+") as f:
                for data in response.iter_content(chunk_size=8192):
                    dl += len(data)
                    if aes_key is None:
                        data_decode = data
                    else:
                        data_decode = lazyCrypto.aes_decode(data, aes_key)
                    f.write(data_decode)
                    f.flush()


def multi_threading(
        task_list,
        each_thread_task_limit=20,
        thread_num=None
):
    """
    此模块是一个多线程控制模块
    task_list:任务列表
    each_thread_task_limit:每个线程的最大任务限制
    """
    showlog.info('本次任务总量：%s' % len(task_list))
    showlog.info('正在分配线程...')
    threads = []
    q = queue.Queue()
    threading_num = 0

    if len(task_list) <= each_thread_task_limit:
        # 任务量小于单个线程的最大任务量限制，设置为单线程
        showlog.info("任务量小于单线程最大任务量限制，将执行单线程模式")
        t = threading.Thread(
            target=worker,
            args=(task_list, q, threading_num)
        )
        # t.setDaemon(True)
        t.start()
        threads.append(t)
        threading_num += 1
        for thread in threads:
            thread.join(timeout=60 * 30)
    else:
        # 任务量大于单个线程的最大任务量限制，设置为多线程
        showlog.info("任务量大于单线程最大任务量限制，将执行多线程模式")
        task_list_temp = list()
        count_num = 0
        for each_task in task_list:
            task_list_temp.append(each_task)
            count_num += 1
            if count_num % each_thread_task_limit == 0 or count_num == len(task_list):
                t = threading.Thread(
                    target=worker,
                    args=(task_list_temp, q, threading_num)
                )
                # t.setDaemon(True)
                t.start()
                threads.append(t)
                threading_num += 1
                task_list_temp = list()
            else:
                continue
        for thread in threads:
            thread.join(timeout=60 * 30 / threading_num)
    showlog.info('线程分配完成，线程总计: %s' % len(threads))
    return


def fragment_merger(
        fragment_path,
        fragment_suffix='ts',
        fragment_keep=False,
        merge_file_name='merge',
        merge_file_path=None,
        merge_file_suffix='ts'
):
    """
    模块功能：将多个碎片文件合成一个大文件，将自动按照ts文件名的数字顺序排序依次合成
    注意：碎片文件名需按照数字顺序组织，否则将会出错
    :param fragment_path: [必填]碎片文件夹
    :param fragment_suffix: 碎片文件后缀名，缺省为ts
    :param fragment_keep: 碎片文件是否保留，默认不保留
    :param merge_file_name: 合成文件名，缺省为merge
    :param merge_file_path: 合成文件夹，缺省为当前文件夹
    :param merge_file_suffix: 合成文件后缀名，缺省为ts
    :return:
    """
    if merge_file_path is None:
        merge_file_dir_name = '%s.%s' % (merge_file_name, merge_file_suffix)
    else:
        # pathx.make_path(merge_file_path)
        lazypath.make_path(merge_file_path)
        merge_file_dir_name = '%s%s%s.%s' % (merge_file_path, path_separator, merge_file_name, merge_file_suffix)

    print(':) 正在合成碎片...')
    # fragment_list = filebox.file_read.dir_file_list(file_dir=fragment_path)  # 获取文件夹下的碎片文件列表
    fragment_list = lazyfile.dir_file_list(file_dir=fragment_path)  # 获取文件夹下的碎片文件列表
    fragment_index_list = list()
    for fragment in fragment_list:
        # 只对指定后缀的文件合成
        if fragment_suffix in fragment:
            fragment_index = fragment.replace('.%s' % fragment_suffix, '')  # 去掉文件的后缀名，以取文件名
            fragment_index_list.append(int(fragment_index))  # 将文件名转换为数字
        else:
            continue
    fragment_index_list.sort(reverse=False)  # 对文件名升序重排

    with open(merge_file_dir_name, "ab+") as f:
        for fragment_index_sort in fragment_index_list:
            fragment_sort = '%s%s%s.%s' % (fragment_path, path_separator, fragment_index_sort, fragment_suffix)
            x = open(fragment_sort, "rb")
            f.write(x.read())
            f.flush()
            x.close()
    print(':) 碎片合成完成')
    time.sleep(1)
    if fragment_keep is False:
        shutil.rmtree(fragment_path)  # 删除文件夹
    else:
        pass
    return merge_file_dir_name


def download_fragment(
        url_list,
        aes_key=None,
        headers=None,
        video_save_path=None,
        fragment_path=None,
        fragment_suffix='ts'
):
    """
    模块功能：下载碎片到指定文件夹
    :param url_list: 碎片下载地址列表
    :param aes_key: aes解密key
    :param headers:请求头
    :param video_save_path:文件保存路径
    :param fragment_path:碎片保存路径
    :param fragment_suffix:碎片文件后缀名
    :return:
    """
    if headers is None:
        headers_local = default_headers
    else:
        headers_local = headers

    if fragment_path is None:
        fragment_path = 'fragment_%s' % str(time.time()).replace('.', '')  # 使用时间戳命名
    else:
        pass

    if video_save_path is not None:
        fragment_path_new = '%s%s%s' % (video_save_path, path_separator, fragment_path)
    else:
        fragment_path_new = fragment_path
    lazypath.make_path(fragment_path_new)
    fragment_file_name_list = list()
    print('开始下载...')
    for index, each_url in enumerate(url_list):
        print(f'  正在下载 {index+1}/{len(url_list)}', each_url)
        fragment_file_name = '%s%s%s.%s' % (fragment_path_new, path_separator, index, fragment_suffix)  # 生成碎片文件名
        # 开始下载碎片文件
        while True:
            try:
                with open(fragment_file_name, "ab+") as f:
                    response = requests.get(
                        url=each_url,
                        headers=headers_local,
                        stream=True,
                        timeout=timeout
                    )
                    total_length = response.headers.get('content-length')

                    if total_length is None:
                        print("Attention: There is no content length in header!")  # 未返回长度信息
                    else:
                        dl = 0
                        total_length = int(total_length)
                        for data in track(
                                sequence=response.iter_content(chunk_size=8192),
                                description='下载中',
                                total=total_length/8192,
                                show_speed=True
                        ):
                            dl += len(data)
                            if aes_key is None:
                                data_decode = data
                            else:
                                data_decode = lazyCrypto.aes_decode(data, aes_key)
                            f.write(data_decode)
                            f.flush()
                break
            except:
                showlog.warning('下载超时，将在1秒后重试...')
                os.remove(fragment_file_name)
                time.sleep(1)
                pass
        fragment_file_name_list.append(fragment_file_name)
        # 碎片文件下载完成

    print("\n:) 下载完成")
    download_res = {
        'fragment_path': fragment_path_new,
        'fragment_suffix': fragment_suffix,
        'fragment_file_name_list': fragment_file_name_list
    }
    return download_res


def download_fragment_single(
        task_index,
        task_info,
):
    """
    模块功能：下载单个碎片到指定文件夹
    :param fragment_url: 碎片下载地址
    :param fragment_url_name: 碎片名
    :param fragment_path:碎片保存路径
    :param aes_key: aes解密key
    :param headers:请求头
    :param fragment_suffix:碎片文件后缀名
    :return:
    """
    fragment_url = task_info['fragment_url']
    fragment_url_name = task_info['fragment_url_name']
    fragment_path = task_info['fragment_path']
    aes_key = None
    fragment_suffix = task_info['fragment_suffix']
    headers = task_info['headers']

    if headers:
        headers_local = headers
    else:
        headers_local = default_headers

    # print('正在下载', fragment_url_name, fragment_url)
    fragment_file_name = '%s%s%s.%s' % (fragment_path, path_separator, fragment_url_name, fragment_suffix)  # 生成碎片文件名
    # 开始下载碎片文件
    while True:
        try:
            with open(fragment_file_name, "ab+") as f:
                response = requests.get(
                    url=fragment_url,
                    headers=headers_local,
                    stream=True,
                    timeout=timeout
                )
                total_length = response.headers.get('content-length')

                if total_length is None:
                    print("Attention: There is no content length in header!")  # 未返回长度信息
                else:
                    dl = 0
                    total_length = int(total_length)
                    for data in track(
                            sequence=response.iter_content(chunk_size=8192),
                            description=f'{fragment_url_name} 下载中',
                            total=total_length/8192,
                            show_speed=True
                    ):
                        dl += len(data)
                        if aes_key is None:
                            data_decode = data
                        else:
                            data_decode = lazyCrypto.aes_decode(data, aes_key)
                        f.write(data_decode)
                        f.flush()
            break
        except:
            showlog.error('下载超时，将在1秒后重试...')
            os.remove(fragment_file_name)
            time.sleep(1)
            pass


def download_fragment_quick(
        url_list,
        subprocess_limit=None,
        headers=None,
        video_path=None
):
    """
    使用多进程并发下载素材，提升下载效率
    """
    if video_path:
        fragment_path = f"{video_path}{path_separator}fragment_{str(time.time()).replace('.', '')}"   # 使用时间戳命名
    else:
        fragment_path = f"fragment_{str(time.time()).replace('.', '')}"  # 使用时间戳命名
    fragment_suffix = 'ts'
    lazypath.make_path(fragment_path)
    task_list = list()
    fragment_file_name_list = list()
    for url_index, each_url in enumerate(url_list):
        task_list.append(
            {
                'fragment_url': each_url,
                'fragment_url_name': url_index,
                'fragment_path': fragment_path,
                'fragment_suffix': fragment_suffix,
                'headers': headers
            }
        )
        fragment_file_name = '%s%s%s.%s' % (fragment_path, path_separator, url_index, fragment_suffix)  # 生成碎片文件名
        fragment_file_name_list.append(fragment_file_name)

    lazyprocess.run(
        task_list=task_list,
        task_function=download_fragment_single,
        subprocess_limit=subprocess_limit,
        silence=True
    )

    download_res = {
        'fragment_path': fragment_path,
        'fragment_suffix': fragment_suffix,
        'fragment_file_name_list': fragment_file_name_list
    }
    return download_res


def download_m3u8(
        m3u8_link=None,
        m3u8_file_path=None,
        filename=lazytime.get_file_name(),
        url_v=None,
        video_suffix_name="ts",
        aes_key=None,
        proxies=None,
        video_save_path='download',
        overwrite=True,
        postfix="m3u8",
        fragment_path=None,
        fragment_suffix=None,
        fragment_merge=True,
        fragment_keep=False,
        headers=None
):
    """
    在同路径下载同名st文件
    :param m3u8_link:
    :param m3u8_file_path:
    :param filename:
    :param url_v: url前缀
    :param video_suffix_name:
    :param aes_key:
    :param proxies:
    :param video_save_path:
    :param overwrite: 覆盖现有文件
    :param postfix: 覆盖现有文件
    :param fragment: 是否下载碎片
    :param fragment_path: 碎片下载地址
    :param fragment_suffix: 碎片文件后缀
    :param fragment_merge: 是否合成碎片
    :return:
    """
    if m3u8_link is None and m3u8_file_path is None:
        print(':( 请传入有效的m3u8地址！')
        return False

    if m3u8_file_path is not None:
        print("正在解析m3u8文件...")
        all_content = lazyfile.read(
            file=m3u8_file_path,
            postfix=postfix
        )
        m3u8_lines = all_content.split("\n")  # 读取文件里的每一行
    else:
        return False

    # 通过判断文件头来确定是否是M3U8文件
    if m3u8_lines[0] != "#EXTM3U":
        print(":( 非M3U8文件")
        return False
    else:
        url_list = list()
        for index, line in enumerate(m3u8_lines):
            if "EXTINF" in line:
                url = m3u8_lines[index + 1]
                if url_v is None:
                    url_list.append(url)
                else:
                    url_list.append(url_v + url)
        print("解析到 [ %s ] 个下载地址，即将下载..." % len(url_list))
        download_res = download_fragment(
            url_list=url_list,
            video_save_path=video_save_path,
            aes_key=aes_key,
            fragment_path=fragment_path,
            fragment_suffix=fragment_suffix,
            headers=headers
        )
        if fragment_merge is True:
            print(':) 碎片下载完成，正在合成碎片...')
            merge_file_dir_name = fragment_merger(
                fragment_path=download_res.get('fragment_path'),
                fragment_suffix=download_res.get('fragment_suffix'),
                fragment_keep=fragment_keep,
                merge_file_name=filename,
                merge_file_path=video_save_path,
                merge_file_suffix=video_suffix_name
            )
            download_res['merge_file_dir_name'] = merge_file_dir_name
        else:
            print(':) 碎片下载完成')
        return download_res


def download_m3u8_to_file(
        m3u8_url=None,
        m3u8_file_dir=None,
        m3u8_content=None,
        m3u8_keep=False,
        video_name=None,
        video_save_path='download',
        video_suffix='ts',  # 视频文件设置
        overwrite=True,  # 是否覆盖原有视频文件
        fragment_path=None,
        fragment_suffix='ts',
        fragment_merge=True,
        fragment_keep=False
):
    """
    m3u8_url/m3u8_file_dir/m3u8_content 3选1，提供3种方式下载
    文件命名：video_name + video_biz_id + file_md5
    先下载碎片，再合成
    fragment_path:碎片保存地址
    fragment_merge:是否合成碎片
    fragment_keep: 是否保留碎片
    """
    temp_filename = str(time.time()).replace('.', '')  # 临时文件使用时间戳命名

    # -------------------- 获取m3u8内容 --------------------
    if m3u8_url is None:
        if m3u8_file_dir is None:
            if m3u8_content is None:
                return False
            else:
                lazyfile.save(
                    file=temp_filename,
                    content=m3u8_content,
                    suffix="m3u8",
                    path=video_save_path,
                    overwrite=overwrite
                )
                if video_save_path is None:
                    m3u8_file_dir_name = '%s.m3u8' % temp_filename
                else:
                    m3u8_file_path = r'%s%s%s' % (video_save_path, path_separator, temp_filename)
                    m3u8_file_dir_name = '%s.m3u8' % m3u8_file_path
        else:
            m3u8_file_dir_name = m3u8_file_dir  # 完整路径
    else:
        try:
            m3u8_file = m3u8_file_maker(m3u8_url=m3u8_url)
            print(':) 获取m3u8内容成功')
            lazyfile.save(
                file=temp_filename,
                content=m3u8_file,
                suffix="m3u8",
                path=video_save_path,
                overwrite=overwrite
            )
            if video_save_path is None:
                m3u8_file_dir_name = '%s.m3u8' % (temp_filename)
            else:
                m3u8_file_path = r'%s%s%s' % (video_save_path, path_separator, temp_filename)
                m3u8_file_dir_name = '%s.m3u8' % m3u8_file_path
        except:
            print(':( 获取m3u8内容失败')
            return False
    # -------------------- 获取m3u8内容 --------------------

    video_file_path = r'%s%s%s' % (video_save_path, path_separator, temp_filename)  # 视频文件路径
    video_file_dir_name = '%s.%s' % (video_file_path, video_suffix)

    print('开始下载m3u8碎片 [%s] ...' % temp_filename)
    start_time = time.time()
    download_res = download_m3u8(
        m3u8_file_path=m3u8_file_dir_name.replace('.m3u8', ''),
        filename=temp_filename,
        video_suffix_name=video_suffix,
        video_save_path=video_save_path,
        overwrite=overwrite,
        fragment_path=fragment_path,
        fragment_suffix=fragment_suffix,
        fragment_merge=fragment_merge,
        fragment_keep=fragment_keep
    )
    finish_time = time.time()
    download_duration = finish_time - start_time
    duration_res = lazytime.get_time_duration(int(download_duration))
    download_duration_str = duration_res.get('duration_str')
    if download_res is False:
        print(':( 下载失败')
        return False
    else:
        print(':) 下载完成，耗时：%s' % download_duration_str)
        merge_file_dir_name = download_res.get('merge_file_dir_name')
        file_md5 = lazymd5.md5_file(
            file_path=merge_file_dir_name
        )

        if m3u8_keep is False:
            os.remove(m3u8_file_dir_name)
        else:
            pass

        print(':) 将文件按照md5重命名')
        if video_name is None:
            new_name = file_md5
        else:
            new_name = '%s-%s' % (video_name, file_md5)

        file_path_md5 = '%s%s%s.%s' % (video_save_path, path_separator, new_name, video_suffix)

        if os.path.exists(file_path_md5):
            print('==> [warning] 文件 [%s] 已存在，将删除文件！' % file_path_md5)
            os.remove(file_path_md5)

        lazyfile.file_rename(
            before_name=video_file_dir_name,
            after_name=file_path_md5
        )  # 修改下载文件名称
        print(':) 重命名成功，新的文件名为：%s' % file_md5)

        file_size_dict = lazyfile.get_file_size(file_dir=file_path_md5)
        res_dict = {
            'file_path': file_path_md5,
            'file_md5': file_md5,
            'download_duration': download_duration_str,
            'file_size_str': file_size_dict.get('size_str'),
            'file_size_byte': file_size_dict.get('size_byte')
        }
        print(':) 最终下载得到的文件路径为：[ %s ]' % file_path_md5)
        print('=' * 50)
        return True, res_dict


def convert_video(
        video_input: str,
        video_output: str
) -> None:
    """
    Convert video from ts to mp4.
    可能会出现实用iMovie播放和苹果手机播放发生的掉帧问题，使用其他播放器未出现
    Parameters
    ----------
    video_input : str
        The input file name
    video_output : str
        The output file name
    """
    flags = ["ffmpeg", "-i", f"{video_input}.ts", "-acodec", "copy", "-vcodec", "copy", video_output]
    subprocess.Popen(flags, stdout=subprocess.DEVNULL).wait()
    # os.unlink(f"{video_input}.ts")  # 删除文件
