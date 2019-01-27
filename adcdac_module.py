import sys
sys.path.append('/home/pi/ABElectronics_Python3_Libraries/ADCDACPi')
import RPi.GPIO as GPIO
import time
from ABE_ADCDACPi import ADCDACPi

class AdcDac:    
    def init_ADCDAC(self):
        """Inicializa o conversor AD/DA"""
        # Gain of the board and reference tension.
        self.adcdac = ADCDACPi(2)
        self.adcdac.set_adc_refvoltage(3.3)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(29, GPIO.OUT)
        GPIO.output(29, 1)
        time.sleep(0.1)

    def readADC(self):
        """This function is used to read the analogic voltage from the ADC that is being used. Change this to match the ADC that is being used"""
        self._readPot = self.adcdac.read_adc_voltage(1, 0)
        return (self._readPot)

    def applyPot(self, arg):
        """This function is used to apply the potential using the desired DAC. Change this to match the DAC that is being used"""
        self.adcdac.set_dac_voltage(1, arg)
        time.sleep(0.1)
