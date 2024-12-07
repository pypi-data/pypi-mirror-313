import json
import os
import psutil
from datetime import datetime
from time import time
import asyncio
import platform
import uuid
import tempfile
from urllib import parse
import requests
import gzip
import shutil
import rpyc
import threading
import multiprocessing
from .sign import sign
from .logger import logger
from .websocket import WebSocketClient
from .profiler import start_service

class Agent:
    def __init__(self, server, app_id, app_secret):
        self.profiler = connect_to_profiler(os.getppid())

        self.ws_client = WebSocketClient(server, app_id, app_secret)
        self.ws_client.set_message_handler(self._handle_message)
        self.ws_client.set_monitor_handler(self._handle_monitor)
        self.ws_client.connect()

    async def _handle_monitor(self):
        pid = os.getppid()

        await self._send_system_log()

        await self.ws_client.send_message('log', {
            'type': 'xprofiler_log',
            'data': {
                "logs": [
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "cpu_now",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "cpu_15",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "cpu_30",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "cpu_60",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "cpu_180",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "cpu_300",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "cpu_600",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "rss",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "heap_used",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "heap_available",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "heap_total",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "heap_limit",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "heap_executeable",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "total_physical_size",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "malloced_memory",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "amount_of_external_allocated_memory",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "new_space_size",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "new_space_used",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "new_space_available",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "new_space_committed",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "old_space_size",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "old_space_used",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "old_space_available",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "old_space_committed",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "code_space_size",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "code_space_used",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "code_space_available",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "code_space_committed",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "map_space_size",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "map_space_used",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "map_space_available",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "map_space_committed",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "lo_space_size",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "lo_space_used",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "lo_space_available",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "lo_space_committed",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "read_only_space_size",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "read_only_space_used",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "read_only_space_available",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "read_only_space_committed",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "new_lo_space_size",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "new_lo_space_used",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "new_lo_space_available",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "new_lo_space_committed",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "code_lo_space_size",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "code_lo_space_used",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "code_lo_space_available",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "code_lo_space_committed",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "uptime",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "total_gc_times",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "total_gc_duration",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "total_scavange_duration",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "total_marksweep_duration",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "total_incremental_marking_duration",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "gc_time_during_last_record",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "scavange_duration_last_record",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "marksweep_duration_last_record",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "incremental_marking_duration_last_record",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "active_handles",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "active_file_handles",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "active_and_ref_file_handles",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "active_tcp_handles",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "active_and_ref_tcp_handles",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "active_udp_handles",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "active_and_ref_udp_handles",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "active_timer_handles",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "active_and_ref_timer_handles",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "live_http_request",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "http_response_close",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "http_response_sent",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "http_request_timeout",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "http_patch_timeout",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "http_rt",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "cpu_now",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "cpu_15",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "cpu_30",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "cpu_60",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "cpu_180",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "cpu_300",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "cpu_600",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "rss",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "heap_used",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "heap_available",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "heap_total",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "heap_limit",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "heap_executeable",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "total_physical_size",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "malloced_memory",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "amount_of_external_allocated_memory",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "new_space_size",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "new_space_used",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "new_space_available",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "new_space_committed",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "old_space_size",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "old_space_used",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "old_space_available",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "old_space_committed",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "code_space_size",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "code_space_used",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "code_space_available",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "code_space_committed",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "map_space_size",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "map_space_used",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "map_space_available",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "map_space_committed",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "lo_space_size",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "lo_space_used",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "lo_space_available",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "lo_space_committed",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "read_only_space_size",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "read_only_space_used",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "read_only_space_available",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "read_only_space_committed",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "new_lo_space_size",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "new_lo_space_used",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "new_lo_space_available",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "new_lo_space_committed",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "code_lo_space_size",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "code_lo_space_used",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "code_lo_space_available",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "code_lo_space_committed",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "uptime",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "total_gc_times",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "total_gc_duration",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "total_scavange_duration",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "total_marksweep_duration",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "total_incremental_marking_duration",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "gc_time_during_last_record",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "scavange_duration_last_record",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "marksweep_duration_last_record",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "incremental_marking_duration_last_record",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "active_handles",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "active_file_handles",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "active_and_ref_file_handles",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "active_tcp_handles",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "active_and_ref_tcp_handles",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "active_udp_handles",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "active_and_ref_udp_handles",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "active_timer_handles",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "active_and_ref_timer_handles",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "live_http_request",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "http_response_close",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "http_response_sent",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "http_request_timeout",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "http_patch_timeout",
                      "value": 0
                    },
                    {
                      "pid": pid,
                      "tid": 0,
                      "key": "http_rt",
                      "value": 0
                    }
                ],
                'xprofiler_version': '',
                'log_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'log_timestamp': int(datetime.now().timestamp() * 1000)
            }
        })

        await self.ws_client.send_message('log', {
            'type': 'core_files',
            'data': { 'list': [] }
        })

        await self.ws_client.send_message('log', {
            'type': 'package',
            'data': {'pkgs': []}
        })

        await self.ws_client.send_message('log', {
            'type': 'error_log',
            'data': {}
        })

    async def _send_system_log(self):
        processes = self._get_python_processes()
        load1, load5, load15 = os.getloadavg()
        used_cpu = psutil.cpu_percent(interval=1) / 100
        memory = psutil.virtual_memory()
        free_memory = memory.available
        total_memory = memory.total
        cpu_count = psutil.cpu_count()
        disks = self._get_disk_usage()
        await self.ws_client.send_message('log', {
            'type': 'system_log',
            'data': {
                'cpu_count': cpu_count,
                'total_memory': total_memory,
                'uptime': int(time() - psutil.boot_time()),
                'used_cpu': used_cpu,
                'free_memory': free_memory,
                'load1': load1,
                'load5': load5,
                'load15': load15,
                'disks': disks,
                'node_count': len(processes),
                'log_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'log_timestamp': int(datetime.now().timestamp() * 1000),
                'version': 0
            }
        })

    async def _handle_message(self, message):
        msg_type = message.get('type')
        if msg_type == 'exec_command':
            await self._handle_exec_command(message)

    async def _handle_exec_command(self, message):
        data = message.get('data', {})
        trace_id = message.get('traceId')
        command = data.get('command')

        if command == 'get_node_processes':
            processes = self._get_python_processes()
            await self.ws_client.send_message('response', {
                'ok': True,
                'data': {
                    'stdout': '\n'.join(processes)
                }
            }, trace_id)
        if 'check_processes_alive' in command:
            pids = command.split()[1:]
            await self.ws_client.send_message('response', {
                'ok': True,
                'data': {
                    'stdout': json.dumps({ pid: self._check_process_alive(int(pid)) for pid in pids })
                }
            }, trace_id)
        if 'start_cpu_profiling' in command:
            options = json.loads(command.split()[-1])
            profiling_time = options.get('profiling_time')
            duration = int(profiling_time)/1000
            filepath = self.profiler.start_profiling(duration)
            if filepath is None:
                return await self.ws_client.send_message('response', {
                    'ok': True,
                    'data': {
                        'stderr': 'start_cpu_profiling is running.'
                    }
                }, trace_id)
            await self.ws_client.send_message('response', {
                'ok': True,
                'data': {
                    'stdout': json.dumps({'filepath': filepath})
                }
            }, trace_id)
            await asyncio.sleep(duration)
            await self.ws_client.send_message('action', {
                'filePath': filepath
            })
        if 'stop_cpu_profiling' in command:
            filepath = self.profiler.stop_profiling()
            await self.ws_client.send_message('response', {
                'ok': True,
                'data': {
                    'stdout': json.dumps({'filepath': filepath})
                }
            }, trace_id)
            await self.ws_client.send_message('action', {
                'filePath': filepath
            })

        if 'upload_file' in command:
            _, file_id, file_type, file_path, server, token = command.split()
            storage = await self._upload_file(file_id, file_type, file_path, server, token)
            await self.ws_client.send_message('response', {
                'ok': True,
                'data': {
                    'stdout': json.dumps({'storage': storage})
                }
            }, trace_id)

    def _get_python_processes(self):
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'python' in proc.info['name'] or (proc.info.get('cmdline') and 'python' in proc.info.cmdline[0].lower()):
                    pid = proc.info['pid']
                    cmdline = proc.info.get('cmdline')
                    if cmdline:
                        cmd = ' '.join(cmdline)
                    else:
                        cmd = "(No command line provided)"
                    processes.append(f"{pid}\u0000{cmd}")
            except Exception:
                pass
        return processes
    
    def _check_process_alive(self, pid):
        try:
            proc = psutil.Process(pid)
            return proc.is_running()
        except psutil.NoSuchProcess:
            return False

    def _get_disk_usage(self):
        disks = {}

        partitions = psutil.disk_partitions(all=True)

        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                usage_percent = round(usage.percent)
                disks[partition.mountpoint] = usage_percent
            except (PermissionError, OSError):
                continue
        return disks

    async def gzip_file(self, file_path: str) -> str:
        with tempfile.NamedTemporaryFile(delete=False) as tempf:
            gzipped_file = file_path + '.gz'

            if os.path.exists(gzipped_file):
                return gzipped_file

            with open(file_path, 'rb') as f:
                content = await asyncio.to_thread(f.read)

            compressed_content = await asyncio.to_thread(gzip.compress, content)

            tempf.write(compressed_content)
            tempf.flush()
            tempf.close()

            try:
                await asyncio.to_thread(shutil.copy, tempf.name, gzipped_file)
            finally:
                await asyncio.to_thread(os.unlink, tempf.name)

        return gzipped_file

    async def _upload_file(self, file_id, file_type, file_path, server, token):
        try:
            nonce = str(uuid.uuid4().int)
            timestamp = str(datetime.now().timestamp() * 1000)
            params = {
                'agentId': platform.node(),
                'fileId': file_id,
                'fileType': file_type,
                'nonce': nonce,
                'timestamp': timestamp
            }
            signature = sign(params, token)
            url = f"{server}/xapi/upload_from_xtransit?{parse.urlencode({'fileId': file_id, 'fileType': file_type, 'nonce': nonce, 'timestamp': timestamp, 'signature': signature})}"
            session = requests.Session()
            gzip_file_path = await self.gzip_file(file_path)
            with open(gzip_file_path, 'rb') as file_stream:
                result = await asyncio.to_thread(session.request, 'POST', url, files={'file': file_stream})
                result.raise_for_status()
                return result.json().get('data', {}).get('storage')
        except Exception as e:
            logger.error(f'error: {e}')
            return None

def get_socket_path(pid=None):
    socket_name = f"profiler-{pid}.sock"
    return os.path.join(tempfile.gettempdir(), socket_name)

def connect_to_profiler(pid=None):
    socket_path = get_socket_path(pid)
    conn = rpyc.utils.factory.unix_connect(socket_path, config={'allow_public_attrs': True, 'allow_all_attrs': True})
    return conn.root

def start(server, app_id, app_secret):
    server_thread = threading.Thread(target=start_service, daemon=True, name='SimpleProfiler.ServiceThread')
    server_thread.start()

    process = multiprocessing.Process(target=Agent, daemon=True, args=(server, app_id, app_secret))
    process.start()
