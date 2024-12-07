import sys
import threading
import time
from collections import defaultdict
import json
from rpyc import Service
from rpyc.utils.server import ThreadedServer
import tempfile
import os
import atexit
from datetime import datetime
from .logger import logger

class SimpleProfiler:
    def __init__(self):
        self.samples = defaultdict(list)
        self.frames = []
        self.frame_to_index = {}
        self.thread_name_map = {}
        self.output_filepath = None
        self._lock = threading.Lock()
        self._stop_signal = threading.Event()

    def simple(self, duration = 30.0, interval = 0.001):
        if self.is_running():
            logger.info('Profiling is already in progress...')
            return None

        self.output_filepath = self._generate_filepath()
        logger.info(f"Profiling to {self.output_filepath} for {duration} seconds with interval {interval}")

        thread = threading.Thread(
            target=self._profile_loop,
            args=(duration, interval),
            name='SimpleProfiler.ProfileThread',
            daemon=True
        )
        thread.start()

        return self.output_filepath

    def is_running(self):
        return self._lock.locked()

    def stop(self):
        if not self._stop_signal.is_set():
            self._stop_signal.set()
        return self.output_filepath

    def _get_frame_index(self, frame):
        key = (
            frame.f_code.co_filename,
            frame.f_code.co_name,
            frame.f_lineno
        )
        if key not in self.frame_to_index:
            idx = len(self.frames)
            self.frame_to_index[key] = idx
            self.frames.append({
                "name": frame.f_code.co_name,
                "file": frame.f_code.co_filename,
                "line": frame.f_lineno
            })
        return self.frame_to_index[key]

    def _profile_loop(self, duration, interval):
        if not self._lock.acquire(blocking=False):
            return

        try:
            self._stop_signal.clear()
            start_time = time.time()
            pid = os.getpid()
            profiler_thread_id = threading.current_thread().ident

            while time.time() - start_time <= duration and not self._stop_signal.is_set():
                try:
                    frames = sys._current_frames()
                    for tid, frame in frames.items():
                        if tid == profiler_thread_id:
                            continue

                        thread_key = (pid, tid)
                        if thread_key not in self.thread_name_map:
                            thread_name = "Unknown"
                            for t in threading.enumerate():
                                if t.ident == tid:
                                    thread_name = t.name
                                    break
                            thread_label = f'Thread {tid} "{thread_name}"'
                            self.thread_name_map[thread_key] = thread_label

                        frame_indices = []
                        current_frame = frame
                        while current_frame:
                            idx = self._get_frame_index(current_frame)
                            frame_indices.append(idx)
                            current_frame = current_frame.f_back

                        if frame_indices:
                            frame_indices.reverse()
                            self.samples[thread_key].append(frame_indices)

                except Exception as e:
                    logger.error(f"Sampling error: {e}")

                time.sleep(interval)

            self._save_speedscope(self.output_filepath, interval)
        finally:
            self._stop_signal.clear()
            self._lock.release()

    def _save_speedscope(self, output_file, interval):
        speedscope_data = {
            "$schema": "https://www.speedscope.app/file-format-schema.json",
            "shared": {
                "frames": self.frames
            },
            "profiles": [],
            "name": "py-profile",
            "activeProfileIndex": 0,
            "exporter": "py-profiler"
        }

        for (pid, tid), samples in self.samples.items():
            thread_name = self.thread_name_map.get((pid, tid), f"Thread {tid}")
            end_value = len(samples)
            scaled_end_value = end_value * interval

            profile = {
                "type": "sampled",
                "name": thread_name,
                "unit": "seconds",
                "startValue": 0.0,
                "endValue": scaled_end_value,
                "samples": samples,
                "weights": [interval] * len(samples)
            }
            speedscope_data["profiles"].append(profile)

        speedscope_data["profiles"].sort(key=lambda p: p["name"])

        os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(speedscope_data, f)

        logger.info(f"\nProfile saved to: {output_file}")
        logger.info(f"Total samples: {sum(len(s) for s in self.samples.values())}")
        logger.info("Visit https://www.speedscope.app/ to view")

    def _generate_filepath(self):

        timestamp = str(int(datetime.now().timestamp() * 1000000))
        pid = os.getpid()
        temp_dir = tempfile.gettempdir()
        profile_name = f"x-cpuprofile-{pid}-{timestamp}"
        filename = f"{profile_name}.cpuprofile"

        return os.path.join(temp_dir, filename)

class ProfilerService(Service):
    def __init__(self):
        super().__init__()
        self.profiler = SimpleProfiler()

    def exposed_start_profiling(self, duration=30.0, interval=0.001):
        return self.profiler.simple(duration, interval)

    def exposed_stop_profiling(self):
        return self.profiler.stop()

    def exposed_is_running(self):
        return self.profiler.is_running()

def get_socket_path():
    socket_name = f"profiler-{os.getpid()}.sock"
    return os.path.join(tempfile.gettempdir(), socket_name)

def start_service():
    socket_path = get_socket_path()

    if os.path.exists(socket_path):
        os.unlink(socket_path)

    def cleanup():
        if os.path.exists(socket_path):
            os.unlink(socket_path)

    atexit.register(cleanup)

    server = ThreadedServer(
        ProfilerService,
        socket_path=socket_path,
        protocol_config={
            'allow_public_attrs': True,
            'allow_all_attrs': True
        }
    )
    logger.info(f"Starting profiler service on {socket_path}")
    server.start()
