from picamera import PiCamera
from time import sleep, gmtime, strftime

camera = PiCamera()
output = strftime("image-%d-%m %H:%M.png", gmtime())


#camera.start_preview()
sleep(5)
camera.capture(output)
#camera.stop_preview()


