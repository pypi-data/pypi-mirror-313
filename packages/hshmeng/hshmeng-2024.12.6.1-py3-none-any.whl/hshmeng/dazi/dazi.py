from pynput.keyboard import Controller
import time

print("打字(文字内容, 打字速度(字每分钟), 等待时间(秒)")
print("需要安装pip install keyboard")

c = Controller()

def dazi(text, apm, sleep):
    # 计算每个按键的间隔时间（秒）
    interval = 60 / apm
    time.sleep(sleep)  # 等待指定的时间
    for char in text:
        c.type(char)  # 模拟单击按键
        time.sleep(max(interval, 0.0001))  # 确保间隔时间不低于0.0001秒