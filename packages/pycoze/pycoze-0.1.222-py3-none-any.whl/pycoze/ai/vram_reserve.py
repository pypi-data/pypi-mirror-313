import subprocess
import sqlite3
import atexit
import time
import os
import psutil
import sys
from pycoze import utils

# 定义数据库连接和初始化
params = utils.read_params_file()
if params:
    DATABASE_PATH = params["appPath"] + "/vram_usage.db"
else:
    DATABASE_DIR = os.path.expanduser("~/pycoze")
    os.makedirs(DATABASE_DIR, exist_ok=True)
    DATABASE_PATH = os.path.join(DATABASE_DIR, "vram_usage.db")

TABLE_NAME = "vram_usage"


def initialize_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY,
            uid TEXT NOT NULL,
            reserved_gb REAL NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


def get_vram_resources():
    try:
        # 使用nvidia-smi命令获取VRAM信息
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.total", "--format=csv,noheader,nounits"],
            stdout=subprocess.PIPE,
            text=True,
        )
        total_memory_list = result.stdout.strip().split("\n")
        total_memory = 0
        for mem in total_memory_list:
            try:
                total_memory += float(mem)
            except:
                pass
        return round(total_memory / 1024, 2)
    except Exception as e:
        print(f"Error getting VRAM resources: {e}")
        return 0.0


def reserve_vram(gb, uid=None):
    if uid is None:
        uid = f"pid:{os.getpid()}"
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT SUM(reserved_gb) FROM {TABLE_NAME}")
        total_reserved = cursor.fetchone()[0]
        if total_reserved is None:
            total_reserved = 0.0
        available_gb = get_vram_resources() - total_reserved
        if available_gb >= gb:
            cursor.execute(
                f"INSERT INTO {TABLE_NAME} (uid, reserved_gb) VALUES (?, ?)",
                (uid, gb),
            )
            conn.commit()
            print(f"预留成功，剩余VRAM大小: {available_gb - gb} GB")
            return True
        else:
            print(f"预留失败，剩余VRAM大小: {available_gb} GB")
            return False


def reserve_vram_retry(gb, retry=None, uid=None):
    if retry is None:
        # 接近无限重试，python中允许无限大的整数，尽管sys.maxsize不是真正的无限大，但足够大
        retry = sys.maxsize
    for i in range(retry):
        time.sleep(1)
        if i % 10 == 0 or i < 10 and i != 0:
            print(f"重试第{i}次")
        if reserve_vram(gb, uid):
            return True
    return False


def unreserve_vram(uid=None):
    if uid is None:
        uid = f"pid:{os.getpid()}"
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE uid = ?", (uid,))
        conn.commit()


# 注册退出时的清理函数
def cleanup():
    unreserve_vram()


def initialize_and_check():
    initialize_db()
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT uid, reserved_gb FROM {TABLE_NAME}")
        rows = cursor.fetchall()
        for row in rows:
            uid, reserved_gb = row
            try:
                # 检查进程是否存在
                if uid.startswith("pid:"):
                    pid = int(uid.split(":")[1])
                    psutil.Process(pid)
            except psutil.NoSuchProcess:
                # 进程不存在，删除对应的记录
                cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE uid = ?", (uid,))
                print(f"进程 {uid} 不存在，已删除对应的预留记录")
        conn.commit()


# 在模块加载时执行初始化检查
initialize_and_check()

# 注册清理函数
atexit.register(cleanup)

if __name__ == "__main__":
    if reserve_vram_retry(5):
        print("(1)VRAM资源预留成功")
        if reserve_vram_retry(5):
            print("(2)VRAM资源预留成功")
            time.sleep(100)
            release_vram()
            print("VRAM资源释放成功")
    else:
        print("VRAM资源不足，无法预留")
