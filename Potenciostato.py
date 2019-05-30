from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QApplication, QMessageBox, QFileDialog
from functools import partial
import sys
import csv
from voltLinear import LinearVoltametry
from voltCyclic import CyclicVoltametry
from voltSquare import SquareWaveVoltametry
from voltCalibrate import CalibratePotential as calibrator
from calibrate_freq import CalibrateFreq as freq_calibrator
import pyqtgraph as pg
from PreDeposition import PreDeposition
import RPi.GPIO as GPIO
from itertools import zip_longest
import json

pg.setConfigOption('background', 'w')

form_main, base_main = uic.loadUiType('/home/pi/Desktop/PotenciosPi/main_window.ui')
form_linear, base_linear = uic.loadUiType('/home/pi/Desktop/PotenciosPi/Linear_window.ui')
form_cyclic, base_cyclic = uic.loadUiType('/home/pi/Desktop/PotenciosPi/Cyclic_window.ui')
form_SQW, base_SQW = uic.loadUiType('/home/pi/Desktop/PotenciosPi/SQW_window.ui')
form_calibrate, base_calibrate = uic.loadUiType('/home/pi/Desktop/PotenciosPi/Calibrate_window.ui')
form_visualize, base_visualize = uic.loadUiType('/home/pi/Desktop/PotenciosPi/data_visualizer.ui')

class main_window(form_main, base_main):
    def __init__(self):
        super(base_main,self).__init__()
        self.setupUi(self)
        self.actionLinear_Voltametry.triggered.connect(partial(slct_GUI, obj=self, gui='linear'))
        self.actionCyclic_Voltametry.triggered.connect(partial(slct_GUI, obj=self, gui='cyclic'))
        self.actionSquare_Wave_Voltametry.triggered.connect(partial(slct_GUI, obj=self, gui='sqw'))
        self.actionCalibrate.triggered.connect(partial(slct_GUI, obj=self, gui='calibrate'))
        self.actionOpen.triggered.connect(partial(open_data, obj=self))
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

class data_visualizer(form_visualize, base_visualize):
    def __init__(self, files):
        super(base_main, self).__init__()
        self.setupUi(self)
        self.slct_linear.triggered.connect(partial(slct_GUI, obj=self, gui='linear'))
        self.slct_cyclic.triggered.connect(partial(slct_GUI, obj=self, gui='cyclic'))
        self.slct_sqw.triggered.connect(partial(slct_GUI, obj=self, gui='sqw'))
        self.ex_xlsx.triggered.connect(self.export_xlsx)
        self.files = files
        filess = int(len(self.files[0]))
        with open((self.files[0])[0]) as data: #Abre o primeiro arquivo da lista para verificar o tamanho do mesmo. 
            data_lines = (data.readlines())
            rows = len(data_lines[1].split(','))

        all_data = [[]for u in range(filess)]
        for i in  range(filess):
            all_data[i] = [[]for u in range(rows)] 
        self.ex_csv.triggered.connect(partial(self.export_csv, data=all_data))
        
        counter = 0
        for i in range(filess):
            counter += 1
            with open((self.files[0])[i]) as data:
                data_liness = (data.readlines())
                for(line) in (data_liness[1:]):
                    for u in range(rows):
                        all_data[i][u].append(float(line.split(',')[u]))

        for i in range(len(all_data)):
            for u in range(1, len(all_data[i])):
                print(len(all_data[i][u]))  
                self.graphicsView.plot(all_data[i][0], all_data[i][u], clear=False)

    def export_xlsx(self):
        pass

    def export_csv(self, data):
        file = QFileDialog.getSaveFileName(self, 'Save File')
        alll_data = []
        first_x = True
        for i in range(len(data)):
            for u in range(1, len(data[i])):
                if(i == 0 and first_x):
                    alll_data.append(data[i][0])
                    first_x = False
                else:
                    alll_data.append(data[i][u])
                #writer.writerows([data[i][u]])
                #for values in zip_longest(*data[i]):
                #    writer.writerows([values])
        with open(file[0] + '.csv', 'a+') as exported_file:
            writer = csv.writer(exported_file, delimiter=',')
            for data in zip_longest(*alll_data):
                writer.writerow(data)

    def closeEvent(self, event):
        msg = QMessageBox()
        message = "Are you sure?"
        msg = msg.information(self, 'Exit?', message, QMessageBox.Yes, QMessageBox.No)
        if msg == QMessageBox.Yes:
            super(base_main, self).closeEvent(event)  # CHama a função original do PyQt ao invés de sobre escrevela totalemnte
            event.accept()

class Linear_window(form_linear, base_linear):
    def __init__(self):
        super(base_linear, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Linear Voltametry')
        self.actionLinear_Voltametry.triggered.connect(partial(slct_GUI, obj=self, gui='linear'))
        self.actionCyclic_Voltametry.triggered.connect(partial(slct_GUI, obj=self, gui='cyclic'))
        self.actionSquare_Wave_Voltametry.triggered.connect(partial(slct_GUI, obj=self, gui='sqw'))
        self.applypot.triggered.connect(partial(slct_GUI, obj=self, gui='calibrate'))
        self.actionOpen.triggered.connect(partial(open_data, obj=self))  
        self.actionCalibrate.triggered.connect(partial(calibrate_pot, obj=self))
        self.actionSave.triggered.connect(partial(save, obj=self))
        self.pushButton_2.clicked.connect(self.run_linear)
        self.pushButton.clicked.connect(self.stop)
        self.actionExit.triggered.connect(self.close)
        self.lineVoltScans.setText("1")
        self.lineVoltScan.setText("50")
        self.lineVoltStep.setText("10")
        self.lineVoltFinal.setText("600")
        self.lineVoltInitia.setText("0")
        self.spinBox.setValue(1)

    def __str__(self):
        return('LINEAR')

    def stop(self):
        LinearVoltametry.started = False
        print("Parou")


    def run_linear(self):
        LinearVoltametry.started = True
        potInii = int(self.lineVoltInitia.text())
        potFinn = int(self.lineVoltFinal.text())
        potStepp = int(self.lineVoltStep.text())
        potScann = int(self.lineVoltScan.text())
        potScanss = int(self.lineVoltScans.text())
        ganhoo = int(self.spinBox.text())
        with open('/home/pi/Desktop/PotenciosPi/configs.json', 'r') as config_file:
            dac_summ = float((json.loads(config_file.read())).get('divider_volt'))
        if (self.checkBox.isChecked()):
            preCond = int(self.ECond.text())
            pre_time_cond = int(self.tCond.text())
            pot_pre_dep = int(self.PreDep.text())
            pre_deposition_time = int(self.TDep.text())

            i2 = PreDeposition(pot_cond=preCond, time_cond=pre_time_cond, pre_dep_pot=pot_pre_dep,
                            pre_dep_time=pre_deposition_time, somadorDA=dac_summ)
            i2.run()

        self.all_data = [[]for i in range(potScanss + 1)]
        for i in range(potScanss):
            i1 = LinearVoltametry(dac_sum=dac_summ, acq_points=300, delay_points=100,
                            potIni=potInii, potFin=potFinn, stepVolt=potStepp, ganho=ganhoo, scanRate=potScann)
            for x in i1.run():
                self.all_data[0].append(x[0])
                self.all_data[i+1].append(x[1])
                self.graphicsView.plot(self.all_data[0], self.all_data[i+1], clear=True)
                QtGui.QApplication.processEvents()
            if(i < potScanss - 1):     #Salva apenas o potencial do último scan. 
                self.all_data[0] = []
                print("zerou")
        LinearVoltametry.started = False

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
        self.actionOpen.triggered.connect(partial(open_data, obj=self))
        self.applypot.triggered.connect(partial(slct_GUI, obj=self, gui='calibrate'))
        self.actionCalibrate.triggered.connect(partial(calibrate_pot, obj=self))
        self.actionSave.triggered.connect(partial(save, obj=self))
        self.pushButton.clicked.connect(self.stop)
        self.pushButton_2.clicked.connect(self.run_cyclic)
        self.actionExit.triggered.connect(self.close)
        self.lineVoltScans.setText("1")
        self.lineVoltScan.setText("50")
        self.lineVoltStep.setText("10")
        self.lineVoltFinal.setText("600")
        self.lineVoltInitia.setText("0")
        self.spinBox.setValue(1)
    def __str__(self):
        return('CYCLIC')

    def stop(self):
        CyclicVoltametry.started = False
        print("Parou")

    def run_cyclic(self):
        CyclicVoltametry.started = True
  #      print(self.lineVoltInitia.text())
        potInii = int(self.lineVoltInitia.text())
        potFinn = int(self.lineVoltFinal.text())
        potStepp = int(self.lineVoltStep.text())
        potScann = int(self.lineVoltScan.text())
        potScanss = int(self.lineVoltScans.text())
        ganhoo = int(self.spinBox.text())
        with open('/home/pi/Desktop/PotenciosPi/configs.json', 'r') as config_file:
            dac_summ = float((json.loads(config_file.read())).get('divider_volt'))

        if(self.checkBox.isChecked()):
            preCond = int(self.ECond.text())
            pre_time_cond = int(self.tCond.text())
            pot_pre_dep = int(self.PreDep.text())
            pre_deposition_time = int(self.TDep.text())

            i2 = PreDeposition(pot_cond = preCond, time_cond = pre_time_cond, pre_dep_pot=pot_pre_dep, 
            pre_dep_time = pre_deposition_time, somadorDA = dac_summ)
            i2.run()

        self.all_data = [[]for i in range(potScanss + 1)]
        for i in range(potScanss):
            i1 = CyclicVoltametry(dac_sum=dac_summ,acq_points=300,delay_points=100,
                        potIni=potInii,potFin=potFinn,stepVolt=potStepp,ganho=ganhoo,scanRate=potScann)
            print("aaaa", i)
            for x in i1.run():
                self.all_data[0].append(x[0])
                self.all_data[i+1].append(x[1])
                self.graphicsView.plot(self.all_data[0], self.all_data[i+1], clear=True)
                QtGui.QApplication.processEvents()
            if(i < potScanss - 1):     #Salva apenas o potencial do último scan. 
                self.all_data[0] = []
                print("zerou")
        CyclicVoltametry.started = False

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
        self.actionOpen.triggered.connect(partial(open_data, obj=self))
        self.applypot.triggered.connect(partial(slct_GUI, obj=self, gui='calibrate'))
        self.actionCalibrate.triggered.connect(partial(calibrate_pot, obj=self))
        self.pushButton.clicked.connect(self.stop)
        self.actionSave.triggered.connect(partial(save, obj=self))
        self.CalibrateFreq.triggered.connect(calibrate_freq)
        self.pushButton_2.clicked.connect(self.run_SQW)
        self.TPostPot.setText("0")
        self.postPot.setText("0")
        self.lineVoltStep.setText("10")
        self.lineVoltFinal.setText("600")
        self.lineVoltInitia.setText("0")
        self.SqwAmplitude.setText("50")
        self.SqwFrequency.setValue(20)
        self.spinBox.setValue(1)

    def __str__(self):
        return('SQW')

    def stop(self):
        SquareWaveVoltametry.started = False    
        print("Parou")

    def run_SQW(self):
        SquareWaveVoltametry.started = True
        potInii = int(self.lineVoltInitia.text())
        potFinn = int(self.lineVoltFinal.text())
        potStepp = int(self.lineVoltStep.text())
        post_pot = int(self.postPot.text())
        post_time = int(self.TPostPot.text())
        ganhoo = int(self.spinBox.text())
        sqw_amplitude = int(self.SqwAmplitude.text())
        sqw_frequency = int(self.SqwFrequency.text())

        with open('/home/pi/Desktop/PotenciosPi/configs.json', 'r') as config_file:
            config_data = json.loads(config_file.read())
            dac_summ = float(config_data.get('divider_volt'))
            data_read_time = float(config_data.get("read_voltage_time"))

        if(self.checkBox.isChecked()):
            preCond = int(self.ECond.text())
            pre_time_cond = int(self.tCond.text())
            pot_pre_dep = int(self.PreDep.text())
            pre_deposition_time = int(self.TDep.text())

            i2 = PreDeposition(pot_cond = preCond, time_cond = pre_time_cond, pre_dep_pot=pot_pre_dep, 
            pre_dep_time = pre_deposition_time, somadorDA = dac_summ)
            i2.run()
        i1 = SquareWaveVoltametry(dac_sum=dac_summ,acq_points=300,delay_points=10,
            potIni=potInii,potFin=potFinn,stepVolt=potStepp,ganho=ganhoo,ampP=sqw_amplitude,
            freq=sqw_frequency, acq_time=data_read_time,postPot = post_pot, postTime=post_time)

        self.all_data = [[]for i in range(4)]

        for x in i1.run():
           self.all_data[0].append(x[0])
           self.all_data[1].append(x[1])
           self.all_data[2].append(x[2])
           self.all_data[3].append(x[3])

        self.graphicsView.plot(self.all_data[0], self.all_data[1], clear=True)
        QtGui.QApplication.processEvents()

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
        self.setWindowTitle('Apply potential')
        self.bt_apply_pot.clicked.connect(self.run_calibrate)

    def run_calibrate(self):
        with open('/home/pi/Desktop/PotenciosPi/configs.json', 'r') as config_file:
            config_data = json.loads(config_file.read())
            dac_summ = float(config_data.get('divider_volt'))
        appott = int(self.text_pot.text())
        calibrarr =  calibrator(refpot = dac_summ)
        self.bt_apply_pot.disconnect()
        self.bt_apply_pot.setText('Stop')
        self.bt_apply_pot.clicked.connect(self.close_cell)
        calibrarr.apply_pot(appott)

    def close_cell(self):
        self.bt_apply_pot.setText('Apply Pot')
        self.bt_apply_pot.clicked.connect(self.run_calibrate)
        GPIO.cleanup()


def calibrate_pot(obj):
    call = calibrator()
    ref = call.calibrar()
    obj.textBrowser.append("Calibrado.\n Ref= {}".format(ref))

def calibrate_freq():
    frq = freq_calibrator()
    frq.calibrate()

def open_data(obj):
    files = QFileDialog.getOpenFileNames(obj, "Open File", filter='csv(*.csv)')
    slct_GUI(obj=obj, gui='data', files = files)

def save(obj):
    name = QFileDialog.getSaveFileName(obj, 'Save File')
    with open(name[0]+'.csv', 'w') as voltametry_data:
        writer = csv.writer(voltametry_data, delimiter=',')
        writer.writerow([str(obj)])
        for values in zip_longest(*obj.all_data):
            writer.writerows([values])


def slct_GUI(obj, gui, files = 0):
    if(gui == 'linear'):
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

    elif(gui == 'data'):
        obj.data = data_visualizer(files)
        obj.data.show()
        obj.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = main_window()
    window.show()
    sys.exit(app.exec_())




