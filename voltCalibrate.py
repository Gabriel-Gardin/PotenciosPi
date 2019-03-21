#coding: utf-8
from adcdac_module import AdcDac
import RPi.GPIO as GPIO

class CalibratePotential:
    def __init__(self, applypotential=0, refpot=3):
        self.refpot = refpot
        self.applypotential = applypotential

    @property
    def applypotential(self):
        return self._applypotential
    @applypotential.setter
    def applypotential(self, var):
        if (not(isinstance(var, int))):
            raise(ValueError("A variável applypot{} deve ser do tipo int".format(var)))
        self._applypotential = var

    @property
    def refpot(self):
        return self._refpot
    @refpot.setter
    def refpot(self, var):
        if (not(isinstance(var, int))):
            raise(ValueError("A variável refpot{} deve ser do tipo int".format(var)))
        self._refpot = var
    
    def apply_pot(self):
        potencial = (self._refpot - self._applypotential/1000)
        ad_da = AdcDac()
        ad_da.init_ADCDAC()
        ad_da.applyPot(potencial)

