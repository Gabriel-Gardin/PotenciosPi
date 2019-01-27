#coding: utf-8
from adcdac_module import AdcDac
import RPi.GPIO as GPIO
import time

class SquareWaveVoltametry:
    def __init__(self, dac_sum,acq_points,delay_points,potIni=0,potFin=600,stepVolt=25,ganho=1,ampP=50,freq=10):
        self.dac_sum = dac_sum
        self.acq_points = acq_points
        self.delay_points = delay_points
        self.potIni = potIni
        self.potFin = potFin
        self.stepVolt = stepVolt
        self.ganho = ganho
        self.ampP = ampP
        self.freq = freq
    
        
    @property
    def dac_sum(self):
        return self._dac_sum
    @dac_sum.setter
    def dac_sum(self, var):
        if(not(isinstance(var,float))):
            raise ValueError("A variável dac_sum(Potencial inicial) deve ser do tipo int {}".format(var))
        self._dac_sum = var

    @property
    def acq_points(self):
        return self._acq_points
    @acq_points.setter
    def acq_points(self, var):
        if(not(isinstance(var,int))):
            raise ValueError("A variável acq_points deve ser do tipo int {}".format(var))
        self._acq_points = var
        
    @property
    def delay_points(self):
        return self._delay_points
    @delay_points.setter
    def delay_points(self, var):
        if(not(isinstance(var,int))):
            raise ValueError("A variável delay_points deve ser do tipo int {}".format(var))
        self._delay_points = var

    @property
    def potIni(self):
        return self._potIni
    @potIni.setter
    def potIni(self, var):
        if(not(isinstance(var,int))):
            raise ValueError("A variável potIni(Potencial inicial) deve ser do tipo int {}".format(var))
        self._potIni = var

    @property
    def potFin(self):
        return self._potFin

    @potFin.setter
    def potFin(self, var):
        if(not(isinstance(var,int))):
            raise ValueError("A variável potFin(Potencial Final) deve ser do tipo int {}".format(var))
        self._potFin = var

    @property
    def stepVolt(self):
        return self._stepVolt
    @stepVolt.setter
    def stepVolt(self, var):
        if(not(isinstance(var,int))):
            raise ValueError("A variável stepVolt(Passo de potencial) deve ser do tipo int {}".format(var))
        self._stepVolt = var

    @property
    def ganho(self):
        return self._ganho
    @ganho.setter
    def ganho(self, var):
        if(not(isinstance(var,int))):
            raise ValueError("A variável ganho deve ser do tipo int {}".format(var))
        self._ganho = var
        
    @property
    def ampP(self):
        return self._ampP
    @ampP.setter
    def ampP(self, var):
        if(not(isinstance(var,int))):
            raise ValueError("A variável ampP(Amplitude de varredura) deve ser do tipo int {}".format(var))
        self._ampP = var

    @property
    def freq(self):
        return self._freq
    @freq.setter
    def freq(self, var):
        if(not(isinstance(var,int))):
            raise ValueError("A variável freq(Frequência de varredura) deve ser do tipo int {}".format(var))
        self._freq = var

    def run(self):
        if (self._ganho == 1):
            self._resistor = 47 
        
        elif(self._ganho == 2):
            self._resistor = 470
        
        elif(self._ganho == 3):
            self._resistor = 4700
        
        elif(self._ganho == 4):
            self._resistor = 47000
        
        elif(self._ganho == 5):
            self._resistor = 470000
    
        ad_da = AdcDac()
        ad_da.init_ADCDAC()
        potencialAp = self._potIni
        ampCorr = self._ampP/1000
        cont = 0
        if self.potIni<self._potFin:
            while potencialAp <= self._potFin:
                cont += 1
                potencial = (potencialAp/1000)
                pulso1 = potencial + ampCorr
                potR = (self._dac_sum - pulso1)
                ad_da.applyPot(potR)

                ii = 0
                somacorrente = 0
                for ii in range(self._acq_points):
                    leitura = ad_da.readADC()
                    if ii > self._delay_points:
                        somacorrente += leitura
                somacorrente = somacorrente /(self._acq_points - self._delay_points)
                corrente = -somacorrente/self._resistor
                potencial = potencialAp/1000
                pulso2 = potencial - ampCorr
                potR = self._dac_sum - pulso2
                ad_da.applyPot(potR)


                somacorrente = 0
                for ii in range(self._acq_points):
                    leitura = ad_da.readADC()
                    if ii > self._delay_points:
                        somacorrente += leitura
                somacorrente = somacorrente / (self._acq_points - self._delay_points)
                corrente2 = -somacorrente/self._resistor
                correnteSQW = corrente - corrente2
                potencialAp = potencialAp + self.stepVolt
                yield (1000*potencial),(1000*correnteSQW)

