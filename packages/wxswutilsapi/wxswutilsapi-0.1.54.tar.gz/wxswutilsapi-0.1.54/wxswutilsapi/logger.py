from datetime import datetime
import os
import queue
import shutil
import threading


class Logger:
    def __init__(self, log_directory='./log', max_file_size=10 * 1024 * 1024, backup_count=5):
        self.log_directory = log_directory
        self.max_file_size = max_file_size  # 文件大小限制，单位字节
        self.backup_count = backup_count  # 最大备份文件数
        self.log_queue = queue.Queue()  # 日志队列用于异步写入

        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        self.log_levels = ['INFO', 'WARNING', 'ERROR', 'DEBUG']

        # 启动异步日志写入线程
        self.stop_event = threading.Event()
        self.write_thread = threading.Thread(target=self._process_log_queue, daemon=True)
        self.write_thread.start()

    def _rotate_log_file(self, log_file):
        """执行日志轮转操作"""
        try:
            for i in range(self.backup_count, 0, -1):
                old_file = f"{log_file}.{i}"
                new_file = f"{log_file}.{i + 1}"
                if os.path.exists(old_file):
                    if i == self.backup_count:
                        os.remove(old_file)  # 删除最旧的备份文件
                    else:
                        shutil.move(old_file, new_file)  # 备份日志文件

            if os.path.exists(log_file):
                # 复制当前日志文件内容到备份文件
                shutil.copyfile(log_file, f"{log_file}.1")
                # 清空原日志文件
                open(log_file, 'w').close()
        except Exception as e:
            print(f"日志轮转失败: {e}")

    def _write_log(self, level, message):
        """将日志写入文件，并执行日志轮转"""
        log_file = os.path.join(self.log_directory, f'{level.lower()}.log')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f'{timestamp} - {level} - {message}\n'

        try:
            with open(log_file, 'a+', encoding='utf-8') as file:
                if file.tell() + len(log_message) > self.max_file_size:
                    self._rotate_log_file(log_file)  # 日志轮转
                file.write(log_message)
        except Exception as e:
            print(f"写入日志失败: {e}")

    def _process_log_queue(self):
        """异步日志写入线程，处理日志队列中的日志条目"""
        while not self.stop_event.is_set() or not self.log_queue.empty():
            try:
                level, message = self.log_queue.get(timeout=0.5)
                self._write_log(level, message)
                self.log_queue.task_done()
            except queue.Empty:
                continue

    def log(self, level, message):
        """将日志信息放入队列进行异步写入"""
        if level not in self.log_levels:
            raise ValueError(f"Invalid log level: {level}")
        self.log_queue.put((level, message))

    def info(self, message):
        self.log('INFO', message)

    def warning(self, message):
        self.log('WARNING', message)

    def error(self, message):
        self.log('ERROR', message)

    def debug(self, message):
        self.log('DEBUG', message)

    def stop(self):
        """停止异步写入线程并处理所有剩余日志"""
        self.stop_event.set()
        self.write_thread.join()