from PyQt5.QtCore import *
from GameClient import *

class Thread(QThread, GameClient):
    # create the signal line
    signalLine = pyqtSignal(str)

    # init method for instantiation
    def __init__(self):
        super(Thread, self).__init__()
        GameClient.__init__(self)

    # when creating a thread class one must override the QThread class's run() method
    # create an object of the class created
    # then call the QThread start() in order to call the run() method ------------- Sololearn
    def run(self):
        while True:
            try:  # to avoid any errors
                message = self.receive_message()
                if len(message):
                    self.signalLine.emit(str(message))
                else:
                    break
            except Exception as exception:  # throw an exception
                print("Error: {}".format(exception))
                break

    # Method to connect to the server
    # this could have been in the game class but i think it's better here
    # grouping similar things together is the point of classes
    # game methods in Tictactoe.py, network methods in Thread.py
    def Connect(self, server):
        while True:
            try:
                self.connect_to_server(server)  # connect to the server
                break
            except Exception as exception:  # throw an exception if one occurs
                print("Error: {}".format(exception))
                break
