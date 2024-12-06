import asyncio
import os
import socket
import sys
import aiofiles
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import StreamingResponse
from starlette.responses import RedirectResponse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from inference.benchmark import run_benchmark
from inference.util import logger

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_DIR = os.path.join(BASE_DIR, "report")


def get_latest_file(directory):
    if not os.path.isdir(directory):
        raise ValueError(f"Directory '{directory}' does not exist or is not a directory.")

    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    if not files:
        return None

    # 获取最新文件
    latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(directory, f)))
    return os.path.join(directory, latest_file)


@app.get("/", response_class=HTMLResponse)
async def root():
    logger.info('Fetching the latest report file')

    try:
        # 获取最新的报告文件
        latest_file = get_latest_file(REPORT_DIR)
        if latest_file is None:
            logger.warning("No report files found.")
            raise HTTPException(status_code=404, detail="No report files found")

        # 从文件路径中提取相对路径
        relative_path = os.path.relpath(latest_file, REPORT_DIR)

        # 重定向到最新文件的路径
        return RedirectResponse(url=f"/report/{relative_path}")

    except ValueError as ve:
        logger.error(f"ValueError: {ve}")
        return HTMLResponse(
            content=f"<h1>Error: {ve}</h1>",
            status_code=400
        )

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return HTMLResponse(
            content=f"<h1>Internal Server Error</h1><p>{str(e)}</p>",
            status_code=500
        )


@app.get("/report/{file_path:path}", response_class=HTMLResponse)
async def serve_report(file_path: str):
    logger.info(f"Fetching file: {file_path}")

    try:
        # 获取指定路径的文件
        full_path = os.path.join(REPORT_DIR, file_path)
        if not os.path.exists(full_path):
            logger.warning(f"File {file_path} does not exist.")
            return HTMLResponse(
                content=f"<h1>File '{file_path}' not found</h1><p>Please check the file path or upload a new report.</p>",
                status_code=404
            )

        # 使用异步方式读取文件内容
        async with aiofiles.open(full_path, 'r', encoding='utf-8') as file:
            content = await file.read()

        logger.info(f"Returning content from file: {full_path}")
        return HTMLResponse(content=content)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return HTMLResponse(
            content=f"<h1>Internal Server Error</h1><p>{str(e)}</p>",
            status_code=500
        )


async def log_generator():
    yield """
    <html>
    <head>
        <title>正在执行</title>
        <meta http-equiv="refresh" content="1800;url=/" />
    </head>
    <body>
        <h3>正在执行中，请稍等...</h3>
        <p>执行时间与并发数量密切相关，请您耐心等待</p>
    </body>
    </html>
    """

    # 运行基准测试
    await asyncio.to_thread(run_benchmark)  # 确保在异步线程中运行阻塞函数

    # 执行完成后重定向到根路径
    yield """
    <html>
    <head>
        <meta http-equiv="refresh" content="0;url=/" />
    </head>
    <body>
        <p>执行已完成，正在获取最新结果...</p>
    </body>
    </html>
    """


@app.get("/run", response_class=HTMLResponse)
async def run():
    # 直接返回表示正在执行的HTML页面
    return StreamingResponse(log_generator(), media_type="text/html")


def get_host_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address


def run_app():
    import uvicorn

    uvicorn.run("inference.app:app", host="0.0.0.0", port=8012, reload=False, log_level="info")


if __name__ == "__main__":
    run_app()
