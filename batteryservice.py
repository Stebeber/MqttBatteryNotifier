# Resource: https://stackoverflow.com/questions/45626937/how-to-get-battery-percentage-with-python

import psutil
import paho.mqtt.client as mqtt
import time
import datetime
import json
import git

def on_connect(client, userdata, flags, rc):
    print("# Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

def get_battery_level():
    battery = psutil.sensors_battery()
    percent = battery.percent
    return percent

def main():
    #Get GitInformation
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha

    #Read config
    with open("conf.json") as json_config:
        data = json.load(json_config)
    conf_datapusher = data["datapusher"]
    conf_mqtt = data["mqttbroker"]

    print("MqttBatteryNotifier - " + sha)
    print("# Config DataPusher: " + str(conf_datapusher))
    print("# Config MQTT: " + str(conf_mqtt))
    print("# Will publish to topic: " + "BatteryStatistics" + "/" + conf_datapusher["client_id"] + "/" + conf_datapusher["topic_batterylevel"])
    
    #Init MQTT
    client = mqtt.Client(conf_datapusher["client_id"])
    client.on_connect = on_connect
    #on_message #just report battery level, no incoming messages

    client.connect(conf_mqtt["server"], conf_mqtt["port"], conf_mqtt["timeout"])
    client.publish("BatteryStatistics" + "/" + conf_datapusher["client_id"] + "/gitsha", sha)

    client.loop_start()
    while True:
        level = get_battery_level()
        result = client.publish("BatteryStatistics" + "/" + conf_datapusher["client_id"] + "/" + conf_datapusher["topic_batterylevel"], level)
        print(str(datetime.datetime.now()) + ": Level: " + str(level) + " with RC: " + str(result.rc))
        time.sleep(conf_datapusher["interval"])  

if __name__ == '__main__':
   main()
