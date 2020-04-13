# Temperature display color scale

A suggested lookup table for temp -> color mapping. 

Hue changed, Saturation and Value remain at 100% for maximum visibility as a light.

| Start temp | Function          | End temp (excluded) |
|------------|-------------------|---------------------|
| -          | y=280             | 0                   |
| 0          | y = 210 - 3x      | 15                  |
| 15         | y = 322.5 - 10.5x | 25                  |
| 25         | y = 210 - 6x      | 35                  |
| 35         | y=0               | +                   |

This would roughly translate to this in python:

```
if temp < 0:
    return 280
elif temp < 15:
    return 210 - 3*temp
elif temp < 25:
    return 322.5 - 10.5*temp
elif temp < 35:
    return 210 - 6*x
else:
    return 0
```

# What's missing

Pixelblaze patterns can take variables and these can be set over the API while selecting the pattern. It makes sense to create a light pattern that will display 24 hours (00:00 -> 23:59) on the lights. 

We have 83 lights so each light then represents around 17m21s. The times represented by the lights become:

```
Light - Time
   00 - 12:00:00 AM
   01 - 12:17:21 AM
   02 - 12:34:42 AM
   03 - 12:52:03 AM
   04 - 1:09:24 AM
   05 - 1:26:45 AM
   . . .
   77 - 10:15:54 PM
   78 - 10:33:15 PM
   79 - 10:50:36 PM
   80 - 11:07:57 PM
   81 - 11:25:18 PM
   82 - 11:42:39 PM
```

I have to figure out how to interpolate the 24 hourly temperatures onto these 83 times.

I will probably send 24 values inside of variables and then use cubic interpolation on the pixelblaze side to map those onto the entire day.