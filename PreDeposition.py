#coding: utf-8
from adcdac_module import AdcDac
import RPi.GPIO as GPIO
import time

class PreDeposition:
    """Class resposible of contrlling the pre depositon."""
    def __init__(self,pot_cond, time_cond, pre_dep_pot, pre_dep_time, somadorDA):
        self.pot_cond = pot_cond
        self.time_cond = time_cond
        self.pre_dep_pot = pre_dep_pot
        self.pre_dep_time = pre_dep_time
        self.somadorDA = somadorDA
        self._adcdac = AdcDac()
    
    @property
    def pot_cond(self):
        return self._pot_cond
    @pot_cond.setter
    def pot_cond(self, var):
        if(not(isinstance(var, int))):
            raise ValueError("The variable pot_cond must be of type int {}".format(var))
        self._pot_cond = var

    @property
    def time_cond(self):
        return self._time_cond
    @time_cond.setter
    def time_cond(self, var):
        if(not(isinstance(var, int))):
            raise ValueError("The variable time_cond must be of type int {}".format(var))
        self._time_cond = var

    @property
    def pre_dep_pot(self):
        return self._pre_dep_pot
    @pre_dep_pot.setter
    def pre_dep_pot(self, var):
        if(not(isinstance(var, int))):
            raise ValueError("The variable pre_dep_pot must be of type int {}".format(var))
        self._pre_dep_pot = var

    @property
    def pre_dep_time(self):
        return self._pre_dep_time
    @pre_dep_time.setter
    def pre_dep_time(self, var):
        if(not(isinstance(var, int))):
            raise ValueError("The variable pre_dep_time must be of type int {}".format(var))
        self._pre_dep_time = var

    @property
    def somadorDA(self):
        return self._somadorDA
    @somadorDA.setter
    def somadorDA(self, var):
        if(not(isinstance(var, float))):
            raise ValueError("The variable somadorDA must be of type int {}".format(var))
        self._somadorDA = var


    def run(self):
        _potAp = self._pot_cond/1000
        _potAp = (self._somadorDA + _potAp)
        self._adcdac.applyPot(_potAp)
        time.sleep(self._time_cond)

        _potAp = self._pre_dep_pot/1000
        _potAp = (self._somadorDA + _potAp)
        self._adcdac.applyPot(_potAp)
        time.sleep(self._pre_dep_time)
