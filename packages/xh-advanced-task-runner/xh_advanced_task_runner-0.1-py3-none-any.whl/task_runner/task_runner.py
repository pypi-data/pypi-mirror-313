import concurrent.futures
import threading
import time
import random
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def run_task_in_pool(func, num_threads, use_process_pool=False, retries=3, *args, **kwargs):
    """
    使用线程池或进程池执行传入的任务函数，并收集每个任务的执行结果。
    支持任务重试。

    :param func: 需要执行的函数
    :param num_threads: 线程池/进程池的大小
    :param use_process_pool: 是否使用进程池，默认为 False 使用线程池
    :param retries: 失败时最大重试次数
    :param args: 函数的位置参数
    :param kwargs: 函数的关键字参数
    :return: 任务执行的结果列表
    """
    start_time = time.time()

    # 选择线程池还是进程池
    PoolExecutor = concurrent.futures.ProcessPoolExecutor if use_process_pool else concurrent.futures.ThreadPoolExecutor

    # 使用线程池或进程池进行并发执行
    with PoolExecutor(max_workers=num_threads) as executor:
        # 提交多个任务并返回 Future 对象
        future_to_func = {executor.submit(func, *args, **kwargs): i for i in range(num_threads)}

        results = []
        for future in concurrent.futures.as_completed(future_to_func):
            try:
                result = future.result()  # 获取每个任务的执行结果
                results.append(result)
            except Exception as e:
                logging.error(f"Task failed: {e}")
                # 重试机制
                if retries > 0:
                    logging.info(f"Retrying task...")
                    results.append(run_task_with_retries(func, retries - 1, *args, **kwargs))
                else:
                    results.append(None)

    logging.info(f"Execution Time: {time.time() - start_time:.2f} seconds")
    return results

def run_task_with_retries(func, retries, *args, **kwargs):
    """
    尝试执行任务，如果失败则重试。
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        if retries > 0:
            logging.info(f"Retrying task due to error: {e}")
            return run_task_with_retries(func, retries - 1, *args, **kwargs)
        else:
            logging.error(f"Task failed after retries: {e}")
            return None

def fetch_url(iterations, url):
    """
    模拟一个任务函数，每次迭代模拟等待。
    :param iterations: 迭代次数
    :param url: 用于打印的 URL
    """
    try:
        thread_id = threading.get_ident()
        for i in range(iterations):
            logging.info(f"Thread ID: {thread_id}, Iteration: {i + 1} for {url}")
            time.sleep(random.randint(1, 3))  # 模拟耗时操作
        return f"Task completed by thread {thread_id} for {url}"
    except Exception as e:
        logging.error(f"Error in fetch_url: {str(e)}")
        return None
