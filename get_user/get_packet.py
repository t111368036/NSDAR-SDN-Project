import pyshark
import re, time
from threading import Thread
from PyQt5.QtCore import QThread,pyqtSignal, QTimer, Qt
from get_user.get_flow import Get_Live_Flow
from ssh.ssh_center import sshCenter
from DBControll.ConnectDatabase import ConnectDatabase
from DBControll.UserTable import UserTable
from sdn_controller.SetRule import SetRule

'''
capture remote
抓取map網卡之arp封包
'''
class Remote_capture(QThread):
    map15_user = pyqtSignal(str)
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        self.user_data = dict()
        self.sshcenter = sshCenter()
        self.capture_node_15 = '15'
        ConnectDatabase()

    def run(self):
        self.get()

    def get(self):
        capture = pyshark.RemoteCapture('192.168.1.{}'.format(self.capture_node_15), 'eth2', bpf_filter='ip src host 10.10.2')
        capture.sniff(packet_count=60)
        capture.close()
        for packet in capture.sniff_continuously(packet_count=60): #逐一取出擷取到的封包並且存到database
            self.add_user(packet['IP'].src, packet['ETH'].src)
        self.restart_get(self.capture_node_15)

    def add_user(self, ip, mac):
        if ip not in UserTable().pop_all_user() and ip != '10.10.2.1' and '10.10.2' in ip:
            vlan = re.search('\d+$',ip).group()
            UserTable().insert_a_user(user_ip=ip, user_mac=mac, user_vlan=vlan, user_path=str(['map15','mp55','mpp98']).replace('\'','"'), user_type='innitial')
            self.map15_user.emit('add user')
            SetRule().excute(ip_address=ip)
            try:
                for i in ['192.168.1.98', '192.168.1.99']:
                    self.sshcenter.send_command(ip=i, command='sudo arp -s {} {} -i ovsbr'.format(ip, mac))
                self.get_flow(ip, vlan)
            except Exception as e:
                print('######get_packet->ssh######\n{}\n######get_packet->ssh######'.format(e))

    def restart_get(self, node):
        if node == '15':
            time.sleep(3)
            self.get()
        
    def get_flow(self, ip, vlan):
        #print('get in thread {}: {}'.format(vlan,time.ctime()))
        self.getflow = Get_Live_Flow(vlan, ip)
        self.getflow.start()
        
if __name__ == '__main__':
    RemoteCapture = Remote_capture()
    RemoteCapture.get()