
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys

form_main, base_main = uic.loadUiType('main_window.ui')
form_linear, base_linear = uic.loadUiType('Linear_window.ui')
form_cyclic, base_cyclic = uic.loadUiType('Cyclic_window.ui')
form_SQW, base_SQW = uic.loadUiType('SQW_window.ui')

class main_window(form_main, base_main):
    def __init__(self):
        super(base_main,self).__init__()
        self.setupUi(self)
        self.actionLinear_Voltametry.triggered.connect(self.slct_linear)
        self.actionCyclic_Voltametry.triggered.connect(self.slct_cyclic)
        self.actionSquare_Wave_Voltametry.triggered.connect(self.slct_SQW)
        self.actionExit.triggered.connect(self.closeEvent)

    def slct_linear(self):
        self.linear = Linear_window()
        self.linear.show()
        self.close()

    def slct_cyclic(self):
        self.cyclic = Cyclic_window()
        self.cyclic.show()
        self.close()

    def slct_SQW(self):
        self.sqw = SQW_window()
        self.sqw.show()
        self.close()

    def closeEvent(self, event):
        msg = QMessageBox()
        message = "Are you sure?"
        msg = msg.information(self, 'Exit?', message, QMessageBox.Yes, QMessageBox.No)
        if msg == QMessageBox.Yes:
            event.accept()

        else:
            event.ignore()


class Linear_window(form_linear, base_linear):
    def __init__(self):
        super(base_linear, self).__init__()
        self.setupUi(self)

class Cyclic_window(form_cyclic, base_cyclic):
    def __init__(self):
        super(base_cyclic, self).__init__()
        self.setupUi(self)

class SQW_window(form_SQW,base_SQW):
    def __init__(self):
        super(base_SQW, self).__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = main_window()
    window.show()
    sys.exit(app.exec_())




