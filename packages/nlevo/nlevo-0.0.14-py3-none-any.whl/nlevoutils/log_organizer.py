import logging
import logging.handlers
import os
import traceback
from multiprocessing import Queue as MultiprocessQueue
from threading import Thread
from nlevoutils.common import get_parents_path


class LogOrganizer():

    def __init__(self, maxsize=500, name='total'):
        self.name = name
        self.listener = None
        self.log_queue = MultiprocessQueue(maxsize=maxsize)
        self.occupied_color_index = 0

        # define log colors
        string_effect = '\033[2m'
        colors = {
            'GREEN': '\033[32m',
            'YELLOW': '\033[33m',
            'BLUE': '\033[34m',
            'MAGENTA': '\033[35m',
            'CYAN': '\033[36m',
            'BRIGHT_GREEN': f'{string_effect}\033[92m',
            'BRIGHT_YELLOW': f'{string_effect}\033[93m',
            'BRIGHT_BLUE': f'{string_effect}\033[94m',
            'BRIGHT_MAGENTA': f'{string_effect}\033[95m',
            'BRIGHT_CYAN': f'{string_effect}\033[96m',
            'RED': '\033[31m',
            'RESET_ALL': '\033[0m',
        }
        self.colors_list = list(colors.values())
        self.default_format = colors['RESET_ALL']

        # make log directory
        if os.path.exists('/app'):
            self.base_log_dir = os.path.join('/app', 'logs', name)
        else:
            self.base_log_dir = os.path.join(
                get_parents_path(__file__, 1), 'logs', name)
        os.makedirs(self.base_log_dir, exist_ok=True)
        self.init()

    def start_listening(self, name: str):
        self.listener = Thread(target=self.consume_log_queue, args=(name, ))
        self.listener.start()

    def end_listening(self):
        self.log_queue.put(None)
        self.listener.join()

    # 자정마다 롤오버하고 최대 100일치 저장 / 100 MB 저장
    def set_time_rotating_file_logger(self, name: str, backup_count: int = 100, max_bytes=1048576*100) -> logging.Logger:
        logger = logging.getLogger(name)
        log_format = f"%(name)-12s | [%(asctime)s] %(levelname)8s | %(message)s"
        formatter = logging.Formatter(log_format)

        filehandler = logging.handlers.TimedRotatingFileHandler(os.path.join(self.base_log_dir, f'{name}.log'),
                                                                when='midnight', backupCount=backup_count, encoding='utf-8-sig')
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)
        return logger

    def consume_log_queue(self, name: str):
        logger = self.set_time_rotating_file_logger(name)
        while True:
            try:
                record = self.log_queue.get()
                if record is None:
                    break
                logger.handle(record)
            except Exception:
                logger.error('logger organizer listener problem')
                logger.info(traceback.format_exc())

    def set_queue_logger(self, name: str) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        qh = logging.handlers.QueueHandler(self.log_queue)
        logger.addHandler(qh)
        return logger

    def set_file_logger(self, name: str) -> logging.Logger:
        logger = logging.getLogger(name)
        log_format = f"{name:<15} | [%(asctime)s] %(levelname)8s | %(message)s"
        formatter = logging.Formatter(log_format)

        filehandler = logging.FileHandler(filename=os.path.join(
            self.base_log_dir, f'{name}.log'), encoding='utf-8-sig')
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)
        return logger

    def set_stream_logger(self, name: str, color_index: int = -1, file_logger=False) -> logging.Logger:
        logger = logging.getLogger(name)

        if color_index < 0:
            color_index = self.occupied_color_index
            self.occupied_color_index += 1

        color = self.colors_list[color_index % len(self.colors_list)]
        colored_log_format = f"{color}{name:<15} | [%(asctime)s] %(levelname)8s | %(message)s {self.default_format}"

        colered_formatter = logging.Formatter(colored_log_format)

        streamhandler = logging.StreamHandler()
        streamhandler.setLevel(logging.INFO)
        streamhandler.setFormatter(colered_formatter)
        logger.addHandler(streamhandler)

        self.set_queue_logger(name)
        if file_logger:
            self.set_file_logger(name)

        return logger

    def init(self):
        self.start_listening(self.name)

    def close(self):
        self.end_listening()
