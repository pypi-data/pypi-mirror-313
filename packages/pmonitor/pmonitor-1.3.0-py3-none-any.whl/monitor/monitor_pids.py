import psutil
import time
import json
from monitor.get_process_name import *
import sys
import asyncio
import platform
import ctypes
import os
import stat
import subprocess
import re


class PidsPerf:

    def __init__(self, process_name, interval=1):
        self.process_name = process_name
        self.interval = interval
        self.processUtil = ProcessName()

    def get_mac_perf(self):
        current_pid = self.processUtil.find_main_process_pid(self.process_name)
        gpu_tool = os.path.join(os.path.dirname(__file__), 'exec', 'GpuMonitor')
        if os.path.exists(gpu_tool):
            if not os.access(gpu_tool, os.X_OK):
                try:
                    current_permissions = os.stat(gpu_tool).st_mode
                    os.chmod(gpu_tool, current_permissions | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
                except Exception as e:
                    raise e
        while True:
            minor_cpu_sum = 0
            minor_real_mem_sum = 0
            minor_mem_percent_sum = 0
            minor_thread_count_sum = 0
            gpu_memory_usage_0 = 0
            gpu_memory_percent_0 = 0
            gpu_memory_usage_1 = 0
            gpu_memory_percent_1 = 0
            current_pids = self.processUtil.get_children_pids(current_pid)  # 获取所有子进程
            current_pids.add(current_pid)  # 将主进程及子进程添加到list中
            pids_process = self.processUtil.get_pids_process(current_pids)  # 获取所有进程

            result = subprocess.run([gpu_tool], stdout=subprocess.PIPE, text=True)
            for line in result.stdout.split('\n'):
                pattern = r"GPU Name:(.*?),Device Percent:(.*?),Dedicated Usage:(\d+)"
                matches = re.findall(pattern, line)
                for match in matches:
                    gpu_name, device_percent, dedicated_usage = match
                    if 'driver' in gpu_name or 'Apple' in gpu_name:
                        gpu_memory_usage_0 = round(float(dedicated_usage) / 1024 / 1024, 2)
                        gpu_memory_percent_0 = round(float(device_percent), 2)
                    else:
                        gpu_memory_usage_1 = round(float(dedicated_usage) / 1024 / 1024, 2)
                        gpu_memory_percent_1 = round(float(device_percent), 2)

            for process in pids_process:
                try:
                    cpu_percent = process.cpu_percent()
                    process_memory = process.memory_info()
                    mem_percent = u'%.2f' % (process.memory_percent())  # 内存利用率
                    real_mem = round(process_memory.rss / 1024 / 1024, 2)  # 实际内存
                    thread_count = process.num_threads()  # 线程总数
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    cpu_percent = 0
                    mem_percent = 0
                    real_mem = 0
                    thread_count = 0

                # 将性能数据保存到对应PID的数据列表中
                if process.pid == current_pid:  # 主进程数据处理
                    main_cpu = cpu_percent
                    main_real_mem = real_mem
                    main_mem_percent = round(float(mem_percent), 2)
                    main_thread_count = thread_count
                    main_data = {'cpu': main_cpu, 'memory': main_real_mem, 'memory percent': main_mem_percent,
                                 'thread count': main_thread_count}
                    # print('主进程', pid_name, main_cpu, main_real_mem, main_mem_percent, main_thread_count)
                else:  # 子进程数据处理
                    minor_cpu_sum += cpu_percent
                    minor_real_mem_sum += real_mem
                    minor_mem_percent_sum += float(mem_percent)
                    minor_thread_count_sum += thread_count
                # pid_data[process.pid].append((cpu_percent, real_mem, mem_percent, thread_count))
            minor_data = {'cpu': round(float(minor_cpu_sum), 2), 'memory': round(float(minor_real_mem_sum), 2),
                          'memory percent': round(float(minor_mem_percent_sum), 2),
                          'thread count': minor_thread_count_sum}
            # print('其他子进程', pid_name, minor_cpu_sum, minor_real_mem_sum, minor_mem_percent_sum,
            #       minor_thread_count_sum)
            # 获取磁盘IO
            io_read_bytes_start, io_write_bytes_start = self.get_disk_usage()
            time.sleep(self.interval)
            io_read_bytes_end, io_write_bytes_end = self.get_disk_usage()  # io read/write
            io_read_bytes = io_read_bytes_end - io_read_bytes_start  # io read/byte
            io_write_bytes = io_write_bytes_end - io_write_bytes_start  # io write/byte
            disk_data = {'io read': io_read_bytes, 'io write': io_write_bytes}
            gpu_data = {'gpu 0 memory usage': gpu_memory_usage_0, 'gpu 0 device Utilization': gpu_memory_percent_0,
                        'gpu 1 memory usage': gpu_memory_usage_1, 'gpu 1 device Utilization': gpu_memory_percent_1}
            data = {'main': main_data, 'other': minor_data, 'disk': disk_data, "gpu": gpu_data}
            json_data = json.dumps(data)
            print(json_data)
            sys.stdout.flush()

    def get_disk_usage(self):
        '''
        Mac 获取进程磁盘读写情况
        :return:
        '''
        try:
            io_counters = psutil.disk_io_counters()
            io_read_bytes = io_counters.read_bytes
            io_write_bytes = io_counters.write_bytes
            return io_read_bytes, io_write_bytes
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
        return 0, 0

    def get_win_perf(self):
        from monitor.WinPidUtil import PidWinPerformance, FILETIME
        from ctypes import CDLL, c_int, c_char_p, byref
        pidWinPerf = PidWinPerformance()
        system_time_pre = pidWinPerf.filetime_to_100nano_seconds(FILETIME())
        p_pid = self.processUtil.find_main_process_pid(self.process_name)
        child_pids = self.processUtil.get_children_pids(p_pid)
        child_pids.add(p_pid)  # app内所有pid
        process_cpu_times_pre = {pid: pidWinPerf.get_process_cpu_time(pid) for pid in child_pids}
        process_io_counters_pre = {pid: pidWinPerf.get_io_counters(pid) for pid in child_pids}

        dll_path = os.path.join(os.path.dirname(__file__), 'DLL', 'GpuMonitorLib.dll')
        gpu_monitor_dll = ctypes.CDLL(dll_path)
        gpu_monitor_dll.GetGPUDataForProcess.argtypes = [ctypes.c_ulong]
        gpu_monitor_dll.GetGPUDataForProcess.restype = ctypes.c_char_p
        while True:
            minor_cpu_sum = 0
            minor_workSet_mem_sum = 0
            minor_private_mem_sum = 0
            minor_mem_percent_sum = 0
            minor_thread_count_sum = 0
            minor_io_read_sum = 0
            minor_io_write_sum = 0
            minor_gpu_dedicated_sum = 0  # （专用内存）
            minor_gpu_system_sum = 0  # (共享内存)
            minor_gpu_committed_sum = 0  # (总使用内存)
            minor_gpu_percent_sum = 0  # (GPU内存占比)
            main_gpu_dedicated_sum = 0  # （专用内存）
            main_gpu_system_sum = 0  # (共享内存)
            main_gpu_committed_sum = 0  # (总使用内存)
            main_gpu_percent_sum = 0  # (GPU内存占比)

            current_pids = self.processUtil.get_children_pids(p_pid)  # 获取所有子进程
            current_pids.add(p_pid)  # 将主进程及子进程添加到list中

            start_time = time.time()  # 记录循环开始的时间
            system_idle_time = FILETIME()
            system_kernel_time = FILETIME()
            system_user_time = FILETIME()
            ctypes.windll.kernel32.GetSystemTimes(byref(system_idle_time),
                                                  byref(system_kernel_time),
                                                  byref(system_user_time))
            system_time_post = pidWinPerf.filetime_to_100nano_seconds(
                system_kernel_time) + pidWinPerf.filetime_to_100nano_seconds(system_user_time)

            child_pids = self.processUtil.get_children_pids(p_pid)
            child_pids.add(p_pid)  # app内所有pid

            new_pids_cpu_time_pre = {pid: pidWinPerf.get_process_cpu_time(pid) for pid in child_pids if
                                     pid not in process_cpu_times_pre}
            process_cpu_times_pre.update(new_pids_cpu_time_pre)
            new_process_io_counters_pre = {pid: pidWinPerf.get_io_counters(pid) for pid in child_pids}
            process_io_counters_pre.update(new_process_io_counters_pre)

            # print('----------------------------------------------------------')
            # print('pid', child_pids)
            for pid in child_pids:
                try:
                    process = psutil.Process(pid)
                    pid_name = process.name()
                    mem_percent = round(process.memory_percent(), 2)
                    thread_count = process.num_threads()
                except (psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess):
                    # print('pid is not found')
                    mem_percent = 0
                    thread_count = 0

                process_cpu_time_post = pidWinPerf.get_process_cpu_time(pid)
                memory_info = pidWinPerf.get_process_memory(pid)
                io_counters = pidWinPerf.get_io_counters(pid)
                read_bytes_sec = (io_counters.ReadTransferCount - process_io_counters_pre[
                    pid].ReadTransferCount) / self.interval
                write_bytes_sec = (io_counters.WriteTransferCount - process_io_counters_pre[
                    pid].WriteTransferCount) / self.interval
                gpu_info_json = gpu_monitor_dll.GetGPUDataForProcess(pid).decode()
                gpu_info = json.loads(gpu_info_json)
                if process_cpu_time_post:
                    # 计算CPU使用率
                    cpu_usage = round((process_cpu_time_post - process_cpu_times_pre[pid]) / (
                            system_time_post - system_time_pre) * 100, 2)
                    # 更新之前的CPU时间
                    process_cpu_times_pre[pid] = process_cpu_time_post
                    workSet_mem = round(memory_info.WorkingSetSize / 1024 / 1024, 2)  # MB
                    private_mem = round(memory_info.PrivateUsage / 1024 / 1024, 2)  # MB
                    if pid == p_pid:

                        if gpu_info is not None:
                            for item in gpu_info:
                                if item['ProcessID'] == p_pid:
                                    main_gpu_dedicated_sum += item['GPUProcessMemoryDedicatedUsage']  # （专用内存）
                                    main_gpu_system_sum += item['GPUProcessMemorySharedUsage']  # (共享内存)
                                    main_gpu_committed_sum += item['GPUProcessMemoryTotalCommitted']  # (总使用内存)
                                    main_gpu_percent_sum += item['GPUUtilizationPercent']  # (GPU内存占比)
                            print('主进程pid：', item['ProcessID'], 'Dedicated:',
                                  main_gpu_dedicated_sum,
                                  'System:', main_gpu_system_sum,
                                  'Committed:', main_gpu_committed_sum, 'GPU Usage:',
                                  main_gpu_percent_sum)
                        main_data = {'cpu': cpu_usage, 'private': private_mem, "workset": workSet_mem,
                                     'gpu_Dedicated': round(float(main_gpu_dedicated_sum), 2),
                                     'gpu_System': round(float(main_gpu_system_sum), 2),
                                     'gpu_Committed': round(float(main_gpu_committed_sum), 2),
                                     'gpu_Usage': round(float(main_gpu_percent_sum), 2)}

                        # print(
                        #     f'主进程数据：cpu：{cpu_usage}，workSet：{workSet_mem}，private：{private_mem}，mem_percent：{mem_percent}，thread_count：{thread_count}')
                    else:
                        minor_cpu_sum += cpu_usage  # 子进程总
                        minor_workSet_mem_sum += workSet_mem  # 子进程workSet内存
                        minor_private_mem_sum += private_mem  # 子进程private内存
                        minor_mem_percent_sum += mem_percent  # 子进程内存使用率
                        minor_thread_count_sum += thread_count  # 子进程线程总数
                        if gpu_info is not None:
                            for item in gpu_info:
                                if item['ProcessID'] != p_pid:
                                    print('子进程pid：', item['ProcessID'], 'Dedicated:',
                                          item['GPUProcessMemoryDedicatedUsage'],
                                          'System:', item['GPUProcessMemorySharedUsage'],
                                          'Committed:', item['GPUProcessMemoryTotalCommitted'], 'GPU Usage:',
                                          item['GPUUtilizationPercent'])
                                    minor_gpu_dedicated_sum += item['GPUProcessMemoryDedicatedUsage']
                                    minor_gpu_system_sum += item['GPUProcessMemorySharedUsage']
                                    minor_gpu_committed_sum += item['GPUProcessMemoryTotalCommitted']
                                    minor_gpu_percent_sum += item['GPUUtilizationPercent']
                    minor_io_read_sum += read_bytes_sec  # 所有进程IO读取速率总数
                    minor_io_write_sum += write_bytes_sec  # 所有进程IO写入速率总数

                else:
                    # print(f"PID {pid}: Process not found or access denied")
                    continue
            disk_data = {'io read': minor_io_read_sum, 'io write': minor_io_write_sum}
            other_data = {'cpu': minor_cpu_sum, 'private': round(float(minor_private_mem_sum), 2),
                          'workset': round(float(minor_workSet_mem_sum), 2),
                          'memory percent': round(float(minor_mem_percent_sum), 2),
                          'thread count': minor_thread_count_sum,
                          'gpu_Dedicated': round(minor_gpu_dedicated_sum, 2),
                          'gpu_System': round(minor_gpu_system_sum, 2),
                          'gpu_Committed': round(minor_gpu_committed_sum, 2),
                          'gpu_Usage': round(minor_gpu_percent_sum, 2)}
            data = {'main': main_data, 'other': other_data, 'disk': disk_data}
            json_data = json.dumps(data)
            print(json_data)
            sys.stdout.flush()
            # 更新系统时间
            system_time_pre = system_time_post
            # 等待以确保大约每秒更新一次
            elapsed = time.time() - start_time
            time.sleep(max(0, self.interval - elapsed))

    async def start_perf(self):
        if platform.system() == 'Windows':
            await asyncio.gather(self.get_win_perf())
        else:
            await asyncio.gather(self.get_mac_perf())
