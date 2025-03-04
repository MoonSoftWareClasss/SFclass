import time
import threading
import random
from queue import Queue
from datetime import datetime, timedelta
import logging

# 全局打印锁防止输出混乱
print_lock = threading.Lock()
data_queue = Queue()
stop_event = threading.Event()

logging.basicConfig(
    filename='desktopApp/app.log', 
    level=logging.WARNING, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def generate_pace(current_time):
    """根据时间计算当前配速"""
    if current_time < 16:
        return 17 + (30 - 17) * (current_time / 16)
    elif current_time < 46:
        return 30 + (25 - 30) * ((current_time - 16) / 30)
    elif current_time < 66:
        return 25 + (3.6 - 25) * ((current_time - 46) / 20)
    else:
        return 3.6


def generate_heart_rate(current_time):
    """根据时间计算当前心率"""
    if current_time < 30:
        return 80 + (160 - 80) * (current_time / 30)
    elif current_time < 66:
        return 160 + random.randint(-5, 5)
    else:
        duration = current_time - 66
        return 160 - (160 - 80) * (duration / 300) if duration < 300 else 80

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

def validate_data(recent_data):
    """验证最近5次数据的合理性"""
    if len(recent_data) < 5:
        return True

    heart_rates = [int(data.split('心率：')[1].split('次/分')[0]) for data in recent_data]
    paces = [float(data.split('配速：')[1].split('公里/小时')[0]) for data in recent_data]

    def count_inflection_points(data):
        inflection_points = 0
        for i in range(1, 4):  # 只检查中间的三个数据点
            if (data[i] > data[i-1] and data[i] > data[i+1]) or (data[i] < data[i-1] and data[i] < data[i+1]):
                inflection_points += 1
        return inflection_points

    heart_rate_inflection_points = count_inflection_points(heart_rates)
    pace_inflection_points = count_inflection_points(paces)

    if heart_rate_inflection_points >= 2 or pace_inflection_points >= 2:
        logging.warning(f"不合理数据检测到: {recent_data}")
        return False

    return True

def device_simulation(device_id, base_time):
    """单个设备的数据生成逻辑"""
    # 生成设备专属随机误差（固定值）
    pace_error = random.uniform(-1, 1)
    heart_rate_error = random.uniform(-5, 5)
    
    # 初始化最近5次数据的数组
    recent_data = []

    for time_diff in range(0, 367, 2):  # 总时长366秒，每2秒一次
        current_time = base_time + timedelta(seconds=time_diff)
        timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

        # 计算基础值
        base_pace = generate_pace(time_diff)
        base_heart_rate = generate_heart_rate(time_diff)

        # 应用设备专属误差
        current_pace = max(base_pace + pace_error, 0.1)  # 保证最小配速
        current_heart_rate = max(min(base_heart_rate + heart_rate_error, 220), 40)  # 限制心率范围

        # 数据四舍五入处理
        formatted_pace = round(current_pace, 1)
        formatted_heart_rate = int(round(current_heart_rate))

        output_content = f"设备{device_id}: 时间{timestamp}，心率：{formatted_heart_rate}次/分，配速：{formatted_pace}公里/小时"

        # 更新最近5次数据数组
        recent_data.append(output_content)
        if len(recent_data) > 5:
            recent_data.pop(0)

        # 验证数据合理性
        fl = validate_data(recent_data)

        with print_lock:
            print(output_content)
            if not fl:
                print("数据异常\n")

        time.sleep(1)

def single_device_simulation(time_diff):
    """单个设备的数据生成逻辑"""
    # 生成设备专属随机误差（固定值）
    pace_error = random.uniform(-1, 1)
    heart_rate_error = random.uniform(-5, 5)
    
    # 计算基础值
    base_pace = generate_pace(time_diff)
    base_heart_rate = generate_heart_rate(time_diff)

    # 应用设备专属误差
    current_pace = max(base_pace + pace_error, 0.1)  # 保证最小配速
    current_heart_rate = max(min(base_heart_rate + heart_rate_error, 220), 40)  # 限制心率范围

    # 数据四舍五入处理
    formatted_pace = round(current_pace, 1)
    formatted_heart_rate = int(round(current_heart_rate))
    
    return formatted_heart_rate, formatted_pace

if __name__ == "__main__":
    start_time = datetime(2025, 3, 1, 16, 0, 0)  # 设定基准时间
    thread_pool = []

    with open("heart_rate.txt", "a") as file:
        start_message = f"Start recording:{time.ctime()}\n"
        file.write(start_message)
        file.flush()
        logging.info(start_message.strip())

    writer_thread = threading.Thread(target=write_to_file, daemon=True)
    writer_thread.start()

    # 创建10个设备线程
    for device_id in range(1, 11):
        device = threading.Thread(target=device_simulation, args=(device_id, start_time))
        thread_pool.append(device)
        device.start()

    # 等待所有线程完成
    for device in thread_pool:
        device.join()


        
