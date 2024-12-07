import threading
import multiprocessing
from functools import partial


class GxlDynamicThreadPool:
    def __init__(self, ):
        """
        多个线程之间才可以使用多个对象
        不能使用多核心,受限于Python的单进程机制,看是多个线程
        ,其实还是单进程,只是对主要时间被IO占据的进程才有效"""
        self._threads = []

    def add_thread(self, func: callable, fun_args: list):
        thread = threading.Thread(target=func, args=fun_args)
        self._threads.append(thread)

    def add_task(self, func: callable, fun_args: list):
        self.add_thread(func, fun_args)

    def start(self):
        for thread in self._threads:
            thread.start()
        self._join()

    def run(self):
        self.start()

    def _join(self):
        for thread in self._threads:
            thread.join()


class GxlDynamicProcessPool:
    """
    多进程之间不能共享同一个对象
    """
    def __init__(self):
        """
        多进程之间不能共享同一个对象
        """
        # self.pool = multiprocessing.Pool(processes=num_threads)
        self.pool = None
        self.threads = []

    def apply_async(self, func: callable, fun_args: list):
        self.threads.append((func, fun_args))
        # self.pool.apply_async(func, fun_args)

    def add_thread(self, func: callable, fun_args: list):
        self.apply_async(func, fun_args)

    def add_task(self, func: callable, fun_args: list):
        self.apply_async(func, fun_args)

    def start(self):
        self.pool = multiprocessing.Pool(processes=len(self.threads))
        for func, fun_args in self.threads:
            self.pool.apply_async(func, fun_args)
        self.pool.close()
        self.pool.join()
    def run(self):
        self.start()

class GxlFixedThreadPool:
    def __init__(self, num_threads: int):
        """
        其实还是多进程， 没法共享对象
        :param num_threads:
        """
        self.pool = multiprocessing.Pool(processes=num_threads)

    def map(self, func: callable, iterable_arg_list: list, other_fun_args: dict):
        """
        要求函数只用第一个参数是遍历list。
        :param func:
        :param fun_args:
        :return:
        """
        partial_my_function = partial(func, **other_fun_args)
        return self.pool.map(partial_my_function, iterable_arg_list)

    def apply_async(self, func: callable, fun_args: list):
        self.pool.apply_async(func, fun_args)

    def add_thread(self, func: callable, fun_args: list):
        self.apply_async(func, fun_args)

    def add_task(self, func: callable, fun_args: list):
        self.apply_async(func, fun_args)

    def start(self):
        self.pool.close()
        self.pool.join()
    def run(self):
        self.start()

class GxlFixedProcessPool:
    def __init__(self, num_threads: int):
        self.pool = multiprocessing.Pool(processes=num_threads)

    def map(self, func: callable, iterable_arg_list: list, other_fun_args: dict):
        """
        要求函数只用第一个参数是遍历list。
        :param func:
        :param fun_args:
        :return:
        """
        partial_my_function = partial(func, **other_fun_args)
        return self.pool.map(partial_my_function, iterable_arg_list)

    def apply_async(self, func: callable, fun_args: list):
        self.pool.apply_async(func, fun_args)

    def add_thread(self, func: callable, fun_args: list):
        self.apply_async(func, fun_args)

    def add_task(self, func: callable, fun_args: list):
        self.apply_async(func, fun_args)

    def start(self):
        self.pool.close()
        self.pool.join()
    def run(self):
        self.start()