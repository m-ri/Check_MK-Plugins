# Check_MK-Plugins
Additional plugins for Check_MK (Nagios)

* MQTT_Broker_LocalCheck/**check_mqtt.py** : Measures performance data about MQTT broker, like sent/received bytes, number of messages,uptime, etc. It requires paho-mqtt for python3 (just type [`sudo -H pip3 install paho-mqtt`](https://pypi.python.org/pypi/paho-mqtt/1.3.1) )
* PiHole_LocalCheck/**check_pihole_basic.py** : Shows performances about number of DNS queries, like cached/blocked queries and types of replies (IP/CNAME..). No authentication is required about PiHole.



If you're looking about an android Check_mk/NSCA agent,  plase take into anccount my Android app [ProbeOmb](https://play.google.com/store/apps/details?id=mrm.marco.probeomd) 
