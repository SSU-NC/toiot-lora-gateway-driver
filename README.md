# toiot-lora-sink-node-driver

### Installation (for Raspberry Pi)
- Step 1   
~~~
$ sudo raspi-config nonint do_spi 0
$ sudo apt-get install python-dev python3-dev
$ sudo apt-get install python-pip python3-pip
~~~
- Step 2   
~~~
$ cd toiot-lora-gateway-driver/app
$ pip3 install -r requirements.txt
~~~

### Run 
```
$ cd toiot-lora-gateway-driver/app
$ python3 run.py --b='MQTT_BROKER_IP' --p=port_number
```
