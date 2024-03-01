import gc
import machine
import network

def connect_wlan(ssid, password):
    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)
    sta_if.active(True)
    ap_if.active(False)

    if not sta_if.isconnected():
        print("Connecting to WLAN ({})...".format(ssid))
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            pass

    return True


def main():
    gc.collect()

    # Wi-Fi credentials
    SSID = "Galaxy S226865"
    PASSWORD = "vpkm1644"


    connect_wlan(SSID, PASSWORD)

    # Install Senko from PyPi
    #upip.install("micropython-senko")

    import senko
    OTA = senko.Senko(user="cicada1212", repo="OTA_Test", working_dir="app", files=["main.py"])
    
    print('ota init')

    if OTA.update():
        print("Updated to the latest version!")
        machine.reset()
        


if __name__ == "__main__":
    main()


