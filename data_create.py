import time
import threading
import random
from queue import Queue
from datetime import datetime, timedelta
import logging

# 全局打印锁防止输出混乱
print_lock = threading.Lock()
data_queue: Queue[str] = Queue()
stop_event = threading.Event()

logging.basicConfig(
    filename='desktopApp/app.log', 
    level=logging.WARNING, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def 生成配速(当前时间):
    """根据时间计算当前配速"""
    if 当前时间 < 16:
        return 17 + (30 - 17) * (当前时间 / 16)
    elif 当前时间 < 46:
        return 30 + (25 - 30) * ((当前时间 - 16) / 30)
    elif 当前时间 < 66:
        return 25 + (3.6 - 25) * ((当前时间 - 46) / 20)
    else:
        return 3.6


def 生成心率(当前时间):
    """根据时间计算当前心率"""
    if 当前时间 < 30:
        return 80 + (160 - 80) * (当前时间 / 30)
    elif 当前时间 < 66:
        return 160 + random.randint(-5, 5)
    else:
        持续时间 = 当前时间 - 66
        return 160 - (160 - 80) * (持续时间 / 300) if 持续时间 < 300 else 80

def write_to_file():
    """ 定期将数据队列中的数据写入文件 """
    while not stop_event.is_set():
        with open("desktopApp/heart_rate.txt", "a") as file:
                while not data_queue.empty():
                    data = data_queue.get()
                    file.write(data + "\n")
                    logging.info(f"已写入文件: {data}")
                file.flush()
        time.sleep(3)

def 验证数据合理性(最近5次数据):
    """验证最近5次数据的合理性"""
    if len(最近5次数据) < 5:
        return True

    心率 = [int(数据.split('心率：')[1].split('次/分')[0]) for 数据 in 最近5次数据]
    配速 = [float(数据.split('配速：')[1].split('公里/小时')[0]) for 数据 in 最近5次数据]

    def 计算拐点数量(数据):
        拐点数量 = 0
        for i in range(1, 4):  # 只检查中间的三个数据点
            if (数据[i] > 数据[i-1] and 数据[i] > 数据[i+1]) or (数据[i] < 数据[i-1] and 数据[i] < 数据[i+1]):
                拐点数量 += 1
        return 拐点数量

    心率拐点数量 = 计算拐点数量(心率)
    配速拐点数量 = 计算拐点数量(配速)

    if 心率拐点数量 >= 2 or 配速拐点数量 >= 2:
        logging.warning(f"不合理数据检测到: {最近5次数据}")
        return False

    return True

def 设备模拟(设备编号, 基准时间):
    """单个设备的数据生成逻辑"""
    # 生成设备专属随机误差（固定值）
    配速误差 = random.uniform(-1, 1)
    心率误差 = random.uniform(-5, 5)
    
    # 初始化最近5次数据的数组
    最近5次数据 = []

    for 时间差 in range(0, 367, 2):  # 总时长366秒，每2秒一次
        当前时间 = 基准时间 + timedelta(seconds=时间差)
        时间戳 = 当前时间.strftime("%Y-%m-%d %H:%M:%S")

        # 计算基础值
        基础配速 = 生成配速(时间差)
        基础心率 = 生成心率(时间差)

        # 应用设备专属误差
        当前配速 = max(基础配速 + 配速误差, 0.1)  # 保证最小配速
        当前心率 = max(min(基础心率 + 心率误差, 220), 40)  # 限制心率范围

        # 数据四舍五入处理
        格式化配速 = round(当前配速, 1)
        格式化心率 = int(round(当前心率))

        输出内容 = f"设备{设备编号}: 时间{时间戳}，心率：{格式化心率}次/分，配速：{格式化配速}公里/小时"

        # 更新最近5次数据数组
        最近5次数据.append(输出内容)
        if len(最近5次数据) > 5:
            最近5次数据.pop(0)

        # 验证数据合理性
        fl = 验证数据合理性(最近5次数据)

        with print_lock:
            print(输出内容)
            if not fl:
                print("数据异常\n")

        time.sleep(1)


if __name__ == "__main__":
    开始时间 = datetime(2025, 3, 1, 16, 0, 0)  # 设定基准时间
    线程池 = []

    with open("heart_rate.txt", "a") as file:
        start_message = f"Start recording:{time.ctime()}\n"
        file.write(start_message)
        file.flush()
        logging.info(start_message.strip())

    writer_thread = threading.Thread(target=write_to_file, daemon=True)
    writer_thread.start()

    # 创建10个设备线程
    for 设备编号 in range(1, 11):
        设备 = threading.Thread(target=设备模拟, args=(设备编号, 开始时间))
        线程池.append(设备)
        设备.start()

    # 等待所有线程完成
    for 设备 in 线程池:
        设备.join()