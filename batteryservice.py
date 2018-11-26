import psutil
import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

def get_battery_level():
    battery = psutil.sensors_battery()
    percent = battery.percent
    return percent

def main():
    #Init MQTT
    client = mqtt.Client()
    client.on_connect = on_connect
    #on_message #just report battery level, no incoming messages

    client.connect_async("iot.eclipse.org", 1883, 60)

    client.loop_start()
    while True:
        level = get_battery_level()
        client.publish("abcdefghijk/xxx", level)
        print("Published level: " + str(level))
        time.sleep(3)  

if __name__ == '__main__':
   main()
