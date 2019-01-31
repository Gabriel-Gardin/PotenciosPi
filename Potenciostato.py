
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox
from functools import partial
import sys

form_main, base_main = uic.loadUiType('main_window.ui')
form_linear, base_linear = uic.loadUiType('Linear_window.ui')
form_cyclic, base_cyclic = uic.loadUiType('Cyclic_window.ui')
form_SQW, base_SQW = uic.loadUiType('SQW_window.ui')

class main_window(form_main, base_main):
    def __init__(self):
        super(base_main,self).__init__()
        self.setupUi(self)
        self.actionLinear_Voltametry.triggered.connect(partial(slct_GUI, obj=self, gui='linear'))
        self.actionCyclic_Voltametry.triggered.connect(partial(slct_GUI, obj=self, gui='cyclic'))
        self.actionSquare_Wave_Voltametry.triggered.connect(partial(slct_GUI, obj=self, gui='sqw'))
        self.actionExit.triggered.connect(self.close)

    def closeEvent(self, event):
        msg = QMessageBox()
        message = "Are you sure?"
        msg = msg.information(self, 'Exit?', message, QMessageBox.Yes, QMessageBox.No)
        if msg == QMessageBox.Yes:
            event.accept()
            super(base_main, self).closeEvent(event)     #CHama a função original do PyQt ao invés de sobre escrevela totalemnte

        else:
            event.ignore()



class Linear_window(form_linear, base_linear):
    def __init__(self):
        super(base_linear, self).__init__()
        self.setupUi(self)
        self.actionLinear_Voltametry.triggered.connect(partial(slct_GUI, obj=self, gui='linear'))
        self.actionCyclic_Voltametry.triggered.connect(partial(slct_GUI, obj=self, gui='cyclic'))
        self.actionSquare_Wave_Voltametry.triggered.connect(partial(slct_GUI, obj=self, gui='sqw'))
        self.actionExit.triggered.connect(self.close)

    def closeEvent(self, event):
        msg = QMessageBox()
        message = "Are you sure?"
        msg = msg.information(self, 'Exit?', message, QMessageBox.Yes, QMessageBox.No)
        if msg == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

class Cyclic_window(form_cyclic, base_cyclic):
    def __init__(self):
        super(base_cyclic, self).__init__()
        self.setupUi(self)
        self.actionLinear_Voltametry.triggered.connect(partial(slct_GUI, obj=self, gui='linear'))
        self.actionCyclic_Voltametry.triggered.connect(partial(slct_GUI, obj=self, gui='cyclic'))
        self.actionSquare_Wave_Voltametry.triggered.connect(partial(slct_GUI, obj=self, gui='sqw'))
        self.actionExit.triggered.connect(self.close)

    def closeEvent(self, event):
        msg = QMessageBox()
        message = "Are you sure?"
        msg = msg.information(self, 'Exit?', message, QMessageBox.Yes, QMessageBox.No)
        if msg == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

class SQW_window(form_SQW,base_SQW):
    def __init__(self):
        super(base_SQW, self).__init__()
        self.setupUi(self)
        self.actionLinear_Voltametry.triggered.connect(partial(slct_GUI, obj=self, gui='linear'))
        self.actionCyclic_Voltametry.triggered.connect(partial(slct_GUI, obj=self, gui='cyclic'))
        self.actionSquare_Wave_Voltametry.triggered.connect(partial(slct_GUI, obj=self, gui='sqw'))
        self.actionExit.triggered.connect(self.close)

    def closeEvent(self, event):
        msg = QMessageBox()
        message = "Are you sure?"
        msg = msg.information(self, 'Exit?', message, QMessageBox.Yes, QMessageBox.No)
        if msg == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()



def slct_GUI(obj, gui):
    if(gui == 'linear'):
        print('cheguei')
        obj.linear = Linear_window()
        obj.linear.show()
        obj.hide()

    elif(gui == 'cyclic'):
        obj.cyclic = Cyclic_window()
        obj.cyclic.show()
        obj.hide()

    elif (gui == 'sqw'):
        obj.sqw = SQW_window()
        obj.sqw.show()
        obj.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = main_window()
    window.show()
    sys.exit(app.exec_())




