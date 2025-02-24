import random
import time
import threading

def generate_heart_rate(device_id):
    """ 持续生成指定设备的心率数据 """
    while True:
        # 生成150-160之间的随机心率
        heart_rate = random.randint(150, 160)
        # 打印设备信息（带时间戳）
        print(f"[{time.ctime()}] 设备{device_id}: 心率 {heart_rate}/min")
        # 暂停1秒（模拟实时数据流）
        time.sleep(1)

def main():
    # 创建并启动10个设备的线程
    threads = []
    for device_id in range(1, 11):
        thread = threading.Thread(
            target=generate_heart_rate,
            args=(device_id,),
            daemon=True  # 设置为守护线程
        )
        thread.start()
        threads.append(thread)

    # 保持主线程运行直到手动停止
    try:
        while True:

            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n程序已停止")

if __name__ == "__main__":
    main()
