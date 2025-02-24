import random
import time
import threading
from queue import Queue

lock = threading.Lock()
data_queue = Queue()
stop_event = threading.Event()

def generate_heart_rate(device_id):
    """ 持续生成指定设备的心率数据 """
    while not stop_event.is_set():
        heart_rate = random.randint(150, 160)
        data = f"[{time.ctime()}] Device{device_id}: Rate {heart_rate}/min"
        data_queue.put(data)
        time.sleep(1)

def write_to_file():
    """ 定期将数据队列中的数据写入文件 """
    while not stop_event.is_set():
        with lock:
            with open("heart_rate.txt", "a") as file:
                while not data_queue.empty():
                    file.write(data_queue.get() + "\n")
                file.flush()
        time.sleep(3)

def main():
    with open("heart_rate.txt", "a") as file:
        file.write(f"Start recording:{time.ctime()}\n")
        file.flush()
    
    writer_thread = threading.Thread(target=write_to_file, daemon=True)
    writer_thread.start()

    threads = []
    for device_id in range(1, 11):
        thread = threading.Thread(
            target=generate_heart_rate,
            args=(device_id,),
            daemon=True
        )
        thread.start()
        threads.append(thread)
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n程序正在结束，请等待当前数据写入\n")
        stop_event.set()
        try:
            writer_thread.join()
        except KeyboardInterrupt:
            pass
        for thread in threads:
            try:
                thread.join()
            except KeyboardInterrupt:
                pass
        print("程序已停止\n")

if __name__ == "__main__":
    main()