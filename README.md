Python control for Tintlink LED bulbs
=====================================

A simple Python API for controlling LED bulbs compatible with the  [Tintlink app](https://play.google.com/store/apps/details?id=com.lede.tintlink). This code makes use of the PyBT2 branch of Mike Ryan's [PyBT](http://github.com/mikeryan/PyBT)

Example use
-----------

This will connect and set the bulb to full red, no green and no blue.
```
import tintlink

bulb = tintlink.tintlink("00:21:4d:00:00:01")
bulb.connect()
bulb.set_colour(0xff, 0x00, 0x00)
```

To set to a white temperature:
```
bulb.set_white(3)
```

where the number is between 0 and 10.