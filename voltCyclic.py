 #coding: utf-8
from adcdac_module import AdcDac
import RPi.GPIO as GPIO
import time

class CyclicVoltametry:
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
    def scanRate(self):
        return self._scanRate
    @scanRate.setter
    def scanRate(self, var):
        if(not(isinstance(var,int))):
            raise ValueError("A variável scanRate(Velocidade de scan) deve ser do tipo int {}".format(var))
        self._scanRate = var

    @property
    def ganho(self):
        return self._ganho
    @ganho.setter
    def ganho(self, var):
        if(not(isinstance(var,int))):
            raise ValueError("A variável ganho deve ser do tipo int {}".format(var))
        elif(var <= 0):
            raise ValueError("O ganho deve ser maior ou igual a 1 {}".format(var))
        self._ganho = var

    def run(self):
        _time = float(self._stepVolt/self._scanRate)

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

        _tempo = 0
    
        ad_da = AdcDac()
        ad_da.init_ADCDAC()
        potencialAp = self._potIni
        if self._potIni < self._potFin:
            tempo_inicial = time.time()
            while (potencialAp <= self._potFin and CyclicVoltametry.started == True):
                potencial = (potencialAp/1000)
                potR = self._dac_sum - potencial
                _nowTime = time.time()
                ad_da.applyPot(potR)
                potencialAp = potencialAp + self._stepVolt
                somacorrente = 0
                for ii in range(self._acq_points):
                    if ii > self._delay_points:
                        somacorrente = ad_da.readADC() + somacorrente
                somacorrente = somacorrente / (self._acq_points - self._delay_points)
                sinal = (somacorrente) / self._resistor    #TODO VERIFICAR ESTA PARTE!!!!
                _elapsed_time = (_nowTime - _tempo) + (time.time() - _nowTime) #Compara o tempo que a função ficou "inativa"(_nowTIme - _tempo) e soma ao tempo que a função perdeu aplicando o potencial(time.time() - _nowTime)
                if(_elapsed_time < _time):
                    time.sleep(_time - _elapsed_time)

                _tempo = time.time()
                yield((1000 * potencial), (1000 * sinal))
                
            potencialAp = potencialAp - (2*self._stepVolt)
            while (potencialAp >= self._potIni and CyclicVoltametry.started == True):
                potencial = (potencialAp/1000)
                potR = self._dac_sum - potencial
                _nowTime = time.time()
                ad_da.applyPot(potR)
                potencialAp = potencialAp - self._stepVolt
                somacorrente = 0
                for ii in range(self._acq_points):
                    if ii > self._delay_points:
                        somacorrente = ad_da.readADC() + somacorrente                        
                somacorrente = somacorrente / (self._acq_points - self._delay_points)
                sinal = (somacorrente) / self._resistor    #TODO VERIFICAR ESTA PARTE!!!!
                _elapsed_time = (_nowTime - _tempo) + (time.time() - _nowTime) #Compara o tempo que a função ficou "inativa"(_nowTIme - _tempo) e soma ao tempo que a função perdeu aplicando o potencial(time.time() - _nowTime)
                if(_elapsed_time < _time):
                    time.sleep(_time - _elapsed_time)
                _tempo = time.time()
                yield((1000 * potencial), (1000 * sinal))

        elif self._potIni > self._potFin:
            tempo_inicial = time.time()
            while (potencialAp >= self._potFin and CyclicVoltametry.started == True):
                potencial = (potencialAp/1000)
                potR = self._dac_sum - potencial
                _nowTime = time.time()
                ad_da.applyPot(potR)
                potencialAp = potencialAp - self._stepVolt
                somacorrente = 0
                for ii in range(self._acq_points):  
                    if ii > self._delay_points:
                        somacorrente = ad_da.readADC() + somacorrente
                somacorrente = somacorrente / (self._acq_points - self._delay_points)
                sinal = (somacorrente) / self._resistor    #TODO VERIFICAR ESTA PARTE!!!!
                _elapsed_time = (_nowTime - _tempo) + (time.time() - _nowTime) #Compara o tempo que a função ficou "inativa"(_nowTIme - _tempo) e soma ao tempo que a função perdeu aplicando o potencial(time.time() - _nowTime)
                if(_elapsed_time < _time):
                    time.sleep(_time - _elapsed_time)
                _tempo = time.time()
                yield((1000 * potencial), (1000 * sinal))
                
            potencialAp = potencialAp + (2*self._stepVolt)
            while (potencialAp <= self._potIni and CyclicVoltametry.started == True):
                potencial = (potencialAp/1000)
                potR = self._dac_sum - potencial
                _nowTime = time.time()
                ad_da.applyPot(potR)
                potencialAp = potencialAp + self._stepVolt
                somacorrente = 0
                for ii in range(self._acq_points):
                    if ii > self._delay_points:
                        somacorrente = ad_da.readADC() + somacorrente
                somacorrente = somacorrente / (self._acq_points - self._delay_points)
                sinal = (somacorrente) / self._resistor    #TODO VERIFICAR ESTA PARTE!!!!
                _elapsed_time = (_nowTime - _tempo) + (time.time() - _nowTime)
                if(_elapsed_time < _time):
                    time.sleep(_time - _elapsed_time)
                _tempo = time.time() 
                yield((1000 * potencial), (1000 * sinal))
        print(tempo_inicial - time.time())
        CyclicVoltametry.started = False
