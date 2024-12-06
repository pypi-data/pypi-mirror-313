import ast
import configparser
import json
from datetime import datetime
import os
import asyncio
import argparse
import time
import sys
import traceback

import httpx
import orjson
import statistics
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import Manager
import paramiko
from openai import AsyncOpenAI
from prettytable import PrettyTable
from transformers import AutoTokenizer

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from inference.util import logger

PROMPTS = [
    {"id": 1, "prompt": "Output from 1 to 100"},
    {"id": 2, "prompt": "List the top 10 most important people in history."},
    {"id": 3, "prompt": "Define the term 'artificial intelligence'."},
    {"id": 4, "prompt": "Count the number of words in this sentence."},
    {"id": 5, "prompt": "Translate the following sentence into French: 'Hello, how are you?'"},
    {"id": 6, "prompt": "Detail the process of photosynthesis."},
]


def cost_time(func):
    def fun(*args, **kwargs):
        t = time.perf_counter()
        result = func(*args, **kwargs)
        logger.info(f'completed successfully [func [{func.__name__}] cost time:{time.perf_counter() - t:.8f} s]')
        return result

    return fun


async def get_remote_resource_usage(endpoint_data, stop_event, ssh):
    resource_usage = {
        'cpu_percentage': 0,
        'memory': {
            'used': 0,
            'total': 0,
            'percentage': 0,
        },
        'gpus': [],
    }

    ip = endpoint_data['ip']

    try:
        stdin, stdout, stderr = ssh.exec_command("top -bn1 | grep 'Cpu(s)'")
        cpu_usage_line = stdout.read().decode().strip()
        cpu_percentage = 100.0 - float(cpu_usage_line.split(',')[3].split()[0])
        resource_usage['cpu_percentage'] = cpu_percentage

        # 获取内存使用情况
        stdin, stdout, stderr = ssh.exec_command("free -m")
        memory_info = stdout.read().decode().strip().split('\n')[1].split()
        memory_used = int(memory_info[2])
        memory_total = int(memory_info[1])
        memory_percentage = (memory_used / memory_total) * 100 if memory_total > 0 else 0

        resource_usage['memory']['used'] = memory_used
        resource_usage['memory']['total'] = memory_total
        resource_usage['memory']['percentage'] = memory_percentage

        # 获取 GPU 使用情况
        stdin, stdout, stderr = ssh.exec_command(
            "nvidia-smi --query-gpu=index,utilization.gpu,utilization.memory,memory.total,memory.used --format=csv,noheader,nounits"
        )
        gpu_info_lines = stdout.read().decode().strip().split('\n')

        for line in gpu_info_lines:
            gpu_data = line.split(',')
            resource_usage['gpus'].append({
                'id': str(gpu_data[0]),
                'gpu_utilization': float(gpu_data[1]),
                'gpu_memory_utilization': float(gpu_data[2]),
                'gpu_memory_used': float(gpu_data[4]),
                'gpu_memory_total': float(gpu_data[3]),
            })

    except Exception as e:
        logger.error(f"[获取资源占用异常] IP：{ip}, result：{str(e)}")
        stop_event.set()

    return resource_usage


async def monitor_resources(endpoint_data, resource_queue, stop_event, ssh):
    cpu_usages = []
    memory_used_values = []
    memory_total_values = []
    memory_percentage_values = []
    gpu_usages = {}

    while not stop_event.is_set():
        usage = await get_remote_resource_usage(endpoint_data, stop_event, ssh)

        # 确保使用情况有效
        if usage:
            # 收集 CPU 使用情况
            cpu_usages.append(usage['cpu_percentage'])

            # 收集内存使用情况
            memory_used_values.append(usage['memory']['used'])
            memory_total_values.append(usage['memory']['total'])
            memory_percentage_values.append(usage['memory']['percentage'])

            # 收集 GPU 使用情况
            for gpu in usage['gpus']:
                gpu_id = gpu['id']
                if gpu_id not in gpu_usages:
                    gpu_usages[gpu_id] = {
                        'gpu_utilization': [],
                        'gpu_memory_utilization': [],
                        'gpu_memory_used': [],
                        'gpu_memory_total': []
                    }
                gpu_usages[gpu_id]['gpu_utilization'].append(gpu['gpu_utilization'])
                gpu_usages[gpu_id]['gpu_memory_utilization'].append(gpu['gpu_memory_utilization'])
                gpu_usages[gpu_id]['gpu_memory_used'].append(gpu['gpu_memory_used'])
                gpu_usages[gpu_id]['gpu_memory_total'].append(gpu['gpu_memory_total'])

            # 将数据放入队列
            await resource_queue.put({
                'cpu': cpu_usages,
                'memory': {
                    'used': memory_used_values,
                    'total': memory_total_values,
                    'percentage': memory_percentage_values,
                },
                'gpus': gpu_usages,
            })
        await asyncio.sleep(3)  # 每 2 秒获取一次资源使用情况


async def calculate_metrics(metrics, queue):
    # 计算 CPU 指标
    cpu_avg = sum(metrics['cpu']) / len(metrics['cpu'])
    cpu_max = max(metrics['cpu'])

    # 计算内存指标
    memory_total = metrics['memory']['total'][0]
    memory_used = metrics['memory']['used']
    memory_percentage = metrics['memory']['percentage']

    avg_memory = {
        'used': sum(memory_used) / len(memory_used),
        'usage_percentage': sum(memory_percentage) / len(memory_percentage),
        'total': memory_total
    }

    max_memory = {
        'used': max(memory_used),
        'usage_percentage': max(memory_percentage),
        'total': memory_total
    }

    avg_gpus, max_gpus = {}, {}

    # 计算 GPU 指标
    for gpu_id, gpu_data in metrics['gpus'].items():
        gpu_memory_used = gpu_data['gpu_memory_used']
        gpu_memory_total = gpu_data['gpu_memory_total'][0]  # 获取 GPU 总内存的第一个元素
        gpu_utilization = gpu_data['gpu_utilization']
        gpu_memory_utilization = gpu_data['gpu_memory_utilization']

        avg_gpus[gpu_id] = {
            'gpu_utilization': sum(gpu_utilization) / len(gpu_utilization),
            'gpu_memory_utilization': sum(gpu_memory_utilization) / len(gpu_memory_utilization),
            'gpu_memory_used': sum(gpu_memory_used) / len(gpu_memory_used),
            'gpu_memory_total': gpu_memory_total
        }

        max_gpus[gpu_id] = {
            'gpu_utilization': max(gpu_utilization),
            'gpu_memory_utilization': max(gpu_memory_utilization),
            'gpu_memory_used': max(gpu_memory_used),
            'gpu_memory_total': gpu_memory_total
        }

    # 创建新的结果字典
    result_metrics = {
        'avg_cpu': cpu_avg,
        'max_cpu': cpu_max,
        'avg_memory': avg_memory,
        'max_memory': max_memory,
        'avg_gpus': avg_gpus,
        'max_gpus': max_gpus
    }
    return result_metrics


async def requests_worker(endpoint_data, client, model_ids, prompts, endpoint, owned_by, prompt_id, pid, batch_id, ssh, queue):
    task_id = asyncio.current_task().get_name()
    prompt = prompts[prompt_id - 1]['prompt']
    logger.info(
        f"[请求发送中] | BatchID: {batch_id} |  PID: {pid:<6} | Task ID: {task_id:<6} | Model: {model_ids:<6} | Endpoint: {endpoint:<6} | Prompt ID: {prompt_id}"
    )

    metrics = {
        'batch_id': batch_id,
        'pid': pid,
        'task_id': task_id,
        'prompt_id': prompt_id,
        'total_tokens': 0,
        'elapsed_time': 0,
        'success_elapsed_time': 0,
        'failure_elapsed_time': 0,
        "success_count": 0,
        "failure_count": 1,
        'request_status': "failed",
        'response_times': 0,
        'completion_tokens': 0,
        'prompt_tokens': 0,
        'tps': 0,
        'endpoint': endpoint,
        'model': model_ids,
        'owned_by': owned_by,
        'project': client.project,
        'end_to_end_delay': 0,
        'first_token_time': 0,
        'server_incremental_delays': [],  # 增量推理时延(模型时间)
        'local_incremental_delays': []  # 增量推理时延(本地时间)
    }

    resource_queue = asyncio.Queue()
    stop_event = asyncio.Event()

    # 启动监控资源的任务
    monitor_task = asyncio.create_task(monitor_resources(endpoint_data, resource_queue, stop_event, ssh)) if ssh else None
    start_time = asyncio.get_event_loop().time()
    try:
        chat_completion = await client.chat.completions.create(
            model=model_ids,
            stream=False,  # 非流式请求
            messages=[{"role": "user", "content": str(prompt)}],
        )
        elapsed_time = asyncio.get_event_loop().time() - start_time
        usage = chat_completion.usage

        metrics.update({
            'total_tokens': usage.total_tokens,
            'completion_tokens': usage.completion_tokens,
            'prompt_tokens': usage.prompt_tokens,
            'elapsed_time': elapsed_time,
            'success_elapsed_time': elapsed_time,  # 更新请求成功已用时间
            "success_count": 1,
            'failure_count': 0,
            'request_status': "success",
            'response_times': elapsed_time,
            'tps': usage.completion_tokens / elapsed_time if elapsed_time > 0 else 0,
            'end_to_end_delay': elapsed_time,
            'first_token_time': elapsed_time,
        })

        logger.info(
            f"[请求成功] | BatchID: {batch_id} |  PID: {pid:<6} | Task ID: {task_id:<6} | Model: {model_ids:<6} | Endpoint: {endpoint:<6} | Prompt ID: {prompt_id:} "
            f"| 耗时: {elapsed_time:.2f}s | TPS: {metrics['tps']:.2f} | 总Tokens: {metrics['total_tokens']} | Completion Tokens: {metrics['completion_tokens']} | Prompt Tokens: {metrics['prompt_tokens']}"
        )

    except Exception as e:
        elapsed_time = asyncio.get_event_loop().time() - start_time  # 计算异常时的耗时

        error_messages = {
            'APITimeoutError': "[请求超时]",
            'APIConnectionError': "[连接失败]",
            'RateLimitError': "[请求速率超限]",
            'APIStatusError': "[非200状态码错误]"
        }
        error_type = type(e).__name__
        error_message = error_messages.get(error_type, f"[请求异常]")
        logger.error(f"PID: {pid:<6} | Task ID: {task_id:<6} | Endpoint: {endpoint:<6} | {error_message}: [{error_type}]{str(e)}")
        # 更新 metrics 的 request_status 和耗时
        metrics.update({
            'request_status': f"failed: [{error_type}]{str(e)}",
            'elapsed_time': elapsed_time,
            'failure_elapsed_time': elapsed_time,  # 更新请求失败已用时间
            'response_times': elapsed_time  # 记录耗时
        })
    finally:
        if monitor_task:
            stop_event.set()
            await monitor_task  # 等待监控任务完成
            resource_usage = await resource_queue.get()
            metrics.update(await calculate_metrics(resource_usage, queue))
        return metrics


async def stream_requests_worker(endpoint_data, client, model_ids, prompts, endpoint, owned_by, prompt_id, pid, batch_id, ssh, queue):
    task_id = asyncio.current_task().get_name()
    prompt = prompts[prompt_id - 1]['prompt']
    logger.info(
        f"[请求发送中] | BatchID: {batch_id} |  PID: {pid:<6} | Task ID: {task_id:<6} | Model: {model_ids:<6} | Endpoint: {endpoint:<6} | Prompt ID: {prompt_id}"
    )

    metrics = {
        'batch_id': batch_id,
        'pid': pid,
        'task_id': task_id,
        'prompt_id': prompt_id,
        'total_tokens': 0,
        'completion_tokens': 0,
        'prompt_tokens': 0,
        'elapsed_time': 0,
        'success_elapsed_time': 0,
        'failure_elapsed_time': 0,
        "success_count": 0,
        "failure_count": 1,
        'request_status': "failed",
        'response_times': 0,
        'tps': 0,
        'endpoint': endpoint,
        'model': model_ids,
        'owned_by': owned_by,
        'project': client.project,
        'end_to_end_delay': 0,  # 总的推理延迟
        'first_token_time': 0,
        'server_incremental_delays': [],  # 增量推理时延(模型时间)
        'local_incremental_delays': []  # 增量推理时延(本地时间)
    }

    resource_queue = asyncio.Queue()
    stop_event = asyncio.Event()

    # 启动监控资源的任务
    monitor_task = asyncio.create_task(monitor_resources(endpoint_data, resource_queue, stop_event, ssh)) if ssh else None
    start_time = asyncio.get_event_loop().time()
    try:
        chat_completion = await client.chat.completions.create(
            model=model_ids,
            stream=True,
            messages=[{"role": "user", "content": str(prompt)}],
        )

        # 初始化时间戳和增量延迟
        previous_server_time = 0
        previous_local_time = 0
        server_incremental_delays = []
        local_incremental_delays = []
        chunk_content = ""
        first_chunk_content = None
        first_token_time = None

        async for chunk in chat_completion:
            current_local_time = asyncio.get_event_loop().time()
            current_server_time = chunk.created
            current_chunk_content = chunk.choices[0].delta.content

            # 增量推理时延计算
            server_incremental_delays.append(current_server_time - previous_server_time)
            local_incremental_delays.append(current_local_time - previous_local_time)
            chunk_content += current_chunk_content

            # 更新时间戳
            previous_server_time = current_server_time
            previous_local_time = current_local_time

            if first_token_time is None:
                first_token_time = current_local_time - start_time
                metrics['first_token_time'] = first_token_time
                metrics['first_chunk_content'] = current_chunk_content

            # logger.info(
            #     f"[流式请求中] | BatchID: {batch_id} | Task ID: {task_id:<6} | Model: {model_ids:<6} | Endpoint: {endpoint:<6} | Prompt ID: {prompt_id} "
            #     f"Chunk Delay (Server): {server_incremental_delays[-1]} | Chunk Delay (Local): {local_incremental_delays[-1]}"
            # )

        elapsed_time = asyncio.get_event_loop().time() - start_time
        # 更新 metrics
        completion_tokens = get_tokens(model_ids, chunk_content)
        prompt_tokens = get_tokens(model_ids, prompt)
        metrics.update({
            'total_tokens': completion_tokens + prompt_tokens,
            'completion_tokens': completion_tokens,
            'prompt_tokens': prompt_tokens,
            'elapsed_time': elapsed_time,
            'success_elapsed_time': elapsed_time,
            'success_count': 1,
            'failure_count': 0,
            'request_status': "success",
            'response_times': elapsed_time,
            'tps': completion_tokens / elapsed_time if elapsed_time > 0 else 0,
            'server_incremental_delays': server_incremental_delays[1:],  # 去掉初始0延迟
            'local_incremental_delays': local_incremental_delays[1:],
            'end_to_end_delay': elapsed_time
        })

        logger.info(
            f"[请求成功] | BatchID: {batch_id} | PID: {pid:<6} | Task ID: {task_id:<6} | Model: {model_ids:<6} | Endpoint: {endpoint:<6} | Prompt ID: {prompt_id} "
            f"| 总推理延迟: {metrics['end_to_end_delay']:.2f}s | 增量推理时延(模型时间): {sum(metrics['server_incremental_delays'])} | 增量推理时延(本地时间): {sum(metrics['local_incremental_delays'])} "
            f"| TPS: {metrics['tps']:.2f} | 总Tokens: {metrics['total_tokens']} | Completion Tokens: {metrics['completion_tokens']} | Prompt Tokens: {metrics['prompt_tokens']}"
        )

    except Exception as e:
        elapsed_time = asyncio.get_event_loop().time() - start_time

        error_messages = {
            'APITimeoutError': "[请求超时]",
            'APIConnectionError': "[连接失败]",
            'RateLimitError': "[请求速率超限]",
            'APIStatusError': "[非200状态码错误]"
        }
        error_type = type(e).__name__
        error_message = error_messages.get(error_type, "[请求异常]")
        logger.error(f"PID: {pid:<6} | Task ID: {task_id:<6} | Endpoint: {endpoint:<6} | {error_message}: [{error_type}]{str(e)}")

        metrics.update({
            'request_status': f"failed: [{error_type}]{str(e)}",
            'elapsed_time': elapsed_time,
            'failure_elapsed_time': elapsed_time,
            'response_times': elapsed_time
        })

    finally:
        if monitor_task:
            stop_event.set()
            await monitor_task  # 等待监控任务结束
            resource_usage = await resource_queue.get()
            metrics.update(await calculate_metrics(resource_usage, queue))

        return metrics


def get_tokens(model_name, text):
    MODEL_PATHS = {
        "qwen": "models/qwen",
        "llama": "models/llama"
    }

    # 获取项目根路径（ai-benchmarks）
    project_root = os.path.dirname(__file__)

    # 将模型名称转为小写，便于匹配
    model_name_lower = model_name.lower()

    # 使用 next 方法来匹配模型路径
    model_path = next((os.path.join(project_root, model_path)
                       for key, model_path in MODEL_PATHS.items()
                       if key in model_name_lower), None)

    if not model_path:
        logger.error(f"未找到匹配的模型路径: {model_name}")
        return 0

    try:
        # 使用构造的模型路径加载分词器
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        tokens_input_ids = tokenizer(text)["input_ids"]

        return len(tokens_input_ids)

    except Exception as e:
        logger.error(f"get_tokens: {e}")
        return 0


async def create_openai_client(endpoint_data):
    # 自定义连接限制
    custom_limits = httpx.Limits(
        max_connections=endpoint_data.get('max_connections', 100),  # 最大连接数为1000
        max_keepalive_connections=endpoint_data.get('max_keepalive_connections', 20),  # 最大保持活动连接数为200
    )

    # 自定义超时时间
    custom_timeout = httpx.Timeout(
        connect=5.0,  # 连接超时为5秒
        read=30.0,  # 读取超时为30秒
        write=5.0,  # 写入超时为5秒
        pool=2.0  # 连接池超时为2秒
    )

    try:
        client = AsyncOpenAI(
            api_key=endpoint_data['api_key'],
            base_url=endpoint_data['endpoint'],
            http_client=httpx.AsyncClient(limits=custom_limits),  # 传递自定义的http_client
            timeout=endpoint_data.get('timeout', 20),
            max_retries=endpoint_data.get('max_retries', 1),  # 可以根据需要调整重试次数
            project="qa-wangyue",
        )
        # 获取模型列表
        models = await client.models.list()

        model_ids = [model.id for model in models.data] if endpoint_data['model'] == 'auto' else endpoint_data['model']
        owned_by = [model.owned_by for model in models.data] if endpoint_data['owned_by'] == 'auto' else endpoint_data['owned_by']
        return client, model_ids[0], owned_by[0]
    except Exception as e:
        logger.error(f"create_openai_client | 端点: {endpoint_data['endpoint']} | [{type(e).__name__}] {e}")


async def concurrency_worker(endpoint_data, batch_id, ssh, queue):
    endpoint = endpoint_data['endpoint']
    concurrent_requests = endpoint_data['concurrent_requests']
    duration_enabled = endpoint_data['duration_enabled']
    duration_time = endpoint_data['duration_time']
    duration_batch = endpoint_data['duration_batch']
    duratio_interval = endpoint_data['duratio_interval']
    prompts = endpoint_data.get('prompts')
    prompt_count = len(prompts)
    pid = os.getpid()

    client, model_ids, owned_by = await create_openai_client(endpoint_data)
    start_time = asyncio.get_event_loop().time()
    batch_results = []
    request_count = 0

    logger.info(
        f"[请求任务开始] BatchID: {batch_id} | PID: {pid:<6} | {'持续时间/s' if duration_enabled else '并发请求数'}: {duration_time if duration_enabled else concurrent_requests} | 端点: {endpoint} "
    )

    if not duration_enabled:
        workers = [
            asyncio.create_task(requests_worker(
                endpoint_data, client, model_ids, prompts, endpoint, owned_by,
                (i % prompt_count) + 1, pid, batch_id, ssh, queue
            )) if not endpoint_data['stream'] else asyncio.create_task(stream_requests_worker(  # 非流式则调用非流式函数，流式调用流式函数
                endpoint_data, client, model_ids, prompts, endpoint, owned_by,
                (i % prompt_count) + 1, pid, batch_id, ssh, queue
            ))
            for i in range(concurrent_requests)
        ]

        for completed_task in asyncio.as_completed(workers):
            result = await completed_task
            batch_results.append(result)

    else:
        last_log_time = start_time
        end_time = start_time + duration_time
        workers = []
        results_futures = []

        async def manage_requests():
            nonlocal request_count
            while asyncio.get_event_loop().time() < end_time:
                workers.append(
                    asyncio.create_task(requests_worker(
                        endpoint_data, client, model_ids, prompts, endpoint, owned_by,
                        (request_count % prompt_count) + 1, pid, batch_id, ssh, queue
                    )) if not endpoint_data['stream'] else asyncio.create_task(stream_requests_worker(  # 非流式则调用非流式函数，流式调用流式函数
                        endpoint_data, client, model_ids, prompts, endpoint, owned_by,
                        (request_count % prompt_count) + 1, pid, batch_id, ssh, queue
                    ))
                )
                request_count += 1

                if request_count % duration_batch == 0:
                    results_futures.append(asyncio.gather(*workers))
                    workers.clear()

                await asyncio.sleep(duratio_interval)

        async def log_status():
            while True:
                current_time = asyncio.get_event_loop().time()
                elapsed_time = current_time - start_time

                logger.info(
                    f"[monitor] BatchID: {batch_id} | 已发送请求数: {request_count} | 持续/已用时间: {duration_time}/{elapsed_time:.2f}秒 | 端点: {endpoint}"
                )

                if current_time >= end_time:
                    break

                await asyncio.sleep(0.5)

        # 创建任务
        manage_task = manage_requests()
        log_task = log_status()

        # await asyncio.gather(manage_requests(), log_status())
        for completed_task in asyncio.as_completed([manage_task, log_task]):
            await completed_task

        if workers:
            results_futures.append(asyncio.gather(*workers))

        all_results = await asyncio.gather(*results_futures)

        for result in all_results:
            batch_results.extend(result)

    final_time = asyncio.get_event_loop().time()
    logger.info(
        f"[请求任务完成] BatchID: {batch_id} | PID: {pid:<6} | 请求总数: {request_count if duration_enabled else concurrent_requests} | 总耗时: {final_time - start_time:.2f}秒 | 端点: {endpoint}"
    )

    return batch_results


async def requests_worker1(endpoint_data, client, model_ids, endpoint, owned_by, prompt_id, pid, batch_id, ssh, queue):
    # 模拟请求的处理时间
    import random
    print(prompt_id, '开始处理')
    if prompt_id == 3:
        # await asyncio.sleep(40)
        time.sleep(5)
    delay = random.uniform(1, 20)  # 随机延迟，模拟网络延迟
    # await asyncio.sleep(delay)
    print(delay, '处理完成')

    # 模拟请求结果
    result = {
        "batch_id": batch_id,
        "prompt_id": prompt_id,
        "pid": pid,
        "endpoint": endpoint,
        "status": "success",
        "data": f"Response from {endpoint} for prompt {prompt_id}"
    }

    # 你可以选择将结果放入队列中，如果需要的话

    return result


async def run_batch_worker(endpoint_data, ssh, queue):
    result = {}
    endpoint = endpoint_data['endpoint']
    for i in range(1, endpoint_data['batch'] + 1):
        try:
            logger.info(f"[批次{i}处理|开始] {endpoint_data['model']} | {endpoint}")
            batch_results = await concurrency_worker(endpoint_data, i, ssh, queue)  # 异步调用批次处理

            if endpoint not in result:
                result[endpoint] = {'batches': {}}

            result[endpoint]['batches'][str(i)] = {
                'results': batch_results,
                'total_time': 123  # 根据实际情况设置
            }

            logger.info(f"[批次{i}处理|完成] {endpoint_data['model']} | {endpoint} ")

        except Exception as e:
            logger.error(f"[批次{i}处理|异常] {endpoint_data['model']} | {endpoint} | result: {e}")
            logger.error(traceback.format_exc())

    logger.info(f"[全部批次处理完成] {endpoint_data['model']} | {endpoint}")
    return result


def run_concurrency_worker(endpoint_data, return_list, queue):
    ssh = ssh_connection(endpoint_data)
    logger.info(f"[开始处理端点] {endpoint_data['model']} | {endpoint_data['endpoint']}")
    queue.put(f"queue-run_concurrency_worker:{endpoint_data['endpoint']}")
    result = asyncio.run(run_batch_worker(endpoint_data, ssh, queue))  # 在进程中运行异步任务
    logger.info(f"[端点处理完成] {endpoint_data['model']} | {endpoint_data['endpoint']}")
    return_list.append(result)
    return result


def ssh_connection(endpoint_data):
    """为每个端点建立 SSH 连接，并处理异常."""
    if not endpoint_data['ip'] == '127.0.0.1':
        logger.info(f'SSH connection [{endpoint_data["ip"]}] ...')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(endpoint_data['ip'], username=endpoint_data['username'], password=endpoint_data['password'])
            return ssh
        except Exception as e:
            logger.error(f"SSH connection failed for {endpoint_data['endpoint']}: {e}")
            return None  # 返回 None 表示连接失败


def save_results_to_file(results):
    if not results:
        logger.info("结果集为空，无法保存。")
        return

    for endpoint_results in results:
        if not endpoint_results:
            logger.info("没有结果可保存，跳过此端点。")
            continue

        # 提取必要的字段信息
        model = endpoint_results[0]['model']
        owned_by = endpoint_results[0]['owned_by']
        now_str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        endpoint = endpoint_results[0]['endpoint'].replace("http://", "").split(":")[0]
        filename = f'result/{now_str}-{model}-{owned_by}@{endpoint}.json'

        json_data = {
            'model': model,
            'owned_by': owned_by,
            "time": now_str,
            "results": endpoint_results
        }

        # 使用 orjson 将数据转为字节
        json_bytes = orjson.dumps(json_data)

        # 打印简洁的日志信息
        try:
            with open(filename, 'wb') as fp:
                fp.write(json_bytes)
            logger.info(f"[保存成功] 文件: {filename} | 数据字节大小: {len(json_bytes)} | 内容: {json_data}")
        except Exception as e:
            logger.info(f"[保存失败] 文件: {filename} | 错误: {e}")


def smart_round(value, ndigits=6):
    if isinstance(value, int):
        return f"{value:.{ndigits}f}"  # 保留整数格式，转换为字符串

    rounded_value = round(value, ndigits)

    if rounded_value.is_integer():
        return f"{int(rounded_value):.{ndigits}f}"  # 转换为整数并格式化为字符串

    return f"{rounded_value:.{ndigits}f}"  # 返回保留小数位的字符串


def generate_task_report(results):
    if not results:
        return

    # 获取所有 GPU 字段
    gpu_fields = set()  # 使用集合来收集 GPU ID
    for endpoint_data in results:  # 遍历列表中的每个 endpoint 数据
        for endpoint, batches in endpoint_data.items():  # endpoint_data 是字典，获取每个端点的批次
            for batch_data in batches['batches'].values():  # 遍历每个批次
                for res in batch_data['results']:
                    if 'max_gpus' in res:
                        gpu_fields.update(res['max_gpus'].keys())  # 添加 GPU ID 到集合中
    sorted_gpu_ids = sorted(gpu_fields)

    # 创建任务统计表
    report_table = PrettyTable()
    report_table.field_names = [
        "Model", "Batch ID", "PID", "TaskID", "PromptID", "请求状态", "总耗时(s)", "总Tokens数",
        "生成Tokens", "提示Tokens", "推理TPS(tokens/s)", "首token时延(s)", "增量推理时延(s)", "e2e时延",
        "Max CPU", "Max Memory", "Max GPU Util", "Max GPU Memory Usage", "ENDPOINT"
    ]

    # 遍历每个端点
    for endpoint_data in results:
        for endpoint, batches in endpoint_data.items():
            for batch_id, batch_data in batches['batches'].items():
                for res in batch_data['results']:
                    elapsed_time = res.get('elapsed_time', 0)
                    max_memory = res.get('max_memory', {})
                    max_gpus = res.get('max_gpus', {})

                    # 格式化内存使用率
                    max_memory_usage = f"{max_memory.get('used', 0)}/{max_memory.get('total', 0)}MB({smart_round(max_memory.get('usage_percentage', 0.0), 2)}%)"

                    # 格式化 GPU 利用率和显存使用情况
                    gpu_utilization_str = ", ".join(
                        f"GPU{gpu_id}: {smart_round(max_gpus[gpu_id].get('gpu_utilization', 0), 2)}%"
                        for gpu_id in sorted_gpu_ids if gpu_id in max_gpus
                    )
                    gpu_memory_str = ", ".join(
                        f"GPU{gpu_id}: {smart_round(max_gpus[gpu_id].get('gpu_memory_used', 0))}/{smart_round(max_gpus[gpu_id].get('gpu_memory_total', 0))}MB({smart_round(max_gpus[gpu_id].get('gpu_memory_utilization', 0), 2)}%)"
                        for gpu_id in sorted_gpu_ids if gpu_id in max_gpus
                    )
                    # 填充表格行数据
                    report_table.add_row([
                        res.get('model', 'N/A'),
                        batch_id,  # 添加 batch_id 到第二列
                        res.get('pid', 'N/A'),
                        res.get('task_id', 'N/A'),
                        res.get('prompt_id', 'N/A'),
                        res.get('request_status', 'N/A'),
                        smart_round(elapsed_time),
                        res.get('total_tokens', 0),
                        res.get('completion_tokens', 0),
                        res.get('prompt_tokens', 0),
                        smart_round(res.get('tps', 0)),
                        smart_round(res.get('first_token_time')),
                        smart_round(sum(res.get('local_incremental_delays'))),
                        smart_round(res.get('end_to_end_delay')),
                        smart_round(res.get('max_cpu', 0.0), 2),
                        max_memory_usage,
                        gpu_utilization_str,
                        gpu_memory_str,
                        res.get('endpoint', 'N/A'),
                    ])

    # 输出任务统计报告
    logger.info(f"\n任务统计报告:\n{report_table}")
    return report_table


def generate_overall_report(results):
    if not results:
        return

    overall_metrics = []

    for endpoint_data in results:
        for endpoint, endpoint_info in endpoint_data.items():
            endpoint_summary = {
                'total_elapsed_time': 0,
                'total_tokens': 0,
                'response_times': [],
                'success_count': 0,
                'failure_count': 0,
                'completion_tokens': 0,
                'prompt_tokens': 0,
                'max_cpu': 0,
                'max_memory': {'used': 0, 'total': 0, 'usage_percentage': 0.0},
                'model_name': endpoint_info['batches']['1']['results'][0].get('model', 'N/A'),
                'tps': [],
                'total_batches': 0,
                'success_elapsed_time': 0,  # 请求成功已用时间
                'failure_elapsed_time': 0,  # 请求失败已用时间
                'end_to_end_delay': [],  # 总的推理延迟
                'first_token_time': [],
                'server_incremental_delays': [],  # 增量推理时延(模型时间)
                'local_incremental_delays': []  # 增量推理时延(本地时间)

            }

            for batch_info in endpoint_info['batches'].values():
                endpoint_summary['total_batches'] += 1
                for res in batch_info['results']:
                    # 更新汇总信息
                    endpoint_summary['total_elapsed_time'] += res.get('elapsed_time', 0)
                    endpoint_summary['total_tokens'] += res.get('total_tokens', 0)
                    endpoint_summary['completion_tokens'] += res.get('completion_tokens', 0)
                    endpoint_summary['prompt_tokens'] += res.get('prompt_tokens', 0)
                    endpoint_summary['success_count'] += res.get('success_count', 0)
                    endpoint_summary['failure_count'] += res.get('failure_count', 0)
                    endpoint_summary['response_times'].extend([res.get('response_times', 0)])
                    endpoint_summary['tps'].extend([res.get('tps', 0)])
                    endpoint_summary['max_cpu'] = max(endpoint_summary['max_cpu'], res.get('max_cpu', 0))

                    max_memory = res.get('max_memory', {})
                    endpoint_summary['max_memory']['used'] = max(endpoint_summary['max_memory']['used'], max_memory.get('used', 0))
                    endpoint_summary['max_memory']['total'] = max_memory.get('total', 0)
                    endpoint_summary['max_memory']['usage_percentage'] = max(endpoint_summary['max_memory']['usage_percentage'], max_memory.get('usage_percentage', 0))

                    endpoint_summary['success_elapsed_time'] += res.get('success_elapsed_time', 0)
                    endpoint_summary['failure_elapsed_time'] += res.get('failure_elapsed_time', 0)
                    endpoint_summary['end_to_end_delay'].extend([res.get('end_to_end_delay', 0)])
                    endpoint_summary['first_token_time'].extend([res.get('first_token_time', 0)])
                    endpoint_summary['server_incremental_delays'].extend([sum(res.get('server_incremental_delays', 0))])
                    endpoint_summary['local_incremental_delays'].extend([sum(res.get('local_incremental_delays', 0))])

            # 计算统计数据
            elapsed_time = endpoint_summary['total_elapsed_time']
            total_requests = endpoint_summary['success_count'] + endpoint_summary['failure_count']
            avg_elapsed_time = (endpoint_summary['success_elapsed_time'] / endpoint_summary['success_count']) if endpoint_summary['success_count'] > 0 else 0
            avg_first_token_time = (sum(endpoint_summary['first_token_time']) / endpoint_summary['success_count']) if endpoint_summary['success_count'] > 0 else 0
            avg_end_to_end_delay = (sum(endpoint_summary['end_to_end_delay']) / endpoint_summary['success_count']) if endpoint_summary['success_count'] > 0 else 0
            avg_local_incremental_delays = (sum(endpoint_summary['local_incremental_delays']) / endpoint_summary['success_count']) if endpoint_summary['success_count'] > 0 else 0

            overall_metrics.append({
                'Model': endpoint_summary['model_name'],
                'Batch': endpoint_summary['total_batches'],
                '成功请求数/耗时': f"{endpoint_summary['success_count']} | {smart_round(endpoint_summary['success_elapsed_time'])}",
                '失败请求数/耗时': f"{endpoint_summary['failure_count']} | {smart_round(endpoint_summary['failure_elapsed_time'])}",
                '总请求数/耗时(s)': f"{total_requests} | {smart_round(elapsed_time)}",
                '成功平均耗时(s)': f"{smart_round(avg_elapsed_time)}",
                '总/提示/生成Tokens': f"{endpoint_summary['total_tokens']} | {endpoint_summary['prompt_tokens']} | {endpoint_summary['completion_tokens']}",
                '平均/最大/最小TPS(tokens/s)': f"{smart_round((endpoint_summary['completion_tokens'] / avg_elapsed_time) if avg_elapsed_time > 0 else 0)} | {smart_round(max(endpoint_summary['tps'])) if endpoint_summary['tps'] else 0} | {smart_round(min(endpoint_summary['tps'])) if endpoint_summary['tps'] else 0}",
                # '单次最大TPS(tokens/s)': smart_round(max(endpoint_summary['tps'])) if endpoint_summary['tps'] else 0,
                # '单次最小TPS(tokens/s)': smart_round(min(endpoint_summary['tps'])) if endpoint_summary['tps'] else 0,
                '平均首token时延(s)': f"{smart_round(avg_first_token_time)}",
                '平均e2e时延(s)': f"{smart_round(avg_end_to_end_delay)}",
                '平均增量推理时延(s)': f"{smart_round(avg_local_incremental_delays)}",
                '最小响应时间(s)': smart_round(min(endpoint_summary['response_times'])) if endpoint_summary['response_times'] else 0,
                '最大响应时间(s)': smart_round(max(endpoint_summary['response_times'])) if endpoint_summary['response_times'] else 0,
                '中位响应时间(s)': smart_round(statistics.median(endpoint_summary['response_times'])) if endpoint_summary['response_times'] else 0,
                '平均响应时间(s)': smart_round(sum(endpoint_summary['response_times']) / len(endpoint_summary['response_times'])) if endpoint_summary['response_times'] else 0,
                'Max CPU': f"{smart_round(endpoint_summary['max_cpu'], 2)}%",
                'Max Memory': f"{smart_round(endpoint_summary['max_memory']['used'])}/{smart_round(endpoint_summary['max_memory']['total'])}MB({smart_round(endpoint_summary['max_memory']['usage_percentage'], 2)}%)"
            })

    # 创建整体统计指标表
    overall_table = PrettyTable()
    overall_table.field_names = [
        "Model", "Batch", "成功请求数/耗时", "失败请求数/耗时",
        "总请求数/耗时(s)", "成功平均耗时(s)",
        "总/提示/生成Tokens",
        "平均/最大/最小TPS(tokens/s)", '平均首token时延(s)', '平均e2e时延(s)', '平均增量推理时延(s)',
        "最小响应时间(s)", "最大响应时间(s)", "中位响应时间(s)",
        "平均响应时间(s)", "Max CPU", "Max Memory"
    ]

    for metric in overall_metrics:
        overall_table.add_row([metric[field] for field in overall_table.field_names])

    # 设置列对齐
    for field in overall_table.field_names:
        overall_table.align[field] = "c"

    logger.info(f"\n整体统计指标:\n{overall_table}")

    return overall_table


def write_prompts_to_html(endpoint):
    # 创建 PrettyTable 对象
    table = PrettyTable()

    # 设置表头
    table.field_names = ["ID", "PROMPTS"]

    # 添加数据行
    for item in endpoint['prompts']:
        table.add_row([item["id"], item["prompt"]])
    logger.info(f"\nPrompts Data - [{endpoint['endpoint']}]:\n{table}")
    return table


def save_table_to_html(report_file, table: PrettyTable, title: str, append: bool = False):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"report_{timestamp}.html"

    report_directory = report_file or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'report')

    # 如果目录不存在，则创建
    if not os.path.exists(report_directory):
        os.makedirs(report_directory)

    # 将文件保存到 report 文件夹中
    file_path = os.path.join(report_directory, filename)

    # 创建 HTML 表格字符串
    html_table = f"""
    <!DOCTYPE html>
    <html lang="zh">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: Arial, sans-serif;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
            }}
            th, td {{
                border: 1px solid black;
                padding: 4px;
                text-align: left;
                font-size: 14px; /* 调整字体大小，例如 14px */
            }}
            th {{
                background-color: #f2f2f2;
                font-size: 14px; /* 标题行字体大小，例如 16px */
            }}
        </style>
    </head>
    <body>
        <h4>{title} | {datetime.now().strftime("%Y.%m.%d %H:%M:%S")}</h1>
        {table.get_html_string()}   
    </body>
    </html>
    """

    # 根据 append 参数决定打开模式 ('a' 表示追加, 'w' 表示覆盖)
    mode = 'a' if append else 'w'

    # 打开文件并写入内容
    with open(file_path, mode, encoding='utf-8') as f:
        f.write(html_table)

    logger.info(f"{title}已{'追加' if append else '生成并'}保存 {file_path}")


def generate_config_table(endpoint_data):
    """生成配置表格"""
    table = PrettyTable()
    table.field_names = ["Section", "Endpoint", "Concurrent Requests", "Batch", "Duration Enabled",
                         "Duration Request", "Duration Batch", "Model", "stream", "Owned By"]

    for section in endpoint_data:
        sections = section['section']
        endpoint = section['endpoint']
        concurrent_requests = section['concurrent_requests']
        batch = section['batch']
        duration_enabled = section['duration_enabled']
        duration_time = section['duration_time']
        duration_batch = section['duration_batch']
        model = section['model']
        stream = section['stream']
        owned_by = section['owned_by']

        # 将信息添加到表格中
        table.add_row([sections, endpoint, concurrent_requests, batch, duration_enabled,
                       duration_time, duration_batch, model, stream, owned_by])
    logger.info(f"\n端点配置:\n{table}")
    return table


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="接收多个端点信息和其他参数"
    )

    parser.add_argument(
        '--config_file',
        type=str,
        help='config路径，如果未提供，则使用默认路径(与其他参数不可同时使用)'
    )
    parser.add_argument(
        '--report_file',
        type=str,
        help='report路径，如果未提供，则使用默认路径,ai-benchmarks/inference/report'
    )
    # 接收多个 endpoint，设置为必填
    parser.add_argument(
        '--endpoint',
        type=str,
        nargs='+',  # 接收多个 endpoint
        # required=True,  # 必填项
        help='[*]端点信息，多个端点用空格分隔'
    )
    parser.add_argument(
        '--api_key',
        type=str,
        nargs='*',
        default=['auto'],  # 默认值
        help='api_key,空格分隔'
    )
    parser.add_argument(
        '--concurrent_requests',
        type=int,
        nargs='*',
        default=[1],  # 默认值
        help='每个端点的并发请求数，空格分隔，默认为 1'
    )
    parser.add_argument(
        '--batch',
        type=int,
        nargs='*',
        default=[2],  # 默认值
        help='每个端点的批次数，空格分隔，默认为 2'
    )
    parser.add_argument(
        '--duration_time',
        type=int,
        nargs='*',
        default=[1],  # 默认值
        help='每个端点的请求持续时间，空格分隔，默认为 1'
    )
    parser.add_argument(
        '--duration_batch',
        type=int,
        nargs='*',
        default=[10],  # 默认值
        help='每个端点的请求持续时间内，批次并发,空格分隔，默认为 1'
    )
    parser.add_argument(
        '--duratio_interval',
        type=int,
        nargs='*',
        default=[0.2],  # 默认值
        help='每个端点的请求持续时间内，批次并发,空格分隔，默认为 0.2'
    )
    parser.add_argument(
        '--duration_enabled',
        type=lambda x: (str(x).lower() == 'true'),  # 转换为布尔值
        nargs='*',
        default=[False],  # 默认值
        help='每个端点的持续时间启用状态，空格分隔，默认为 False'
    )
    parser.add_argument(
        '--model',
        type=str,
        nargs='*',
        default=['auto'],  # 默认值
        help='每个端点的model，空格分隔，默认为自动获取'
    )
    parser.add_argument(
        '--stream',
        type=lambda x: (str(x).lower() == 'true'),  # 转换为布尔值
        nargs='*',
        default=[False],  # 默认值
        help='每个端点流式开关，默认关闭'
    )
    parser.add_argument(
        '--owned_by',
        type=str,
        nargs='*',
        default=['auto'],  # 默认值
        help='每个端点的owned_by，空格分隔，默认为自动获取'
    )
    parser.add_argument(
        '--prompts',
        type=str,
        nargs='*',
        help='PROMPTS,默认内置PROMPTS'
    )
    parser.add_argument(
        '--ip',
        type=str,
        nargs='*',
        default=['127.0.0.1'],  # 默认值
        help='每个端点的 IP 地址，空格分隔，默认为 192.168.1.1'
    )
    parser.add_argument(
        '--username',
        type=str,
        nargs='*',
        default=['root'],  # 默认值
        help='每个端点的用户名，空格分隔，默认为 root'
    )
    parser.add_argument(
        '--password',
        type=str,
        nargs='*',
        default=['hengshi@1qazxsw21'],  # 默认值
        help='每个端点的密码，空格分隔，默认为 hengshi@1qazxsw21'
    )
    parser.add_argument(
        '--timeout',
        type=int,
        nargs='*',
        default=[100],  # 默认值
        help='每个端点的openai超时时间，空格分隔，默认为 100'
    )
    parser.add_argument(
        '--max_retries',
        type=int,
        nargs='*',
        default=[0],  # 默认值
        help='每个端点的openai重试次数，空格分隔，默认为 0'
    )
    parser.add_argument(
        '--max_connections',
        type=int,
        nargs='*',
        default=[1000],  # 默认值
        help='最大连接数，默认为 1000'
    )
    parser.add_argument(
        '--max_keepalive_connections',
        type=int,
        nargs='*',
        default=[200],  # 默认值
        help='最大长连接保持活动状态连接数，默认为 200'
    )
    args = parser.parse_args()

    if args.config_file:
        # 如果传入了 config_file，endpoint 不是必填项
        parser.set_defaults(endpoint=[])
        config_path = args.config_file
        endpoint_data = read_config(config_path)
        return endpoint_data
    else:
        # 如果没有传入 config_file，endpoint 必填
        if not args.endpoint:
            parser.print_help()
            sys.exit("Error: '--endpoint' is required when --config_file is not provided.")

    # 输出最终的参数
    endpoint_data_list = []
    num_endpoints = len(args.endpoint)

    # 如果某些参数只提供了一个值，则使用这个值填充所有端点
    for i in range(num_endpoints):
        endpoint_data = {
            'section': 'auto',
            'endpoint': args.endpoint[i],
            'api_key': args.api_key[i] if i < len(args.api_key) else args.api_key[0],
            'concurrent_requests': args.concurrent_requests[i] if i < len(args.concurrent_requests) else args.concurrent_requests[0],
            'batch': args.batch[i] if i < len(args.batch) else args.batch[0],
            'duration_time': args.duration_time[i] if i < len(args.duration_time) else args.duration_time[0],
            'duration_enabled': args.duration_enabled[i] if i < len(args.duration_enabled) else args.duration_enabled[0],
            'duration_batch': args.duration_batch[i] if i < len(args.duration_batch) else args.duration_batch[0],
            'duratio_interval': args.duratio_interval[i] if i < len(args.duratio_interval) else args.duratio_interval[0],
            'model': args.model[i] if i < len(args.model) else args.model[0],
            'stream': args.stream[i] if i < len(args.stream) else args.stream[0],
            'prompts': json.loads(args.prompts[i] if i < len(args.prompts) else args.prompts[0]) if args.prompts else PROMPTS,
            'owned_by': args.owned_by[i] if i < len(args.owned_by) else args.owned_by[0],
            'ip': args.ip[i] if i < len(args.ip) else args.ip[0],
            'username': args.username[i] if i < len(args.username) else args.username[0],
            'password': args.password[i] if i < len(args.password) else args.password[0],
            'timeout': args.timeout[i] if i < len(args.timeout) else args.timeout[0],
            'max_retries': args.max_retries[i] if i < len(args.max_retries) else args.max_retries[0],
            'max_connections': args.max_connections[i] if i < len(args.max_connections) else args.max_connections[0],
            'max_keepalive_connections': args.max_keepalive_connections[i] if i < len(args.max_keepalive_connections) else args.max_keepalive_connections[0],
            'report_file': args.report_file[i] if i < len(args.report_file) else args.report_file[0],
        }
        endpoint_data_list.append(endpoint_data)
    return endpoint_data_list


def read_config(file_path):
    """读取配置文件并返回端点数据列表。"""
    config = configparser.ConfigParser()
    config.read(file_path, encoding='utf-8')

    endpoints = []
    for section in config.sections():
        endpoint_data = {
            'section': section,
            'endpoint': config[section]['endpoint'],
            'api_key': config[section]['api_key'],
            'concurrent_requests': config.getint(section, 'concurrent_requests'),
            'batch': config.getint(section, 'batch'),
            'duration_time': config.getint(section, 'duration_time'),
            'duration_enabled': config.getboolean(section, 'duration_enabled'),
            'duration_batch': config.getint(section, 'duration_batch'),
            'duratio_interval': config.getfloat(section, 'duratio_interval'),
            'owned_by': config.get(section, 'owned_by', fallback='auto'),
            'model': config.get(section, 'model', fallback='auto'),
            'stream': config.getboolean(section, 'stream'),
            'prompts': json.loads(config.get(section, 'prompts')) if config.get(section, 'prompts') else PROMPTS,
            'ip': config[section]['ip'],
            'username': config[section]['username'],
            'password': config[section]['password'],
            'timeout': config.getint(section, 'timeout'),
            'max_retries': config.getint(section, 'max_retries'),
            'max_connections': config.getint(section, 'max_connections'),
            'max_keepalive_connections': config.getint(section, 'max_keepalive_connections'),
        }
        endpoints.append(endpoint_data)
    return endpoints


def save_all_tables_to_html(results, endpoint_data):
    # 生成表格

    config_table = generate_config_table(endpoint_data)
    task_report = generate_task_report(results)
    overall_report = generate_overall_report(results)

    report_file = endpoint_data[0].get('report_file', None)
    save_table_to_html(report_file, config_table, title="端点配置", )
    save_table_to_html(report_file, task_report, title='任务报告', append=True)
    save_table_to_html(report_file, overall_report, title='统计报告', append=True)
    for endpoint in endpoint_data:
        prompts_table = write_prompts_to_html(endpoint)
        save_table_to_html(report_file, prompts_table, title=f"Prompts Data | {endpoint['section']}-{'config' if endpoint['prompts'] else 'default'}", append=True)


@cost_time
def run_benchmark():
    if len(sys.argv) == 1:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, 'config.ini')
        endpoint_data = read_config(config_path)
    else:
        endpoint_data = parse_arguments()

    manager = Manager()  # 使用 Manager 创建共享队列
    queue = manager.Queue()
    return_list = manager.list()

    with ProcessPoolExecutor(max_workers=len(endpoint_data)) as pool:
        futures = {
            pool.submit(run_concurrency_worker, endpoint, return_list, queue): endpoint['endpoint']
            for endpoint in endpoint_data
        }

        results = []
        for future in as_completed(futures):
            endpoint = futures[future]
            try:
                result = future.result()  # 从进程中获取结果
                results.append(result)
            except Exception as e:
                logger.error(f"Endpoint {endpoint} failed: {e}")
                logger.error(traceback.format_exc())

    # 获取所有队列中的日志内容
    while not queue.empty():
        logger.info(f"From Queue: {queue.get()}")

    # 生成报告
    save_all_tables_to_html(results, endpoint_data)


if __name__ == "__main__":
    run_benchmark()
