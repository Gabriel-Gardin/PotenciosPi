#coding: utf-8
from adcdac_module import AdcDac
import RPi.GPIO as GPIO
import json

class CalibratePotential():
    """Calibra o potencial de referência lendo a tensão do eletrodo de trabalho, e também aplica o potencial desejado"""
    def __init__(self, refpot=1.65):
        self.refpot = refpot
        self._adcdac = AdcDac()
        with open('/home/pi/Desktop/PotenciosPi/configs.json') as json_file:
            try:
                self.data_file = json.load(json_file)
            except Exception as e:
                print(e)
            

    @property
    def refpot(self):
        return self._refpot
    @refpot.setter
    def refpot(self, var):
        if (not(isinstance(var, float))):
            raise(ValueError("A variável refpot{} deve ser do tipo float".format(var)))
        self._refpot = var
    
    def apply_pot(self, potential):
        """Aplica o potencial desejado"""
        potencial = (self._refpot + potential/1000)          
        self._adcdac.applyPot(potencial)

    def calibrar(self):
        """Calibra o potencial de referência lendo 100 pontos sem aplicar nenhuma tensão e salva no arquivo de configurações"""
        voltage = 0
        for i in range(500):
            voltage  += self._adcdac.readADC()

        ref_pot = round((voltage/500), 4)
        print(ref_pot)
        data = {'divider_volt':(ref_pot)}
        self.data_file.update(data)
        with open('/home/pi/Desktop/PotenciosPi/configs.json', 'w') as filee:
            json.dump(self.data_file, filee)
        GPIO.cleanup()
        return(ref_pot)
        


