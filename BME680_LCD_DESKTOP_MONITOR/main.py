#import filesystem_checker
import os
import uos
import micropython
from pico_i2c_lcd import I2cLcd
import json
from machine import Pin
import utime as time
from breakout_bme68x import BreakoutBME68X, STATUS_HEATER_STABLE
from pimoroni_i2c import PimoroniI2C
 
#I2C setup for LCD display
PINS_LCD = {"sda": 0, "scl": 1}
i2c2 = PimoroniI2C(**PINS_LCD)
lcd = I2cLcd(i2c2, 0x27, 2, 16)

#I2C setup for BME680
PINS_BREAKOUT_GARDEN = {"sda": 2, "scl": 3}
i2c = PimoroniI2C(**PINS_BREAKOUT_GARDEN)
bme = BreakoutBME68X(i2c)

def lcd_entry():
      lcd.clear()
      temperature, pressure, humidity, gas, status, _, _ = bme.read()
      lcd.move_to(0,0)
      lcd.putstr("  Temperature:")
      lcd.move_to(0,1)
      lcd.putstr("     {:0.2f} c".format(temperature))
      time.sleep(4)
      lcd.clear()
      lcd.move_to(0,0)
      lcd.putstr("    Humidity:")
      lcd.move_to(0,1)
      lcd.putstr("     {:0.2f} %".format(humidity))
      time.sleep(4)
      lcd.clear()
      lcd.move_to(0,0)
      lcd.putstr("    Pressure:")
      lcd.move_to(0,1)
      lcd.putstr("   {:0.2f} Pa".format(pressure))
      time.sleep(4)
      lcd.clear()
      lcd.move_to(0,0)
      lcd.putstr("      Air:")
      lcd.move_to(0,1)
      lcd.putstr(" {:0.2f} ohms".format(gas))
      time.sleep(4)

def sensor_readings():    
      temperature, pressure, humidity, gas, status, _, _ = bme.read()
      heater = "Stable" if status & STATUS_HEATER_STABLE else "Unstable"
      #print("Temp: {:0.2f} c, Pressure: {:0.2f} pa, Humidity: {:0.2f} %, Gas: {:0.2f} Ohms, Heater: {}".format(temperature, pressure, humidity, gas, heater))
      time.sleep(4)
      
def logging_json():      
      temperature, pressure, humidity, gas, status, _, _ = bme.read()
      f = open("data.txt", "a")
      time_now = time.time()
      time_known = (time_now) - (start_time)     
      values = {
          "time": (time_known),
          "temperature": "{:0.2f}".format(temperature),
          "humidity": "{:0.2f}".format(humidity),
          "pressure": "{:0.2f}".format(pressure),
          "gas": "{:0.2f}".format(gas)
      }
      f.write(json.dumps(values))
      f.write("\r\n")
      f.close()
      
def file_checker():
      statinfo = ((os.stat("data.txt")[6])/1024)      
      blocksize = uos.statvfs("/")[1]
      totalblocks = uos.statvfs("/")[2]
      freeblocks = uos.statvfs("/")[3]

      free_space = ((freeblocks*blocksize) /1024)
      used_space = ((totalblocks*blocksize)/1024)
      total_space = (used_space - free_space)      
      
      if statinfo >= (free_space*0.75):
          lcd.clear()
          lcd.move_to(0,0)
          lcd.putstr(" Drive 75% full!")
          lcd.move_to(0,1)
          lcd.putstr("  Download Data")
      if statinfo >= (free_space*0.9):
          os.remove("data.txt")
          lcd.clear()
          lcd.move_to(0,0)
          lcd.putstr(" File Restarted!")
          time.sleep(2)
          lcd.move_to(0,1)
          lcd.putstr("   Data Lost!")
          time.sleep(3)
          
          
          
          
          
    
      
start_time = time.time()

f = open("data.txt", "a")
f.write("Time = Seconds, Temp = Celcius, Humidity = %, Pressure = pa, Gas = ohms\r\n")
f.close()

while True:
      logging_json()
      sensor_readings()
      lcd_entry()
      file_checker()
      
      