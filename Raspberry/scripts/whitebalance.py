########################################################################################
# USE THIS SCRIPT TO CALIBRATE THE WHITEBALANCE OF THE RPI CAMERA                      #
# How to use this script:                                                              #
#   1) Place the car in the environment where is will drive                            #
#   2) Hold something white in front of the camera that covers its entire view         #
#   3) Run the scipt and wait until it is done                                         #
#   4) The script will output values for Red and Blue and will try to convert to       #
#         optimal values. In the last few result pick one that has the best wb         #
#         and put these values in /Raspberry/ControlLoop/ImageProcessing/FrameFetch.py #
#   5) If the lightning has changed to much over time, repeat/recalibrate              #
########################################################################################

import picamera
import picamera.array
import numpy as np

with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
    camera.awb_mode = 'off'
    # Start off with ridiculously low gains
    rg, bg = (0.5, 0.5)
    camera.awb_gains = (rg, bg)
    with picamera.array.PiRGBArray(camera, size=(128, 72)) as output:
        # Allow 30 attempts to fix AWB
        for i in range(100):
            # Capture a tiny resized image in RGB format, and extract the
            # average R, G, and B values
            camera.capture(output, format='rgb', resize=(128, 72), use_video_port=True)
            r, g, b = (np.mean(output.array[..., i]) for i in range(3))
            print('R:%5.2f, B:%5.2f = (%5.2f, %5.2f, %5.2f)' % (
                rg, bg, r, g, b))
            # Adjust R and B relative to G, but only if they're significantly
            # different (delta +/- 2)
            if abs(r - g) > 2:
                if r > g:
                    rg -= 0.1
                else:
                    rg += 0.1
            if abs(b - g) > 1:
                if b > g:
                    bg -= 0.1
                else:
                    bg += 0.1
            camera.awb_gains = (rg, bg)
            output.seek(0)
            output.truncate()