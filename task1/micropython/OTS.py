import network
import urequests
import ujson

# WiFi设置
wifi_ssid = "TP-LINK_1760"
wifi_password = "987654321"

# 版本和更新信息
version = "1_0_0"
baseUpdateUrl = "http://192.168.56.1:5500/esp32/"
updateJson = "http://192.168.56.1:5500/esp32/esp32_update.json"

# 连接WiFi
def connect_wifi(ssid, password):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)
    while not station.isconnected():
        pass
    print("Connected to WiFi")

# 获取远程json升级文件
def http_get_request(url):
    response = urequests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to get data")
        return None

# 判断是否需要升级
def is_or_not_need_update():
    global version
    json_data = http_get_request(updateJson)
    print(json_data)
    obj = ujson.loads(json_data)
    print(obj)
    ota_version = obj['version']

    print("远程版本：", ota_version)
    print("本地版本：", version)

    if version != ota_version:
        print("需要升级。")
        full_update_url = baseUpdateUrl + "esp32_" + ota_version + ".bin"
        print("OTA 升级地址为：", full_update_url)
        # 在MicroPython中执行OTA更新的代码与Arduino ESP32库不同，需要自定义实现
        # perform_ota_update(full_update_url)
    else:
        print("无需升级。")

def setup():
    print("Connecting to WiFi")
    connect_wifi(wifi_ssid, wifi_password)
    is_or_not_need_update()

def loop():
    i = 0
    while True:
        print(i)
        print("OTA 升级成功")
        i += 1
        time.sleep(2)

# 主程序开始
setup()
# 因为MicroPython中通常不使用类似Arduino的loop函数，所以这里直接调用setup()，对于持续运行的代码，可以在setup内部使用循环。
