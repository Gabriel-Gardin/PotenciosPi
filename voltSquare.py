#coding: utf-8
from adcdac_module import AdcDac
import RPi.GPIO as GPIO
import time

class SquareWaveVoltametry:
    started = False
    def __init__(self, dac_sum,acq_points,delay_points,potIni=0,potFin=600,stepVolt=25,ganho=1,ampP=50,freq=10, acq_time=7.0e-5, postPot=0, postTime=0):
        self.dac_sum = dac_sum
        self.acq_points = acq_points
        self.delay_points = delay_points
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

    @property
    def acq_time(self):
        return self._dac_sum
    @acq_time.setter
    def acq_time(self, var):
        if(not(isinstance(var,float))):
            raise ValueError("A variável acq_time(Acquisition time) deve ser do tipo float {}".format(var))
        self._acq_time = var

    @property
    def postPot(self):
        return self._postPot
    @postPot.setter
    def postPot(self, var):
        if(not(isinstance(var, int))):
            raise ValueError("A variavel postPot deve ser do tipo int {}".format(var))
        self._postPot = var

    @property
    def postTime(self):
        return self._postTime
    @postTime.setter
    def postTime(self, var):
        if(not(isinstance(var, int))):
            raise ValueError("A variavel postTIme deve ser do tipo int")
        self._postTime = var

    def run(self):
        if (self._ganho == 1):
            self._resistor = 1000 
        
        elif(self._ganho == 2):
            self._resistor = 4700
        
        elif(self._ganho == 3):
            self._resistor = 47000
        
        elif(self._ganho == 4):
            self._resistor = 100000
        
        elif(self._ganho == 5):
            self._resistor = 470000
    
        potencialAp = self._potIni
        ampCorr = self._ampP/1000
        cont = 0
        frequency_time = 1/self._freq
        _delay_points = ((frequency_time/self._acq_time) - self._acq_points) / 2
        if self.potIni<self._potFin:
            _t0 = time.time()
            while (potencialAp <= self._potFin and SquareWaveVoltametry.started == True):
                cont += 1
                potencial = (potencialAp/1000)
                pulso1 = potencial + ampCorr + self.stepVolt/1000
                potR = (self._dac_sum + pulso1)
                self._adcdac.applyPot(potR)
                somacorrente = 0
                for ii in range(self._acq_points):
                    leitura = self._adcdac.readADC()
                    if ii > self._delay_points:
                        somacorrente += leitura
                for i in range(int(_delay_points)):
                    self._adcdac.readADC()
                
                somacorrente = somacorrente /(self._acq_points - self._delay_points)
                corrente = somacorrente/self._resistor
              #  potencial = potencialAp/1000
                pulso2 = pulso1 - ampCorr
                potR = self._dac_sum +  pulso2
                self._adcdac.applyPot(potR)
                somacorrente = 0
                for ii in range(self._acq_points):
                    leitura = self._adcdac.readADC()
                    if ii > self._delay_points:
                        somacorrente += leitura
                for i in range(int(_delay_points)):
                    self._adcdac.readADC()

                somacorrente = somacorrente / (self._acq_points - self._delay_points)
                corrente2 = -somacorrente/self._resistor
                correnteSQW = corrente - corrente2
                potencialAp = potencialAp + self.stepVolt
                yield (1000*potencial),(1000*correnteSQW)
        _t = time.time()
        self._adcdac.applyPot((self._postPot/1000)+self._dac_sum)
        time.sleep(self._postTime)
        print("delta_t= ", _t - _t0)
                
        GPIO.cleanup()
        SquareWaveVoltametry.started = False

