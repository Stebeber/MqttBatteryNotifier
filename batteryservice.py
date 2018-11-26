import psutil
import paho.mqtt.client as mqtt
import time
import json

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
    #Read config
    with open("conf.json") as json_config:
        data = json.load(json_config)
    conf_datapusher = data["datapusher"]
    conf_mqtt = data["mqttbroker"]

    print(conf_datapusher)
    print(conf_mqtt)
    
    #Init MQTT
    client = mqtt.Client(conf_datapusher["client_id"])
    client.on_connect = on_connect
    #on_message #just report battery level, no incoming messages

    client.connect_async(conf_mqtt["server"], conf_mqtt["port"], conf_mqtt["timeout"])

    client.loop_start()
    while True:
        level = get_battery_level()
        result = client.publish("abcdefghijk/xxx", level)
        print("Published level: " + str(level) + " with RC: " + str(result.rc))
        time.sleep(conf_datapusher["interval"])  

if __name__ == '__main__':
   main()
