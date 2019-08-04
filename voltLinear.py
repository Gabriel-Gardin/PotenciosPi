#coding: utf-8
from adcdac_module import AdcDac
import RPi.GPIO as GPIO
import time
import json

class LinearVoltametry:
    started = False
    def __init__(self,dac_sum,acq_points,delay_points,potIni=0,potFin=100,stepVolt=25,scanRate=50,ganho=1):
        self.dac_sum = dac_sum
        self.acq_points = acq_points
        self.delay_points = delay_points
        self.potIni = potIni
        self.potFin = potFin
        self.stepVolt = stepVolt
        self.scanRate = scanRate
        self.ganho = ganho
        self._adcdac = AdcDac()

        if (self._ganho == 1):
            with open('/home/pi/Desktop/PotenciosPi/configs.json', 'r') as config_file:
                self._resistor = float((json.loads(config_file.read())).get('resistor1'))
        
        elif(self._ganho == 2):
            with open('/home/pi/Desktop/PotenciosPi/configs.json', 'r') as config_file:
                self._resistor = float((json.loads(config_file.read())).get('resistor2'))
        
        elif(self._ganho == 3):
            with open('/home/pi/Desktop/PotenciosPi/configs.json', 'r') as config_file:
                self._resistor = float((json.loads(config_file.read())).get('resistor3'))
        
        elif(self._ganho == 4):
            with open('/home/pi/Desktop/PotenciosPi/configs.json', 'r') as config_file:
                self._resistor = float((json.loads(config_file.read())).get('resistor4'))
        
    @property
    def dac_sum(self):
        return self._dac_sum
    @dac_sum.setter
    def dac_sum(self, var):
        if(not(isinstance(var,float))):
            raise ValueError("The variable dac_sum {} must be of type int".format(var))
        self._dac_sum = var

    @property
    def acq_points(self):
        return self._acq_points
    @acq_points.setter
    def acq_points(self, var):
        if(not(isinstance(var,int))):
            raise ValueError("The variable acq_points {} must be of type int".format(var))
        self._acq_points = var
        
    @property
    def delay_points(self):
        return self._delay_points
    @delay_points.setter
    def delay_points(self, var):
        if(not(isinstance(var,int))):
            raise ValueError("The variable delay_points {} must be of type int".format(var))
        self._delay_points = var

    @property
    def potIni(self):
        return self._potIni
    @potIni.setter
    def potIni(self, var):
        if(not(isinstance(var,int))):
            raise ValueError("The variable potIni {} must be of type int".format(var))
        self._potIni = var

    @property
    def potFin(self):
        return self._potFin

    @potFin.setter
    def potFin(self, var):
        if(not(isinstance(var,int))):
            raise ValueError("The variable potFin {} must be of type int.".format(var))
        self._potFin = var

    @property
    def stepVolt(self):
        return self._stepVolt
    @stepVolt.setter
    def stepVolt(self, var):
        if(not(isinstance(var,int))):
            raise ValueError("The variable setpVolt {} must be of type int.".format(var))
        self._stepVolt = var

    @property
    def scanRate(self):
        return self._scanRate
    @scanRate.setter
    def scanRate(self, var):
        if(not(isinstance(var,int))):
            raise ValueError("The variable ScanRate {} must be of type int".format(var))
        self._scanRate = var

    @property
    def ganho(self):
        return self._ganho
    @ganho.setter
    def ganho(self, var):
        if(not(isinstance(var,int))):
            raise ValueError("The variable ganho {} must be of type int".format(var))
        elif(var <= 0):
            raise ValueError("The variable gain {} must be greater than 0".format(var))
        self._ganho = var

    def run(self):
        """Funtion that runs a linear voltatry and yields back the data"""
        _time = float(self._stepVolt/self._scanRate)
        _tempo = 0
        potencialAp = self._potIni
        if self._potIni < self._potFin:
       #     tempo_inicial = time.time()
            while (potencialAp <= self._potFin and LinearVoltametry.started == True):
                potencial = (potencialAp/1000)
                potR = self._dac_sum + potencial
                _nowTime = time.time()
                self._adcdac.applyPot(potR)
                potencialAp = potencialAp + self._stepVolt
                somacorrente = 0
                for ii in range(self._acq_points):
                    leitura = self._adcdac.readADC()
                    if ii > self._delay_points:
                        somacorrente = leitura + somacorrente
                somacorrente = somacorrente / (self._acq_points - self._delay_points)
                sinal = (somacorrente - self.dac_sum) / self._resistor
                _elapsed_time = (_nowTime - _tempo) + (time.time() - _nowTime) #Compara o tempo que a função ficou "inativa"(_nowTIme - _tempo) e soma ao tempo que a função perdeu aplicando o potencial(time.time() - _nowTime)
                if(_elapsed_time < _time):
                    time.sleep(_time - _elapsed_time)

                _tempo = time.time()
                yield((potencial), (1000 * sinal))

        elif self._potIni > self._potFin:
            tempo_inicial = time.time()
            while (potencialAp >= self._potFin and LinearVoltametry.started == True):
                potencial = (potencialAp/1000)
                potR = self._dac_sum - potencial
                _nowTime = time.time()
                self._adcdac.applyPot(potR)
                potencialAp = potencialAp - self._stepVolt
                somacorrente = 0
                for ii in range(self._acq_points):  
                    if ii > self._delay_points:
                        somacorrente = self._adcdac.readADC() + somacorrente
                somacorrente = somacorrente / (self._acq_points - self._delay_points)
                sinal = (somacorrente) / self._resistor
                _elapsed_time = (_nowTime - _tempo) + (time.time() - _nowTime) #Compara o tempo que a função ficou "inativa"(_nowTIme - _tempo) e soma ao tempo que a função perdeu aplicando o potencial(time.time() - _nowTime)
                if(_elapsed_time < _time):
                    time.sleep(_time - _elapsed_time)
                _tempo = time.time()
                yield((potencial), (1000 * sinal))

            LinearVoltametry.started = False
            GPIO.cleanup()
     #       tempo_final = time.time()
     #       print(tempo_final - tempo_inicial)
        









