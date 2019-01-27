#coding: utf-8
from adcdac_module import AdcDac
import RPi.GPIO as GPIO
import time

class PreDeposition:
    def __init__(self,pot_cond, time_cond, pre_dep_pot, pre_dep_time, somadorDA):
        self.pot_cond = pot_cond
        self.time_cond = time_cond
        self.pre_dep_pot = pre_dep_pot
        self.pre_dep_time = pre_dep_time
        self.somadorDA = somadorDA
    
    @property
    def pot_cond(self):
        return self._pot_cond
    @pot_cond.setter
    def pot_cond(self, var):
        if(not(isinstance(var, int))):
            raise ValueError("A variável pot_cond(Potêncial de condicionamento deve ser inteira){}".format(var))
        self._pot_cond = var

    @property
    def time_cond(self):
        return self._time_cond
    @time_cond.setter
    def time_cond(self, var):
        if(not(isinstance(var, int))):
            raise ValueError("A variável time_cond(Tempo de condicionamento) deve ser do tipo int {}".format(var))
        self._time_cond = var

    @property
    def pre_dep_pot(self):
        return self._pre_dep_pot
    @pre_dep_pot.setter
    def pre_dep_pot(self, var):
        if(not(isinstance(var, int))):
            raise ValueError("A variável pre_dep_pot(Potencial de pré deposição) deve ser do tipo int {}".format(var))
        self._pre_dep_pot = var

    @property
    def pre_dep_time(self):
        return self._pre_dep_time
    @pre_dep_time.setter
    def pre_dep_time(self, var):
        if(not(isinstance(var, int))):
            raise ValueError("A variável pre_dep_time(Tempo de pré deposição) deve ser do tipo int {}".format(var))
        self._pre_dep_time = var

    @property
    def somadorDA(self):
        return self._somadorDA
    @somadorDA.setter
    def somadorDA(self, var):
        if(not(isinstance(var, float))):
            raise ValueError("A variável somadorDA deve ser do tipo float {}".format(var))
        self._somadorDA = var


    def run(self):
        ad_da = AdcDac()
        ad_da.init_ADCDAC()


        _potAp = self._pot_cond/1000
        _potAp = (self._somadorDA - _potAp)
        ad_da.applyPot(_potAp)
        time.sleep(self._time_cond)

        _potAp - self._pre_dep_pot/1000
        _potAp = (self._somadorDA - _potAp)
        ad_da.applyPot(_potAp)
        time.sleep(self._pre_dep_time)
