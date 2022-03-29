# Write your code here :-)
import camera

# ESP32-CAM (default configuration) - https://bit.ly/2Ndn8tN
#camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)

# camera.init(0,d0=5,d1=14,d2=4,d3=15,d4=18,d5=23,d6=36,d7=39,href=25,
#             vsync=27,sioc=12,siod=13,xclk=32,pclk=19,xclk_freq=camera.XCLK_10MHz,reset=-1,pwdn=26)

# Worked with the cmake....bin file for upload to board
camera.init(0, d0=34, d1=13, d2=14, d3=35, d4=39, d5=38, d6=37, d7=36,
            format=camera.JPEG, framesize=camera.FRAME_VGA, xclk_freq=camera.XCLK_10MHz,
            href=27, vsync=5, reset=-1, sioc=23, siod=18, xclk=4, pclk=25)

# These parameters: format=camera.JPEG, xclk_freq=camera.XCLK_10MHz are standard for both cameras.
# You can try using a faster xclk (20MHz), this also worked with the esp32-cam and m5camera
# but the image was pixelated and somehow green.

buf = camera.capture()
# if capture failed then buf = false
# if capture succeeded len(buf) > 0
f = open('image.jpg','w')
f.write(buf)
f.close()
