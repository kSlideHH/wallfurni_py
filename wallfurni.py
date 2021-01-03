import threading
import time
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget

from g_python.hdirection import Direction
from g_python.hmessage import HMessage
from g_python.hpacket import HPacket

HEADER_ON_PLACE_WALL_ITEM = 108

from wallfurnigui import  Ui_WallFurniUI


class WallFurni:
    def __init__(self, extension):
        self.__extension = extension
        self.furni_id = 0
        self.z = 0
        self.x = 0
        self.depth = 0
        self.y = 0
        self.orientation = "l"
        self.__verbose = True
        self.__block = True
        self.__lock = threading.Lock()
        self.__guiLoopThread = None

        extension.intercept(Direction.TO_SERVER, self.__on_place_wall_item, HEADER_ON_PLACE_WALL_ITEM)

        self.__app = None
        self.__window = None
        self.__ui = None

        self.__initialize_gui()

    def __initialize_gui(self):
        self.__app = QApplication(sys.argv)
        self.__window = QtWidgets.QMainWindow()
        self.__window.setWindowTitle("WallFurni by kSlide")
        self.__ui = Ui_WallFurniUI()
        self.__ui.setupUi(self.__window)
        self.__window.show()
        sys.exit(self.__app.exec_())

    def __on_place_wall_item(self, message: HMessage):
        (self.__furni_id, self.z, self.x, self.depth, self.y, self.orientation) = message.packet.read("liiiis")
        self.log(
            f'<PlaceWallitem> [{self.furni_id}] - Z: {self.z} - X: {self.x} - D: {self.depth} - Y: {self.y} - '
            f'orientation: {self.orientation}')
        message.is_blocked = self.__block

    def __place_wall_item(self, furni, z, x, depth, y, orientation):
        self.__extension \
            .send_to_server(
            HPacket('{l}{h:' + str(HEADER_ON_PLACE_WALL_ITEM) + '}{l:' + str(furni) + '}{i:' + str(x) + '}{i:' + str(
                z) + '}{i:' + str(depth) + '}{i:' + str(y) + '}{s:"' + str(orientation) + '"}'))

    def __refresh_wall_item_position(self):
        self.__place_wall_item(self.furni_id, self.z, self.x, self.depth, self.y, self.orientation)

    def set_furni(self, furni: str):
        self.furni_id = furni
        self.__refresh_wall_item_position()
        return self

    def set_z(self, z: int):
        self.z = z
        self.__refresh_wall_item_position()
        return self

    def set_x(self, x: int):
        self.x = x
        self.__refresh_wall_item_position()
        return self

    def set_depth(self, depth: int):
        self.depth = depth
        self.__refresh_wall_item_position()
        return self

    def set_y(self, y: int):
        self.y = y
        self.__refresh_wall_item_position()
        return self

    def set_orientation(self, orientation: str):
        self.orientation = orientation
        self.__refresh_wall_item_position()
        return self

    def log(self, message):
        if self.__verbose:
            print(f'({time.strftime("%d %b %Y %H:%M:%S", time.gmtime())}) <WallFurni> {message}')
