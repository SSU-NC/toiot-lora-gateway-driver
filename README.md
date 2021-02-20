# toiot-LoRa2MQTT-Gateway (Simple Single Channel Gateway)
This toiot single-channel gateway helps to communicate between LoRa and MQTT communication.   
 ![Introduce](https://user-images.githubusercontent.com/49184890/108085783-0a5c1680-70b9-11eb-8d49-5b4d0961b098.jpg)   
For more information on LoRaWAN, please refer to the following repository(https://github.com/gjlee0802/LoRaWAN-Study).   
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
