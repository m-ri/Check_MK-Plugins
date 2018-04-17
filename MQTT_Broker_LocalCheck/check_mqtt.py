#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import time as time_
import datetime as datetime_

SERVER_ADDRESS='127.0.0.1' #e.g.  192.168.1.1
TIMEOUT_RESPONSE_MILLIS=4000

#list of interesting topics https://mosquitto.org/man/mosquitto-8.html
 
debug=False
mapTopicToMessage=dict()

def on_message(client, userdata, message):
  mapTopicToMessage[message.topic]=str(message.payload.decode("utf-8"))
  if debug:
    print("########################")
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    print("")
	
def convertNumberToMultiple_1024(number, suffix='B'):
  number=int(number)
  for unit in ['','Ki','Mi','Gi','Ti']:
    if abs(number) < 1024.0:
      return "%3.1f%s%s" % (number, unit, suffix)
    number /= 1024.0
  return number+suffix
  
def convertNumberToMultiple_1000(number, suffix=''):
  number=int(number)
  for unit in ['','K','M','G','T']:
    if abs(number) < 1000.0:
      return "%3.1f%s%s" % (number, unit, suffix)
    number /= 1000.0
  return number+suffix
	
def queryMqttBroker(): 
  mqtt_QoS=0

  client.loop_start()
  '''
  client.subscribe(
    [('$SYS/broker/clients/connected',mqtt_QoS),
    ('$SYS/broker/bytes/sent',mqtt_QoS),
    ('$SYS/broker/bytes/received',mqtt_QoS),
    ('$SYS/broker/messages/sent',mqtt_QoS),
    ('$SYS/broker/messages/received',mqtt_QoS),	
	
    ('$SYS/broker/load/bytes/sent/+',mqtt_QoS), #3 topics
    ('$SYS/broker/load/bytes/received/+',mqtt_QoS), #3 topics   
    ('$SYS/broker/load/messages/received/+',mqtt_QoS), #3 topics
    ('$SYS/broker/load/messages/sent/+',mqtt_QoS),  #3 topics
	('$SYS/broker/uptime',mqtt_QoS),
	('$SYS/broker/version',mqtt_QoS)		
    ])  
  '''
  client.subscribe(
    [('$SYS/#',mqtt_QoS)]
  )
  numberExpectedTopics=19  
  timestampMaxTimeout=TIMEOUT_RESPONSE_MILLIS + (time_.time()*1000)
  
  #wait until timeout OR received all messages
  while (len(mapTopicToMessage)<numberExpectedTopics) and (time_.time()*1000)<=timestampMaxTimeout :
    time_.sleep(0.100)  
  time_.sleep(0.100)
  client.disconnect()
  #client.loop_stop() #this method is very slow,like 0.8s
  
def printPerformanceData():

  print("0 MQTT_ConnectedClients " + 
    " ConnectedClients=" + mapTopicToMessage['$SYS/broker/clients/connected'] +
    "    - Connected clients: " + mapTopicToMessage['$SYS/broker/clients/connected']
  )
  print("0 MQTT_TotalBytes " + 
    " BytesSent=" + mapTopicToMessage['$SYS/broker/bytes/sent'] + "B" +
    "|BytesReceived=" + mapTopicToMessage['$SYS/broker/bytes/received']  + "B" +
    "  - Bytes since last start. Sent: " + 
	convertNumberToMultiple_1024(mapTopicToMessage['$SYS/broker/bytes/sent']) + 
	", Received: " + 
	convertNumberToMultiple_1024(mapTopicToMessage['$SYS/broker/bytes/received'])
  )
  print("0 MQTT_AverageBytes " + 
    " BytesSent_1min=" + mapTopicToMessage['$SYS/broker/load/bytes/sent/1min'] + "B" +
    "|BytesReceived_1min=" + mapTopicToMessage['$SYS/broker/load/bytes/received/1min']  + "B" +
    "|BytesSent_5min=" + mapTopicToMessage['$SYS/broker/load/bytes/sent/5min'] + "B" +
    "|BytesReceived_5min=" + mapTopicToMessage['$SYS/broker/load/bytes/received/5min']  + "B" +
    "|BytesSent_15min=" + mapTopicToMessage['$SYS/broker/load/bytes/sent/15min'] + "B" +
    "|BytesReceived_15min=" + mapTopicToMessage['$SYS/broker/load/bytes/received/15min']  + "B" +
    "  - Bytes transmitted/received during last N minutes " 
  )
  print("0 MQTT_TotalMessages " + 
    " MessagesSent=" + mapTopicToMessage['$SYS/broker/messages/sent'] +
    "|MessagesReceived=" + mapTopicToMessage['$SYS/broker/messages/received']  +
    "  - Messages since last start. Sent: " + 
	convertNumberToMultiple_1000(mapTopicToMessage['$SYS/broker/messages/sent']) + 
	", Received: " + 
	convertNumberToMultiple_1000(mapTopicToMessage['$SYS/broker/messages/received'])
  )
  print("0 MQTT_AverageMessages " + 
    " MessagesSent_1min=" + mapTopicToMessage['$SYS/broker/load/messages/sent/1min'] +
    "|MessagesReceived_1min=" + mapTopicToMessage['$SYS/broker/load/messages/received/1min']  +
    "|MessagesSent_5min=" + mapTopicToMessage['$SYS/broker/load/messages/sent/5min'] +
    "|MessagesReceived_5min=" + mapTopicToMessage['$SYS/broker/load/messages/received/5min']  +
    "|MessagesSent_15min=" + mapTopicToMessage['$SYS/broker/load/messages/sent/15min'] +
    "|MessagesReceived_15min=" + mapTopicToMessage['$SYS/broker/load/messages/received/15min']  +
    "  - Messages transmitted/received during last N minutes " 
  )
  print("0 MQTT_Messages_ActuallyStored " + 
    " TotActuallyStored_Messages=" + mapTopicToMessage['$SYS/broker/messages/stored'] +
    "|ActuallyRetained_Messages=" + mapTopicToMessage['$SYS/broker/retained messages/count']  +
    "  - Num. messages actually stored : " + 
	convertNumberToMultiple_1000(mapTopicToMessage['$SYS/broker/messages/stored']) + 
	" (retained+durable), Num. retained messages: " + 
	convertNumberToMultiple_1000(mapTopicToMessage['$SYS/broker/retained messages/count'])
  )
  print("0 MQTT_Number_Subscriptions " + 
    " NumSubscriptions=" + mapTopicToMessage['$SYS/broker/subscriptions/count'] +    
    "  - Number of subscriptions active on the broker : " + 
	convertNumberToMultiple_1000(mapTopicToMessage['$SYS/broker/subscriptions/count']) 	
  )
  secondsFrom_brokerStarted=int(mapTopicToMessage['$SYS/broker/uptime'].replace('seconds','').replace(' ',''))
  datetime_brokerStarted=datetime_.datetime.fromtimestamp(time_.time()-secondsFrom_brokerStarted)
  print("0 MQTT_Uptime " + 
    " Uptime_seconds=" + str(secondsFrom_brokerStarted) + "s" +
    "  - Up since " + datetime_brokerStarted.strftime('%a %d %b %H:%M:%S %Y')
  )  
  try:
    print("0 MQTT_HeapMemory " + 
    " current_HeapMemory=" + mapTopicToMessage['$SYS/broker/heap/current'] +
    "B|max_HeapMemory=" + mapTopicToMessage['$SYS/broker/heap/maximum']  +
    "  - Size of heap memory in use by MQTT broker. Current " + 
	convertNumberToMultiple_1024(mapTopicToMessage['$SYS/broker/heap/current']) + 
	", maximum: " + 
	convertNumberToMultiple_1024(mapTopicToMessage['$SYS/broker/heap/maximum'])
  )
  except:
    pass

def printMqttStatus(mqttIsReachable):
  if mqttIsReachable:
    print("0 MQTT_Running - MQTT broker is running. Version: " + mapTopicToMessage['$SYS/broker/version'] )
  else:
    print("2 MQTT_Running - MQTT broker is unreachable")

client=mqtt.Client()
client.on_message=on_message

isClientConnected=False
try:
  client.connect(SERVER_ADDRESS)
  isClientConnected=True
  
except:
  isClientConnected=False
  printMqttStatus(False)  
  
if isClientConnected:
  queryMqttBroker()
  printMqttStatus(True)
  printPerformanceData()

 
#command from bash
# mosquitto_sub -v -h 127.0.0.1 -p 1883 -t '$SYS/broker/bytes/sent' -t '$SYS/broker/bytes/received' -t   '$SYS/broker/clients/connected' -t '$SYS/broker/load/messages/received/+' -t  '$SYS/broker/load/messages/sent/+' -t ''