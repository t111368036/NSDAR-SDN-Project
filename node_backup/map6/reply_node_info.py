import paho.mqtt.client as mqtt
import json, time, threading, os, iperf3, re

MQTT_BROKER = '192.168.1.143'
MQTT_PORT = 1883
MQTT_ALIVE = 60

class MQTT():
    def __init__(self):
        self.client = mqtt.Client()
        self.client.connect(MQTT_BROKER, MQTT_PORT, MQTT_ALIVE)
        self.client.on_connect = self.on_connect

    def on_connect(self, client, userdata, flags, rc, properties=None):
        print("Connected with result code "+str(rc))
        self.client.subscribe('info_request')

    def on_message(self, client, userdata, msg):
        data = msg.payload.decode("utf-8").strip('"')
        if data == 'dpidrequest':
            self.publish('node_info', self.dpid_info())
        elif data == 'test3':
            #self.publish('node_info', {'chquality': ('map16', 'mp56', self.ett_measure('10.10.1.56'))})
            parameters = self.ch_parameter_collect('10.10.1.46')
            parameters['start'] = 'map6'
            parameters['end'] = 'mp46'
            self.publish('node_info', {'chquality': parameters})
        elif data == 'test11':
            #self.publish('node_info', {'chquality': ('map16', 'mp56', self.ett_measure('10.10.1.56'))})
            parameters = self.ch_parameter_collect('10.10.1.56')
            parameters['start'] = 'map6'
            parameters['end'] = 'mp56'
            self.publish('node_info', {'chquality': parameters})
        elif data == 'iwrequest':
            self.publish('node_info', self.iw_info())

    def subscribe(self):
        self.client.on_message = self.on_message
        self.client.loop_forever()
    
    def publish(self, topic, parameters):
        data = json.dumps(parameters)
        self.client.publish(topic, data)
    
    def dpid_info(self):
        dpid = os.popen("sudo ovs-ofctl -O openflow13 show ovsbr |grep -P -o '(?<=dpid:)[a-z0-9]{16}'").read().strip('\n')
        #ip = os.popen("ifconfig ovsbr |grep -P -o '(?<=inet )\d+.\d+.\d+.\d+'").read().strip('\n')
        mac = os.popen("ifconfig ovsbr |grep -P -o '(?<=ether )[a-z0-9]+:[a-z0-9]+:[a-z0-9]+:[a-z0-9]+:[a-z0-9]+:[a-z0-9]+'").read().strip('\n')
        data = {'dpidinfo': {'map6': {'dpid': str(int(dpid, 16)), 'mac': mac}}}
        #print(data)
        return data

    def iw_info(self):
        wlan_mac = "dc:a6:32:1b:0b:c1" #55mac -> 55to15 infomation
        tx_bitrate = os.popen("iw dev wlan0 station get {}|grep -P -o '(?<=tx bitrate:)\s+\d+.\d+'".format(wlan_mac)).read().strip('\t').strip('\n')
        signal = os.popen("iw dev wlan0 station get {}|grep -P -o '(?<=signal:)\s+-\d+'".format(wlan_mac)).read().strip(' ').strip('\t').strip('\n')
        #rx_bitrate = os.popen("iw dev wlan0 station get {}|grep -P -o '(?<=rx packets:)\s+\d+'".format(wlan_mac)).read().strip('\t').strip('\n')
        data = {'iwinfo': {'map6': {'signal': float(signal), 'tx_bitrate': float(tx_bitrate)}}}
        #print(data)
        return data

    def ett_measure(self, host):
        packetsize = 12112 #bits
        bandwidth = self.iperf_measure(host)
        etx = self.etx_extract(host)
        ett = etx*(packetsize/bandwidth)
        return ett
    
    def ch_parameter_collect(self, host):
        bandwidth = self.iperf_measure(host)
        etx = self.etx_extract(host)
        return {'bandwidth': bandwidth, 'etx': etx}

    def iperf_measure(self, host):
        iperf_client = iperf3.Client()
        iperf_client.duration = 1 # Measurement time [sec]
        iperf_client.server_hostname = host # Server's IP address
        iperf_client.port = 5202
        result = iperf_client.run()
        if result.error:
            print(result.error)
            return None
        else:
            print(float(result.sent_bps))   
            return float(result.sent_bps)
    
    def etx_extract(self, host):
        data = os.popen("echo /link | nc localhost 2006 | grep {}".format(host)).read()
        print(data)
        return float(re.search('\d+.\d+(?=\Wt\Wn)', repr(data)).group())

if __name__ == '__main__':
    nodeinfo = MQTT()
    nodeinfo.subscribe()
