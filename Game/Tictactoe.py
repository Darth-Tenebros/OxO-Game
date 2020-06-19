import sys
from PyQt5.QtWidgets import*
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import*
from GameServer import GameServer
from GameClient import*
from socket import*
from Thread import Thread
# noinspection PyRedundantParentheses

class Tictactoe(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setGeometry(250, 250, 600, 300)
        self.setWindowTitle("TenElevenGames OXO")
        self.setWindowIcon(QIcon("icon.jpg"))
        self.show()

        # NERDZONE
        # implement a simple help menu
        # create QAction buttons for the menu
        Instructions = QAction("How to play", self)
        AboutGame = QAction("About", self)
        More = QAction("More", self)

        # add the buttons to the menu
        menu = QMenuBar()
        menu.addAction(Instructions)
        menu.addAction(AboutGame)
        menu.addAction(More)

        # connect the buttons to their respective methods
        # when clicked, each button is supposed to show a popup dialogue
        # with the relevant information as per the name of the button suggests
        Instructions.triggered.connect(self.instructions)
        AboutGame.triggered.connect(self.about)
        More.triggered.connect(self.more)

        # images
        self.cross = QPixmap("cross.gif")
        self.nought = QPixmap("nought.gif")
        self.blank = QtGui.QIcon("blank.gif")

        # create a thread to run parallel to the gui
        self.messageThread = Thread()
        self.messageThread.signalLine.connect(self.threadLine)

        # Game board
        # create game buttons and set their sizes when window changes size
        # connect each button to it's OWN method
        self.buttonArray = []
        # first row
        self.button1 = QPushButton()
        self.button1.setIcon(QtGui.QIcon('blank.gif'))
        self.button1.setIconSize(QtCore.QSize(60, 85))
        self.buttonArray.append(self.button1)
        self.button1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button1.clicked.connect(self.button1Event)

        self.button2 = QPushButton()
        self.button2.setIcon(QtGui.QIcon('blank.gif'))
        self.button2.setIconSize(QtCore.QSize(60, 85))
        self.buttonArray.append(self.button2)
        self.button2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button2.clicked.connect(self.button2Event)

        self.button3 = QPushButton()
        self.button3.setIcon(QtGui.QIcon('blank.gif'))
        self.button3.setIconSize(QtCore.QSize(60, 85))
        self.buttonArray.append(self.button3)
        self.button3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button3.clicked.connect(self.button3Event)
        #
        # second row
        self.button4 = QPushButton()
        self.button4.setIcon(QtGui.QIcon('blank.gif'))
        self.button4.setIconSize(QtCore.QSize(60, 85))
        self.buttonArray.append(self.button4)
        self.button4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button4.clicked.connect(self.button4Event)

        self.button5 = QPushButton()
        self.button5.setIcon(QtGui.QIcon('blank.gif'))
        self.button5.setIconSize(QtCore.QSize(60, 85))
        self.buttonArray.append(self.button5)
        self.button5.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button5.clicked.connect(self.button5Event)

        self.button6 = QPushButton()
        self.button6.setIcon(QtGui.QIcon('blank.gif'))
        self.button6.setIconSize(QtCore.QSize(60, 85))
        self.buttonArray.append(self.button6)
        self.button6.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button6.clicked.connect(self.button6Event)
        #
        # third row
        self.button7 = QPushButton()
        self.button7.setIcon(QtGui.QIcon('blank.gif'))
        self.button7.setIconSize(QtCore.QSize(60, 85))
        self.buttonArray.append(self.button7)
        self.button7.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button7.clicked.connect(self.button7Event)

        self.button8 = QPushButton()
        self.button8.setIcon(QtGui.QIcon('blank.gif'))
        self.button8.setIconSize(QtCore.QSize(60, 85))
        self.buttonArray.append(self.button8)
        self.button8.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button8.clicked.connect(self.button8Event)

        self.button9 = QPushButton()
        self.button9.setIcon(QtGui.QIcon('blank.gif'))
        self.button9.setIconSize(QtCore.QSize(60, 85))
        self.buttonArray.append(self.button9)
        self.button9.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button9.clicked.connect(self.button9Event)
        #
        self.Quit = QPushButton("Quit")
        self.Quit.setShortcut("ctrl+v")
        self.Quit.setToolTip("Exit the game: ctrl+v")
        self.Quit.resize(10, 10)
        # self.Quit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.Quit.clicked.connect(self.quit)
        self.connectServer = QPushButton("Connect")
        self.connectServer.setShortcut("ctrl+e")
        self.connectServer.setToolTip("Connect to the server: ctrl+e")
        self.connectServer.clicked.connect(self.connectEvent)

        self.messageBox = QTextEdit()
        self.messageBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # ensure that the QTextEdit allows for reading messages only, no typing/editing. "lock" the QTextEdit.
        self.messageBox.setReadOnly(True)

        # server entry
        self.label = QLabel("Enter server: ")
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.getServer = QLineEdit('127.0.0.1')

        # player character display
        self.character = QLabel("Game Character: ")
        self.pixmap = QPixmap('cross.gif')
        self.pixmap2 = QPixmap("nought.gif")
        self.picLabel = QLabel()
        self.picLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # enhancement
        # will most probably remove this later on
        self.comboBox = QComboBox()
        self.comboBox.addItems(['Pink', 'Grey', 'Red', 'Orange', 'Yellow', 'Purple'])
        self.comboBox.activated.connect(self.setColour)
        self.setStyleSheet("background-color: pink")
        self.messageBox.setStyleSheet('background-color: white')
        self.getServer.setStyleSheet('background-color: white')
        # self.comboBox.setStyleSheet('background-color: white')

        hbox = QHBoxLayout()
        hbox.addWidget(menu)
        hbox2 = QWidget()
        hbox2.setLayout(hbox)

        # present everything in a Gridlayout
        # making sure to set span width and length (rows, columns) to avoid overlapping
        grid = QGridLayout()
        grid.addWidget(hbox2, 0, 4, 1, 3)
        grid.addWidget(self.label, 1, 0, 1, 1)
        grid.addWidget(self.getServer, 1, 1, 1, 1)
        grid.addWidget(self.connectServer, 1, 2, 1, 1)
        grid.addWidget(self.comboBox, 1, 3, 1, 1)
        #
        grid.addWidget(self.button1, 2, 0, 1, 1)
        grid.addWidget(self.button2, 2, 1, 1, 1)
        grid.addWidget(self.button3, 2, 2, 1, 1)
        #
        grid.addWidget(self.button4, 3, 0, 1, 1)
        grid.addWidget(self.button5, 3, 1, 1, 1)
        grid.addWidget(self.button6, 3, 2, 1, 1)
        #
        grid.addWidget(self.button7, 4, 0, 1, 1)
        grid.addWidget(self.button8, 4, 1, 1, 1)
        grid.addWidget(self.button9, 4, 2, 1, 1)
        #
        grid.addWidget(self.messageBox, 2, 3, 3, 4)
        grid.addWidget(self.character, 5, 1, 1, 1)
        grid.addWidget(self.picLabel, 5, 2, 1, 1)
        grid.addWidget(self.Quit, 5, 5, 1, 1)
        #
        self.setLayout(grid)

    # event handlers for all buttons
    def connectEvent(self):
        self.messageThread.Connect(self.getServer.displayText())  # connect to server currently entered in the QLineEdit
        self.messageThread.start()          # call the QThread class start() method in order to call the run() method
        self.messageBox.append("Connected to server.")
        self.connectServer.setEnabled(False)    # disable the connect button when it's clicked

    # methods for the game board buttons
    # write to the messageBox when a button is clicked
    # this on happens if it's a player's turn to play
    # A player will not be able to click any of the buttons if it's not their turn to play
    def button1Event(self):
        self.messageThread.send_message(str(0))
        self.messageBox.append("Button 1 clicked")

    def button2Event(self):
        self.messageThread.send_message(str(1))
        self.messageBox.append("Button 2 clicked")

    def button3Event(self):
        self.messageThread.send_message(str(2))
        self.messageBox.append("Button 3 clicked")

    def button4Event(self):
        self.messageThread.send_message(str(3))
        self.messageBox.append("Button 4 clicked")

    def button5Event(self):
        self.messageThread.send_message(str(4))
        self.messageBox.append("Button 5 clicked")

    def button6Event(self):
        self.messageThread.send_message(str(5))
        self.messageBox.append("Button 6 clicked")

    def button7Event(self):
        self.messageThread.send_message(str(6))
        self.messageBox.append("Button 7 clicked")

    def button8Event(self):
        self.messageThread.send_message(str(7))
        self.messageBox.append("Button 8 clicked")

    def button9Event(self):
        self.messageThread.send_message(str(8))
        self.messageBox.append("Button 9 clicked")

    def quit(self):
        exitTheGame = QMessageBox.question(self, "Exit the game?", "Do you really want to exit the game.", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if(exitTheGame == QMessageBox.Yes):
            sys.exit()
        else: pass

    def handle_message(self, msg):
        # the message might/will be comma separated(multiple components)
        # split it into an array so as to individualise each component for later use----.split(",")
        # remove any trailing or leading white space
        message = msg.lower().strip().split(",")
        # lengthOfMessage = len(message)
        # print(message)

        if (message[0] == "new game"):
            shape = message[1]
            if (shape == "x"):
                self.pixmap2 = QPixmap("cross.gif")
            elif (shape == "o"):
                self.pixmap2 = QPixmap("nought.gif")
            self.picLabel.setPixmap(self.pixmap2)
            self.messageBox.append("The game has started, your character is " + message[1])

        elif(message[0] == "your move"):
            self.messageBox.append(message[0])
            for i in range(len(self.buttonArray)):
                self.buttonArray[i].setEnabled(True)    # enable all buttons when it's a player's turn to play

        # disable all buttons when it's not a player's turn to play
        elif(message[0] == "opponents move"):
            self.messageBox.append(message[0])
            for i in range(len(self.buttonArray)):
                self.buttonArray[i].setEnabled(False)
            # print(message[0])

        # when a player makes a valid move at position n, their given character should
        # be added to the board array at index n
        elif(message[0] == "valid move"):
            shape = message[1]
            chosenPosition = message[2]
            if(shape == "x"):
                self.pixmap = QtGui.QIcon("cross.gif")
            elif(shape == "o"):
                self.pixmap = QtGui.QIcon("nought.gif")
            # found that short way I mentioned in assignment 7 :-)
            # rather than have if-else statements for all the buttons
            # I added them to an array then i just iterate over the array and change
            # the icon for the clicked button
            for i in range(9):
                if(chosenPosition == str(i)):
                    self.buttonArray[i].setIcon(QIcon(self.pixmap))
                else: pass

        elif (message[0] == "invalid move"):
            self.messageBox.append(message[0])

        elif (message[0] == "game over"):
            if(message[1].upper() == "T"):
                self.messageBox.append("<strong>Game over, it's a Tie<strong>")
            else:
                self.messageBox.append("<strong>Game over, the winner is player {}</strong>".format(message[1].upper()))

        # we shouldn't have a new game button
        # a popup made sense
        # if a player chooses to play again:
        # clear the board
        # send word to the server
        # else:......
        elif (message[0] == "play again"):
            endGame = QMessageBox.question(self, 'Play Again?', "Game over. Do you want to play again?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if endGame == QMessageBox.Yes:
                self.messageBox.clear()
                self.messageThread.send_message("y")
                for i in range(len(self.buttonArray)):
                    self.buttonArray[i].setIcon(QtGui.QIcon('blank.gif'))
            else:
                self.messageThread.send_message("n")

        elif (message[0] == "exit game"):
            self.messageBox.append("Game ended\nG.G")   # "Good Game"

    def setColour(self):
        self.setStyleSheet('background-color:' + str(self.comboBox.currentText()))
        # set the background colour of the messageBox and getServer box explicitly
        # so that it is not affected(coloured in) by the color of the window
        # i.e: remains white at all times
        self.messageBox.setStyleSheet('background-color: white')
        self.getServer.setStyleSheet('background-color: white')

    def instructions(self):
        QMessageBox.information(self, self.tr("How to play"),
                                self.tr(
                                    "The goal of the game is to get three of your given character\n"
                                    "symbol into a row, column or diagonal of three before your opponent does so."
                                ), QMessageBox.Ok)

    def about(self):
        QMessageBox.information(self, self.tr("About"),
                                self.tr(
                                    "TenElevenGames OXO\n"
                                    "Project Leader   : Bhekanani Cele\n"
                                    "Developers         : Yolisa Pingilili\n\t\t    Jane Doe\n\t\t    John Doe\n"
                                    "Release date       : 15 June 2020\n"
                                    "Contact info       : yogatab277@gmail.com"
                                ), QMessageBox.Ok)

    def more(self):
        QMessageBox.information(self, self.tr("More"), self.tr("Keep an eye out\nmore games coming soon!"), QMessageBox.Ok)

    # handle messages via thread
    def threadLine(self, msg):
        self.handle_message(msg)

# main
def main():
    App = QApplication(sys.argv)
    game = Tictactoe()
    sys.exit(App.exec())
main()
