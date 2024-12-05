#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker

相关文档：
https://docs.python.org/zh-cn/3/library/multiprocessing.html
"""
import random
from multiprocessing import Process
from multiprocessing import Queue
import showlog
import time
import copy
import os
os_cpu_count = os.cpu_count()  # CPU核心数


def run(
        task_list: list,
        task_function,
        subprocess_keep: bool = False,
        subprocess_limit: int = None,
        master_process_delay: int = 1,
        return_data: bool = False,
        silence: bool = True,
        task_run_time: int = None,
        task_over_time_reboot: bool = True
):
    """
    多进程 进程控制
    :param task_list: 任务列表，list格式，会将list中的每个元素传入给task_function中的task_info，作为任务的详细信息；
    :param task_function: 子任务的function，需提前写好，入参为：(task_index, task_info)，例如：task_function(task_index, task_info)
    :param subprocess_keep: 是否保持子进程，True为保持进程，死掉会自动重启；False为不保持，自然退出
    :param subprocess_limit: 进程数限制，0为无限制，否则按照设定的数量限制并行的子进程数量
    :param master_process_delay: 主进程循环延时，单位为秒，默认为1秒
    :param return_data: 是否返回数据，True返回，False不返回
    :param silence: 静默模式，为True是不产生任何提示
    :param task_run_time: 单次任务运行时长限制，单位为秒
    :param task_over_time_reboot: 单次任务超时是否重启

    demo:
    def task_function(
            task_index,
            task_info
    ):
        # 进程详细的内容
        print(task_index, task_info)
    """
    inner_task_list = copy.deepcopy(task_list)  # 深度拷贝，防止篡改
    if subprocess_limit:
        # 存在自定义的子进程数量限制，将采用
        pass
    else:
        # 不存在自定义的子进程数量限制，将使用默认计算方式
        if os_cpu_count > 1:
            # 如果cpu核心数大于1个
            subprocess_limit = os_cpu_count - 1  # 子进程数设置为cpu核心数减1
        else:
            # 如果cpu核心数等于1个
            subprocess_limit = 1
    active_process = dict()  # 存放活跃进程进程，以task_index为key，进程信息为value的dict
    total_task_num = len(inner_task_list)  # 总任务数量
    task_index_start = 0  # 用来计算启动的累计进程数
    if return_data:
        q = Queue()  # 生成一个队列对象，以实现进程通信
    else:
        pass

    if silence:
        pass
    else:
        showlog.info(f'[P-MASTER] 正在准备多进程执行任务，总任务数为：{total_task_num}，进程数限制为：{subprocess_limit}...')
    # 创建并启动进程
    while True:
        this_time_start = copy.deepcopy(task_index_start)  # 深度拷贝累积启动的进程数，以确定本次循环的起点任务序号，假设subprocess_keep为False
        for task_index in range(this_time_start, total_task_num):  # 按照任务量遍历
            # 判断是否需要创建新的子进程
            if len(active_process.keys()) >= subprocess_limit:
                # 当前活跃进程数量达到子进程数限制，本次循环不再新增进程，跳出
                if silence is False:
                    showlog.info(f'[P-MASTER] 达到子进程数限制：{subprocess_limit}')
                break
            else:
                # 未达到进程数限制
                if task_index in active_process.keys():
                    # 进程已存在，不重复创建，跳过
                    continue
                else:
                    # 进程不存在，待定
                    # 不存在子进程限制规则/当前活跃进程数量未达到进程数限制，将开启一个新进程
                    if silence is False:
                        showlog.info(f'[P-MASTER] 发现需要开启的子进程：{task_index}/{total_task_num}')
                    task_info = inner_task_list[task_index]  # 提取将开启的进程的任务内容
                    # ---------- 开启进程 ----------
                    if return_data is True:
                        p = Process(
                            target=task_function,
                            args=(task_index, task_info, q)
                        )
                    else:
                        p = Process(
                            target=task_function,
                            args=(task_index, task_info)
                        )
                    p.start()
                    # ---------- 开启进程 ----------
                    active_process[task_index] = {
                        'task_index': task_index,  # 任务序号
                        'task_info': task_info,  # 任务详情
                        'process': p,  # 进程对象
                        'task_start_time': time.time()
                    }  # 记录开启的进程
                    if silence is False:
                        showlog.info(f'[P-MASTER] 子进程：{task_index}/{total_task_num} 已开启')
                    task_index_start += 1  # 记录累计开启进程数

        # 检测非活跃进程，并从active_process中剔除非活跃进程，以便开启新的进程
        inactive_process_temp = list()  # 非活跃进程
        for process_index, process_info in active_process.items():
            # print(q.qsize())
            # print(q.get())
            # print(q.get_nowait())
            if process_info['process'].is_alive() is True:
                # 该子进程仍然运行
                if task_run_time and int(time.time() - process_info['task_start_time']) > task_run_time:
                    if not silence:
                        showlog.warning(f'[P-MASTER] 子进程：{process_info["task_index"]}/{total_task_num} 运行超时，正在关闭...')
                    process_info["process"].terminate()
                    process_info["process"].join()
                    if not silence:
                        showlog.warning(f'[P-MASTER] 子进程：{process_info["task_index"]}/{total_task_num} 运行超时，已关闭')
                    if task_over_time_reboot:
                        if not silence:
                            showlog.warning(f'[P-MASTER] 子进程：{process_info["task_index"]}/{total_task_num} 运行超时，正在重启...')
                        # ---------- 开启进程 ----------
                        if return_data is True:
                            p = Process(
                                target=task_function,
                                args=(process_info['task_index'], process_info['task_info'], q)
                            )
                        else:
                            p = Process(
                                target=task_function,
                                args=(process_info['task_index'], process_info['task_info'])
                            )
                        p.start()
                        # ---------- 开启进程 ----------
                        active_process[process_info['task_index']] = {
                            'task_index': process_info['task_index'],  # 任务序号
                            'task_info': process_info['task_info'],  # 任务详情
                            'process': p,  # 进程对象
                            'task_start_time': time.time()
                        }  # 记录开启的进程
                        if not silence:
                            showlog.warning(f'[P-MASTER] 子进程：{process_info["task_index"]}/{total_task_num} 运行超时，已重启')
                    else:
                        pass
                continue
            else:
                # 该子进程停止运行
                if silence is False:
                    showlog.info(f'[P-MASTER] 进程 {process_index}/{total_task_num} 不活跃，将被剔除...')
                inactive_process_temp.append(process_index)

        if inactive_process_temp:
            # 存在需要剔除的子进程
            for each_dead_process in inactive_process_temp:
                # 尝试终止进程
                active_process[each_dead_process]['process'].terminate()
                active_process[each_dead_process]['process'].join()
                active_process.pop(each_dead_process)
        else:
            # 不存在需要剔除的子进程
            pass
        if silence is False:
            showlog.info(f'[P-MASTER] 当前活跃进程：count:{len(active_process.keys())} --> index:{active_process.keys()}')
        else:
            pass

        if task_index_start >= len(inner_task_list) and len(active_process.keys()) == 0:
            if silence is False:
                showlog.info('[P-MASTER] 全部任务执行完成')
            else:
                pass
            if subprocess_keep is True:
                task_index_start = 0  # 将累计启动进程数重置为0
            else:
                return
        else:
            pass
        time.sleep(master_process_delay)


def run_v2(
        task_list: list,
        task_function,
        subprocess_keep: bool = False,
        subprocess_limit: int = None,
        master_process_delay: int = 1,
        # return_data: bool = False,
        silence: bool = False,
        task_run_time_limit: int = None,
        task_over_time_reboot: bool = True
):
    """
    多进程 进程控制
    在一开始就生成好全部的任务详情，按照任务详情去具体执行和控制

    :param task_list: 任务列表，list格式，会将list中的每个元素传入给task_function中的task_info，作为任务的详细信息；
    :param task_function: 子任务的function，需提前写好，入参为：(task_index, task_info)，例如：task_function(task_index, task_info)
    :param subprocess_keep: 是否保持子进程，True为保持进程，死掉会自动重启；False为不保持，自然退出
    :param subprocess_limit: 进程数限制，0为无限制，否则按照设定的数量限制并行的子进程数量
    :param master_process_delay: 主进程循环延时，单位为秒，默认为1秒
    # :param return_data: 是否返回数据，True返回，False不返回
    :param silence: 静默模式，为True是不产生任何提示
    :param task_run_time_limit: 单次任务运行时长限制，单位为秒
    :param task_over_time_reboot: 单次任务超时是否重启

    demo:
    def task_function(
            task_index,
            task_info
    ):
        # 进程详细的内容
        print(task_index, task_info)
    """
    # process_task_list = copy.deepcopy(task_list)  # 深度拷贝，防止篡改源数据
    if task_list:
        pass
    else:
        if not silence:
            showlog.warning('无任务需要执行')
        return

    active_process = dict()  # 存放活跃进程进程，以task_index为key，进程信息为value的dict

    # 任务初始化
    process_task_dict = dict()
    for each_index, each_task in enumerate(task_list):
        task_index = copy.deepcopy(each_index+1)
        process_task_dict[task_index] = {
            'task_index': task_index,
            'task_info': copy.deepcopy(each_task),
            'task_state': 0  # 默认为等待状态
        }
    total_task_num = len(process_task_dict.keys())  # 总任务数量

    # ---------------------- 决定子进程数量限制 ----------------------
    if subprocess_limit:
        # 存在自定义的子进程数量限制，将采用
        pass
    else:
        # 不存在自定义的子进程数量限制，将使用默认计算方式
        if os_cpu_count > 1:
            # 如果cpu核心数大于1个
            subprocess_limit = os_cpu_count - 1  # 子进程数设置为cpu核心数减1
        else:
            # 如果cpu核心数等于1个
            subprocess_limit = 1
    # ---------------------- 决定子进程数量限制 ----------------------

    if not silence:
        showlog.info(f'[P-MASTER] 正在准备多进程执行任务，总任务数为：{total_task_num}，进程数限制为：{subprocess_limit}...')
    # 创建并启动进程
    proces_running_count = 0  # 用来计算正在运行的进程数
    while True:
        finish_count = 0
        for task_index, task_info in process_task_dict.items():
            process = task_info.get('process')
            task_start_time = task_info.get('task_start_time')
            task_state = task_info.get('task_state')

            if task_state == 0:  # 任务处于待开启状态
                # 检查进程数限制
                if not subprocess_limit:
                    # 无进程数限制，直接将任务打开
                    task_info['task_state'] = 1
                elif subprocess_limit and proces_running_count < subprocess_limit:
                    # 有进程数限制，但是未达到限制，打开任务
                    task_info['task_state'] = 1
                else:
                    # 有进程数限制，且达到了限制，什么也不做
                    pass
            elif task_state == 1:  # 任务处于开启状态
                pass
            else:
                finish_count += 1
                continue  # 当任务状态不属于等待和待开启状态时，表示该进程结束，将跳过检查

            # 先检查进程是否存活
            if process:
                if process.is_alive():
                    # 进程存在且进程存活
                    if task_run_time_limit:
                        # 存在进程最大运行时间限制
                        if int(time.time() - task_start_time) > task_run_time_limit:
                            # 运行超时
                            if not silence:
                                showlog.warning(f'[P-MASTER] 子进程：{task_index}/{total_task_num} 运行超时，正在关闭...')
                            process.terminate()
                            process.join()
                            proces_running_count -= 1
                            if not silence:
                                showlog.warning(f'[P-MASTER] 子进程：{task_index}/{total_task_num} 运行超时，已关闭')

                            if task_over_time_reboot:
                                # 超时将重启
                                if not silence:
                                    showlog.warning(f'[P-MASTER] 子进程：{task_index}/{total_task_num} 运行超时，将重启...')
                                task_info.pop('process')
                            else:
                                # 超时不重启，直接标记为结束
                                task_info['task_state'] = 2
                        else:
                            # 运行未超时
                            pass
                    else:
                        # 不存在进程最大运行时间限制
                        pass
                else:
                    # 进程存在但已结束
                    if not silence:
                        showlog.info(f'[P-MASTER] 进程 {task_index}/{total_task_num} 已结束 <dead>')
                    process.terminate()
                    process.join()
                    task_info['task_state'] = 2
                    proces_running_count -= 1
            else:
                # 进程不存在，需要判断是否开启进程
                pass

            # 开启进程
            if task_info['task_state'] == 1 and task_info.get('process') is None:
                if silence is False:
                    showlog.info(f'[P-MASTER] 发现需要开启的子进程：{task_index}/{total_task_num}')
                p = Process(
                    target=task_function,
                    args=(task_index, task_info)
                )
                p.start()
                task_info['process'] = p
                task_info['task_start_time'] = time.time()
                proces_running_count += 1
            else:
                continue
        if not subprocess_keep and finish_count == total_task_num:
            break
        else:
            time.sleep(master_process_delay)


def task_function_demo(
        task_index,
        task_info,
        q=None
):
    showlog.info(f'[p-{task_index}] start')
    # print(task_index, task_info)
    count_down = task_info.get('count_down')
    this_randint = random.randint(0,10)
    print(task_index, 'this_randint:', this_randint)

    time.sleep(this_randint)
    # q.put(task_index)
    showlog.info(f'[p-{task_index}] finish')


if __name__ == '__main__':
    """
    尝试增加对进程运行时间计时，超时的将关闭重启
    """
    task_list_demo = [
        {'task_id': 1, 'count_down': 1},
        {'task_id': 2, 'count_down': 2},
        {'task_id': 3, 'count_down': 3},
        {'task_id': 4, 'count_down': 4},
        {'task_id': 5, 'count_down': 5},
        {'task_id': 6, 'count_down': 6},
        {'task_id': 7, 'count_down': 7},
        {'task_id': 8, 'count_down': 8},
        {'task_id': 9, 'count_down': 9},
        {'task_id': 10, 'count_down': 10},
        {'task_id': 11, 'count_down': 11},
    ]
    run_v2(
        task_list=task_list_demo,
        task_function=task_function_demo,
        task_run_time_limit=5
        # return_data=True,
        # silence=True
    )
