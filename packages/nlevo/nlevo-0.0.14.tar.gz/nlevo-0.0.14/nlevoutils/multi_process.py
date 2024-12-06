import logging
import os
import threading
import traceback
from multiprocessing import Event, Process, Queue

logger = logging.getLogger('main')


class ProcessMaintainer:
    def __init__(self, func, args=(), kwargs={}, revive_interval=None, daemon=True):
        self.init_property()
        self.func = func    # func must be wrapped with stop_event loop
        self.args = args
        self.kwargs = kwargs
        self.revive_interval = revive_interval
        self.daemon = daemon

    def init_property(self):
        self.process = None
        self.reviver = None
        self.stop_event = None
        self.run_state_event = None

    def start(self):
        if self.process:
            raise Exception('duplicate processes')

        self.stop_event = Event()
        self.run_state_event = Event()
        self.process = Process(target=self.func, args=(
            *self.args, self.stop_event, self.run_state_event,), kwargs=self.kwargs)
        self.process.daemon = self.daemon
        self.process.start()
        # If interval is set, run the revive task
        if self.revive_interval:
            self.revive(self.revive_interval)

    def stop(self):
        if self.process:
            # Stop revive task first
            if self.reviver:
                self.reviver.cancel()

            # Stop process on running state
            if self.process.is_alive():
                self.stop_event.set()

            # Wait whether forced or normal exit
            self.process.join()
            self.init_property()

    def join(self):
        if self.process:
            self.process.join()

    # Periodic task when interval is given, also it can be done immediately without interval as needed
    def revive(self, interval=None):
        if not self.process.is_alive():
            logger.info(f'Revive {self.func.__name__}() process.')
            self.stop()
            self.start()
            interval = None

        # If interval is set, run timer to execute task after a few seconds
        if interval:
            self.reviver = threading.Timer(
                self.revive_interval, self.revive, args=(interval, ))
            self.reviver.daemon = True
            self.reviver.start()

    def is_running(self):
        return self.run_state_event and self.run_state_event.is_set()

    def __del__(self):
        self.stop()


class ProcessUtil(Process):
    def __init__(self):
        Process.__init__(self)
        self.stop_msg = 'STOP_EVENT'

    # Common methods about queue
    def get_queue_size(self, queue: Queue) -> int:
        if os.name == 'posix' and os.uname().sysname == 'Darwin':
            # Mutliprocessing queue in OSX cannot use qsize function.
            # Raises NotImplementedError on Mac OSX because of broken sem_getvalue()
            size = 0 if queue.empty() else 1
        else:
            size = queue.qsize()
        return size

    def stop_queue(self, queue: Queue):
        queue.put(self.stop_msg)

    # queue.get function wrapper for checking stop queue
    def get_queue(self, queue: Queue):
        recv = queue.get()
        if recv == self.stop_msg:
            logger.warning('queue stopped.')
            return None
        else:
            return recv

    def clear_queue(self, queue: Queue) -> bool:
        while self.get_queue_size(queue) > 0:
            try:
                queue.get_nowait()  # consume all of queue elements
            except:
                logger.error('Failed to clear queue.')
                traceback.print_exc()
                return False
        return True

    # you can overriding this method
    def run(self):
        pass
