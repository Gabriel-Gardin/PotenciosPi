
from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QApplication, QMessageBox, QFileDialog
from functools import partial
import sys
import csv
from voltLinear import LinearVoltametry
from voltCyclic import CyclicVoltametry
from voltSquare import SquareWaveVoltametry
from voltCalibrate import CalibratePotential as calibrator
import pyqtgraph as pg
from PreDeposition import PreDeposition
import RPi.GPIO as GPIO
import json

pg.setConfigOption('background', 'w')

form_main, base_main = uic.loadUiType('/home/pi/Desktop/PotenciosPi/main_window.ui')
form_linear, base_linear = uic.loadUiType('/home/pi/Desktop/PotenciosPi/Linear_window.ui')
form_cyclic, base_cyclic = uic.loadUiType('/home/pi/Desktop/PotenciosPi/Cyclic_window.ui')
form_SQW, base_SQW = uic.loadUiType('/home/pi/Desktop/PotenciosPi/SQW_window.ui')
form_calibrate, base_calibrate = uic.loadUiType('/home/pi/Desktop/PotenciosPi/Calibrate_window.ui')

class main_window(form_main, base_main):
    def __init__(self):
        super(base_main,self).__init__()
        self.setupUi(self)
        self.actionLinear_Voltametry.triggered.connect(partial(slct_GUI, obj=self, gui='linear'))
        self.actionCyclic_Voltametry.triggered.connect(partial(slct_GUI, obj=self, gui='cyclic'))
        self.actionSquare_Wave_Voltametry.triggered.connect(partial(slct_GUI, obj=self, gui='sqw'))
        self.actionCalibrate.triggered.connect(partial(slct_GUI, obj=self, gui='calibrate'))
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
        self.setWindowTitle('Linear Voltametry')
        self.actionLinear_Voltametry.triggered.connect(partial(slct_GUI, obj=self, gui='linear'))
        self.actionCyclic_Voltametry.triggered.connect(partial(slct_GUI, obj=self, gui='cyclic'))
        self.actionSquare_Wave_Voltametry.triggered.connect(partial(slct_GUI, obj=self, gui='sqw'))
        self.actionCalibrate.triggered.connect(partial(slct_GUI, obj=self, gui='calibrate'))
        self.actionSave.triggered.connect(partial(save, obj=self))
        self.pushButton_2.clicked.connect(self.run_linear)
        self.pushButton.clicked.connect(self.stop)
        self.actionExit.triggered.connect(self.close)
        self.lineAcqPoint.setText("300")
        self.lineDelayPoint.setText("100")
        self.lineVoltScans.setText("1")
        self.lineVoltScan.setText("50")
        self.lineVoltStep.setText("10")
        self.lineVoltFinal.setText("600")
        self.lineVoltInitia.setText("0")

    def stop(self):
        LinearVoltametry.started = False
        print("Parou")


    def run_linear(self):
        LinearVoltametry.started = True
        #self.pushButton_2.disconnect()
        #self.pushButton_2.clicked.connect(partial(stop_voltamogram, obj=self))
        if (self.checkBox.isChecked()):
            preCond = int(self.linePreCond.text())
            pre_time_cond = int(self.linePretime.text())
            pot_pre_dep = int(self.linePreDep.text())
            pre_deposition_time = int(self.linePreDepTime.text())

            i2 = PreDeposition(pot_cond=preCond, time_cond=pre_time_cond, pre_dep_pot=pot_pre_dep,
                            pre_dep_time=pre_deposition_time, somadorDA=3.0)
            i2.run()

        print("aqui caraio")
        print(self.lineVoltInitia.text())
        potInii = int(self.lineVoltInitia.text())
        potFinn = int(self.lineVoltFinal.text())
        potStepp = int(self.lineVoltStep.text())
        potScann = int(self.lineVoltScan.text())
        potScanss = int(self.lineVoltScans.text())
        acq_pointss = int(self.lineAcqPoint.text())
        delay_pointss = int(self.lineDelayPoint.text())
        ganhoo = int(self.spinBox.text())

        i1 = LinearVoltametry(dac_sum=3.0, acq_points=acq_pointss, delay_points=delay_pointss,
                            potIni=potInii, potFin=potFinn, stepVolt=potStepp, ganho=ganhoo, scanRate=potScann)

        self.Xdata = []
        self.Ydata = []
        for x in i1.run():
            self.Xdata.append(x[0])
            self.Ydata.append(x[1])
            print(self.Xdata[0],self.Ydata[0])
            self.textBrowser.append(str([x[0],x[1]]))
            self.graphicsView.plot(self.Xdata, self.Ydata, clear=True)
            QtGui.QApplication.processEvents()
            print([x[0],x[1]])

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
        self.setWindowTitle('Cyclic Voltametry')
        self.actionLinear_Voltametry.triggered.connect(partial(slct_GUI, obj=self, gui='linear'))
        self.actionCyclic_Voltametry.triggered.connect(partial(slct_GUI, obj=self, gui='cyclic'))
        self.actionSquare_Wave_Voltametry.triggered.connect(partial(slct_GUI, obj=self, gui='sqw'))
        self.actionCalibrate.triggered.connect(partial(slct_GUI, obj=self, gui='calibrate'))
        self.actionSave.triggered.connect(partial(save, obj=self))
        self.pushButton.clicked.connect(self.stop)
        self.pushButton_2.clicked.connect(self.run_cyclic)
        self.actionExit.triggered.connect(self.close)
        self.lineAcqPoint.setText("300")
        self.lineDelayPoint.setText("100")
        self.lineVoltScans.setText("1")
        self.lineVoltScan.setText("50")
        self.lineVoltStep.setText("10")
        self.lineVoltFinal.setText("600")
        self.lineVoltInitia.setText("0")

    def stop(self):
        CyclicVoltametry.started = False
        print("Parou")

    def run_cyclic(self):
        CyclicVoltametry.started = True
        if(self.checkBox.isChecked()):
            preCond = int(self.linePreCond.text())
            pre_time_cond = int(self.linePretime.text())
            pot_pre_dep = int(self.linePreDep.text())
            pre_deposition_time = int(self.linePreDepTime.text())

            i2 = PreDeposition(pot_cond = preCond, time_cond = pre_time_cond, pre_dep_pot=pot_pre_dep, pre_dep_time = pre_deposition_time, somadorDA = 3.0)
            i2.run()

        print(self.lineVoltInitia.text())
        potInii = int(self.lineVoltInitia.text())
        potFinn = int(self.lineVoltFinal.text())
        potStepp = int(self.lineVoltStep.text())
        potScann = int(self.lineVoltScan.text())
        potScanss = int(self.lineVoltScans.text())
        acq_pointss = int(self.lineAcqPoint.text())
        delay_pointss = int(self.lineDelayPoint.text())
        ganhoo = int(self.spinBox.text()) 


        i1 = CyclicVoltametry(dac_sum=3.0,acq_points=acq_pointss,delay_points=delay_pointss,
                         potIni=potInii,potFin=potFinn,stepVolt=potStepp,ganho=ganhoo,scanRate=potScann)

        self.Ydata = []
        self.Xdata = []
        for x in i1.run():
            self.Xdata.append(x[0])
            self.Ydata.append(x[1])
            # print(data[0],data[1])
            self.textBrowser.append(str([x[0], x[1]]))
            self.graphicsView.plot(self.Xdata, self.Ydata, clear=True)
            QtGui.QApplication.processEvents()
            print([x[0], x[1]])

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
        self.setWindowTitle('SQW voltametry')
        self.actionLinear_Voltametry.triggered.connect(partial(slct_GUI, obj=self, gui='linear'))
        self.actionCyclic_Voltametry.triggered.connect(partial(slct_GUI, obj=self, gui='cyclic'))
        self.actionSquare_Wave_Voltametry.triggered.connect(partial(slct_GUI, obj=self, gui='sqw'))
        self.actionCalibrate.triggered.connect(partial(slct_GUI, obj=self, gui='calibrate'))
        self.pushButton.clicked.connect(self.stop)
        self.actionSave.triggered.connect(partial(save, obj=self))
        self.pushButton_2.clicked.connect(self.run_SQW)
        self.actionExit.triggered.connect(self.close)
        self.lineAcqPoint.setText("300")
        self.lineDelayPoint.setText("100")
        self.lineVoltScans.setText("1")
        self.lineVoltScan.setText("50")
        self.lineVoltStep.setText("10")
        self.lineVoltFinal.setText("600")
        self.lineVoltInitia.setText("0")

    def stop(self):
        SquareWaveVoltametry.started = False
        print("Parou")

    def run_SQW(self):
        SquareWaveVoltametry.started = True
        if(self.checkBox.isChecked()):
            preCond = int(self.linePreCond.text())
            pre_time_cond = int(self.linePretime.text())
            pot_pre_dep = int(self.linePreDep.text())
            pre_deposition_time = int(self.linePreDepTime.text())

            i2 = PreDeposition(pot_cond = preCond, time_cond = pre_time_cond, pre_dep_pot=pot_pre_dep, pre_dep_time = pre_deposition_time, somadorDA = 3.0)
            i2.run()
        print(self.lineVoltInitia.text())
        potInii = int(self.lineVoltInitia.text())
        potFinn = int(self.lineVoltFinal.text())
        potStepp = int(self.lineVoltStep.text())
        potScann = int(self.lineVoltScan.text())
        potScanss = int(self.lineVoltScans.text())
        acq_pointss = int(self.lineAcqPoint.text())
        delay_pointss = int(self.lineDelayPoint.text())
        ganhoo = int(self.spinBox.text()) 
        
        i1 = SquareWaveVoltametry(dac_sum=3.0,acq_points=acq_pointss,delay_points=delay_pointss,
                         potIni=potInii,potFin=potFinn,stepVolt=potStepp,ganho=ganhoo,ampP=50,freq=10)

        self.Ydata = []
        self.Xdata = []
        for x in i1.run():
            self.Xdata.append(x[0])
            self.Ydata.append(x[1])
            # print(data[0],data[1])
            self.textBrowser.append(str([x[0], x[1]]))
            self.graphicsView.plot(self.Xdata, self.Ydata, clear=True)
            QtGui.QApplication.processEvents()
            print([x[0], x[1]])

    def closeEvent(self, event):
        msg = QMessageBox()
        message = "Are you sure?"
        msg = msg.information(self, 'Exit?', message, QMessageBox.Yes, QMessageBox.No)
        if msg == QMessageBox.Yes:
            super(base_main, self).closeEvent(event)  # CHama a função original do PyQt ao invés de sobre escrevela totalemnte
            event.accept()
        else:
            event.ignore()

class Calibrate_window(base_calibrate, form_calibrate):
    def __init__(self):
        super(base_calibrate, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Calibrate')
        self.text_pot.setText('500')
        self.text_ref.setText('3')
        self.bt_apply_pot.clicked.connect(self.run_calibrate)
        self.bt_calibrate.clicked.connect(self.calibrar)

    def run_calibrate(self):
        appott = int(self.text_pot.text())
        refpott = int(self.text_ref.text())
        calibrar =  calibrator(applypotential = appott, refpot = refpott)
        self.bt_apply_pot.disconnect()
        self.bt_apply_pot.setText('Stop')
        self.bt_apply_pot.clicked.connect(self.close_cell)
        calibrar.apply_pot()

    def close_cell(self):
        self.bt_apply_pot.setText('Apply Pot')
        self.bt_apply_pot.clicked.connect(self.run_calibrate)
        GPIO.cleanup()

    def calibrar(self):
        data = {'refpot':(int(self.text_ref.text()))}
        print('aaaaaa')
        print(type(data))
        with open('/home/pi/Desktop/PotenciosPi/configs.json', 'w') as json_file:
            json.dump(data, json_file)

        


def save(obj):
    name = QFileDialog.getSaveFileName(obj, 'Save File')
    with open(name[0]+'.csv', 'w') as voltametry_data:
        writer = csv.writer(voltametry_data, delimiter=',')
        for i in range(len(obj.Ydata)):
            writer.writerow([obj.Xdata[i], obj.Ydata[i]])


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
    elif(gui == 'calibrate'):
        obj.calibrate = Calibrate_window()
        obj.calibrate.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = main_window()
    window.show()
    sys.exit(app.exec_())




