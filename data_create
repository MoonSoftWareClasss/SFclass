import time
import threading
import random
from datetime import datetime, timedelta

# 全局打印锁防止输出混乱
print_lock = threading.Lock()


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


def 设备模拟(设备编号, 基准时间):
    """单个设备的数据生成逻辑"""
    # 生成设备专属随机误差（固定值）
    配速误差 = random.uniform(-5, 5)
    心率误差 = random.uniform(-5, 5)

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

        with print_lock:
            print(输出内容)

        time.sleep(2)


if __name__ == "__main__":
    开始时间 = datetime(2025, 3, 1, 16, 0, 0)  # 设定基准时间
    线程池 = []

    # 创建10个设备线程
    for 设备编号 in range(1, 11):
        设备 = threading.Thread(target=设备模拟, args=(设备编号, 开始时间))
        线程池.append(设备)
        设备.start()

    # 等待所有线程完成
    for 设备 in 线程池:
        设备.join()
