#!/usr/bin/python
# -*- coding: utf-8 -*-

import paho.mqtt.client as paho
import time, urllib
import json,sys
import funkcje as log
from modules.f_mqtt_payload import getMQTT

class mqtt:

    def __init__(self):
        self.connected=0
        self.temat='#'
        self.broker=''
        self.port=1883
        self.client=paho.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        log.log("+ Załadowany plugin MQTT")

    def on_connect(self,client, userdata, flags, rc):
        self.connected=1
        self.client.subscribe(self.temat)
        log.log("+ Zapisano do kanału "+str(self.temat))

    def on_disconnect(self,client, userdata, rc):
        self.connected=0
        log.log("- Rozłączony klient MQTT ("+self.broker+")")

    def rcon(self):
        connected=self.connected
        if self.connected==0:
            for i in range(10):
                if (connected==1):
                    break
                log.log("! Ponowne łączenie MQTT: "+str(self.broker)+":"+str(self.port))
                try:
                    self.client.reconnect()
                    connected=1
                except:
                    time.sleep(3)
        if connected==0:
            log.log("!! Błąd połączenia z MQTT")
            sys.exit()
        self.connected=connected

    def loop(self):
        self.client.loop()
        self.rcon()

    def connect(self):
        self.client.connect(self.broker, self.port, 60)
        log.log("! Łączenie MQTT "+str(self.broker)+":"+str(self.port))

    def send(self,temat,co):
        self.client.publish(temat,co)

    def on_message(self,client, userdata, msg):
        w=str(msg.payload.decode("utf-8","ignore"))
        wj=json.loads(w)
        t=msg.topic
#        print(getMQTT(wj,t))
