# micropython-sn76489
Micropython driver for the SN76489 sound chip voor gebuik in SEGA Genesis en BBV Micro B. Use SPI shift registers or I2C I/O expanders via the mxUnifiedIO API.

0.01 20201027 Dit werkt nog niet.  This is NOT working, not yet.

<img src="https://segaretro.org/images/thumb/1/17/SN76489.jpg/243px-SN76489.jpg" width="20%" height="20%">


```python
# stupid demo
import utime
import sn76489
from pcf8574 import pcf8574


def main():
    global i2cAddr
    global index1
    i2cAddr = int(0x3e)
    pcfAddr = 0x23
    index1 = 1
    
    wemosPinsDict8266 = {"TX":1, "RX":3,"D4":2, "D3":0, "D2":4, "D1":5, "RX":3, "TX":1, "D8":15, "D7":13, "D6":12, "D5":14, "D0":16, "SCL":5, "SDA":4}
    wemosSPI8266 = {"MISO":wemosPinsDict8266["D6"], "MOSI":wemosPinsDict8266["D7"], "SCK":wemosPinsDict8266["D5"], "CSN":wemosPinsDict8266["D4"], "CE":wemosPinsDict8266["D3"]}
    
    i2c1 = machine.I2C(scl=machine.Pin(wemosPinsDict8266["SCL"]),sda=machine.Pin(wemosPinsDict8266["SDA"]),freq=100000)
    pcf1 = PCF8574(i2c=i2c1, address=pcfAddr)

    mxUnifiedSN76489 sound(i2c1,4)
    print("mxUnifiedSN76489 SN76489_test")

    print(F("beep()"))
      sound.beep(100)
      utime.sleep_ms(900)

    # sound a siren
    println("siren");
    for n in range(0, 10):
      for(ftTone in range (100.0, 4000.0, 10):
        sound.tone(ftTone, n)
        utime.sleep_ms(1)
        
    sound.stop();

print("APP start")
main()
print("APP eind")

```

# SN76489 gebruikt in:
- Sega Mastersystem
<img src="https://www.alyjameslab.com/img/sms_console.png" width="20%" height="20%">


CREDITS:
 - Arduino lib door https://github.com/maxint-rd/mxUnifiedSN76489
 - Micropython-versie Michiel Erasmus en #easylab4kids
 
