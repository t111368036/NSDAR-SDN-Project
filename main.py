from platform import node
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from workwidget.main_widget import MainWindow
from get_user.get_packet import Remote_capture
from sdn_controller.excute_ryu import Excute_ryu
from node_info.info_center import MQTT
from sdn_controller.SetRule import SetRule
from DBControll.AppTable import AppTable
#from sdn_controller.innitial import innitial_mesh_rule
#from node_info.mqtt_subscriber import MQTT_Subscriber

class Mainapp:
    def __init__(self):
        app = QApplication(sys.argv)
        mainwindow = MainWindow()
        widget = QtWidgets.QStackedWidget()
        widget.addWidget(mainwindow)
        widget.setFixedHeight(850)
        widget.setFixedWidth(1120)
        widget.show()

        start_ryu = Excute_ryu(mainwindow) # => excute ryu
        start_ryu.start()

        getUser = Remote_capture(mainwindow) # => capture user_data 
        getUser.start()
        getUser.map15_user.connect(mainwindow.loaddata_table_userdata) # => throw user_data to ui

        nodeinfo = MQTT(mainwindow) # => get infomation of node
        nodeinfo.start()
        nodeinfo.dpid_info.connect(mainwindow.loaddata_table_nodeinfo)
        
        try:
            sys.exit(app.exec_())
        except:
            SetRule().delete_rule(action='all')
            AppTable().delete_all()
            print("Exiting")
            pass

if __name__ == '__main__':
    text_GUI = Mainapp()