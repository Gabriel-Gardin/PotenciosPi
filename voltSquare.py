#coding: utf-8
from adcdac_module import AdcDac
import RPi.GPIO as GPIO
import time
import json

class SquareWaveVoltametry:
    started = False
    def __init__(self, dac_sum, acq_points, delay_points, potIni=0,potFin=600,stepVolt=25,ganho=1,ampP=50,freq=10, acq_time=7.0e-5, postPot=0, postTime=0):
        self.dac_sum = dac_sum
        self.potIni = potIni 
        self.potFin = potFin
        self.stepVolt = stepVolt
        self.ganho = ganho
        self.ampP = ampP
        self.freq = freq
        self.acq_time = acq_time
        self.postPot = postPot
        self.postTime = postTime
        self._adcdac = AdcDac()
        self._acq_points = acq_points
        self._delay_points = delay_points
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
        if (not (isinstance(var, float))):
            raise ValueError("The variable dac_sum {} must be of type int".format(var))
        self._dac_sum = var

    @property
    def acq_points(self):
        return self._acq_points

    @acq_points.setter
    def acq_points(self, var):
        if (not (isinstance(var, int))):
            raise ValueError("The variable acq_points {} must be of type int".format(var))
        self._acq_points = var

    @property
    def delay_points(self):
        return self._delay_points

    @delay_points.setter
    def delay_points(self, var):
        if (not (isinstance(var, int))):
            raise ValueError("The variable delay_points {} must be of type int".format(var))
        self._delay_points = var

    @property
    def potIni(self):
        return self._potIni

    @potIni.setter
    def potIni(self, var):
        if (not (isinstance(var, int))):
            raise ValueError("The variable potIni {} must be of type int".format(var))
        self._potIni = var

    @property
    def potFin(self):
        return self._potFin

    @potFin.setter
    def potFin(self, var):
        if (not (isinstance(var, int))):
            raise ValueError("The variable potFin {} must be of type int.".format(var))
        self._potFin = var

    @property
    def stepVolt(self):
        return self._stepVolt

    @stepVolt.setter
    def stepVolt(self, var):
        if (not (isinstance(var, int))):
            raise ValueError("The variable setpVolt {} must be of type int.".format(var))
        self._stepVolt = var
        
    @property
    def ampP(self):
        return self._ampP
    @ampP.setter
    def ampP(self, var):
        if(not(isinstance(var,int))):
            raise ValueError("The variable ampP {} must be of type int".format(var))
        self._ampP = var

    @property
    def freq(self):
        return self._freq
    @freq.setter
    def freq(self, var):
        if(not(isinstance(var,int))):
            raise ValueError("The variable freq {} must be of type int".format(var))
        self._freq = var

    @property
    def acq_time(self):
        return self._dac_sum
    @acq_time.setter
    def acq_time(self, var):
        if(not(isinstance(var,float))):
            raise ValueError("The variable acq_time {} must be of type float".format(var))
        self._acq_time = var

    @property
    def postPot(self):
        return self._postPot
    @postPot.setter
    def postPot(self, var):
        if(not(isinstance(var, int))):
            raise ValueError("The variable postPot {} must be of type int".format(var))
        self._postPot = var

    @property
    def postTime(self):
        return self._postTime
    @postTime.setter
    def postTime(self, var):
        if(not(isinstance(var, int))):
            raise ValueError("The variable postTime {} must be of type int")
        self._postTime = var

    def run(self):
        """
        Function that run a SQW voltammetry and yields back the data
        """
        potencialAp = self._potIni
        ampCorr = self._ampP/1000
        cont = 0
        frequency_time = 1/self._freq
        _time_delay = ((frequency_time/self._acq_time) - self.acq_points) / 2
        if self.potIni < self._potFin:
            _t0 = time.time()
            while (potencialAp <= self._potFin and SquareWaveVoltametry.started == True):
                cont += 1
                potencial = (potencialAp/1000)
                pulso1 = potencial + ampCorr + self.stepVolt/1000
                potR = (self._dac_sum + pulso1)
                self._adcdac.applyPot(potR)
                somacorrente = 0
                for ii in range(int(self._acq_points)):
                    leitura = self._adcdac.readADC()
                    if ii > self._delay_points:
                        somacorrente += leitura
                for i in range(int(_time_delay)):
                    self._adcdac.readADC()
                
                somacorrente = somacorrente /(self._acq_points - self._delay_points)
                corrente = somacorrente/self._resistor
                pulso2 = pulso1 - ampCorr
                potR = self._dac_sum +  pulso2
                self._adcdac.applyPot(potR)
                somacorrente = 0
                for ii in range(int(self._acq_points)):
                    leitura = self._adcdac.readADC()
                    if ii > self._delay_points:
                        somacorrente += leitura
                for i in range(int(_time_delay)):
                    self._adcdac.readADC()

                somacorrente = somacorrente / (self._acq_points - self._delay_points)
                corrente2 = -somacorrente/self._resistor
                correnteSQW = corrente - corrente2
                potencialAp = potencialAp + self.stepVolt
                _tempo = time.time()
                yield (potencial),(1000*correnteSQW),(corrente*1000),(corrente2*1000)

        elif self._potIni > self._potFin:
            _t0 = time.time()
            while (potencialAp >= self._potFin and SquareWaveVoltametry.started == True):
                cont += 1
                potencial = (potencialAp/1000)
                pulso1 = potencial - ampCorr - self.stepVolt/1000
                potR = (self._dac_sum + pulso1)
                self._adcdac.applyPot(potR)
                somacorrente = 0
                for ii in range(int(self._acq_points)):
                    leitura = self._adcdac.readADC()
                    if ii > self._delay_points:
                        somacorrente += leitura
                for i in range(int(_time_delay)):
                    self._adcdac.readADC()
                
                somacorrente = somacorrente /(self._acq_points - delay_points)
                corrente = somacorrente/self._resistor
                potencial = potencialAp/1000
                pulso2 = pulso1 + ampCorr
                potR = self._dac_sum +  pulso2
                self._adcdac.applyPot(potR)
                somacorrente = 0
                for ii in range(int(self._acq_points)):
                    leitura = self._adcdac.readADC()
                    if ii > self._delay_points:
                        somacorrente += leitura
                for i in range(int(_time_delay)):
                    self._adcdac.readADC()

                somacorrente = somacorrente / (self._acq_points - self._delay_points)
                corrente2 = -somacorrente/self._resistor
                correnteSQW = corrente - corrente2
                potencialAp = potencialAp - self.stepVolt
                yield (potencial),(1000*correnteSQW),(corrente*1000),(corrente2*1000)
            
    #    _t = time.time()
        self._adcdac.applyPot((self._postPot/1000)+self._dac_sum)
        time.sleep(self._postTime)
        GPIO.cleanup()
        SquareWaveVoltametry.started = False

