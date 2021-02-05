import argparse

parser = argparse.ArgumentParser(description='toiot-lora-GW options')
parser.add_argument('--b', required=True, help="broker-ip")
parser.add_argument('--p', type=int, default = 1883, required=False, help="mqtt_port")
args = parser.parse_args()
