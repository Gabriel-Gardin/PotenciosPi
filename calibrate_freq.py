#coding: utf-8
from adcdac_module import AdcDac
import time
import json

class CalibrateFreq:
    """
    Classe responsável por calcular o tempo necessário para a leitura de um pulso. 
    Isto é necessário uma vez que é através do tempo que se leva para realizar a leitura de um ponto de corrente,
    que controlamos a frequencia da onda quadrada e o delay nas voltametrias linear e cíclica. 
    """
    def __init__(self):
        self._adcdac = AdcDac()
        with open('/home/pi/Desktop/PotenciosPi/configs.json') as json_file:
            try:
                self.data_file = json.load(json_file)
            except:
                pass
        

    def calibrate(self):
        _t0 = time.time()
        fator_correcao = 0.85
        number_of_cycles = 0
        while(number_of_cycles < 10):
            number_of_cycles += 1
            self._adcdac.applyPot(0)
            for ii in range(1000):
                self._adcdac.readADC()
                self._adcdac.applyPot(0)
            _delta_t = time.time() - _t0

        read_voltage_time = (_delta_t/10000) * fator_correcao
        data = {'read_voltage_time':(float(read_voltage_time))}
        self.data_file.update(data)
        with open('/home/pi/Desktop/PotenciosPi/configs.json', 'w') as filee:
            json.dump(self.data_file, filee)
        print("read_time= ", read_voltage_time)
