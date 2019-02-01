
from PyQt5 import uic, QtGui
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
            super(base_main, self).closeEvent(event)  # CHama a função original do PyQt ao invés de sobre escrevela totalemnte
            event.accept()

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

    def run_linear(self):
        if (self.checkBox.isChecked()):
            preCond = int(self.linePreCond.text())
            pre_time_cond = int(self.linePretime.text())
            pot_pre_dep = int(self.linePreDep.text())
            pre_deposition_time = int(self.linePreDepTime.text())

            #i2 = PreDeposition(pot_cond=preCond, time_cond=pre_time_cond, pre_dep_pot=pot_pre_dep,
            #                   pre_dep_time=pre_deposition_time, somadorDA=3.0)
          #  i2.run()

        print(self.lineVoltInitia.text())
        potInii = int(self.lineVoltInitia.text())
        potFinn = int(self.lineVoltFinal.text())
        potStepp = int(self.lineVoltStep.text())
        potScann = int(self.lineVoltScan.text())
        potScanss = int(self.lineVoltScans.text())
        acq_pointss = int(self.lineAcqPoint.text())
        delay_pointss = int(self.lineDelayPoint.text())
        ganhoo = int(self.spinBox.text())

       # i1 = LinearVoltametry(dac_sum=3.0, acq_points=acq_pointss, delay_points=delay_pointss,
       #                       potIni=potInii, potFin=potFinn, stepVolt=potStepp, ganho=ganhoo, scanRate=potScann)

        Ydata = []
        Xdata = []

        #for x in i1.run():
        #    Xdata.append(x[0])
        #    Ydata.append(x[1])
            #    print(Xdata[0],Ydata[0])
            #    self.textBrowser.append(str([x[0],x[1]]))
            #self.graphicsView.plot(Xdata, Ydata, clear=True)
            #QtGui.QApplication.processEvents()
            # print([x[0],x[1]])

    def closeEvent(self, event):
        msg = QMessageBox()
        message = "Are you sure?"
        msg = msg.information(self, 'Exit?', message, QMessageBox.Yes, QMessageBox.No)
        if msg == QMessageBox.Yes:
            super(base_main, self).closeEvent(event)  # CHama a função original do PyQt ao invés de sobre escrevela totalemnte
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
            super(base_main, self).closeEvent(event)  # CHama a função original do PyQt ao invés de sobre escrevela totalemnte
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
            super(base_main, self).closeEvent(event)  # CHama a função original do PyQt ao invés de sobre escrevela totalemnte
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




